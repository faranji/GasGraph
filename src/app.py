import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster 
from streamlit_folium import st_folium
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import supabase

st.set_page_config(page_title="GasGraph Optimizer", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 0. SESSION STATE (Hafıza Yönetimi)
# ==========================================
if "remaining_range" not in st.session_state:
    st.session_state.remaining_range = 150 # Default hesaplanan başlangıç menzili
if "current_location" not in st.session_state:
    st.session_state.current_location = "Diyarbakır" 

# ==========================================
# 1. LOAD REAL CLOUD DATA
# ==========================================
@st.cache_data(ttl=3600)
def load_gold_data():
    response = supabase.table("gasgraph_gold_stations").select("*").execute()
    return pd.DataFrame(response.data)

df = load_gold_data()

# ==========================================
# 2. OPTIMIZATION UI (FORM YAPISI)
# ==========================================
# st.sidebar.form ile tüm girdileri bir pakete alıyoruz.
# Butona basılana kadar sayfa ASLA yenilenmez (Ekran kararmaz!)
with st.sidebar.form(key="route_setup_form"):
    st.title("🛣️ Route Setup")
    start_loc = st.text_input("Başlangıç Noktası", value=st.session_state.current_location)
    end_loc = st.text_input("Varış Noktası", value="İstanbul")

    st.markdown("---")
    st.title("🚗 Vehicle & Capacity")
    engine_type = st.selectbox("Araç Tipi", ["İçten Yanmalı (Fuel)", "Elektrikli (EV)"])
    
    # Kullanıcıdan kapasite ve anlık durumu alıyoruz
    max_range = st.number_input("Tam Depo / Tam Şarj Menzili (KM)", min_value=100, max_value=1500, value=600, step=50)
    current_fuel_pct = st.slider("Mevcut Yakıt/Şarj Seviyesi (%)", min_value=1, max_value=100, value=25, step=1)
    
    st.markdown("---")
    st.title("⭐ Preferences")
    req_wc = st.checkbox("WC Bulunsun (Bonus)")
    req_market = st.checkbox("Market Bulunsun (Bonus)")
    req_strict = st.checkbox("Sadece LPG (Fuel) / Hızlı Şarj (EV) (Strict)")

    # Butonu aşağı itmek için görünmez bir boşluk ekliyoruz
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Formu tetikleyen aksiyon butonu
    submit_button = st.form_submit_button(label="Rotayı Optimize Et   🚀")

# Butona basıldığında matematiksel hesaplamaları yapıp state'i güncelliyoruz
if submit_button:
    st.session_state.current_location = start_loc
    # Gerçek menzil hesabı: (Tam kapasite) * (Yüzde / 100)
    st.session_state.remaining_range = int(max_range * (current_fuel_pct / 100))

# ==========================================
# 3. FILTERING THE DATA
# ==========================================
target_type = "fuel" if "Fuel" in engine_type else "ev"
filtered_df = df[df['station_type'] == target_type].copy()

if "Fuel" in engine_type and req_strict:
    filtered_df = filtered_df[filtered_df['has_lpg'] == True]
elif "EV" in engine_type and req_strict:
    filtered_df = filtered_df[filtered_df['has_fast_charge'] == True]

# ==========================================
# 4. MAIN DASHBOARD UI
# ==========================================
st.title("GasGraph - Akaryakıt & Rota Optimizasyonu")

col1, col2, col3 = st.columns(3)
col1.metric(label="Hedefe Kalan Yol", value="~1200 KM") # Diyarbakır - İstanbul ortalama
col2.metric(label="Mevcut Menzil", value=f"{st.session_state.remaining_range} KM", delta="- Kritik İkmal Gerekiyor" if st.session_state.remaining_range < 150 else "")
col3.metric(label="Taranan İstasyon", value=len(filtered_df))

# ==========================================
# 5. MAP CREATION
# ==========================================
m = folium.Map(location=[39.2, 35.6], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m)

filtered_df = filtered_df.dropna(subset=['lat', 'lon'])

for idx, row in filtered_df.iterrows():
    marka = str(row['provider'])
    img_name = marka.replace(" ", "_") 
    icon_path = f"src/assets/{img_name}.png"
    
    tooltip_text = f"<b>{marka}</b><br>Type: {row['station_type'].upper()}"
    if row['has_wc'] == True: tooltip_text += "<br>WC: ✔️"
    if row['has_market'] == True: tooltip_text += "<br>Market: ✔️"
    
    if os.path.exists(icon_path):
        custom_icon = folium.CustomIcon(icon_path, icon_size=(35, 35))
        folium.Marker(
            location=[row['lat'], row['lon']],
            tooltip=tooltip_text,
            icon=custom_icon
        ).add_to(marker_cluster)  
    else:
        folium.Marker(
            location=[row['lat'], row['lon']],
            tooltip=tooltip_text,
            icon=folium.Icon(color='blue' if row['station_type'] == 'ev' else 'red', icon='info-sign')
        ).add_to(marker_cluster) 

st_folium(m, width="100%", height=600, returned_objects=[])