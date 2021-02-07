from django.db import migrations
from countryinfo import CountryInfo
import awoc  # pip install a-world-of-countries


def addWorldDb(apps, schema_editor):
    continent = apps.get_model("covid19", "Continent")
    country = apps.get_model("covid19", "Country")
    db_alias = schema_editor.connection.alias
    id_continent = 0
    obj_continent = []
    obj_country = []
    world = awoc.AWOC()
    for itm_continent in world.get_continents():
        id_continent = id_continent + 1
        obj_continent.append(continent(id=id_continent, continent=itm_continent["Continent Name"]))
        for itm_country in world.get_countries_data_of(itm_continent["Continent Name"]):
            obj_country.append(country(country=itm_country["Country Name"],
                                       iso2=itm_country["ISO2"],
                                       population=0,
                                       continent=obj_continent[-1]))
        # Error keys in CountryInfo ;(
        key_error = ["gambia", "sao tome and principe", "antarctica", "cocos islands", "myanmar", "palestine",
                     "andorra", "kosovo", "macedonia", "montenegro", "vatican", "bahamas", "british virgin islands",
                     "curacao", "netherlands antilles", "saint barthelemy", "saint martin", "sint maarten",
                     "turks and caicos islands", "u.s. virgin islands", "micronesia", "pitcairn"]
        for obj in obj_country:
            if obj.country.lower() not in key_error:
                obj.population = CountryInfo(obj.country).population()

    continent.objects.using(db_alias).bulk_create(obj_continent)
    country.objects.using(db_alias).bulk_create(obj_country)


class Migration(migrations.Migration):
    dependencies = [
        ('covid19', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(addWorldDb),
    ]
