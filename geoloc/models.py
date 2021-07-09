from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry

class Continent(models.Model):
    #nom
    name = models.CharField(max_length=50)
    #continent code
    code = models.CharField(max_length=2)
    #population
    pop = models.FloatField('population 2005 en millions')
    #surface
    area = models.IntegerField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

#model d'un pays avec ses frontières
class Country(models.Model):
    #nom
    name = models.CharField(max_length=50)
    #surface
    area = models.IntegerField()
    #population en 2005
    pop2005 = models.IntegerField('Population 2005')
    #code fips (ex : FR)
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    #code iso 2 (ex : FR)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    #code iso 3 (ex : FRA)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    #code des nations unis (ex : FR)
    un = models.IntegerField('United Nations Code')
    #code region
    region = models.IntegerField('Region Code')
    #code subregion
    subregion = models.IntegerField('Sub-Region Code')
    #coordonnées
    lat = models.FloatField()
    lon = models.FloatField()
    
    #continent
    cont = models.ForeignKey(Continent, on_delete=models.CASCADE, null=True)

    # frontières
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name
    
    def contain(self, point):
        return self.mpoly.contains(point)
    


#model d'une ville
class City(models.Model):
    #nom de la ville
    name = models.CharField(max_length=200)
    #population de la ville
    pop = models.IntegerField()
    #densité de la ville
    #den = models.FloatField()
    #pays dans lequel elle est
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    #position geographique
    lat = models.FloatField()
    lng = models.FloatField()
    
    
    # Returns the string representation of the model.
    def __str__(self):
        return self.name

#model d'un point qu'on voudrait placer
class Point(models.Model):

    def which_country(self):
        for country in Country.objects.all():
            if country.contain(self.get_point()):
                return country

    #nom
    name = models.CharField(max_length=50) 

    #position
    lat = models.FloatField()
    lng = models.FloatField()
    

    #srid
    srid = models.CharField(max_length=10, default=4326)

    def get_point(self):
        return GEOSGeometry('SRID=' + self.srid + ';POINT(' + repr(self.lng) + ' ' + repr(self.lat) + ')')

    
    def near_city(self):
        try:
            cities = City.objects.filter(country=self.which_country())
        except:
            return None

        if(len(cities) == 0):
            cities = City.objects.all()
        near = cities[0]
        pnt = GEOSGeometry('SRID=4326;POINT(' + repr(near.lng) + ' ' + repr(near.lat) + ')')
        coord = self.get_point()
        best_distance = pnt.distance(coord)
        #cherche la ville la plus proche
        for city in cities:
            pnt = GEOSGeometry('SRID=4326;POINT(' + repr(city.lng) + ' ' + repr(city.lat) + ')')
            dist = pnt.distance(coord)
            if dist < best_distance :
                best_distance = dist
                near = city
        return near
