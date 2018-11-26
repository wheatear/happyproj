from django.shortcuts import render
from functools import wraps

# Create your views here.

def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner
