#coding=utf-8
from django.shortcuts import render,redirect
from df_user.models import UserInfo
from df_cart.models import CartInfo
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal

def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    address = user.uaddress
    receiver = user.ureceiver
    phone = user.uphone
    get = request.GET
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    context = {'title':'确认订单','address':address,'receiver':receiver,'phone':phone,
               'user':user,'carts':carts,'cart_ids':','.join(cart_ids)}
    return render(request,'df_order/place_order.html',context)

@transaction.atomic()
def order_handle(request):
    # 创建还原点
    tran_id = transaction.savepoint()
    # 接受购物车编号
    cart_ids = request.POST.get('cart_ids')
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST.get('total'))
        order.save()
        # 创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrederDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gcount >= cart.count:  # 如果库存大于购物车数量
                # 减少商品库存
                goods.gcount = cart.goods.gcount-cart.count
                goods.save()
                # 完善详细信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车数据
                cart.delete()
            else:  # 如果库存小鱼购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('=============%s'%e)
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/user_center_order/')

