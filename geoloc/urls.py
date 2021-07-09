from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'continents', views.ContinentViewSet)
router.register(r'points', views.PointViewSet)

urlpatterns = [
    path('', include(router.urls)),
]