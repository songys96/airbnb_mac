from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django_countries import countries
from . import models, forms

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



class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                filtered_rooms = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    filter_args["amenities"] = amenity
                    filtered_rooms = filtered_rooms.filter(**filter_args)

                for facility in facilities:
                    filter_args["facilities"] = facility
                    filtered_rooms = filtered_rooms.filter(**filter_args)
                
                filtered_rooms.order_by("-created")
                paginator = Paginator(filtered_rooms, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(request, "rooms/search.html", {"form": form, "rooms": rooms})
        else:

            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})










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
    
