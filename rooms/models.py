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

class Amenity(AbstractItem):

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
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey('Room', related_name="photos", on_delete=models.CASCADE)

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
    # rooms에 있다는 것을 알려줌

    room_type = models.ForeignKey('RoomType', related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField('Amenity', related_name="rooms", blank=True)
    facilities = models.ManyToManyField('Facility', related_name="rooms", blank=True)
    house_rules = models.ManyToManyField('HouseRule', related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        # self는 room모델이고 review가 related_name을 가지고있음
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        return all_ratings / all_reviews.count()