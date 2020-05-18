from datetime import datetime
from django.shortcuts import render
#render는 html을 넣어서 보낼 수 있게 도와줌
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
    all_rooms = models.Room.objects.all()
    #아래에 들어갈 html이름은 template폴더안의 이름과 같아야함
    return render(request, "rooms/home.html", context={"rooms":all_rooms})

