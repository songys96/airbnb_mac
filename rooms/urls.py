from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name = "detail"),
    path("search/", views.SearchView.as_view(), name='search')
    
    ]
#<int:pk> 인것은 naver.com/rooms/132 -> {'pk':132}로 만들어줌

