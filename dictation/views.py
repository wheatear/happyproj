from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import happyproj.settings

import os
import dictation
import logging
from dictation import voicebuilder
from dictation import models
from login.views import check_login


# Create your views here.
# voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
# builder = voicebuilder.VoiceBuilder(voicePath)

# initLogger = logging.getLogger('django')
logger = logging.getLogger('django')
errlog = logging.getLogger('error')
# initLogger.suffix = '%Y%m%d'

def page_not_found(request):
    return render(request, '404.html')

def logRequest(fn):
    def new_fn(*args):
        request = args[0]
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        # print('ip: %s' % ip)
        # userAgent = request.META.get('HTTP_USER_AGENT', '')
        logger.info('request: %s %s from %s', request.method, request.path, ip)
        result = fn(*args)
        return result
    return new_fn

@check_login
@logRequest
def index(request):
    # request.session['ip'] = ip
    # extra = getExtra(request)
    # logger = LoggerAdapter(initLogger,extra)

    # logger.info('access',extra)
    return render(request,'dictation/index.html')

@check_login
@logRequest
def initQry(request):
    userId = request.session['userId']
    if not userId:
        return None
    choiceSelected = jsonDict(dictation.models.ChoiceSelected.objects.filter(user=userId), ['choicename','choicecode'])
    # request.session['choiceSelected'] = choiceSelected
    logger.info('choiceSelected: %s', choiceSelected)
    # logger.info(choiceSelected)
    dRes = {'choiceSelected':choiceSelected}
    press = jsonArraySet(dictation.models.Press.objects.all())
    dRes['press'] = press
    logger.debug(press)
    if len(choiceSelected) < 1:
        choiceSelected['press'] = 1
        dRes['choiceSelected'] = choiceSelected
        selectedPress = choiceSelected['press']
        book = jsonArraySet(dictation.models.Book.objects.filter(press=selectedPress))
        logger.debug(book)
        dRes['book'] = book
        wordScope = jsonArraySet(dictation.models.Choice.objects.filter(type='scope'), ['id', 'name'])
        dRes['wordscope'] = wordScope
        logger.debug(wordScope)
        return JsonResponse(dRes)
    selectedPress = choiceSelected['press']
    book = jsonArraySet(dictation.models.Book.objects.filter(press=selectedPress))
    dRes['book'] = book
    logger.debug(book)
    selectedBook = choiceSelected['book']
    unit = jsonArraySet(dictation.models.Unit.objects.filter(book=selectedBook))
    dRes['unit'] = unit
    logger.debug(unit)
    selectedUnit = choiceSelected['unit']
    lesson = jsonArraySetLesson(dictation.models.Lesson.objects.filter(unit=selectedUnit))
    dRes['lesson'] = lesson
    logger.debug(lesson)
    selectedLesson = choiceSelected['lesson']
    test = jsonArraySet(dictation.models.Test.tests.filter(lesson=selectedLesson),['id', 'testname'])
    dRes['test'] = test
    logger.debug(test)
    testTime = jsonArraySet(dictation.models.Choice.objects.filter(type='time'),['id', 'name'])
    dRes['testtime'] = testTime
    logger.debug(testTime)
    wordScope = jsonArraySet(dictation.models.Choice.objects.filter(type='scope'),['id', 'name'])
    dRes['wordscope'] = wordScope
    logger.debug(wordScope)
    return JsonResponse(dRes)

def jsonDict(aQrySet,aFields=None):
    di = {}
    if aFields is None:
        aFields = ['id', 'name']
    for i in aQrySet:
        di[getattr(i, aFields[0])] = getattr(i, aFields[1])
    return di

def jsonDictSet(aQrySet,aFields=None):
    aDi = []
    if aFields is None:
        aFields = ['id', 'name']
    for i in aQrySet:
        di = {}
        for f in aFields:
            di[f] = getattr(i, f)
        aDi.append(di)
    return aDi

def jsonArraySet(aQrySet, aFields=None):
    aDi = []
    if aFields is None:
        aFields = ['id', 'name']
    for i in aQrySet:
        di = []
        for f in aFields:
            di.append(getattr(i, f))
        aDi.append(di)
    return aDi

