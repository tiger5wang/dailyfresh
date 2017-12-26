#coding=utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# 如果未登录先转到登陆界面
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            redi = HttpResponseRedirect('/user/login/')
            redi.set_cookie('url',request.get_full_path())
            return redi
    return login_fun