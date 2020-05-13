from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class RoomInline(admin.TabularInline):
    from rooms.models import Room
    model = Room

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """
    field를 가지고 있는 기본 포멧으로 나오지만
    fieldset에 User가 가지고 있는 정보를 넣지 않았으므로 아직 만들어지지 않음
    """
    fieldsets = UserAdmin.fieldsets + (
        ("profile", {"fields":("avatar", "gender", "bio", 'birthdate', 'language', 'currency', 'superhost')}),
    )
    #("FieldName", {"fields":("attr1", "attr2")}), ...
        
    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username", "first_name", "last_name", "email", "is_active", "language", "currency", "superhost", "is_staff", "is_superuser"
    )

    inlines = (RoomInline,)


# 아래 만든 코드는 직접 하나하나 구현하는 것

# @admin.register(models.User)
# class CustomUserAdmin(admin.ModelAdmin):

#     """ Custom User Admin """

#     """
#     it creates user panel on admin
#     admin의 register 함수를 models.User를 인자롤 받아 적용시키는 데코레이터
#     it is same as
#     admin.site.register(models.User, CustomUserAdmin)
#     """
#     list_display = ('username', 'gender', 'language', 'currency', 'superhost')
#     #list_display는 ModelAdmin에 내장된 기능이고 튜플안에 들어갈 내용은 users.models에서 가져온것
#     list_filter = ('language', 'currency', 'superhost')
#     empty_value_display = '-empty-'
#     """ 
#     자세한 것은 admin site
#     https://docs.djangoproject.com/en/3.0/ref/contrib/admin/ 
#     참조
#     """
# """