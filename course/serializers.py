#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        # exclude = ('id',)
        # fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at',)
        fields = '__all__'
        depth = 2

# class CourseSerializer(serializers.HyperlinkedModelSerializer):
#     teacher = serializers.ReadOnlyField(source='teacher.username')
#
#     class Meta:
#         model = Course
#         # url是默认值,可在settings.py中RESTFRAMEWORK设置URL_FIELD_NAME
#         fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at',)
