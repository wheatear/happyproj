from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import FileResponse
import happyproj.settings

import os,logging,time
import base64

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
        #  获取base64格式的图片
        homeworkImg = request.POST.get("homework", None)
        # 提取出base64格式，并进行转换为图片
        index = homeworkImg.find('base64,')
        base64Str = homeworkImg[index + 6:]
        img = base64.b64decode(base64Str)
        # 将文件保存
        backupDate = time.strftime("%Y%m%d%H%M%S")
        fileName = 'mathImg_%s' % backupDate
        fullName = os.path.join(happyproj.settings.STATIC_ROOT, 'hcm', 'homework',fileName)
        with open(fullName,'wb') as file:
            file.write(img)
        return JsonResponse({'mathFile': fileName})


def correct(request):
    pass
