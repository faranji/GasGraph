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
    # TODO 1: Nominatim sınıfını çağır. (user_agent olarak 'gasgraph_app' gibi bir isim ver)
    # TODO 2: geocode() fonksiyonu ile location_name'i arat.
    # TODO 3: Eğer sonuç (location) bulunursa (location.latitude, location.longitude) tuple'ı döndür.
    # TODO 4: Bulunamazsa veya hata verirse (None, None) döndür.
    
    pass