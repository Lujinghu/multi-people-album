from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    name = models.CharField(verbose_name='相册名', default='未命名', max_length=50)
    creater = models.ForeignKey(User, verbose_name='创建者', related_name='own_albums')
    sharers = models.ManyToManyField(User, verbose_name='共享者', related_name='share_albums')
    description = models.CharField(verbose_name='相册描述', default='', max_length=200)

    ALBUM_TYPE_CHOICES = (
        ('cy', '出游'),
        ('jh', '聚会'),
        ('qt', '其他'),
    )

    type = models.CharField(verbose_name='相册类别', choices=ALBUM_TYPE_CHOICES, max_length=2)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True) #创建时间，自动添加
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def str(self):
        return '相册: %s' % self.name

    def is_creater(self, user):
        return user == self.creater

    def is_sharer(self, user):
        return (user in self.sharers.all()) or self.is_creater(user)

    class Meta:
        ordering = ('-created_time', )
        verbose_name = '相册'
        verbose_name_plural = verbose_name


class Photo(models.Model):
    name = models.CharField(verbose_name='照片名字', default='', max_length=50) # 照片名字，可以不填
    creater = models.ForeignKey(User, verbose_name='创建者')
    image = models.ImageField(upload_to='photos/%Y/%m', verbose_name='照片')
    description = models.CharField(verbose_name='照片描述', default='', max_length=200)
    album = models.ForeignKey(Album, verbose_name='相册')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def is_creater(self, user):
        return user == self.creater

    def str(self):
        return '照片: %s' % self.name

    class Meta:
        ordering = ('-created_time', )
        verbose_name = '照片'
        verbose_name_plural = verbose_name
