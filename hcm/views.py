from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import FileResponse

import os,logging

# Create your views here.

logger = logging.getLogger('django')
errlog = logging.getLogger('error')

def mathCorrection(request):
    # request.session['ip'] = ip
    # extra = getExtra(request)
    # logger = LoggerAdapter(initLogger,extra)

    # logger.info('access',extra)
    return render(request,'hcm/mathcorrection.html')

def uploadMath(request):
    logger.info('upload math homework')
    if request.method == "POST":  # 请求方法为POST时，进行处理
        homework = request.POST.get("homework", None)


def correct(request):
    pass
