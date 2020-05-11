"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    """
    향후에는 데이터를 AWS나 기타 DB서버를 이용할 것이기 때문에 
    후 False로 바꿀 DEBUG를 조건으로 만들었고
    static 도움으로 url을 추가하면서 VIEW를 연결시켜줌(화면에 이미지를 올려줌)
    """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    """static(url, folder) 아마 folder에 서버 DB연결하지 않을까? 싶음"""