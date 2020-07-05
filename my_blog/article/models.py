from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ArticlePost(models.Model):
    # 作者 设置on_delete 级联删除
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 文章创建时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # 设置以倒叙排序
        ordering = ('-created',)
    def __str__(self):
        # 返回文章标题
        return self.title



