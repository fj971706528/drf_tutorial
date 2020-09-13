#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True
