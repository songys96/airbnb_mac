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
    list_display = ("name", "country", "city", "price", "beds", "guests", "bedrooms", "baths", "check_in", "check_out", "instant_book","count_amenities")
    
    list_filter = ("instant_book", "host__superhost", "room_type", "amenities", "facilities", "house_rules", "country", "city")
    # host__superhost 의 경우는 room.host -> user model .... user.superhost -> boolean 을 가져옴..!
    
    search_fields = ("city",)
    #search_fields = ("^city",) 이렇게하면 입력값으로부터 시작하는 것들을 찾음 start with 역할
    
    filter_horizontal = ("amenities", "facilities", "house_rules")

    ordering = ('name', 'price')
    # 우선순위를 줄 수 있으면서 동시에 정렬시켜줌

    def count_amenities(self, obj):
        """
        self는 admin 클래스를 받고 obj는 해당 열을 받음
        함수이지만 객체로 작용하며 list_display에 string으로 위 메서드명을 넣으면
        알아서 찾은 후 return 값을 넣어줌
        obj은 Room model객체를 반환할 것임
        """
        #print(obj)
        print(obj.amenities.count())
        return "hello"
    count_amenities.short_description = "여기서 필드명을 바꿀 수 있음"
    # 위 count_amenities는 함수이기 때문에 admin패널에서 정렬시킬 수 없음


    
        
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    pass
