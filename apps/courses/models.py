# -*- coding:utf-8 -*-
from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj',u'初级'),('zj',u'中级'), ('gj',u'高级')), max_length=2, verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'所属机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='课程讲师', null=True, blank=True)
    category = models.CharField(max_length=10, default='', verbose_name='课程类别')
    tag = models.CharField(max_length=10, default='', verbose_name='课程标签')
    youneed_know = models.CharField(max_length=300, default=' ', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=300, default=' ', verbose_name='老师告诉你')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    url = models.CharField(max_length=100, default='', verbose_name=u'视频地址')
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resourse/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
