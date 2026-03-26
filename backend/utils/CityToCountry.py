from organization.models import City
def CityToCountry(city_name):
    city = City.objects.filter(name__icontains=city_name).first()
    if city is not None:
        return city
    else:
        return None
