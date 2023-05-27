from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet


router = DefaultRouter()
router.register("places", PlaceViewSet)

urlpatterns = router.urls

app_name = "geo"
