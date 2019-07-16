from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import FileResponse
import happyproj.settings
from login.views import check_login

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hcm.v20181106 import hcm_client, models

import os,logging,time
import base64
import urllib
import json


# Create your views here.

logger = logging.getLogger('django')
errlog = logging.getLogger('error')

@check_login
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
    logger.info('correct math homework')
    rs = None
    if request.method == "POST":
        file = request.POST.get("hwImg", None)
        mathUrl = "https://193.112.63.237/static/hcm/homework/%s" % file
        fullFile = os.path.join(happyproj.settings.STATIC_ROOT, 'hcm', 'homework',file)
        with open(fullFile, 'rb') as f:
            img = f.read()
        b64Str = base64.b64encode(img)
        logger.debug("mathUrl: %s", mathUrl)
        try:
            cred = credential.Credential("AKIDNcbKo3PlKekbDbJcEhvzmLegSyKQguHO", "2GIxRgfOvFK93oIWYK0Sr1uXx83h5DY9")
            httpProfile = HttpProfile()
            httpProfile.endpoint = "hcm.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = hcm_client.HcmClient(cred, "ap-guangzhou", clientProfile)

            req = models.EvaluationRequest()
            # params = '{"SessionId":"hcm1","HcmAppid":"hcm_1001479","Url":mathUrl,"RejectNonArithmeticImage":true}'
            params = '{"SessionId":"hcm1","HcmAppid":"hcm_1001479","Image":"%s","RejectNonArithmeticImage":true}' % str(b64Str,"utf-8")
            # logger.debug(params)
            req.from_json_string(params)

            resp = client.Evaluation(req)
            logger.info(resp.to_json_string())
            rs = resp.to_json_string()


        except TencentCloudSDKException as err:
            logger.error(err)
    return JsonResponse({'mathCorrection': json.loads(resp.to_json_string())})
