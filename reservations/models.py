from django.db import models
from django.utils import timezone
from core import models as core_models

class Reservation(core_models.TimeStampedModel):
    
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled")
    )

    status = models.CharField(max_length=12, choices = STATUS_CHOICES, default=STATUS_PENDING)
    guest = models.ForeignKey("users.User", related_name='reservation', on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", related_name='reservation', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.room.name} - {self.check_in}'

    def in_progress(self):
        # django time server zone을 이용해서 장고가 시간을 해당 시각에 맞게 변환해줄것
        # 어플리케이션의 시간을 알 수 있음
        now = timezone.now().date()
        return now > self.check_in and now < self.check_out
    in_progress.boolean = True

    def in_finished(self):
        now = timezone.now().date()
        return now > self.check_out
    in_finished.boolean = True