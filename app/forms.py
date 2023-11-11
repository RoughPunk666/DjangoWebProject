"""
Definition of forms.
"""

import email
from random import choices
from secrets import choice
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import Comment
from app.models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    
class FeedbackForm(forms.Form):
    name = forms.CharField(label='Ваше имя', widget=forms.TextInput({'class':'form-control','placeholder':'Имя'}), min_length=2, max_length=20)
    gender = forms.ChoiceField(label='Ваш пол', choices=[('1', 'Мужской'), ('2', 'Женский')], widget=forms.RadioSelect, initial=1)
    country = forms.ChoiceField(label='Ваша страна', choices=(('1','Россия'), ('2','США'), ('3','Италия'), ('4','Япония')),widget=forms.Select({'class':'form-control'}), initial=1)
    email = forms.EmailField(label='Ваш e-mail', widget=forms.EmailInput({'class':'form-control','placeholder':'E-mail'}), min_length=7)
    agreement = forms.BooleanField(label='Я согласен на обработку персональных данных', required=True)
    message = forms.CharField(label='Ваше отзыв', widget=forms.Textarea({'row':12, 'cols':20, 'class':'form-control','placeholder':'Сообщение'}))
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text':"Комментарий"}
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','discription', 'content', 'image', 'video', 'videoposter')
        labels = {'title':"Заголовок", 'discription':"Краткое содержание", 'content':"Полное содержание", 'image':"Картинка",'video':"Видео",'videoposter':"Постер видео" }