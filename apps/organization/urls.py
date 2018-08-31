#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-31 14:23
# @Author  : lzzhang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm


from django.urls import path, re_path, include
from .views import OrgView, AddUserAskView

app_name = "organization"

urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
]