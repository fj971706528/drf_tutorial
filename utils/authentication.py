#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from api import models


class Authtication(BaseAuthentication):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass