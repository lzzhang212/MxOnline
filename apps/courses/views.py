from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments


# Create your views here.

class CourseListView(View):
    """
    公开课列表
    """
    def get(self, request):
        # 获取所有课程，默认按添加时间排序
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-students')

        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "hot_courses": hot_courses,
            "sort": sort,
        })


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 课程点击数+1
        course.click_nums += 1
        course.save()

        # 根据tag标签查找推荐课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:3]

        has_fav_course = False
        has_fav_org = False

        # 必须是用户已登录我们才需要判断收藏情况。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            "all_resources": all_resources,
        })


class CommentsView(View):
    """
    公开课评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
        })


class AddCommentsView(View):
    """
    用户评论
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse("{'status':'fail', 'msg':'用户未登陆'}", content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # 获取所评论的课程
            course = Course.objects.get(id=int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse("{'status':'success', 'msg':'评论成功'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail', 'msg':'评论失败'}", content_type='application/json')
