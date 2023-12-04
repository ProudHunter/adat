from rest_framework import serializers
from .models import BookInfo


class BookInfoSerializer(serializers.ModelSerializer):
    """BookInfo模型类的序列化器"""

    class Meta:  # 元类做配置操作
        model = BookInfo  # 指定序列化从哪个模型映射字段
        fields = '__all__'  # 指定映射哪些字段


"""
BookInfoSerializer():
    id = IntegerField(label='ID', read_only=True)
    btitle = CharField(label='名称', max_length=20)
    bpub_date = DateField(label='发布日期')
    bread = IntegerField(label='阅读量', required=False)
    bcomment = IntegerField(label='评论量', required=False)
    is_delete = BooleanField(label='逻辑删除', required=False)

"""
