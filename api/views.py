from django.core import serializers
from django.http import JsonResponse
from rest_framework.views import APIView

from api import models
from api.models import UserInfo
from utils.authentication import Authtication
from utils.permissions import MyPermission
from utils.throttle import VisitThrottle, UserThrottle

ORDER_DICT = {
    1: {
        'name': 'udp',
        'desc': 'udp',
    },
    2: {
        'name': 'phone',
        'desc': 'phone',
    },
}


def md5(user):
    import hashlib
    import time

    cur_time = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(cur_time, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    authentication_classes = ()
    permission_classes = ()
    throttle_classes = (VisitThrottle,)

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为登录用户创建token
            token = md5(user)
            # 存在就更新, 不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常,请重新登陆'
        return JsonResponse(ret)


class OrderView(APIView):
    """
    订单相关的业务
    """
    authentication_classes = (Authtication,)
    permission_classes = (MyPermission,)
    throttle_classes = (UserThrottle,)

    def get(self, request, *args, **kwargs):
        # token = request._request.GET.get('token')
        # if not token:
        #     return JsonResponse(data={'msg': 'Token must be required'})

        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    用户信息相关业务
    """
    authentication_classes = (Authtication,)
    permission_classes = (MyPermission,)
    throttle_classes = (UserThrottle,)

    def get(self, request, *args, **kwargs):
        ret = serializers.serialize('json', UserInfo.objects.all())
        return JsonResponse(data=ret, safe=False)
