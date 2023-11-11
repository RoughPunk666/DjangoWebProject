"""
Definition of views.
"""

from datetime import datetime
from symbol import parameters
from django.shortcuts import render, redirect
from django.http import HttpRequest

from app.forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db import models
from .models import Blog
from .models import Comment
from .forms import BlogForm, CommentForm

import os


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    aboutSF = {'app/content/AboutSF.png'}
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    logo = {'app/content/Logo.png'}
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Portable Moose - это команда разработчиков из одного человека',
            'year':datetime.now().year,
        }
    )
        
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(
        request,
        'app/registration.html',
       {
           'form': form,
           'year':datetime.now().year,
       }
    )
        
def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    country = {'1': 'Россия', '2': 'США', '3': 'Япония', '4': 'Италия'}
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['country'] =country[form.cleaned_data['country']]
            data['email'] = form.cleaned_data['email']
            if(form.cleaned_data['agreement'] == True):
                data['agreement'] = 'Да'
            else:
                data['agreement'] = 'Нет'
            data['message'] = form.cleaned_data['message']
            form = None;
    else:
        form = FeedbackForm()
        
    return render(
        request,
        'app/pool.html',
        {
            'form':form,
            'data':data,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts,
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    post_l = Blog.objects.get(id = parametr)
    comments = Comment.objects.filter(post = parametr)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            coment_f = form.save(commit=False)
            coment_f.author = request.user
            coment_f.date = datetime.now()
            coment_f.post = Blog.objects.get(id = parametr)
            coment_f.save()
            
            return redirect('blogpost', parametr=post_l.id)
    else:
        form = CommentForm()
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_l':post_l,
            'comments':comments,
            'form':form,
            'year':datetime.now().year,
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)
    
    if request.method == 'POST':
        blogform = BlogForm(request.POST,request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            
            return redirect('blog')
    else:
        blogform = BlogForm
        
    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,
            'title': 'Добавление статьи',

            'year':datetime.now().year,
        }
    )