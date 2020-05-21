from django.urls import path
from rooms import views as room_views

app_name = "core"
# this app_name should be same as config/urls.py namespace

urlpatterns = [
    path("", room_views.HomeView.as_view(), name = "home")
]
# urlpatterns의 2번째 인자는 함수만 받기때문에 클래스를 넣어주면 안됨