#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"

import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

course_dict = {
    'name': '课程名称',
    'introduction': '课程介绍',
    'price': 0.11
}


# Django FBV 编写API接口
@csrf_exempt
def course_list(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps(course_dict), content_type='application/json')
        # return JsonResponse(course_dict)

    if request.method == 'POST':
        course = json.loads(request.body.decode('utf-8'))
        return HttpResponse(json.dumps(course), content_type='application/json')
        # return JsonResponse(coures)


# Django CBV 编写API接口
@method_decorator(csrf_exempt, name='dispatch')
class CourseList(View):

    def get(self, request):
        return JsonResponse(course_dict)

    def post(self, request):
        course = json.loads(request.body.decode('utf-8'))
        return JsonResponse(course)
