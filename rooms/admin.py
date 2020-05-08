from django.contrib import admin
from . import models

# register는 여러개의 모델을 인자로 받을 수 있음
@admin.register(models.RoomType, models.Facility, models.Amenitiy, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    pass

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    fieldsets =(
        ("Basic Info", {"fields": ("name", "description", "country", "address", "price")}),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Space", {"fields": ("guests", "beds", "baths", "bedrooms")}),
        ("More About the Space", {"fields": ("amenities", "facilities", "house_rules")}),
        ("Details", {"fields": ("host",)})
    )
    list_display = ("name", "country", "city", "price", "beds", "guests", "bedrooms", "baths", "check_in", "check_out", "instant_book")
    list_filter = ("instant_book", "host__superhost", "room_type", "amenities", "facilities", "house_rules", "country", "city")
    # host__superhost 의 경우는 room.host -> user model .... user.superhost -> boolean 을 가져옴..!
    search_fields = ("city",)
    #search_fields = ("^city",) 이렇게하면 입력값으로부터 시작하는 것들을 찾음 start with 역할
    filter_horizontal = ("amenities", "facilities", "house_rules")



@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    pass
