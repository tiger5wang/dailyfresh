# -*- coding: utf-8 -*-
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelelte=models.BooleanField(default=False)
    class Meta:
        db_table = 'typeinfo'
    def __str__(self):
        return self.ttitle.encode('utf8')

class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=20)
    gpic=models.ImageField(upload_to='df_goods')
    gprice=models.DecimalField(max_digits=5,decimal_places=2)
    isDelete=models.BooleanField(default=False)
    gunit=models.CharField(max_length=20,default='500g')
    gclick=models.IntegerField()
    gintroduction=models.CharField(max_length=200)
    gcount=models.IntegerField()
    gcontent=HTMLField()
    gtype=models.ForeignKey('TypeInfo')
    class Meta:
        db_table = 'goodsinfo'