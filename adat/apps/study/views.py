import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import BookInfo


def index(request):
    """
    index视图
    :param request: 包含了请求信息的请求对象，类型 HttpRequest
    :return: 响应对象
    """
    return HttpResponse("hello the world!")


# /weather/bejing/2018
def weather(request, city, year):
    """演示获取 URL 路径"""
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')


def weather2(request, year, city):
    """演示路径参数"""
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')


def qs(request):
    """演示获取查询字符串参数"""
    a = request.GET.get('a')
    b = request.GET.get('b')
    alist = request.GET.getlist('a')
    print(a)  # 3
    print(b)  # 2
    print(alist)  # ['1', '3']
    return HttpResponse('OK')


# POST /get_body/
def get_body(request):
    """演示获取请求体表单数据"""
    a = request.POST.get('a')
    b = request.POST.get('b')
    alist = request.POST.getlist('a')
    print(a)
    print(b)
    print(alist)
    return HttpResponse('OK')


# POST /get_body_json
def get_body_json(request):
    """演示获取请求体中的非表单数据：json"""
    json_bytes = request.body  # bytes 类型
    json_str = json_bytes.decode()  # 转换成 json 字符串类型，python3.6 无需执行此步
    req_data = json.loads(json_str)  # 把 json 字符串转换成 json 字典或 json 列表
    print(req_data['a'])
    print(req_data['b'])
    return HttpResponse('OK')


def get_user(request):
    """演示获取当前请求对象"""
    print(request.META['CONTENT_TYPE'])
    # 当前如果没有登录，获取 request.user 会是一个匿名用户 AnonymousUser
    # 如果当前已经登录，获取 request.user 会是当前登录的用户对象
    print(request.user)
    return HttpResponse('get_user')


def demo_view(request):
    return JsonResponse({'city': 'beijing', 'subject': 'python'})


def demo_view1(request):
    response = HttpResponse('ok')
    response.set_cookie('itcast1', 'python1')  # 临时cookie
    response.set_cookie('itcast2', 'python2', max_age=3600)  # 有效期一小时
    return response


def demo_view2(request):
    cookie1 = request.COOKIES.get('itcast1')
    print(cookie1)
    # HttpResponse.delete_cookie(cookie名)
    return HttpResponse('OK')


def session_demo(request):
    # session 依赖于 cookie，当代码执行到这行时，会将 session 设置到 redis 数据
    # 同时，生成一个唯一 session_id 的东西，把 session_id 通过后期的响应对象设置到浏览器的 cookie 中
    request.session["name"] = "zhansan"  # 设置 session，其实这一步是预操作，当执行到 return HttpResponse 时才会生成

    # 先通过 请求对象 读取到 cookie 中的 session_id，然后通过 session_id 再读取出 redis 中的 session 记录，再通过 name key 获取 value
    print(request.session.get("name"))  # 获取 session，虽然上一步还没生成，但这一步能够获取到值，因为是同一个对象，没有从 Redis 数据库中读取
    return HttpResponse("ok")  # 内部相当于执行 response.set_cookie("sessionid", "xxx")


def register(request):
    """处理注册"""

    # 获取请求方法，判断是GET/POST请求
    if request.method == 'GET':
        # 处理GET请求，返回注册页面
        return render(request, 'register.html')
    else:
        # 处理POST请求，实现注册逻辑
        return HttpResponse('这里实现注册逻辑')


from django.views import View


class RegisterView(View):
    """类视图：处理注册"""

    def get(self, request):
        """处理GET请求，返回注册页面"""
        # return render(request, 'register.html')
        return HttpResponse('这里实现注册逻辑')

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        return HttpResponse('这里实现注册逻辑')


from django.views import View


class BookListView(View):
    """列表视图"""

    def get(self, request):
        """查询所有图书接口"""
        # 1.查询出所有图书模型，返回的是查询集，即一个个模型对象，RESTful 建议返回的是 Json 数据
        books = BookInfo.objects.all()
        # 2.遍历查询集，取出里面的每个书籍模型对象，把模型对象转换成字典。定义一个列表变量用来保存每个字典
        book_list = []
        for book in books:
            book_dict = {
                'id': book.id,
                'btitle': book.btitle,
                'bpub_data': book.bpub_date
            }
            book_list.append(book_dict)  # 将转换好的字典添加到列表中
        # 3.响应
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """新增图书接口"""
        # 1. 获取前端传入的请求体数据（json）request.body
        json_str_bytes = request.body
        # 2. 把 bytes 类型的 json 字符转换成 json_str
        json_str = json_str_bytes.decode()
        # 3. 利用 json.loads 将 json 字符串转换成 json（字典、列表）
        book_dict = json.loads(json_str)
        # 4. 创建模型对象并保存（把字典转换成模型并存储）
        book = BookInfo(
            btitle=book_dict['btitle'],
            bpub_date=book_dict['bpub_date']
        )
        book.save()
        # 把新增的模型转换成字典
        json_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_data': book.bpub_date
        }
        # 5. 响应（把新增的数据再响应回去，201）
        return JsonResponse(json_dict, status=201)