def jsonArraySetLesson(aQrySet):
    aLi = []
    aFields = ['id', 'lessoncode','lessonname']
    for i in aQrySet:
        li = [i.id]
        val = '%s %s' % (i.lessoncode, i.lessonname)
        li.append(val)
        aLi.append(li)
    return aLi

# @check_login
def qryBook(request):
    pressId = request.GET['press']
    logger.info('query book of press: %s',pressId)
    book = jsonArraySet(dictation.models.Book.objects.filter(press=pressId))

    dRes = {'book':book}
    logger.info(book)
    return JsonResponse(dRes)

@check_login
def qryUnit(request):
    bookId = request.GET['book']
    logger.info('query unit of book: %s',bookId)
    unit = jsonArraySet(dictation.models.Unit.objects.filter(book=bookId))
    # unit = jsonArraySet(dictation.models.Unit.objects.filter(book=selectedBook))
    logger.info(unit)
    dRes = {'unit':unit}
    return JsonResponse(dRes)

# @logRequest
@check_login
def qryLesson(request):
    unitId = request.GET['unit']
    logger.info('query lesson fo unit: %s',unitId)
    lesson = jsonArraySetLesson(dictation.models.Lesson.objects.filter(unit=unitId))

    dRes = {'lesson':lesson}
    logger.info(lesson)
    return JsonResponse(dRes)

# @logRequest
@check_login
def qryTest(request):
    userId = request.session['userId']
    if not userId:
        return None
    lessonId = request.GET['lesson']
    logger.info('query test by lessonid: %s', lessonId)
    test = jsonArraySet(dictation.models.Test.tests.filter(user=userId, lesson=lessonId),['id', 'testname'])

    dRes = {'test':test}
    logger.info(test)
    return JsonResponse(dRes)

@check_login
@logRequest
def dispWords(request):
    userId = request.session['userId']
    if not userId:
        return None
    pressId = request.GET.get('press', None)
    bookId = request.GET.get('book', None)
    unitId = request.GET.get('unit', None)
    lessonId = request.GET.get('lesson', None)
    testtime = request.GET.get('testtime', None)
    testId = request.GET.get('test', None)
    wordscope = request.GET.get('wordscope', None)
    dictype = request.GET.get('dictype', None)
    review = request.GET.get('review', None)
    dictate = request.GET.get('dictate', None)
    # choiceSelected = request.session['choiceSelected']

    choiceSelected = {}
    if pressId:
        # request.session['pressId'] = pressId
        choiceSelected['press'] = pressId
    if bookId:
        # request.session['bookId'] = bookId
        choiceSelected['book'] = bookId
    if unitId:
        # request.session['unitId'] = unitId
        choiceSelected['unit'] = unitId
    if lessonId:
        # request.session['lessionId'] = lessonId
        choiceSelected['lesson'] = lessonId
    if testtime:
        choiceSelected['testtime'] = testtime
    if testId:
        # request.session['testId'] = testId
        choiceSelected['test'] = testId
    if wordscope:
        choiceSelected['wordscope'] = wordscope
    if dictype:
        # request.session['dictype'] = dictype
        choiceSelected['dictype'] = dictype
    # choiceSelected['lession'] = lessonId
    request.session['choiceSelected'] = choiceSelected
    saveChoiceSelected(choiceSelected, userId)
    return render(request, 'dictation/dictating.html')

@check_login
@logRequest
def qryWords(request):
    choiceSelected = request.session['choiceSelected']
    dicType = choiceSelected['dictype']
    wordScope = choiceSelected['wordscope']
    logger.info('dictype: %s', dicType)
    if dicType == 'newword':
        lessonId = choiceSelected['lesson']
        logger.info('lessonid: %s', lessonId)
        aWords = dictation.models.Word.objects.filter(lesson=lessonId)
        # jsonWords = jsonArraySet(aWords, ['id', 'word'])
        # request.session['words'] = jsonWords
        # print(jsonWords)
    elif dicType == 'wrongword':
        testId = choiceSelected['test']
        logger.info('testid: %s', testId)
        # aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True,testword__test__exact=testId)
        aWords = getWrongWords(choiceSelected)
        # jsonWords = jsonArraySet(aWords, ['id', 'word'])
        # print(jsonWords)
    # voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
    # builder = voicebuilder.VoiceBuilder(voicePath)
    # builder.builderPinyin(jsonWords)
    aScopeWord = getWordScope(aWords,wordScope)
    jsonWords = jsonArraySet(aScopeWord, ['id', 'word'])
    request.session['words'] = jsonWords
    logger.info(jsonWords)
    dRes = {'words': jsonWords}
    return JsonResponse(dRes)

