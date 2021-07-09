from rest_framework import serializers
from .models import Country, Continent, City, Point

class ContinentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Continent
        fields = ['name', 'code', 'pop', 'area']

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'area', 'pop2005', 'fips', 'iso2', 'iso3',
                'un', 'region', 'subregion', 'lon', 'lat', 'cont', 'mpoly']

class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'pop', 'country', 'lng', 'lat']

class PointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Point
        fields = ['name', 'lng', 'lat', 'srid']
