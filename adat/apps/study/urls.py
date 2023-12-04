"""定义当前子应用下的所有路由"""
from django.urls import path, re_path

from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns = [
    # 每个路由信息都需要使用path函数来构造
    # path(路径, 视图函数的名字)
    path('index/', views.index),

    # 利用正则组才可以提取 url 路径参数，对应位置参数
    re_path(r'weather/([a-z]+)/(\d{4})/', views.weather),

    # 利用正则组起别名提取 url 路径参数，对应关键字参数。（如果给正则组起了别名，
    # 那么对应的形参名必须和别名一致、顺序可以不一致），它在调用的时候等价于 views.weather(city=xxx，year=xxx)
    re_path(r'weather2/(?P<city>[a-z]+)/(?P<year>\d{4})/$', views.weather2),

    # /qs/?a=1&b=2&a=3
    path('qs/', views.qs),

    path('body/', views.get_body),

    path('body_json/', views.get_body_json),

    path('get_user/', views.get_user),

    path('demo_view/', views.demo_view),

    path('demo_view1/', views.demo_view1),

    path('session_demo/', views.session_demo),

    # 函数视图：注册
    # url(r'^register/$', views.register, name='register'),
    # 类视图：注册
    # as_view()方法的作用将类中的方法转换为函数，根据请求方法动态查找类中的方法
    path('register/', views.RegisterView.as_view()),

]

"""使用类视图开发 REST 接口
注意：不会在 API 文档中显示
"""
urlpatterns += [
    # 列表视图的路由
    path('books/', views.BookListView.as_view()),
    # 详情视图的路由
    re_path('books/(?P<pk>\d+)/', views.BookDetailView.as_view())
]

"""使用 DRF 的 APIView 基类开发 REST 接口
`APIView` 与 `View` 的不同之处在于：
- 传入到视图方法中的是 REST framework 的`Request`对象，而不是 Django 的 `HttpRequeset` 对象；
- 视图方法可以返回 REST framework 的 `Response` 对象，视图会为响应数据设置（render）符合前端要求的格式；
- 任何 `APIException` 异常都会被捕获到，并且处理成合适的响应信息；
- 在进行 `dispatch()` 分发前，会对请求进行身份认证、权限检查、流量控制。(重写了 `dispatch()` 方法)
"""
urlpatterns += [
    path('books_apiview/', views.BookListAPIView.as_view()),
    re_path(r'books_apiview/(?P<pk>\d+)/', views.BookDetailAPIView.as_view())
]

"""使用 DRF 的 GenericAPIView 开发 REST 接口
继承自 APIView，主要增加了操作序列化器和数据库查询的方法
"""
urlpatterns += [
    path('books_generic_apiview/', views.BookListGenericAPIView.as_view()),
    re_path(r'books_generic_apiview/(?P<pk>\d+)/', views.BookDetailGenericAPIView.as_view())
]

"""
GenericAPIView 类搭配 5 个扩展类：
mixin 类提供用于基本视图行为的操作增删改查，如 ListModelMixin 提供 .list() 方法
视图可以通过继承相应的扩展类来复用代码，减少自己编写的代码量.
"""

urlpatterns += [
    path('books_mixin/', views.BookListMixinView.as_view()),
    re_path(r'books_mixin/(?P<pk>\d+)/', views.BookDetailMixinView.as_view())
]

"""
在上面的案例中，仍然要写 get()、post() 等方法.
REST Framework 提供了一组已经混合的通用视图，可以使用它来进一步精简 views.py 模块.
例如 ListAPIView 提供 get() 方法，继承自：GenericAPIView、ListModelMixin
CreateAPIView 提供 post() 方法，继承自：GenericAPIView、CreateModelMixin
"""

urlpatterns += [
    path('books_common_view/', views.BookListCommonView.as_view()),
    re_path(r'books_common_view/(?P<pk>\d+)/', views.BookDetailCommonView.as_view())
]

"""
上面列表视图和详情视图中有两行代码是完全一样的，无法再进行精简，原因在于两个类都实现了 get() 方法，
而  Django 中 View 类的 as_view() 中的 dispatch() 方法分发的时候会去找请求方法的小写（request.method.lower()，
例如 get、post）运行类中的方法

Django REST 框架允许将一组相关视图的逻辑组合在一个类中，称为 ViewSet(继承 APIView).
ViewSet 视图集类不再实现 get()、post() 等方法，而是需要实现动作 action 如 list()、create() 等
视图集 ViewSet 只在使用 as_view() 方法的时候，才会将 action 动作与具体请求方式对应上.
"""
urlpatterns += [
    path('books_viewset/', views.BookInfoViewSet.as_view({'get': 'list'})),
    re_path(r'books_viewset/(?P<pk>\d+)/', views.BookInfoViewSet.as_view({'get': 'retrieve'}))
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_viewset1', views.BookInfoViewSet, basename='books')
urlpatterns += router.urls

"""
使用 ViewSet 通常并不方便，因为 list、retrieve、create、update、destory 等方法都需要自己编写，
而这些方法与前面讲过的 Mixin 扩展类提供的方法同名，所以可以通过继承 Mixin 扩展类来复用这些方法而无需自己编写。
但是 Mixin 扩展类依赖与 GenericAPIView，所以还需要继承 GenericAPIView。
GenericViewSet 就帮助我们完成了这样的继承工作，继承自 GenericAPIView 与 ViewSetMixin，在实现了调用as_view() 时
传入字典（如 {'get':'list'}）的映射处理工作的同时，还提供了 GenericAPIView 提供的基础方法，
可以直接搭配 Mixin 扩展类使用。
"""
urlpatterns += [
    path('books_generic_viewset/', views.BookInfoViewSet2.as_view({'get': 'list'})),
    re_path(r'books_generic_viewset/(?P<pk>\d+)/', views.BookInfoViewSet2.as_view({'get': 'retrieve'})),
    # 如果此行为不需要pk，那么它就是列表视图，但是列表视图默认只有 list、create，所以应该将 latest 行为暴露出来
    path('books_generic_viewset/latest/', views.BookInfoViewSet2.as_view({'get': 'latest'})),
    re_path(r'books_generic_viewset/(?P<pk>\d+)/read/', views.BookInfoViewSet2.as_view({'put': 'read'})),
]

"""
ModelViewSet
"""
# # 创建路由对象
# router = DefaultRouter()
# # 将视图集注册到路由
# router.register(r'bookss', views.BookInfoViewSet)
# urlpatterns += router.urls  # 把生成好的路由拼接到 urlpatterns
