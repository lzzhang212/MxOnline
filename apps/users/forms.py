#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-28 15:03
# @Author  : lzzhang
# @Site    : 
# @File    : forms.py
# @Software: PyCharm


from django import forms


class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)