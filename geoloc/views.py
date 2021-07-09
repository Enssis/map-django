from .models import Country, Continent, City, Point
from .serializers import CountrySerializer, ContinentSerializer, CitySerializer, PointSerializer
from rest_framework import viewsets, renderers
from rest_framework.decorators import action, renderer_classes
from rest_framework.response import Response

#vues pour les pays
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

#vue pour les continents
class ContinentViewSet(viewsets.ModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer


#vue pour les villes
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

#vue de creation de point
class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def nearest(self, request, *args, **kwargs):
        point = self.get_object()
        near = point.near_city()
        return Response(near)
