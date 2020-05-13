from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# register는 여러개의 모델을 인자로 받을 수 있음
@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    list_display = ("name", "used_by")

    def used_by(self, obj):
        """아이템 개체마다 사용된 횟수를 나타내는 메서드"""
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    """
    PhotoAdmin class를 인라인 클래스에 상속시키고 
    이 class인 PhotoInline을 RoomAdmin에 적용시키면
    알아서 foreignKey를 가져옴
    """
    model = models.Photo
    


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = (PhotoInline,)

    fieldsets =(
        ("Basic Info", {"fields": ("name", "description", "country", "address", "price")}),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Space", {"fields": ("guests", "beds", "baths", "bedrooms")}),
        ("More About the Space", {"fields": ("amenities", "facilities", "house_rules")}),
        ("Details", {"fields": ("host",)})
    )
    list_display = ("name", "country", "city", "price", "beds", "guests", "bedrooms", "baths", "check_in", "check_out", "instant_book","count_amenities", "count_photos", "total_rating")
    
    list_filter = ("instant_book", "host__superhost", "room_type", "amenities", "facilities", "house_rules", "country", "city")
    # host__superhost 의 경우는 room.host -> user model .... user.superhost -> boolean 을 가져옴..!
    
    search_fields = ("city",)
    #search_fields = ("^city",) 이렇게하면 입력값으로부터 시작하는 것들을 찾음 start with 역할
    
    filter_horizontal = ("amenities", "facilities", "house_rules")

    ordering = ('name', 'price')
    # 우선순위를 줄 수 있으면서 동시에 정렬시켜줌

    raw_id_fields = ("host", )



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

    def count_photos(self, obj):
        # obj is PhotoModel.object
        return obj.photos.count()

    
        
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'get_thumbnail')

    def get_thumbnail(self, obj):
        # print(obj.file)
        # obj.file은 string처럼 보이지만 클라스객체임
        # file의 정보를 가지고 있음
        # f'<img src="{obj.file.url}"/>' 이렇게 하면 쟝고가 string으로 바꿈
        # 보안상의 이유임. JS로 해킹하는 것을 막기 위하여
        return mark_safe(f'<img width=25 height=35 src="{obj.file.url}"/>')
    get_thumbnail.short_description = "Thumbnail"