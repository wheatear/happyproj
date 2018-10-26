from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^initQry/$', views.initQry),
    url(r'^lesson/$', views.lesson),
    url(r'^dictating/$', views.dictating),
    url(r'^dispWords/$', views.dispWords),
    url(r'^dispPinyin/$', views.dispPinyin),
]