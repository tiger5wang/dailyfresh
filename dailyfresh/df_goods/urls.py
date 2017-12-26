from django.conf.urls import url
from views import *
import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^list/(\d+)/$',views.list),
    url(r'^(\d+)/$',views.detail),
    url(r'^search/',MySearch())
]