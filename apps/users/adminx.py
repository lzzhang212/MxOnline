#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-28 18:16
# @Author  : lzzhang
# @Site    : 
# @File    : adminx.py
# @Software: PyCharm

import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views


# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)


# 全局修改，固定写法
class GlobalSettings(object):
    #修改title
    site_title = u'慕学后台管理系统'
    #修改footer
    site_footer = u'慕学网'
    #菜单收起
    menu_style = 'accordion'


# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)