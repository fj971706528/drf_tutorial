#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Samul__"
# import time
#
# VISIT_RECORD = {}
#
# class VisitThrottle:
#
#     def __init__(self):
#         self.history = None
#
#     def allow_request(self, request, view):
#         remote_addr = request.META.get('REMOTE_ADDR')
#         cur_time = time.time()
#         if remote_addr not in VISIT_RECORD:
#             VISIT_RECORD[remote_addr] = [cur_time,]
#             return True
#         history = VISIT_RECORD.get(remote_addr)
#         self.history = history
#         while history and history[-1] < cur_time - 60:
#             history.pop()
#
#         if len(history) < 3:
#             history.insert(0, cur_time)
#             return True
#
#     def wait(self):
#         cur_time = time.time()
#         return 60 - (cur_time - self.history[-1])


from rest_framework.throttling import SimpleRateThrottle

class VisitThrottle(SimpleRateThrottle):
    scope = "cplatform"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    scope = "cplatformUser"

    def get_cache_key(self, request, view):
        # return self.get_ident(request)
        return request.user.username