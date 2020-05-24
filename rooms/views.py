from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django_countries import countries
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



def search(request):
    # below for html select options
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries":countries, 
        "room_types":room_types,
        "amenities": amenities,
        "facilities": facilities,
        }

    # below for getting values from request(from website)
    city = request.GET.get("city", "anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))

    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city":city, 
        "s_country":country, 
        "s_room_type":room_type,
        "price":price,
        "guests":guests,
        "bedrooms":bedrooms,
        "beds":beds,
        "baths":baths,
        "instant": instant,
        "superhost": superhost,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        }

    # to make httpresponce, set dict for filtering
    filter_args = {}
    if city != "Anywhere":
        filter_args['city__startswith'] = city

    filter_args['country'] = country

    if price != 0:
        filter_args['price__lte'] = price
    
    if bedrooms != 0:
        filter_args['bedrooms__gte'] = bedrooms

    if beds != 0:
        filter_args['beds__gte'] = beds

    if baths != 0:
        filter_args['baths__gte'] = baths

    if instant is True:
        filter_args['instant_book'] = True
    
    if superhost is True:
        filter_args['host__superhost'] = True


    rooms = models.Room.objects.filter(**filter_args)
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args['amenities__pk'] = s_amenity
            rooms = rooms.filter(**filter_args)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args['facilities_pk'] = s_facility
            rooms = rooms.filter(**filter_args)
    
    return render(request, "rooms/search.html", context=
    {**choices, **form, "rooms":rooms})










def room_detail(request, pk):
    """
    위 RoomDetail와 같은 느낌인데 조금 더 하드코딩
    urls.py urlpatters에 추가하지 않아서 작동하진 않지만 
    """
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room":room})
    except models.Room.DoesNotExist:
        raise Http404()
    
