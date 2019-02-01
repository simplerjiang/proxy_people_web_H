"""proxy_people_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url,patterns
from django.contrib import admin
from main_app.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admins/', include(admin.site.urls)),
    url(r'^$',index_page,name='index'),
    url(r'^accounts/login/$',login_view,name='login'),
    url(r'^accounts/logout/$',log_out_view,name='logout'),
    url(r'^accounts/register/$',reg,name='register'),
    url(r'^shop/$',shop_page,name='shop'),
    url(r'^test/$', test_web, name='test'),
    url(r'admin/post_code/$',Admin_Post_Code,name="Admin_Post_Code"),
    url(r'admin/post_vip/$',Admin_Post_Vip,name="Admin_Post_Vip"),
    url(r'^shop/item/(?P<software_id>[0-9]+)/$',shop_detail,name="shop_detail"),
    url(r'^shop/item/buy_items/$',buy_items,name='buy_items'),
    url(r'^shop/check_deal/(?P<deal_code>[0-9]+)/$',check_deal,name="check_deal"),
    url(r'^shop/check_my_code/(?P<code>[a-zA-Z0-9]+)/$', check_my_code, name="check_my_code"),
    url(r'^shop/check_all_deal/$',check_all_deal,name='check_all_deal'), #查看自己的订单
    url(r'^shop/check_all_down_deal/$', check_all_down_deal, name='check_all_down_deal'),  #查看下级代理的订单
    url(r'^shop/check_code_page/$',check_code_page,name='check_code_page'), #搜索卡密的页面
    url(r'^profile_setting/$',profile_setting,name='profile_setting'), #个人资料设置
    url(r'^check_all_auth/$',check_all_auth,name='check_all_auth'), #查看所有授权 #要删掉
    url(r'^check_auth/(?P<pk>[0-9]+)/$',check_auth,name='check_auth'), #查看授权 #要删掉
    url(r'^check_all_down_proxy/$',check_all_down_proxy,name='check_all_down_proxy'), #查看所有下级代理
    url(r'^change_down_proxy_info/(?P<pk>[0-9]+)/$',change_down_proxy_info,name='change_down_proxy_info'),
    url(r'^create_new_down_account/$',create_new_down_account,name='create_new_down_account'),
    url(r'^transfer/$',transfer,name='transfer'), #转账
]

urlpatterns +=patterns('',
                        url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
                        url(r'^static/<?P<path>.*>$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
                       )