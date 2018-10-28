from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^initQry/$', views.initQry),
    url(r'^qryLesson/$', views.qryLesson),
    url(r'^dispwords/$', views.dispWords),
    url(r'^qryWords/$', views.qryWords),
    url(r'^dictating/$', views.dictating),
    url(r'^qryVoice/$', views.qryVoice),
]