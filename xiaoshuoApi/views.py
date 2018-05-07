from django.shortcuts import render
from xiaoshuoApi.models import Book
from xiaoshuoApi.models import Chapacter
from xiaoshuoApi.models import AuthUser
from xiaoshuoApi.serializers import BookSerializer
from xiaoshuoApi.serializers import ChapacterSerializer
from xiaoshuoApi.serializers import AuthUserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
# 测试爬虫
from xiaoshuoApi.Splider.Splider import SpliderPY
from django.http import HttpResponse

# Token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your views here.

# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 1000
#     page_size_query_param = 'page_size'

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'

class LimitResultsSetPagination(LimitOffsetPagination):
    # 默认每页显示的数据条数
    default_limit = 2
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = None

class BookList(APIView):
	def get(self, request, format=None):
		book = Book.objects.all()
		# serializer = BookSerializer(book,many=True)
		paginator = StandardResultsSetPagination()
		page_user_list = paginator.paginate_queryset(book, self.request,view=self)
		serializer = BookSerializer(page_user_list,many=True)
		return paginator.get_paginated_response(serializer.data)
		# return Response(serializer.data)

class ChapList(APIView):
	def get(self, request, format=None):
		chap = Chapacter.objects.all()
		paginator = StandardResultsSetPagination()
		page_chap_list = paginator.paginate_queryset(chap,self.request,view=self)
		#获取parames
		getTitle = request.query_params.get('temp')
		getChapId = request.query_params.get('chapid')
		if getTitle == "true":
			serializer = ChapacterSerializer(page_chap_list,fields=('bookid','chapid','title'),many=True)
		else:
			serializer = ChapacterSerializer(page_chap_list,many=True)
		return paginator.get_paginated_response(serializer.data)

class ChapContent(APIView):
	def get(self, request, format=None):
		chapId = request.query_params.get('chapid')
		if chapId:
			chap = Chapacter.objects.get(chapid=chapId)
			serializer = ChapacterSerializer(chap)
			return Response(serializer.data)
		else:
			chap = Chapacter()
			serializer = ChapacterSerializer(chap)
			return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(APIView):
	def get(self, request, format=None):
		users = AuthUser.objects.all()
		serializer = AuthUserSerializer(users,many=True)
		return Response(serializer.data)


class UserDetail(APIView):
	def get(self, request, format=None):
		userid = request.query_params.get('userid')
		if userid:
			user = AuthUser.objects.get(userid=userid)
			serializer = AuthUserSerializer(user)
			return Response(serializer.data)
		else:
			user = AuthUser()
			serializer = AuthUserSerializer(user)
			return Response(status=status.HTTP_204_NO_CONTENT)

# 为用户建立token
class MakeToken(APIView):
	def get(self, request, format=None):
		for user in User.objects.all():
			print("1111")
			Token.objects.get_or_create(user=user)
		return Response(status=status.HTTP_204_NO_CONTENT)

# 根据爬虫爬来的内容进行展示
class XiaoShuoIndex(APIView):
	def get(self,request, format=None):
		responseJson = SpliderPY.SoupSplider("http://m.biqukan.com/")
		# return Response(responseJson,status=status.HTTP_200_OK)
		return HttpResponse(content=responseJson)

# 小说信息和所有章节
class BookInfo(APIView):
	def get(self,request, format=None):
		path = request.query_params.get('path')
		responseJson = SpliderPY.bookInfoSplider(path)
		return HttpResponse(content=responseJson)

# 章节内容
class ChapContent(APIView):
	def get(self,request, format=None):
		path = request.query_params.get('path')
		responseJson = SpliderPY.ChapContent(path)
		return HttpResponse(content=responseJson)