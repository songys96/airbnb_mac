import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from django.views import View
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from . import forms, models
# Create your views here.

class LoginView(FormView):

    form_class = forms.LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)




def log_out(request):
    logout(request)
    return redirect("core:home")

class SignUpView(FormView):

    form_class = forms.SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        print(username, password)
        user = authenticate(self.request, username=username, password=password)
        print(user)
        if user is not None:
            login(self.request, user)
            print("login~~~")
        return super().form_valid(form)


class GithubException(Exception):
    pass


def login_github(request):
    github_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={github_id}&redirect_uri={redirect_uri}&scope=read:user")

def login_github_callback(request):
    # code랑 access token 이랑 바꿀것
    # access token으로 유저정보를 가져온다
    code = request.GET.get("code", None)
    github_id = os.environ.get("GITHUB_ID")
    github_secret = os.environ.get("GITHUB_PW")
    print(code)
    try:
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={github_id}&client_secret={github_secret}&code={code}",
                headers={"Accept": "application/json"}
            )
            result_json = result.json()
            error = result_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json"
                    }
                )
                profile_json = profile_request.json()
                print(profile_json)
                username = profile_json.get("login", None)
                print("a",username)
                if username is not None:
                    # 1. github에 정보가 있는지 확인
                    print("user exist")
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    print("info", name, email, bio)
                    try:
                        # 2. 기존 DB에 등록한적이 있는지 확인
                        user = models.User.objects.get(username=username)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            # 2-1. 다른 방식으로 가입했으면 에러발생
                            """개인적으로 이부분이 에러가 아닌 상태로 가능하도록 했으면 좋겠음.!"""
                            raise GithubException()
                    except models.User.DoesNotExist:
                        # 3. 등록정보가 없으면 새롭게 만들기
                        user = models.User.objects.create(
                            username=username, first_name=name, bio=bio, email=email, login_method=models.User.LOGIN_GITHUB
                        )
                        user.set_unusable_password()
                        user.save()

                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))

class KakaoException(Exception):
    pass

def login_kakao(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")

def login_kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://localhost:8000/users/login/kakao/callback"
        token_request = requests.post(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
        access_token = token_request.json().get("access_token")
        profile_request = requests.get(
            f"https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"})
        profile_json = profile_request.json()
        user_account = profile_json.get("properties", None)
        user_profile = profile_json.get("kakao_account", None)
        if user_account is None and user_profile is None:
            raise KakaoException()
        nickname = user_account.get("nickname")
        profile_img = user_account.get("profile_image", None)
        print("profile_img", profile_img)
        email = user_profile.get("email")
        username = email.split("@")[0]
        print("------",username)
        try:
            """ 조군샵의 경우 중복확인을 휴대폰 번호로 검사했음 """
            user = models.User.objects.get(username=username)
            if user.login_method != models.User.LOGIN_KAKAO:
                print("user already exists in other flatform")
                raise KakaoException()
        except models.User.DoesNotExist:

            user = models.User.objects.create(
                username = username,
                email = email,
                first_name = nickname,
                login_method = models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.save()
            if profile_img is not None:
                # 이미지를 추가할 것인데 
                # django.core.files.base.contentfile에서 바이너리 상태로 바꾸기
                img_request = requests.get(profile_img)
                print(img_request)
                user.avatar.save(
                    f"{nickname}_avatar",
                    ContentFile(img_request.content)
                )
        login(request, user)
        print("done")
        return redirect(reverse("core:home"))

    except KakaoException:
        return redirect(reverse("users:login")) 





class LoginView_가내수공업(View):
    
    def get(self, request):
        form = forms.LoginForm(initial={"username":"songys"})
        return render(request, "users/login.html", context={"form":form})

    def post(self, request):
        """
        work flow - form 인스턴스를 먼저 만들고 is_valid과정에서 form.clean()으로 넘어감
        """
        form = forms.LoginForm(request.POST)
        print("------------")
        if form.is_valid():
            print("valid")
            username = form.cleaned_data.get("username")
            print(username)
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
            return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form":form})
