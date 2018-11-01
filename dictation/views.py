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

def dispWords(request):
    lessonId = request.GET.get('lesson',None)
    pressId = request.GET.get('press', None)
    bookId = request.GET.get('book', None)
    unitId = request.GET.get('unit', None)
    if lessonId:
        request.session['lessionId'] = lessonId
    if pressId:
        request.session['pressId'] = pressId
    if bookId:
        request.session['bookId'] = bookId
    if unitId:
        request.session['unitId'] = unitId
    return render(request, 'dictation/dispwords.html')

def qryWords(request):
    lessonId = request.session['lessionId']
    print(lessonId)
    aWords = dictation.models.Word.objects.filter(lesson=lessonId)
    jsonWords = jsonArraySet(aWords, ['id', 'word'])
    request.session['words'] = jsonWords
    print(jsonWords)
    dRes = {'words': jsonWords}
    return JsonResponse(dRes)

def dictating(request):
    lessonId = request.session['lessionId']
    unitId = request.session['unitId']
    bookId = request.session['bookId']
    pressId = request.session['pressId']
    if lessonId:
        # lesson = dictation.models.Lesson.objects.filter(id=lessonId)
        lesson = dictation.models.Lesson.objects.get(id=lessonId)
    if unitId:
        unit = dictation.models.Unit.objects.get(id=unitId)
    if bookId:
        book = dictation.models.Book.objects.get(id=bookId)
    if pressId:
        press = dictation.models.Press.objects.get(id=pressId)
    test = models.Test.tests.create(press,book,unit,lesson)
    test.save()
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

def dispPinyin(request):
    return render(request,'dictation/index.html')


