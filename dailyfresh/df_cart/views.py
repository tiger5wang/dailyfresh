#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from df_user import user_decorator
from models import *

# 购物车页面
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context ={'title':'购物车','page_name':1,'carts':carts}
    return render(request,'df_cart/cart.html',context)

@user_decorator.login
def add(request,gid,count):
    # 获取用户和商品的id号
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 判断该商品有没存放在该用户的购物车中
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)  #这是该用户的购物车中该商品的对象
    if len(carts)>=1:
        cart = carts[0]
        cart.count +=count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

# 修改购物车中商品的数量
def edit(request,cart_id,count):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        count1=cart.count=int(count)
        cart.save()
        data={'ok':1}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

# 删除购物车中点击的商品信息
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)