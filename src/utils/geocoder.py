import googlemaps
import streamlit as st

try:
    from config import GOOGLE_MAPS_API_KEY
except ModuleNotFoundError:
    GOOGLE_MAPS_API_KEY = st.secrets["GOOGLE_MAPS_API_KEY"]

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_coordinates(location_name: str) -> dict:
    if not gmaps:
        return {}
        
    try:
        geocode_result = gmaps.geocode(location_name, components={"country": "TR"})
        
        results = {}
        
        for place in geocode_result[:5]:
            tam_adres = place['formatted_address']
            lat = place['geometry']['location']['lat']
            lon = place['geometry']['location']['lng']
            
            results[tam_adres] = (lat, lon)
            
        return results
        
    except Exception as e:
        print(f"Google Maps Error: {e}")
        return {}