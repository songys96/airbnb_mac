from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login/github", views.login_github, name="login-github"),
    path("login/github/callback", views.login_github_callback, name="login-github-callback"),
    path("login/kakao", views.login_kakao, name="login-kakao"),
    path("login/kakao/callback", views.login_kakao_callback, name="login-kakao-callback"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup")
]