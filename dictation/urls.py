from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^initQry/$', views.initQry),
    url(r'^qryLesson/$', views.qryLesson),
    url(r'^qryTest/$', views.qryTest),
    url(r'^dispwords/$', views.dispWords),
    # url(r'^checkwords/$', views.checkWords),
    url(r'^qryWords/$', views.qryWords),
    # url(r'^dictating/$', views.dictating),
    url(r'^qryVoice/$', views.qryVoice),
    url(r'^makeVoice/$', views.makeVoice),
    url(r'^qryTestWords/$', views.qryTestWords),
    url(r'^saveTest/$', views.saveTest),
    url(r'^tabtest/$', views.tabtest),
]