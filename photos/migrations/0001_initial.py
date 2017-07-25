# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='相册名', max_length=50, default='未命名')),
                ('description', models.CharField(verbose_name='相册描述', max_length=200, default='')),
                ('type', models.CharField(verbose_name='相册类别', max_length=2, choices=[('cy', '出游'), ('jh', '聚会'), ('qt', '其他')])),
                ('created_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('creater', models.ForeignKey(verbose_name='创建者', related_name='own_albums', to=settings.AUTH_USER_MODEL)),
                ('sharers', models.ManyToManyField(verbose_name='共享者', related_name='share_albums', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '相册',
                'verbose_name_plural': '相册',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='照片名字', max_length=50, default='')),
                ('image', models.ImageField(verbose_name='照片', upload_to='photos/%Y/%m')),
                ('description', models.CharField(verbose_name='照片描述', max_length=200, default='')),
                ('created_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('updated_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('album', models.ForeignKey(verbose_name='相册', to='photos.Album')),
                ('photo_creater', models.ForeignKey(verbose_name='创建者', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '照片',
                'verbose_name_plural': '照片',
                'ordering': ('-created_time',),
            },
        ),
    ]
