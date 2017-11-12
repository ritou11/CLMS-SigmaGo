from django.db import models

# Create your models here.

class Menu(models.Model):
    info = models.TextField(u'按钮详情', blank=True, null=True)
    modify_time = models.DateTimeField(u'刷新时间', auto_now_add=True)
    count = models.IntegerField(u'刷新次数', blank=True, null=True)
    backup = models.TextField(u'测试字段', blank=True, null=True)

    def to_dict(self):
        return dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = verbose_name = u'按钮组'


class Actions(models.Model):
    action_type = models.CharField(u'类型', blank=True, null=True, max_length=100)
    action_name = models.CharField(u'名称', blank=True, null=True, max_length=100)
    level = models.IntegerField(u'优先级', blank=True, null=True)
    rule = models.CharField(u'匹配规则', blank=True, null=True, max_length=100)
    description = models.CharField(u'中文描述', blank=True, null=True, max_length=100)
    back = models.CharField(u'back', blank=True, null=True, max_length=100)

    def to_dict(self):
        return dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = verbose_name = u'所有动作'


class MessageLog(models.Model):
    user_id = models.CharField(u'用户id', blank=True, null=True, max_length=256)
    user_name = models.CharField(u'用户名', blank=True, null=True, max_length=256)
    request = models.CharField(u'发送内容', blank=True, null=True, max_length=256)
    response = models.CharField(u'返回内容', blank=True, null=True, max_length=256)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def to_dict(self):
        return dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = verbose_name = u'消息日志'
