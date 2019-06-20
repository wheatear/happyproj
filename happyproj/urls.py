"""happyproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from login import views
from dictation import views as dviews
from hcm import views as hcmViews
from django.views.generic.base import RedirectView

urlpatterns = [
    path(r'favicon.ico',RedirectView.as_view(url=r'static/favicon.ico')),
    path(r'MP_verify_EddIaEBDpA3ond3X.txt',RedirectView.as_view(url=r'static/MP_verify_EddIaEBDpA3ond3X.txt')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=r'dictation/')),
    path(r'dictation/', include('dictation.urls')),
    path(r'login/', views.login),
    path(r'logout/', views.logout),
    path(r'register/', views.register),
    path(r'mathcorrection/', hcmViews.mathCorrection),
]
handler404 = "login.views.page_not_found"

