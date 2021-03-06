from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index$', views.index),
    url(r'^initQry/$', views.initQry),
    url(r'^qryBook/$', views.qryBook),
    url(r'^qryUnit/$', views.qryUnit),
    url(r'^qryLesson/$', views.qryLesson),
    url(r'^qryTest/$', views.qryTest),
    url(r'^dispwords/$', views.dispWords),
    # url(r'^checkwords/$', views.checkWords),
    url(r'^qryWords/$', views.qryWords),
    url(r'^dictate/$', views.dictate),
    # url(r'^qryVoice/$', views.qryVoice),
    url(r'^makeVoice/$', views.makeVoice),
    url(r'^qryTestWords/$', views.qryTestWords),
    url(r'^saveTest/$', views.saveTest),
    url(r'^wordimport/$', views.wordImport),
    url(r'^qryLsWords/$', views.qryLessonWords),
    url(r'^saveLsWords/$', views.saveLessonWords),
    url(r'^delLsWords/$', views.delLessonWords),
    url(r'^tabtest/$', views.tabtest),
]

handler404 = views.page_not_found
