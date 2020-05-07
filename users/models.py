from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    """
    Custom user model 
    it designs User Info
    """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other")
    )

    LANGUAGE_ENG = "english"
    LANGUAGE_KOR = "korea"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENG, "Eng"),
        (LANGUAGE_KOR, "Kor")
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW")
    )

    """ 
    choice의 경우 튜플안의 튜플 구조로 (그룹에 들어갈 이름, 보여질 이름)형식을 맞춰주되 
    위 처럼 각 필요한 변수의 이름을 지정해 줌으로써 추상화에 신경써줌
    """

    avatar = models.ImageField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10, null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=6, null=True, blank=True)
    superhost = models.BooleanField(default=False)
    


