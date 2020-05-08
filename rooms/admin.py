from django.contrib import admin
from . import models

# register는 여러개의 모델을 인자로 받을 수 있음
@admin.register(models.RoomType, models.Facility, models.Amenitiy, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    pass
 


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    
    pass

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    pass
