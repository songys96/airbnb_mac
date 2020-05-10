from django.db import models
from core import models as core_models

class Review(core_models.TimeStampedModel):

    review = models.TextField()
    Accuracy = models.IntegerField()
    communications = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()

    user = models.ForeignKey("users.User", related_name="reviews", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", related_name="reviews", on_delete=models.CASCADE)


    def __str__(self):
        # self안에 위 속성값들이 모두 들어가게 되고 각각이 모델의 '결과값'으로 들어감
        # review -> string  cleanliness-> integer  room -> model
        return self.room.name
        
    def rating_average(self):
        avg = sum([self.Accuracy, self.communications, self.cleanliness, self.location, self.check_in, self.value]) / 6
        avg = round(avg, 2)
        return avg
    
    rating_average.short_description = "average"