def getWrongWords(choiceSelected):
    testId = int(choiceSelected['test'])
    testtimeId = int(choiceSelected['testtime'])
    lessonId = int(choiceSelected['lesson'])
    unitId = int(choiceSelected['unit'])
    bookId = int(choiceSelected['book'])
    aWords = None
    if testId > 0:
        aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True, testword__test__exact=testId)
    elif testtimeId > 0 and lessonId > 0:
        aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True, lesson=lessonId)
    elif unitId > 0:
        aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True, lesson__unit__exact=unitId)
    elif bookId > 0:
        aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True, lesson__unit__book__exact=bookId)
    return aWords

def getWordScope(aWords, scope):
    if scope == '0':
        return aWords
    wordScope = dictation.models.Choice.objects.get(pk=scope).name
    logger.info('scope: %s %s', scope,wordScope)
    if wordScope == '前30':
        aScpWords = aWords[:30]
    elif wordScope == '前50':
        aScpWords = aWords[:50]
    elif wordScope == '前100':
        aScpWords = aWords[:100]
    elif wordScope == '全部':
        aScpWords = aWords
    else:
        aScpWords = aWords[:50]
    return aScpWords

@check_login
@logRequest
def qryLessonWords(request):
    lessonId = request.GET.get('lesson', None)
    aWords = dictation.models.Word.objects.filter(lesson=lessonId)
    sWord = ''
    for wd in aWords:
        if sWord == '':
            sWord = wd
        else:
            sWord = '%s %s' % (sWord, wd)
    logger.info(sWord)
    return JsonResponse({'words': sWord})

@check_login
@logRequest
def saveLessonWords(request):
    lessonId = request.POST.get('lesson', None)
    sWord = request.POST.get('words', None)
    aWords = sWord.split()
    logger.info('add lessonid: %s', lessonId)
    logger.info('add word: %s', sWord)
    # oldWords = dictation.models.Word.objects.filter(lesson=lessonId)
    # print('old words: %s' % oldWords)
    # # oldWords.all().delete()
    # oldWords.delete()
    # for w in oldWords:
    #     w.delete()
    for wd in aWords:
        # lswd = models.Word.objects.create(lessonId, wd)
        lswd = models.Word(lesson_id=lessonId, word=wd)
        lswd.save()
    return JsonResponse({'response': 'ok'})

@check_login
@logRequest
def delLessonWords(request):
    lessonId = request.POST.get('lesson', None)
    sWord = request.POST.get('words', None)
    aWords = sWord.split()
    logger.info('delete lessonid: %s', lessonId)
    logger.info('delete word: %s', sWord)
    for wd in aWords:
        # lswd = models.Word.objects.create(lessonId, wd)
        lswd = models.Word.objects.filter(lesson_id=lessonId, word=wd)
        lswd.delete()
    return JsonResponse({'response': 'ok'})

def saveChoiceSelected(choiceSelected, userId):
    logger.info('save choice selected...')
    for k in choiceSelected:
        chses = dictation.models.ChoiceSelected.objects.filter(user=userId, choicename=k)
        if chses:
            chse = chses[0]
            chse.setChoicecode(k,choiceSelected[k])
        else:
            chse = models.ChoiceSelected.objects.create(userId, k, choiceSelected[k])
        logger.info('name: %s  value: %s   code: %s', chse.choicename,chse.choicevalue,chse.choicecode)
        chse.save()

# def checkWords(request):
#     return render(request, 'dictation/checkwords.html')

# def dictating(request):
#     lessonId = request.session['lessionId']
#     unitId = request.session['unitId']
#     bookId = request.session['bookId']
#     pressId = request.session['pressId']
#
#     if lessonId:
#         lesson = dictation.models.Lesson.objects.get(id=lessonId)
#         print('dictate lesson: %s' % lessonId)
#     if unitId:
#         unit = dictation.models.Unit.objects.get(id=unitId)
#         print('dictate unit: %s' % unitId)
#     if bookId:
#         book = dictation.models.Book.objects.get(id=bookId)
#     if pressId:
#         press = dictation.models.Press.objects.get(id=pressId)
#     print('dictate lesson: %s' % lesson)
#     print('dictate unit: %s' % unit)
#     test = models.Test.tests.create(press,book,unit,lesson)
#     test.save()
#     request.session['testId'] = test.id
#     return render(request,'dictation/dictating.html')

