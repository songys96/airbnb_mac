from django.contrib import admin
from . import models

@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
    """
    it creates user panel on admin
    admin의 register 함수를 models.User를 인자롤 받아 적용시키는 메서드
    
    """