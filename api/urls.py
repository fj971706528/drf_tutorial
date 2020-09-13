#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"

from django.urls import path
from api import views


urlpatterns = [
    path("v1/auth/", views.AuthView.as_view(), name="v1-auth"),
    path("v1/order/", views.OrderView.as_view(), name="v1-order"),
    path("v1/users/", views.UserInfoView.as_view(), name="v1-user-info"),
]