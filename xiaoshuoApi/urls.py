# -*- coding: utf-8 -*-
# @Author: wayneking
# @Date:   2018-01-12 10:09:20
# @Last Modified by:   wayneking
# @Last Modified time: 2018-04-04 18:01:08

from django.conf.urls import url
from xiaoshuoApi import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
urlpatterns = [
	url(r'^book/$',views.BookList.as_view()),
	url(r'chap/$',views.ChapList.as_view()),
	url(r'^chapContent/$',views.ChapContent.as_view()),
	url(r'^userlist/$',views.UserList.as_view()),
	url(r'^userDetail/$',views.UserDetail.as_view()),
	# 页面右上角出现 登录 按钮
	url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
	url(r'^makeToken/$',views.MakeToken.as_view()),

	# 爬虫接口
	url(r'^index/',views.XiaoShuoIndex.as_view()),
	url(r'^bookInfo/$',views.BookInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)