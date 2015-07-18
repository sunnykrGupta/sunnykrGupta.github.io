Title: A Practical Guide to Geopy
Date: 2015-07-19 01:31:31
Category: Blog
Tags: Geopy, Geocoder, Python, GoogleV3, Yandex, Geonames
Author: Sunny Kr Gupta


# A Practical Guide to Geopy

During my final major academic project, i was working with [Twitter](http://twitter.com) data (ie. tweets). I did some research and found out approximately only 1% of all Tweets published on Twitter are geolocated (ie. have location information). This is a very small portion of the Tweets, and i needed almost every tweets location to segregate data country-wise. 
  - How to resolve a string location to determine country ("Banagher", "Ipoh" etc )
  - How to resolve a Coordinate into country. ('4.581' - '101.082' etc)

There comes a [Geopy](http://geopy.readthedocs.org/) to rescue us to this problem.

#### Geopy
>Geopy makes it easy for Python developers to locate the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources.

Geocoding is the process of converting addresses (like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic coordinates (like latitude 37.423021 and longitude 122.083739) or reverse.

#####Available Geocoder APIs
There are several Geocoding service provided by different Map APIs, populars are listed below: 
 - [Google Maps Geocoding V3 API](https://developers.google.com/maps/documentation/geolocation/intro) (2500 per-day)
 - [Geonames](http://www.geonames.org/about.html) (30000 per-day | 2000 per-hour)
 - [Nominatim - Open Street Map](http://wiki.openstreetmap.org/wiki/Nominatim) (refer Usage Docs)
 - [Yandex Map API](https://tech.yandex.com/maps/doc/geocoder/desc/concepts/About-docpage/)  (25,000 per-day)
 - [Bing  Map API (Microsoft)](https://msdn.microsoft.com/en-us/library/ff428643.aspx) (refer Usage Docs)
 - [Yahoo BOSS Finder](https://developer.yahoo.com/boss/geo/) (refer Usage Docs)

> Note : Geocoder APIs may have request limts on per-day or per-IP or others. Increasing those limts can result in blacklisting. At the time of writing this post, limits are mentioned in brackets above.


####Installation
-----------------------------------------------------------
Open your favorite Terminal and run these commands. Install using `pip` with:
```sh
$ pip install geopy
```

####Geocoding
To query a location using string using `Google MAP V3`. To acquire key you need to register your app on google developer console. 
```python
from geopy.geocoders import GoogleV3
import json
geolocator = GoogleV3(api_key='AIzaSyCxk0i1WQokYRgUxAZieq')
location = geolocator.geocode("Washington", language='en')
if location != None:
    print json.dumps(location.raw, indent=4)
    print location.address
else:
    print "No location!" , location
```

Gocoders have different service api classes, here i have used `GoogleV3`, then an object is created named `geolocator` to query and saved results of my query string "Washington" in `location`. If query string doesnt contain valid place name or city, it throws `None`. Now lets see what we got after this script:

```JSON
{
    "geometry": {
        "location_type": "APPROXIMATE",
        "bounds": {
            "northeast": {
                "lat": 38.995548, "lng": -76.909393
            }, 
            "southwest": {
                "lat": 38.8031495, "lng": -77.11974}
        },
        "location": {
            "lat": 38.9071923, "lng": -77.0368707}
        },
    "address_components": [
        {
            "long_name": "Washington",
            "types": ["locality", "political"], 
            "short_name": "D.C."
        },
        {
            "long_name": "District of Columbia",
            "types": ["administrative_area_level_1", "political"], 
            "short_name": "DC"
        },
        { 
            "long_name": "United States",
            "types": ["country", "political"], 
            "short_name": "US"
        }
    ],
    "place_id": "ChIJW-T2Wt7Gt4kRKl2I1CJFUsI", 
    "formatted_address": "Washington, DC, USA", 
    "types": ["locality", "political"]
}
Washington, DC, USA
```

So, you can see its a format of data returned from Google Map API, so we need to extract the information we are looking for from this resulted data. Easy huh! You can see lattitude. longitude , Country name, District name, and other place information.
</br>
You can query a string of coordinate too, in above code replace the geolocator lines with follows and run:

```python
location = geolocator.reverse("52.509669, 13.376294")
```
You can see the raw JSON output as result. See below, if you want formatted address, use `location.address` , `location.latitude`, `location.longitude` gives you coordinates of place and `location.raw` gives you the result like we saw above in JSON format, that contains lots of other information.


```python
>>> print(location.address)
Potsdamer Platz, Mitte, Berlin, 10117, Deutschland, European Union
>>> print((location.latitude, location.longitude))
(52.5094982, 13.3765983)
```
Similarly we can use other Geocoder APIs too, `Nominatim` as openstreet map, `Yandex` for Yandex Map, `GeoNames` as Geonames Geocoder etc. 

Geopy code for `GeoNames` and `Yandex` :

```python
from geopy.geocoders import GeoNames
import json
geolocator = GeoNames(username='Ur_user_NAME')  # Register at Geonames
location = geolocator.geocode("冥府", timeout=10)
if location != None:
        json.dump(location.raw, f)
    print location.address
else:
    print "No location!" , location
```

```python
from geopy.geocoders import Yandex
import json
geolocator = Yandex(lang='en_US')
location = geolocator.geocode("بغداد، العراق", timeout=10)
if location != None:
    print json.dumps(location.raw, indent=4)
    print location.address
    print location.latitude, " -> ", location.longitude
else:
    print location
```

So simple right! for using other Geocoder Map APIs , refer to full documentation of [Geopy](http://geopy.readthedocs.org/en/latest/#). I hope you understands the working of Geocoder APIs and power of Geopy. 
</br>Comment below if you come across any problem and give feedback. Thanks you all! Have a good day!



