from django.db import models

class TimeStampedModel(models.Model):
    
    """ this is working like abstract class in other app such as rooms.models"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add : 새로운 모델을 생성하면 현재 날짜와 시간을 넣어줌
    # auto_add : 매번 모델을 저장하면 새로운 날짜를 넣어줌

    class Meta:
        abstract = True
        """ abstract 해주어야 데이타 베이스에 안들어감 """