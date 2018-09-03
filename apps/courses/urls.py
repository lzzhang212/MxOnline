#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/3 下午7:30
# @Author  : lzzhang
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path, re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView

app_name = "courses"

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),
    re_path('detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name='course_detail'),
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    re_path('comment/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),
]