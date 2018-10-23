from django.shortcuts import render
from django.http import JsonResponse
import happyproj.settings

import dictation
import logging

# Create your views here.
def index(request):
    return render(request,'dictation/index.html')

def lesson(request):
    return render(request,'dictation/index.html')

def dictating(request):
    return render(request,'dictation/index.html')

def dispWords(request):
    return render(request,'dictation/index.html')

def dispPinyin(request):
    return render(request,'dictation/index.html')

