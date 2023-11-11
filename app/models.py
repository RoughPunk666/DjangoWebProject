"""
Definition of models.
"""

from tkinter import Label
from django.db import models
from datetime import datetime
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    discription = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    image = models.FileField(default='temp.png',upload_to = 'postImage/', verbose_name = "Изображение")
    video = models.FileField(default='temp.mp4',upload_to = 'postVideo/', verbose_name = "Видео")
    videoposter = models.FileField(default='temp.png',upload_to = 'postVideo/', verbose_name = "Постер видео")
    
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])   

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"
        
class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name= "Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return 'Комментарий %s к %s : %s'%(self.author,self.post,self.text)

    class Meta:
        db_table = "Comments"
        ordering = ["-date"]
        verbose_name = "комментарии"
        verbose_name_plural = "коментарии к статьям блога"
     
admin.site.register(Blog)
admin.site.register(Comment)