from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    """
    index视图
    :param request: 包含了请求信息的请求对象，类型 HttpRequest
    :return: 响应对象
    """
    return HttpResponse("hello the world!")
