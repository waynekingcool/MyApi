# -*- coding: utf-8 -*-
# @Author: wayneking
# @Date:   2018-01-12 10:00:59
# @Last Modified by:   wayneking
# @Last Modified time: 2018-04-04 17:10:58
from rest_framework import serializers
from xiaoshuoApi.models import Book
from xiaoshuoApi.models import Chapacter
from xiaoshuoApi.models import AuthUser

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = ('bookid','bookname','bookauthor','lastupdate')

class ChapacterSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		fields = kwargs.pop('fields', None)
		# Instantiate the superclass normally
		super(ChapacterSerializer, self).__init__(*args, **kwargs)
		if fields is not None:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(fields)
			existing = set(self.fields.keys())
			for field_name in existing - allowed:
				self.fields.pop(field_name)
				
	class Meta:
		model = Chapacter
		fields = ('chapid','bookid','title','content')

class AuthUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = AuthUser
		# ,'is_superuser'
		fields = ('userid','username','last_login','password','is_superuser','email','is_staff','is_active','date_joined')

