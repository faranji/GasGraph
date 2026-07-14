import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster 
from streamlit_folium import st_folium
import os
import sys
from utils.geocoder import get_coordinates

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import supabase

st.set_page_config(page_title="GasGraph Optimizer", layout="wide", initial_sidebar_state="expanded", page_icon=":no_mouth:")

# ==========================================
# 0. SESSION STATE
# ==========================================
if "remaining_range" not in st.session_state:
    st.session_state.remaining_range = 150 
if "current_location" not in st.session_state:
    st.session_state.current_location = "Istanbul" 

# ==========================================
# 1. LOAD REAL CLOUD DATA
# ==========================================
@st.cache_data(ttl=3600)
def load_gold_data():
    response = supabase.table("gasgraph_gold_stations").select("*").execute()
    return pd.DataFrame(response.data)

df = load_gold_data()

# ==========================================
# 2. OPTIMIZATION UI
# ==========================================
col1, col_logo, col2 = st.sidebar.columns([1, 4, 1]) 
with col_logo:
    st.image("src/assets/gasgraph_logo.png", use_container_width=True)

with st.sidebar.form(key="route_setup_form"):
    st.title("Route Setup")
    start_loc = st.text_input("Start Location", value=st.session_state.current_location)
    end_loc = st.text_input("Destination", value="Ankara")

    st.divider()
    
    st.title("Vehicle & Capacity")
    engine_type = st.selectbox("Vehicle Type", ["Combustion (Fuel)", "Electric (EV)"])
    
    current_range = st.number_input("Current Dashboard Range (KM)", min_value=10, max_value=1500, value=st.session_state.remaining_range, step=10)
    
    st.divider()
    
    st.title("Preferences")
    brand_options = ["All Brands"] + sorted(df['provider'].dropna().unique().tolist())
    selected_brand = st.selectbox("Preferred Brand", brand_options)
    
    req_wc = st.checkbox("WC Available (Bonus)")
    req_market = st.checkbox("Market Available (Bonus)")
    req_strict = st.checkbox("LPG (Fuel) / Fast Charge (EV) Only (Strict)")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_space1, col_btn, col_space2 = st.columns([1, 4, 1])
    with col_btn:
        submit_button = st.form_submit_button(label="Optimize Route", use_container_width=True)

if submit_button:
    st.session_state.current_location = start_loc
    st.session_state.remaining_range = current_range 
    
    # --- TRANSLATED MESSAGES ---
    with st.spinner("🗺️ Calculating coordinates..."): 
        start_coords = get_coordinates(start_loc)
        end_coords = get_coordinates(end_loc)
        
        if start_coords == (None, None) or end_coords == (None, None):
            st.error("City not found. Please enter a valid location name.")
        else:
            st.success(f"Route is being generated! Start: {start_coords}, Destination: {end_coords}")

# ==========================================
# 3. FILTERING THE DATA
# ==========================================
target_type = "fuel" if "Fuel" in engine_type else "ev"
filtered_df = df[df['station_type'] == target_type].copy()

# Marka filtresi eğer "All Brands" değilse, sadece seçilen markayı filtrele
if selected_brand != "All Brands":
    filtered_df = filtered_df[filtered_df['provider'] == selected_brand]

if "Fuel" in engine_type and req_strict:
    filtered_df = filtered_df[filtered_df['has_lpg'] == True]
elif "EV" in engine_type and req_strict:
    filtered_df = filtered_df[filtered_df['has_fast_charge'] == True]

# ==========================================
# 4. MAIN DASHBOARD UI
# ==========================================
col1, col2, col3 = st.columns(3)
col1.metric(label="Distance to Destination", value="~450 KM") 
col2.metric(label="Current Range", value=f"{st.session_state.remaining_range} KM", delta="- Critical Refuel Needed" if st.session_state.remaining_range < 150 else "")
col3.metric(label="Scanned Stations", value=len(filtered_df))

st.markdown("<br>", unsafe_allow_html=True)

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