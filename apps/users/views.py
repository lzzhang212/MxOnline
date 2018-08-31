from django.shortcuts import render
from django.contrib.auth import authenticate, login

from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email

# Create your views here.


# 邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        #实例化login_form
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': u'请激活后再登录', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': u'用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证码记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)

        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    '''用户注册'''
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            # 如果用户已存在，提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':u'用户已存在'})

            pass_word = request.POST.get('password', None)
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form':register_form})


class ForgetPwdView(View):
    def get(self, request):
        '''忘记密码'''
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        # 查找验证码记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email':email})
        else:
            return  render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', None)
            pwd2 = request.POST.get('password2', None)
            email = request.POST.get('email', None)
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email':email, 'msg':'密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', None)
            return render(request, 'password_reset.html', {'email':email, 'modify_form':modify_form})
