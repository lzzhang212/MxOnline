#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-5-28 15:03
# @Author  : lzzhang
# @Site    : 
# @File    : forms.py
# @Software: PyCharm


from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    """
    登录验证表单
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    """
    注册验证表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetPwdForm(forms.Form):
    """
    找回密码表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


class ModifyPwdForm(forms.Form):
    """
    重置密码表单
    """
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.Form):
    """
    用户修改头像
    """
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
    个人中心信息修改
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birth', 'address', 'mobile']
