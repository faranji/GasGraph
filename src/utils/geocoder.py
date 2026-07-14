import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Mac'lerdeki SSL Sertifika doğrulama hatasını aşmak için güvenlik esnetmesi
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
geopy.geocoders.options.default_ssl_context = ctx

def get_coordinates(location_name: str) -> tuple:
    """
    Girilen şehir/ilçe ismini koordinatlara çevirir.
    """
    try:
        locator = Nominatim(user_agent="gasgraph_app")
        location = locator.geocode(location_name)

        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
        
    except GeocoderTimedOut:
        print("timeout error")
        return (None, None)