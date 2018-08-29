#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-5-28 15:03
# @Author  : lzzhang
# @Site    : 
# @File    : forms.py
# @Software: PyCharm


from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    '''登录验证表单'''

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    '''注册验证表单'''

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})
