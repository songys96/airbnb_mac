from django.db import models
from django_countries.fields import CountryField
from core import models as core_models

class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class RoomType(AbstractItem):
    
    pass

    class Meta:
        verbose_name_plural = "RoomTypes"
        ordering = ["name"]

class Amenitiy(AbstractItem):

    pass

    class Meta:
        verbose_name_plural = "Amenities"

class Facility(AbstractItem):

    pass

    class Meta:
        verbose_name_plural = "Facilities"

class HouseRule(AbstractItem):

    pass

    class Meta:
        verbose_name_plural = "HouseRules"

class Photo(core_models.TimeStampedModel):

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140, )
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)

    beds = models.IntegerField()
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    baths =  models.IntegerField()
    
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey('users.User', related_name="rooms", on_delete=models.CASCADE)
    # 'user'만 써도 알아서 모델을 찾아줌!!!!!!(장고의 기능)
    # user model의 입장에서는 변한게 없다. 여기서만 임의로 연결함 read 의 영역
    # cascade는 유저가 지워지면 같이 지워짐
    # related_name은 다른 모델에서 연결된 모델을 찾을 때 사용될 이름

    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField('Amenitiy', blank=True)
    facilities = models.ManyToManyField('Facility', blank=True)
    house_rules = models.ManyToManyField('HouseRule', blank=True)

    def __str__(self):
        return self.name