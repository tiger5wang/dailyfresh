# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import HttpResponseRedirect,JsonResponse
from . import user_decorator
import sys
sys.path.append("/home/python/Desktop/django_test/dailyfresh/dailyfresh/df_goods/models.py")
from df_goods.models import GoodsInfo

def register(request):
    return render(request,'df_user/register.html')

def user_exit(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uanme=uname).count()
    return JsonResponse({'count':count})

def register_handle(request):
    # 接收用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1=sha1()
    s1.update('upwd')
    upwd3=s1.hexdigest()
    # 创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    # 注册成功，转到登陆页面
    return redirect('/user/login/')

def login(request):
    uname = request.COOKIES.get('uname','')
    context={'title':'用户登陆','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 获取用户输入的用户名，密码
    post=request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember',0)
    # 根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)
    print(uname)
    # 如果用户名正确，验证密码,密码正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update('upwd')
        if s1.hexdigest() == users[0].upwd:
            url= request.COOKIES.get('url','/goods/index/')
            redi = HttpResponseRedirect(url)
            if remember!=0:
                redi.set_cookie('uname',uname)
            else:
                redi.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return redi
        # 密码不正确
        else:
            context = {'title': '用户登陆', 'error_name': 0, 'error_pwd':1, 'uname': uname,'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    # 用户名不正确，重新输入
    else:
        context = {'title': '用户登陆', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/goods/index/')

@user_decorator.login
def user_center_info(request):
    uname = request.session['user_name']
    uemail = UserInfo.objects.get(id=request.session['user_id']).uemail
    uphone = UserInfo.objects.get(id=request.session['user_id']).uphone
    uaddress = UserInfo.objects.get(id=request.session['user_id']).uaddress
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 = goods_ids.split(',')
    goods_list =[]
    # GoodsInfo.objects.filter(id__in=goods_ids1)
    for goods_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context={'title':'用户中心','page_name':1,
             'uname':uname,'uemail':uemail,
             'uphone':uphone,'uaddress':uaddress,
             'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def user_center_order(request):
    context={'title':'全部订单','page_name':1}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
    user = UserInfo.objects.get(uname=request.session['user_name'])
    address = user.uaddress
    receiver = user.ureceiver
    phone = user.uphone
    context = {'title': '收货地址', 'page_name': 1,'address':address,
               'receiver':receiver,'phone':phone}
    return render(request,'df_user/user_center_site.html',context)

@user_decorator.login
def site_handle(request):
    # 接受用户输入的地址信息
    post = request.POST
    receiver = post.get('receiver')
    phone = post.get('phone')
    postcode = post.get('postcode')
    address = post.get('address')
    # 保存用户输入的地址信息
    user = UserInfo.objects.get(uname=request.session['user_name'])
    user.ureceiver = receiver
    user.uaddress = address
    user.uphone = phone
    user.upostcode = postcode
    user.save()
    context = {'title': '收货地址', 'page_name': 1,'receiver':receiver,'phone':phone,'postcode':postcode,'address':address}
    return render(request,'df_user/user_center_site.html',context)



