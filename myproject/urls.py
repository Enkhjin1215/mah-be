from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import LotteryViewSet, LotteryByPhoneView, LotteryNumberAllView


router = DefaultRouter()
router.register(r'lotteries', LotteryViewSet, basename='lottery')


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('by-phone/', LotteryByPhoneView.as_view(), name='lottery-by-phone'),
    path("lotteries/numbers/all/", LotteryNumberAllView.as_view(), name="lottery-numbers-all"),

]

# MEDIA файлуудыг serve хийх тохиргоо
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

