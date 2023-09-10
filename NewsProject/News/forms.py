from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from captcha.fields import CaptchaField

class UserRegisterForm(UserCreationForm):

    username= forms.CharField(label='Имя пользователя',help_text='Максимум 150 символов',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email= forms.EmailField(label='e-mail',
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha=CaptchaField()

    class Meta:
        model=User
        fields=('username', 'email', 'password1','password2')


class UserLoginForm( AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class NewsForm(forms.ModelForm):

    def clean_title(self):
        title=self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValueError('Заголовок не должен начинаться с цифр')
        return title


    class Meta:
        model=News
        fields=['title','content','is_published','category']
        widget = {
            'title':forms.TextInput(attrs={
                 'class':'form_control'
             }),
            'content':forms.Textarea(attrs={
                'class':'form_control',
                'rows':5
                }),
            'category':forms.Select(attrs={
                'class':'form_control'})
        }
    # title=forms.CharField(max_length=150,label='Заголовок',widget=forms.TextInput(attrs={
    #     'class':'form_control'
    # }))
    # content=forms.CharField(label='Teкст', required=False,widget=forms.Textarea(attrs={
    #     'class':'form_control',
    #     'rows':5
    # }))
    # is_published=forms.BooleanField(label='Публикация', initial=True)
    # category=forms.ModelChoiceField(queryset=Category.objects.all(),label='Категория', empty_label='Выберите категорию',widget=forms.Select(attrs={
    #     'class':'form_control'
    #
    # }))