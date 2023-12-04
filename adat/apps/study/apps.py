from django.apps import AppConfig


class StudyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 表示这个配置类是加载到哪个应用的，每个配置类必须包含此属性，默认自动生成
    name = 'adat.apps.study'
    # 设置该应用的直观可读的名字，此名字在 Django 提供的 Admin 管理站点中会显示
    verbose_name = '图书管理'
