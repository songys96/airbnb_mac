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

    LOGIN_SIGNUP = "signup"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"

    LOGIN_CHOICES = (
        (LOGIN_SIGNUP, "Signup"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_NAVER, "Naver")
    )

    """ 
    choice의 경우 튜플안의 튜플 구조로 (그룹에 들어갈 이름, 보여질 이름)형식을 맞춰주되 
    위 처럼 각 필요한 변수의 이름을 지정해 줌으로써 추상화에 신경써줌
    """

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    # upload_to사용시 해당 폴더가 만들어질것임
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10, null=True, blank=True, default=LANGUAGE_KOR)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=6, null=True, blank=True, default=CURRENCY_KRW)
    superhost = models.BooleanField(default=False)

    login_method = models.CharField(choices=LOGIN_CHOICES, max_length=50, null=True, blank=True, default=LOGIN_SIGNUP)

    
    def __str__(self):
        return self.username


