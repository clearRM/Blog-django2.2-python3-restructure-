from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image


class ArticleColumn(models.Model):
    # 栏目的model
    title = models.CharField(max_length=100,blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


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
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 标签
    tags = TaggableManager(blank=True)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    def save(self, *args,**kwargs):
        article = super(ArticlePost,self).save(*args,**kwargs)
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 400
            new_y = int(new_x*(y/x))
            resized_image = image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article


    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    class Meta:
        # 设置以倒叙排序
        ordering = ('-created',)
    def __str__(self):
        # 返回文章标题
        return self.title
    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])