class BookDetailView(View):
    """详情视图"""

    def get(self, request, pk):
        """查询指定某个图书接口"""
        # 1. 获取出指定 pk 的那个模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'message': '查询的数据不存在'}, status=404)
        # 2. 模型对象转字典
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_data': book.bpub_date
        }
        # 3. 响应
        return JsonResponse(book_dict)

    def put(self, request, pk):
        """修改指定某个图书接口"""
        # 先查询要修改的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'message': '要修的数据不存在'}, status=404)
        # 获取前端传入的新数据（把数据转换成字典）
        json_str_bytes = request.body
        json_str = json_str_bytes.decode()
        book_dict = json.loads(json_str)
        # 重新给模型指定的属性赋值
        book.btitle = book_dict['btitle']
        book.pbub_date = book_dict['bpub_date']
        # 调用 save 方法进行修改操作
        book.save()
        # 把修改后的模型再转换成字典
        json_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_data': book.bpub_date
        }
        # 响应
        return JsonResponse(json_dict)

    def delete(self, request, pk):
        """删除指定某个图书接口"""
        # 获取要删除的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse({'message': '查询的数据不存在'}, status=404)
        # 删除模型对象
        book.delete()  # 物理删除（真正从数据库中删除）
        # book.is_delete = True
        # book.save()
        # 响应：删除时不需要有响应体，但要指定状态码为 204
        return HttpResponse(stauts=204)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


class BookListAPIView(APIView):
    """列表视图"""

    def get(self, request):
        """查询所有"""
        books = BookInfo.objects.all()
        serializer = serializers.BookInfoSerializer(instance=books, many=True)
        return Response(serializer.data)  # 不需要指定状态码，默认200
        # response = Response(serializer.data)
        # print(response.data) # 响应对象未渲染处理的数据
        # print(response.content) # 处理后要响应给前端的数据
        # print(response.status_code)
        # return response

    def post(self, request):
        """新增"""
        # 获取前端传入的请求体数据
        data = request.data
        # 创建序列化器进行反序列化
        serializer = serializers.BookInfoSerializer(data=data)
        # 调用序列化器的 is_valid 方法进行校验
        serializer.is_valid(raise_exception=True)
        # 调用序列化器的 save 方法执行 create 方法
        serializer.save()
        # 响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    """详情视图"""

    def get(self, request, pk):
        # 查询 pk 指定的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response({'message': '查询的数据不存在'}, status=status.HTTP_404_NOT_FOUND)
        # 创建序列化器进行序列化
        serializer = serializers.BookInfoSerializer(instance=book)
        # 响应
        return Response(serializer.data)

    def put(self, request, pk):
        # 查询 pk 所指定的模型对象
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 获取前端传入的请求体数据
        # 创建序列化器进行反序列化
        serializer = serializers.BookInfoSerializer(instance=book, data=request.data)
        # 校验
        serializer.is_valid(raise_exception=True)
        # save --> update
        serializer.save()
        # 响应
        return Response(serializer.data)


# 假设现在要针对另外一个模型编写视图，可以看出在这些增删改查中无非就是
# 模型不一样以及序列化器的类不一样，因此可以将这些模型类以变量的方式指定。

# class BookListAPIView1(APIView):
#     """列表视图"""
#     serializer_class = serializers.BookInfoSerializer
#
#     def get(self, request):
#         """查询所有"""
#         books = BookInfo.objects.all()
#         serializer = serializer_class(instance=books, many=True)
#         return Response(serializer.data)  # 不需要指定状态码，默认200
#         # response = Response(serializer.data)
#         # print(response.data) # 响应对象未渲染处理的数据
#         # print(response.content) # 处理后要响应给前端的数据
#         # return response
#
#     def post(self, request):
#         """新增"""
#         # 获取前端传入的请求体数据
#         data = request.data
#         # 创建序列化器进行反序列化
#         serializer = serializer_class(data=data)
#         # 调用序列化器的 is_valid 方法进行校验
#         serializer.is_valid(raise_exception=True)
#         # 调用序列化器的 save 方法执行 create 方法
#         serializer.save()
#         # 响应
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# GenericAPIView
from rest_framework.generics import GenericAPIView


class BookListGenericAPIView(GenericAPIView):
    """列表视图"""
    # 指定序列化器类
    serializer_class = serializers.BookInfoSerializer
    # 指定查询集“数据来源”
    queryset = BookInfo.objects.all()

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailGenericAPIView(GenericAPIView):
    """列表视图"""
    # 指定序列化器类
    serializer_class = serializers.BookInfoSerializer
    # 指定查询集“数据来源”
    queryset = BookInfo.objects.all()

    def get(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object()
        serializer = self.get_serializer(book, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


from rest_framework.mixins import ListModelMixin, CreateModelMixin


class BookListMixinView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """列表视图"""
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin


class BookDetailMixinView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    """详情视图"""
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)


# 可用子类视图
from rest_framework.generics import ListAPIView, CreateAPIView


class BookListCommonView(ListAPIView, CreateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer


from rest_framework.generics import RetrieveUpdateDestroyAPIView


class BookDetailCommonView(RetrieveUpdateDestroyAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer


# 视图集
from rest_framework.viewsets import ViewSet


class BookInfoViewSet(ViewSet):

    def list(self, request):
        books = BookInfo.objects.all()
        serializer = serializers.BookInfoSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            books = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.BookInfoSerializer(books)
        return Response(serializer.data)


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action


class BookInfoViewSet2(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.BookInfoSerializer

    def latest(self, request):
        """
        返回最新的图书信息
        """
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('bread')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    # detail 为 False 表示路径名格式应该为 books/latest/
    @action(methods=['get'], detail=False)
    def latest1(self, request):
        """
        返回最新的图书信息
        """
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    # detail为True，表示路径名格式应该为 books/{pk}/read/
    @action(methods=['put'], detail=True)
    def read1(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('bread')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)


from rest_framework.viewsets import ModelViewSet


class BookInfoModelViewSet(ModelViewSet):
    """使用DRF实现增删改查的后端API"""

    # 指定查询集
    queryset = BookInfo.objects.all()
    # 指定序列化器
    serializer_class = serializers.BookInfoSerializer
