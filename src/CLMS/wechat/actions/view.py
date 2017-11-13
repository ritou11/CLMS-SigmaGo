# coding:utf-8
import inspect
from django.http import HttpResponse
from wechat.utils.com import json
from wechat.models import Actions


def all_actions(request):
    pass
    return HttpResponse(json.dumps(d))
