from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from . import models

# class based view!

class HomeView(ListView):
    """
    model을 필요로 하고
    template을 자동으로 찾아줌
    template 이름은 modelname_list.html 
    template에 object_list로 모델이 들어감
    template에 page_obj하면 Page를 리턴함
    https://ccbv.co.uk/ 에서 view에 관한 정보 획득 가능
    """
    model = models.Room
    # template에 object_list만 치면 알아서 room.objects가 나옴
    context_object_name = "rooms" # context이름 변경 가능
    
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    # 최신순, 인기순 등 정렬가능
    # paginator_class << paginator 가져옴

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(context.keys())
        now = timezone.now()
        context['now'] = now
        return context


class RoomDetail(DetailView):
    model = models.Room
    # model의 소문자를 html에서 인식하게 함

def room_detail(request, pk):
    """
    위와 같은 느낌인데 조금 더 하드코딩
    urls.py urlpatters에 추가하지 않아서 작동하진 않지만 
    """
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room":room})
    except models.Room.DoesNotExist:
        raise Http404()
    