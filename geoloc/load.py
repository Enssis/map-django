from .custom_layer import CustomLayerMapping
from datapackage import Package
from pathlib import Path
from .models import Continent, Country, City
import csv

def get_country_to_continent():
    package = Package('https://datahub.io/JohnSnowLabs/country-and-continent-codes-list/datapackage.json')

    # print list of all resources:
    print(package.resource_names)

    # print processed tabular data (if exists any)
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            print("reading country ressources")
            return resource.read()

#recupere les données de la liste de continents/pays pour créer les continents
def create_continents():
    #garde les iso des continents déjà créer pour éviter de les recréer
    already_done = []
    countries_to_continent = get_country_to_continent()
    for elements in countries_to_continent:
        if not already_done.__contains__(elements[1]):  
            already_done.append(elements[1])
            continent = Continent.objects.create(name = elements[0], 
                        code = elements[1],
                        pop = 0,
                        area = 0)
        #continents[elements[1]] = continent

    return countries_to_continent, continent

cities_csv = Path(__file__).resolve().parent / 'data' / 'worldcities.csv'

def add_cities():
    with open(str(cities_csv)) as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'city':
                continue
            try:
                City.objects.create(name = row[0],
                        pop = row[9],
                        country = Country.objects.get(iso3=row[6]),
                        lng = row[3],
                        lat = row[2])
            except:
                print("Country ", row[6], " does'nt exist")

def update_countries(countries_to_continent):
    for element in countries_to_continent:
        try:
            continent = Continent.objects.get(code=element[1])
            country = Country.objects.get(iso3=element[4])
            
            country.cont = continent
            country.save()
        except:
            print("marche pas pour : ", element[4])

world_mapping = {
    'fips' : 'FIPS',
    'iso2' : 'ISO2',
    'iso3' : 'ISO3',
    'un' : 'UN',
    'name' : 'NAME',
    'area' : 'AREA',
    'pop2005' : 'POP2005',
    'region' : 'REGION',
    'subregion' : 'SUBREGION',
    'lon' : 'LON',
    'lat' : 'LAT',
    'mpoly' : 'MULTIPOLYGON',
}

world_shp = Path(__file__).resolve().parent / 'data' / 'countries' / 'TM_WORLD_BORDERS-0.3.shp'

def run(verbose=True):
    """
    Country.objects.all().delete()
    Continent.objects.all().delete()
    City.objects.all().delete()
    countries_to_continent, continent = create_continents()
    lm = CustomLayerMapping(Country, str(world_shp), world_mapping, custom = {'cont' : continent} ,transform=False)
    lm.save(strict=True, verbose=verbose)
    add_cities()
    """
    update_countries(get_country_to_continent())

#met a jour les valeurs de population et surface des continents
def update_continents():
    #met a 0 les valeurs de population et de surface
    for continent in Continent.objects.all():
        continent.pop = 0
        continent.area = 0
        continent.save()
    
    countries = Country.objects.all()
    for country in countries:
        continent = country.cont
        print(continent, continent.pop, continent.area)
        continent.pop += country.pop2005 / 1000000
        continent.area += country.area
        continent.save()