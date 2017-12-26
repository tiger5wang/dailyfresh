# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import *
from df_cart.models import CartInfo

def index(request):
    typelist = TypeInfo.objects.all()
    type01 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type02 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type12 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type22 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type32 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type42 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type52 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context={'title':'首页','guest_cart':1,
             'type01':type01,'type02':type02,
             'type11': type11, 'type12': type12,
             'type21': type21, 'type22': type22,
             'type31': type31, 'type32': type32,
             'type41': type41, 'type42': type42,
             'type51': type51, 'type52': type52,
             }
    return render(request,'df_goods/index.html',context)

def list(request,id):
    # types = TypeInfo.objects.get(pk=int(id))
    typelist = TypeInfo.objects.all()
    goods = typelist[int(id)].goodsinfo_set.order_by('-id')[0:15]
    news = typelist[int(id)].goodsinfo_set.order_by('-id')[0:2]
    context = {'title': '商品列表', 'guest_cart': 1,'goods':goods,'news':news,'id':id}
    return render(request,'df_goods/list.html',context)

def detail(request,id):
    # 将商品的点击量加一
    goods=GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()
    # 将新加入的两个商品（id倒叙排列的前两个）展现在新品推荐处
    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': goods.gtype.ttitle, 'guest_cart': 1,
               'g': goods, 'id': id, 'news': news}
    response = render(request, 'df_goods/detail.html', context)

    # 将最进浏览的商品放到个人中心的最近浏览处
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d'%goods.id  # 将这个商品的id号转为字符串型，用于添加到goods_ids中
    if goods_ids != '':    # 判断是否又浏览记录，如果有则继续判断
        goods_ids1 = goods_ids.split(',')  # 转换为列表
        if goods_ids1.count(goods_id)>=1:   #判断次商品有没有浏览记录，如果有则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)  # 添加到第一个
        if len(goods_ids1)>=6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id  # 如果没有则直接赋值给goods_ids
    response.set_cookie('goods_ids',goods_ids)   # 写入cookie

    return response

# 购物车数量
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id'])
    else:
        return 0

from haystack.views import SearchView
class MySearch(SearchView):
    def extra_context(self):
        context = super(MySearch, self).extra_context()
        context['title'] = '搜索'
        context['guest_cart'] = 1
        context['cart_count'] = cart_count(self.request)
        return context

