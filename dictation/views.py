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
def index(request):
    return render(request,'dictation/index.html')

def initQry(request):
    choiceSelected = jsonDict(dictation.models.ChoiceSelected.objects.all(), ['choicename','choicecode'])
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
    testTime = jsonArraySet(dictation.models.Choice.objects.filter(type='time'))
    dRes['testtime'] = testTime
    wordScope = jsonArraySet(dictation.models.Choice.objects.filter(type='scope'))
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
    lessonId = request.GET.get('lesson',None)
    pressId = request.GET.get('press', None)
    bookId = request.GET.get('book', None)
    unitId = request.GET.get('unit', None)
    testtime = request.GET.get('testtime', None)
    testId = request.GET.get('test', None)
    dictype = request.GET.get('dictype', None)
    study = request.GET.get('study', None)
    if pressId:
        request.session['pressId'] = pressId
    if bookId:
        request.session['bookId'] = bookId
    if unitId:
        request.session['unitId'] = unitId
    if lessonId:
        request.session['lessionId'] = lessonId
    if testId:
        request.session['testId'] = testId
    if dictype:
        request.session['dictype'] = dictype
    return render(request, 'dictation/dispwords.html')

def qryWords(request):
    dicType = request.session['dictype']
    print('dictype: %s' % dicType)
    if dicType == 'newword':
        lessonId = request.session['lessionId']
        print(lessonId)
        aWords = dictation.models.Word.objects.filter(lesson=lessonId)
        jsonWords = jsonArraySet(aWords, ['id', 'word'])
        # request.session['words'] = jsonWords
        # print(jsonWords)
    elif dicType == 'wrongword':
        testId = request.session['testId']
        print('testid: %s' % testId)
        aWords = dictation.models.Word.objects.filter(testword__wrong__exact=True,testword__test__exact=testId)
        jsonWords = jsonArraySet(aWords, ['id', 'word'])
        print(jsonWords)
    request.session['words'] = jsonWords
    print(jsonWords)
    dRes = {'words': jsonWords}
    return JsonResponse(dRes)

def checkWords(request):
    return render(request, 'dictation/checkwords.html')

def dictating(request):
    lessonId = request.session['lessionId']
    unitId = request.session['unitId']
    bookId = request.session['bookId']
    pressId = request.session['pressId']

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
    print('dictate lesson: %s' % lesson)
    print('dictate unit: %s' % unit)
    test = models.Test.tests.create(press,book,unit,lesson)
    test.save()
    request.session['testId'] = test.id
    return render(request,'dictation/dictating.html')

def qryVoice(request):
    print('qryVoice...')
    aWords = request.session['words']
    print(aWords)
    print('make voice...')
    voicePath = os.path.join(happyproj.settings.BASE_DIR, 'static', 'dictation', 'voice')
    builder = voicebuilder.VoiceBuilder(voicePath)
    builder.builderVoice(aWords)
    # jsonVoice = jsonArraySet(aWords, ['id', 'word', 'pinyin', 'voice'])
    dRes = {'words': aWords}
    return JsonResponse(dRes)

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
    return

def tabtest(request):
    return render(request,'dictation/tabtest.html')
