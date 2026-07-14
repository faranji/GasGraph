from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_coordinates(location_name: str) -> tuple:
    """
    Girilen şehir/ilçe ismini koordinatlara çevirir.
    
    Args:
        location_name (str): Örn: "Ankara" veya "Diyarbakır"
    Returns:
        tuple: (latitude, longitude)
    """
    try:
        # TODO 1: Nominatim sınıfını çağır.
        locator = Nominatim(user_agent = "gasgraph_app")

        # TODO 2: geocode() fonksiyonu ile location_name'i arat.
        location = locator.geocode(location_name)

        # TODO 3: Eğer sonuç (location) bulunursa (location.latitude, location.longitude) tuple'ı döndür.
        if location:
            return  (location.latitude, location.longitude)
        else:
            return (None, None)
        
    except GeocoderTimedOut:
        print("timeout error")
        return (None, None)
    pass