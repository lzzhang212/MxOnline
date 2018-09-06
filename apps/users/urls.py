#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 16:35
# @Author  : lzzhang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from .views import UserInfoView, UploadImageView, UpdatePwdView, MyCourseView, MyFavOrgView, MyFavTeacherView, \
    MyFavCourseView, MyMessageView, UpdateEmailView


app_name = "users"

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('image/upload/', UploadImageView.as_view(), name='upload_image'),
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    path('mycourse/', MyCourseView.as_view(), name='my_course'),
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    path('my_message/', MyMessageView.as_view(), name='my_message'),
    path('update_email/', UpdateEmailView.as_view(), name='update_info'),
]