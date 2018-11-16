from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
import happyproj.settings

import os
import dictation
import logging
from dictation import voicebuilder
from dictation import models


# Create your views here.
# voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
# builder = voicebuilder.VoiceBuilder(voicePath)

def index(request):
    return render(request,'dictation/index.html')

def initQry(request):
    choiceSelected = jsonDict(dictation.models.ChoiceSelected.objects.all(), ['choicename','choicecode'])
    request.session['choiceSelected'] = choiceSelected
    print(choiceSelected)
    dRes = {'choiceSelected':choiceSelected}
    press = jsonArraySet(dictation.models.Press.objects.all())
    dRes['press'] = press
    selectedPress = choiceSelected['press']
    book = jsonArraySet(dictation.models.Book.objects.filter(press=selectedPress))
    dRes['book'] = book
    selectedBook = choiceSelected['book']
    unit = jsonArraySet(dictation.models.Unit.objects.filter(book=selectedBook))
    dRes['unit'] = unit
    selectedUnit = choiceSelected['unit']
    lesson = jsonArraySetLesson(dictation.models.Lesson.objects.filter(unit=selectedUnit))
    dRes['lesson'] = lesson
    selectedLesson = choiceSelected['lesson']
    test = jsonArraySet(dictation.models.Test.tests.filter(lesson=selectedLesson),['id', 'testname'])
    dRes['test'] = test
    testTime = jsonArraySet(dictation.models.Choice.objects.filter(type='time'),['id', 'name'])
    dRes['testtime'] = testTime
    wordScope = jsonArraySet(dictation.models.Choice.objects.filter(type='scope'),['id', 'name'])
    dRes['wordscope'] = wordScope
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

def qryLesson(request):
    unitId = request.GET['unit']
    lesson = jsonArraySetLesson(dictation.models.Lesson.objects.filter(unit=unitId))
    dRes = {'lesson':lesson}
    return JsonResponse(dRes)

def qryTest(request):
    lessonId = request.GET['lesson']
    print('query test by lessonid: %s' %  lessonId)
    test = jsonArraySet(dictation.models.Test.tests.filter(lesson=lessonId),['id', 'testname'])
    dRes = {'test':test}
    return JsonResponse(dRes)

def dispWords(request):
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
    choiceSelected = request.session['choiceSelected']
    # choiceSelected = {}
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
    saveChoiceSelected(choiceSelected)
    return render(request, 'dictation/dictating.html')

def qryWords(request):
    choiceSelected = request.session['choiceSelected']
    dicType = choiceSelected['dictype']
    wordScope = choiceSelected['wordscope']
    print('dictype: %s' % dicType)
    if dicType == 'newword':
        lessonId = choiceSelected['lesson']
        print(lessonId)
        aWords = dictation.models.Word.objects.filter(lesson=lessonId)
        # jsonWords = jsonArraySet(aWords, ['id', 'word'])
        # request.session['words'] = jsonWords
        # print(jsonWords)
    elif dicType == 'wrongword':
        testId = choiceSelected['test']
        print('testid: %s' % testId)
        aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True,testword__test__exact=testId)
        # jsonWords = jsonArraySet(aWords, ['id', 'word'])
        # print(jsonWords)
    # voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
    # builder = voicebuilder.VoiceBuilder(voicePath)
    # builder.builderPinyin(jsonWords)
    aScopeWord = getWordScope(aWords,wordScope)
    jsonWords = jsonArraySet(aScopeWord, ['id', 'word'])
    request.session['words'] = jsonWords
    print(jsonWords)
    dRes = {'words': jsonWords}
    return JsonResponse(dRes)

def getWordScope(aWords, scope):
    wordScope = dictation.models.Choice.objects.get(pk=scope).name
    print('scope: %s %s' % (scope,wordScope))
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

def qryLessonWords(request):
    lessonId = request.GET.get('lesson', None)
    aWords = dictation.models.Word.objects.filter(lesson=lessonId)
    sWord = ''
    for wd in aWords:
        if sWord == '':
            sWord = wd
        else:
            sWord = '%s %s' % (sWord, wd)
    print(sWord)
    return JsonResponse({'words': sWord})

def saveLessonWords(request):
    lessonId = request.POST.get('lesson', None)
    sWord = request.POST.get('words', None)
    aWords = sWord.split()
    print('add lessonid: %s' % lessonId)
    print('add word: %s' % sWord)
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

def delLessonWords(request):
    lessonId = request.POST.get('lesson', None)
    sWord = request.POST.get('words', None)
    aWords = sWord.split()
    print('delete lessonid: %s' % lessonId)
    print('delete word: %s' % sWord)
    for wd in aWords:
        # lswd = models.Word.objects.create(lessonId, wd)
        lswd = models.Word.objects.filter(lesson_id=lessonId, word=wd)
        lswd.delete()
    return JsonResponse({'response': 'ok'})

def saveChoiceSelected(choiceSelected):
    print('save choice selected...')
    for k in choiceSelected:
        chses = dictation.models.ChoiceSelected.objects.filter(choicename=k)
        if chses:
            chse = chses[0]
            chse.setChoicecode(k,choiceSelected[k])
        else:
            chse = models.ChoiceSelected.objects.create(k, choiceSelected[k])
        print('name: %s  value: %s   code: %s' % (chse.choicename,chse.choicevalue,chse.choicecode) )
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

def makeVoice(request):
    print('make word voice...')
    aWords = request.session['words']

    # request.session['words'] = None
    # print(aWords)
    voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
    builder = voicebuilder.VoiceBuilder(voicePath)
    # ['id', 'word', 'pinyin', 'voice']
    builder.builderVoice(aWords)
    # request.session['words'] = aWords
    request.session['words'] = None
    print('make voice ok.')
    print(aWords)
    # jsonVoice = jsonArraySet(aWords, ['id', 'word', 'pinyin', 'voice'])
    dRes = {'words': aWords}
    return JsonResponse(dRes)
    # return JsonResponse({'response':'ok'})

def dictate(request):
    print('dictate')
    choiceSelected = request.session['choiceSelected']
    lessonId = choiceSelected['lesson']
    unitId = choiceSelected['unit']
    bookId = choiceSelected['book']
    pressId = choiceSelected['press']
    if lessonId:
        lesson = dictation.models.Lesson.objects.get(id=lessonId)
        print('dictate lesson: %s' % lessonId)
    if unitId:
        unit = dictation.models.Unit.objects.get(id=unitId)
        print('dictate unit: %s' % unitId)
    if bookId:
        book = dictation.models.Book.objects.get(id=bookId)
    if pressId:
        press = dictation.models.Press.objects.get(id=pressId)
    test = models.Test.tests.create(press, book, unit, lesson)
    test.save()
    request.session['testId'] = test.id
    print('dictate test: %s' % test.id)
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

def qryTestWords(request):
    aWords = request.session['words']
    dRes = {'words': aWords}
    return JsonResponse(dRes)

def dispPinyin(request):
    return render(request,'dictation/index.html')

def saveTest(request):
    testid = request.session['testId']
    # testRlt = request.POST.get('test[]', None)
    print('savetest %s' % testid)
    testRlt = request.POST
    print('save test words %s' % testRlt)
    for w in testRlt:
        tstWd = models.TestWord.objects.create(testid, w, testRlt[w])
        tstWd.save()
    return JsonResponse({'response':'ok'})

def tabtest(request):
    return render(request,'dictation/tabtest.html')

def wordImport(request):
    return render(request, 'dictation/wordimport.html')
