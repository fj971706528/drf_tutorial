#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from course.models import Course
from course.serializers import CourseSerializer
from peimissions import IsOwnerReadOnly


@receiver(post_save, sender=User)
def generate_token(sender, instance=None, created=False, **kwargs):
    """
    创建用户后触发信号机制，发送消息创建Token
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Token.objects.create(user=instance)



"""1、函数式编程 Function Based View"""


@api_view(["GET", "POST"])
@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes((BasicAuthentication, SessionAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated, IsAdminUser))
def course_list(request):
    """
    获取所有课程信息或新增单条课程信息
    :param request:
    :return:
    """
    if request.method == "GET":
        ser = CourseSerializer(instance=Course.objects.all(), many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        ser = CourseSerializer(data=request.data, partial=True)
        if ser.is_valid():
            ser.save(teacher=request.user)
            return Response(data=ser.data, status=status.HTTP_201_CREATED)
        return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def course_detail(request, pk):
    """
    获取、更新、删除单条课程
    :param request:
    :param pk:
    :return:
    """
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
    else:

        if request.method == "GET":
            ser = CourseSerializer(instance=course)
            return Response(data=ser.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            ser = CourseSerializer(instance=course, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(data=ser.data, status=status.HTTP_200_OK)
            return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


"""2、类视图 Class Based View"""


class CourseList(APIView):

    authentication_classes = (BasicAuthentication, SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        queryset = Course.objects.all()
        ser = CourseSerializer(instance=queryset, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser = CourseSerializer(data=request.data)
        if ser.is_valid():
            ser.save(teacher=self.request.user)
            return Response(data=ser.data, status=status.HTTP_201_CREATED)
        return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):

    @staticmethod
    def get_object(pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return

    def get(self, request, pk):
        obj = self.get_object(pk=pk)
        if obj:
            ser = CourseSerializer(instance=obj)
            return Response(data=ser.data, status=status.HTTP_200_OK)
        return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        obj = self.get_object(pk=pk)
        if obj:
            ser = CourseSerializer(instance=obj, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(data=ser.data, status=status.HTTP_200_OK)
            return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if obj:
            obj.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)


"""3、通用类视图 Generic Class Based View"""


class GCourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class GCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


"""4、DRF的视图集viewsets"""


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)