@check_login
@logRequest
def makeVoice(request):
    logger.info('make word voice...')
    aWords = request.session['words']

    # request.session['words'] = None
    # print(aWords)
    voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
    builder = voicebuilder.VoiceBuilder(voicePath)
    logger.info('builde word voicefile')
    # ['id', 'word', 'pinyin', 'voice']
    builder.builderVoice(aWords)
    logger.info('builde announcer voicefile')
    aAnnouncer = builder.buildeAnnouncer()
    # request.session['words'] = aWords
    request.session['words'] = None
    logger.info('make voice ok.')
    logger.info(aWords)
    logger.info(aAnnouncer)
    # jsonVoice = jsonArraySet(aWords, ['id', 'word', 'pinyin', 'voice'])
    dRes = {'words': aWords}
    dRes['announcer'] = aAnnouncer
    return JsonResponse(dRes)
    # return JsonResponse({'response':'ok'})

@check_login
@logRequest
def dictate(request):
    logger.info('dictate')
    userId = request.session['userId']
    if not userId:
        return None
    choiceSelected = request.session['choiceSelected']
    lessonId = choiceSelected['lesson']
    unitId = choiceSelected['unit']
    bookId = choiceSelected['book']
    pressId = choiceSelected['press']
    if lessonId:
        lesson = dictation.models.Lesson.objects.get(id=lessonId)
        logger.info('dictate lesson: %s', lesson)
    if unitId:
        unit = dictation.models.Unit.objects.get(id=unitId)
        logger.info('dictate unit: %s', unit)
    if bookId:
        book = dictation.models.Book.objects.get(id=bookId)
    if pressId:
        press = dictation.models.Press.objects.get(id=pressId)
    test = models.Test.tests.create(userId, press, book, unit, lesson)
    test.save()
    request.session['testId'] = test.id
    logger.info('dictate test: %s', test)
    return JsonResponse({'response':'ok'})

    # # aWordId = request.POST.get('word', None)
    # # print('dictate words: %s' % aWordId)
    # # # aWords = request.session['words']
    # # aWords = dictation.models.Word.objects.filter(pk__in=aWordId)
    # jsonWords = request.session['words']
    # # jsonWords = jsonArraySet(aWords, ['id', 'word'])
    # print(jsonWords)
    # # voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
    # # builder = voicebuilder.VoiceBuilder(voicePath)
    # # builder.getVoice(jsonWords)
    # # jsonVoice = jsonArraySet(aWords, ['id', 'word', 'pinyin', 'voice'])
    # dRes = {'words': jsonWords}
    # return JsonResponse(dRes)

@check_login
@logRequest
def qryTestWords(request):
    # userId = request.session['userId']
    # if not userId:
    #     return None
    aWords = request.session['words']
    dRes = {'words': aWords}
    return JsonResponse(dRes)

@check_login
@logRequest
def dispPinyin(request):
    return render(request,'dictation/index.html')

@check_login
@logRequest
def saveTest(request):
    # userId = request.session['userId']
    # if not userId:
    #     return None
    testid = request.session['testId']
    # testRlt = request.POST.get('test[]', None)
    logger.info('savetest %s', testid)
    testRlt = request.POST
    logger.info('save test words %s', testRlt)
    for w in testRlt:
        tstWd = models.TestWord.objects.create(testid, w, testRlt[w])
        tstWd.save()
    return JsonResponse({'response':'ok'})

@logRequest
def tabtest(request):
    return render(request,'dictation/tabtest.html')

@logRequest
def wordImport(request):
    return render(request, 'dictation/wordimport.html')

def getIp(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def getExtra(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    # print('ip: %s' % ip)
    extra_dict = {"ip": ip, "username": "Dictation"}
    return extra_dict

class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        self.logger = logger
        self.extra = extra

    def process(self, msg, kwargs):
        if 'extra' not in kwargs:
            kwargs["extra"] = self.extra
        return msg, kwargs

    def debug(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.critical(msg, *args, **kwargs)
