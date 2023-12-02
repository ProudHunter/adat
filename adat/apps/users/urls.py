"""定义当前子应用下的所有路由"""
from django.urls import path

from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    # 每个路由信息都需要使用path函数来构造
    # path(路径, 视图函数的名字)
    path('index/', views.index)
]
