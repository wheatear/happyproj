from django.conf.urls import url
from . import views

urlpatterns = [
    # html
    url(r'^$', views.mathCorrection),
    url(r'^index$', views.mathCorrection),
    url(r'^uploadMath/$', views.uploadMath),
    url(r'^correct/$', views.correct),
    # url(r'^wordimport/$', views.wordImport),

    # json
    # url(r'^initQry/$', views.initQry),
    # url(r'^qryBook/$', views.qryBook),
    # url(r'^qryUnit/$', views.qryUnit),
    # url(r'^qryLesson/$', views.qryLesson),
    # url(r'^qryTest/$', views.qryTest),
    # # url(r'^checkwords/$', views.checkWords),
    # url(r'^qryWords/$', views.qryWords),
    # url(r'^dictate/$', views.dictate),
    # # url(r'^qryVoice/$', views.qryVoice),
    # url(r'^makeVoice/$', views.makeVoice),
    # url(r'^qryTestWords/$', views.qryTestWords),
    # url(r'^saveTest/$', views.saveTest),
    # url(r'^qryLsWords/$', views.qryLessonWords),
    # url(r'^saveLsWords/$', views.saveLessonWords),
    # url(r'^delLsWords/$', views.delLessonWords),
]

# handler404 = views.page_not_found