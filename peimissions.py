#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerReadOnly(permissions.BasePermission):
    """自定义权限：只允许对象的所有者能够执行该操作"""

    def has_object_permission(self, request, view, obj):
        """
        所有的request请求都有读权限，因此一律允许GET/HEAD/OPTIONS方法
        :param request:
        :param view:
        :param obj:
        :return: bool
        """
        if request.method in SAFE_METHODS:
            return True
        # 对象的所有者才具有对该数据的操作权限
        return obj.teacher == request.user