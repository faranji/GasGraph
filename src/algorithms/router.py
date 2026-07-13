import math
import pandas as pd

def calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    İki koordinat arasındaki kuş uçuşu mesafeyi (KM) hesaplar.
    """
    # İPUCU: Dünyanın yarıçapı R = 6371 km'dir.
    # TODO 1: Enlem ve boylamları math.radians() ile radyana çevir.
    # TODO 2: Haversine formülünü uygula: a = sin²(Δlat/2) + cos(lat1)*cos(lat2)*sin²(Δlon/2)
    # TODO 3: c = 2 * atan2(√a, √(1−a)) hesapla.
    # TODO 4: Sonuç = R * c döndür.
    
    pass

def calculate_station_cost(station_lat, station_lon, start_lat, start_lon, end_lat, end_lon, 
                           has_wc, has_market, wc_bonus=5.0, market_bonus=3.0) -> float:
    """
    İstasyonun algoritma için "Maliyet" puanını hesaplar. Düşük maliyet = Daha iyi istasyon.
    """
    # TODO 1: start_lat, start_lon ile station_lat, station_lon arasındaki mesafeyi hesapla (calculate_haversine ile).
    # TODO 2: station_lat, station_lon ile end_lat, end_lon arasındaki mesafeyi hesapla.
    # TODO 3: start ile end arasındaki direkt mesafeyi hesapla (Sapmayı bulmak için).
    # TODO 4: Sapma (Detour) = (Start->Station) + (Station->End) - (Start->End)
    
    # TODO 5: Toplam Maliyet = Detour. Eğer has_wc True ise maliyetten wc_bonus'u çıkar. Market varsa market_bonus'u çıkar.
    # TODO 6: Toplam Maliyeti döndür.
    
    pass

def find_optimal_route(start_coords: tuple, end_coords: tuple, df_stations: pd.DataFrame, 
                       max_range: int, current_range: int) -> list:
    """
    Zincirleme (Multi-stop) rota hesaplayıcısı.
    """
    route_history = []
    current_loc = start_coords
    current_remaining_range = current_range
    
    # Hedefe olan toplam mesafeyi hesapla
    dist_to_destination = calculate_haversine(current_loc[0], current_loc[1], end_coords[0], end_coords[1])
    
    # ZİNCİRLEME DÖNGÜSÜ
    # TODO: "while dist_to_destination > current_remaining_range:" döngüsü kur.
    # TODO: df_stations içinden, current_loc'a mesafesi 'current_remaining_range'den KÜÇÜK olan istasyonları filtrele (Aday Kümesi).
    # TODO: Aday kümedeki her istasyon için calculate_station_cost()'u çağır.
    # TODO: En düşük maliyetli (min cost) istasyonu bul.
    # TODO: Bulunan istasyonu route_history listesine ekle (.append)
    # TODO: current_loc'u seçilen istasyonun koordinatları yap.
    # TODO: current_remaining_range'i max_range'e eşitle (Tam depo doldurduk varsayalım).
    # TODO: dist_to_destination'ı yeni konumdan hedefe göre tekrar hesapla. (Döngü devam etsin mi kontrolü)
    
    # Döngü bitince route_history'yi döndür
    return route_history