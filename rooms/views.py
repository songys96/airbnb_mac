from math import ceil
from datetime import datetime
from django.shortcuts import render, redirect
#render는 html을 넣어서 보낼 수 있게 도와줌
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from . import models

def all_rooms(request):
    """
    request를 받으면 response를 보낸다
    render를 통해 html을 보낼것임
    render은 httpresponse를 반환한다
    좋은점은 여기서 만든 변수를 html(template)에 보낼수 있다는 것
    render 인자로 들어가는 context는 dictionary형태로 받고
        'time':now하면 html에서 {{time}}을 적으면 now가 들어감
    """
    page = request.GET.get('page', 1)
    room_list = models.Room.objects.all()
    # QuerySet is lazy, so it just create QuerySet(not all data)
    paginator = Paginator(room_list, 10, orphans=5)
    # orphans = 마지막 남은 것의 수가 orphans값 이하이면 그 전 페이지에 넣어버림
    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", context={
            "page":rooms
            })
    except EmptyPage:
        # 모든 예외 핸들 : except Exception
        return redirect("/")
        
        # 에러를 하나하나 컨트롤 가능함

    # paginator의 get_page와 page차이
    # get_page는 에러가 없는대신 간편하게 사용가능
    # page는 에러를 뛰움으로써 에러 핸들가능

    print(dir(rooms))
    #아래에 들어갈 html이름은 template폴더안의 이름과 같아야함


