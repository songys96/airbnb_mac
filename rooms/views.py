from django.views.generic import ListView
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
    # context_object_name = "rooms" context이름 변경 가능
    
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    print(page_obj)
    # 최신순, 인기순 등 정렬가능
    # paginator_class << paginator 가져옴

