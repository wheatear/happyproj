from django.conf.urls import url
from . import views

urlpatterns = [
    # html
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^dispwords/$', views.dispWords),
    url(r'^tabtest/$', views.tabtest),
    url(r'^wordimport/$', views.wordImport),

    # json
    url(r'^initQry/$', views.initQry),
    url(r'^qryBook/$', views.qryBook),
    url(r'^qryUnit/$', views.qryUnit),
    url(r'^qryLesson/$', views.qryLesson),
    url(r'^qryTest/$', views.qryTest),
    # url(r'^checkwords/$', views.checkWords),
    url(r'^qryWords/$', views.qryWords),
    url(r'^dictate/$', views.dictate),
    # url(r'^qryVoice/$', views.qryVoice),
    url(r'^makeVoice/$', views.makeVoice),
    url(r'^qryTestWords/$', views.qryTestWords),
    url(r'^saveTest/$', views.saveTest),
    url(r'^qryLsWords/$', views.qryLessonWords),
    url(r'^saveLsWords/$', views.saveLessonWords),
    url(r'^delLsWords/$', views.delLessonWords),
]

handler404 = views.page_not_found
