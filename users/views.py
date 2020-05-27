import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView
from django.views import View
from django.urls import reverse_lazy
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

def login_kakao(request):
    pass

def login_kakao_callback(request):
    pass









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
