from django.shortcuts import render

# Create your views here.
def mathCorrection(request):
    # request.session['ip'] = ip
    # extra = getExtra(request)
    # logger = LoggerAdapter(initLogger,extra)

    # logger.info('access',extra)
    return render(request,'hcm/mathcorrection.html')
