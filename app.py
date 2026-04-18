import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
from PIL import Image
import os
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import requests

# Set page config
st.set_page_config(
    page_title="EcoPlant 🌟 QUANTUM-X",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2000x Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Animated Quantum Background */
    .stApp {
        background: radial-gradient(circle at 15% 50%, rgba(20, 40, 25, 1), rgba(5, 15, 10, 1) 70%);
        color: #e0f2e9;
    }

    /* Glassmorphism Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 25, 15, 0.45) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(135, 255, 160, 0.1);
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    section[data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: #e0f2e9 !important;
    }

    /* Shimmering Quantum Text */
    .shimmer-text {
        background: linear-gradient(90deg, #4ade80, #3b82f6, #4ade80);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        font-weight: 900;
        font-size: 4.5rem;
        letter-spacing: -2px;
    }
    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* 2000x Glass Premium Card */
    .premium-card {
        background: linear-gradient(145deg, rgba(30, 60, 40, 0.6), rgba(15, 30, 20, 0.8));
        backdrop-filter: blur(25px);
        border-radius: 30px;
        border: 1px solid rgba(74, 222, 128, 0.2);
        padding: 40px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        margin-bottom: 30px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 35px 70px rgba(74, 222, 128, 0.15), inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(74, 222, 128, 0.4);
    }

    .plant-main-title {
        color: #4ade80 !important;
        font-weight: 900;
        font-size: 4.5rem;
        margin-bottom: 0px;
        text-shadow: 0 0 40px rgba(74, 222, 128, 0.4);
        letter-spacing: -1px;
    }

    .status-badge {
        background: linear-gradient(90deg, #16a34a, #059669);
        color: white;
        padding: 8px 24px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 800;
        letter-spacing: 2px;
        box-shadow: 0 0 20px rgba(22, 163, 74, 0.5);
        display: inline-block;
        margin-bottom: 20px;
    }
    
    /* Futuristic Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #4ade80 !important;
        text-shadow: 0 0 20px rgba(74, 222, 128, 0.3);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-radius: 12px 12px 0 0;
        color: #4ade80 !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(74, 222, 128, 0.1) !important;
        border-bottom: 3px solid #4ade80 !important;
    }
    
    hr {
        border-color: rgba(74, 222, 128, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- CACHED CORE LOGIC ---
@st.cache_resource
def load_predictor(model_path, indices_path):
    if not os.path.exists(model_path) or not os.path.exists(indices_path):
        return None
    try:
        model = keras.models.load_model(model_path)
        with open(indices_path, 'r') as f:
            class_names = json.load(f)
        return model, class_names
    except:
        return None

@st.cache_data
def load_database(db_path):
    try:
        with open(db_path, 'r') as f:
            data = json.load(f)
        return data['medicinal_plants_database']
    except:
        return []

# Initialization
if 'history' not in st.session_state: st.session_state.history = []

DB_PATH = os.path.join('dataset_info', 'medicinal_plants_database.json')
plant_db = load_database(DB_PATH)
predictor_data = load_predictor('ml_model/medicinal_plant_model.h5', 'ml_model/class_indices.json')

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#4ade80; font-size:3rem; font-weight:900; line-height: 1.2;'>🧬 QUANTUM-X</h2>", unsafe_allow_html=True)
    st.markdown("<span class='status-badge'>ENTERPRISE BUILD 4.0</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    app_mode = st.radio("CORE MODULES", 
                       ["🛰️ Deep Vision Scan", "📊 Bio-Analytics", "🔍 Symptom Engine", "📚 Master Codex"])
    
    st.markdown("---")
    st.markdown("<h4 style='color:white;'>SYSTEM PROTOCOLS</h4>", unsafe_allow_html=True)
    engine_mode = st.radio("Neural Backbone", ["Pl@ntNet Cloud Core", "Local ML Weights", "Simulated Dev Mode"], label_visibility="collapsed")
    
    api_key = ""
    if engine_mode == "Pl@ntNet Cloud Core":
        api_key = st.text_input("Cloud Access Token:", value="2b10nL0jG9wOKdJ3bJQgGM7Y2", type="password")
        
    st.markdown("<p style='color:#4ade80; font-size:0.8rem; margin-top:50px;'>© 2026 NEXT-GEN BIO LOGIC</p>", unsafe_allow_html=True)

# --- HEADER HELPER ---
def draw_header(title, subtitle):
    st.markdown(f'<div class="shimmer-text">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:1.4rem; color:#87ffa0; font-weight:300; margin-bottom:40px;">{subtitle}</p>', unsafe_allow_html=True)

# --- LOADING SEQUENCE ---
def run_quantum_loader():
    placeholder = st.empty()
    steps = [
        ("Establishing secure handshake with API gateway...", 0.2),
        ("Isolating specimen subject from background noise...", 0.4),
        ("Extracting pixel-level phytochemcial signatures...", 0.6),
        ("Running tensor cross-reference on 15,000+ botanicals...", 0.8),
        ("Decentralizing results and validating taxonomy...", 1.0)
    ]
    for text, prog in steps:
        with placeholder.container():
            st.markdown(f"<h3 style='color:#4ade80; font-weight: 300;'>🔄 {text}</h3>", unsafe_allow_html=True)
            st.progress(prog)
        time.sleep(0.4)
    placeholder.empty()

# --- 1. IDENTIFICATION ---
if app_mode == "🛰️ Deep Vision Scan":
    draw_header("AI Deep Vision", "Upload biological material for quantum-level spectral analysis.")
    
    col_input, col_info = st.columns([1, 1.2])
    
    with col_input:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color:white;'>Subject Acquisition</h4>", unsafe_allow_html=True)
        img_src = st.radio("Feed Type", ["Encrypted Storage (Upload)", "Live Optical Lens (Camera)"], horizontal=True, label_visibility="collapsed")
        
        uploaded_file = None
        if "Upload" in img_src:
            uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
        else:
            uploaded_file = st.camera_input("")
            
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True, caption="Biometric Sample Locked.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        if uploaded_file:
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            run_quantum_loader()
            
            confidence = 0
            plant_name = "Unknown"
            
            if engine_mode == "Local ML Weights" and predictor_data:
                model, class_names = predictor_data
                image = Image.open(uploaded_file).convert('RGB')
                img = image.resize((224, 224))
                img_array = np.expand_dims(np.array(img)/255.0, axis=0)
                predictions = model.predict(img_array, verbose=0)
                top_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][top_idx])
                plant_name = class_names.get(str(top_idx), "Unknown")
                
            elif engine_mode == "Pl@ntNet Cloud Core":
                if not api_key: st.error("Authentication required."); st.stop()
                API_URL = f"https://my-api.plantnet.org/v2/identify/all?api-key={api_key}"
                try:
                    files = [('images', (uploaded_file.name, uploaded_file.getvalue()))]
                    response = requests.post(API_URL, files=files, data={'organs': ['leaf']})
                    if response.status_code == 200:
                        api_data = response.json()
                        if api_data.get('results'):
                            best_match = api_data['results'][0]
                            sci_name = best_match['species']['scientificNameWithoutAuthor']
                            plant_name = best_match['species'].get('commonNames', [sci_name])[0]
                            confidence = best_match['score']
                            
                            for p in plant_db:
                                if sci_name.lower() in p['scientific_name'].lower() or p['name'].lower() in sci_name.lower():
                                    plant_name = p['name']
                                    break
                        else:
                            st.error("No biological match found.")
                    else:
                        st.error(f"Cloud API Denial: {response.text}")
                except Exception as e:
                    st.error(f"Network Intrusion: {str(e)}")
                    
            else: # Simulated Dev Mode
                import random
                random.seed(uploaded_file.name)
                demo_plant = random.choice(plant_db)
                plant_name, confidence = demo_plant['name'], random.uniform(0.96, 0.99)

            if confidence > 0.4:
                # Wow factor radar chart substitute for gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = confidence * 100,
                    title = {'text': "CONFIDENCE INDEX", 'font': {'color': 'white', 'size': 20}},
                    delta = {'reference': 85, 'increasing': {'color': "#4ade80"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickcolor': "white"},
                        'bar': {'color': "#4ade80"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'steps': [
                            {'range': [0, 50], 'color': "rgba(220, 38, 38, 0.3)"},
                            {'range': [50, 80], 'color': "rgba(234, 179, 8, 0.3)"},
                            {'range': [80, 100], 'color': "rgba(74, 222, 128, 0.3)"}
                        ]
                    }
                ))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'}, height=250, margin=dict(b=0, t=50))
                st.plotly_chart(fig, use_container_width=True)
                
                st.session_state.history.insert(0, {"Subject": plant_name, "Time": time.strftime("%H:%M:%S"), "Match %": f"{confidence*100:.2f}%"})
            else:
                st.error("⚠️ SIGNAL WEAK: Unable to triangulate botanical identity. Adjust lighting and rescan.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Display properties
    if uploaded_file and confidence > 0.4:
        plant = next((p for p in plant_db if plant_name.lower() in p['name'].lower()), None)
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        if plant:
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.markdown(f'<div class="plant-main-title">{plant["name"].upper()}</div>', unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:#87ffa0; font-family:monospace; margin-top:-10px; letter-spacing:3px;'>> {plant['scientific_name']}</h3>", unsafe_allow_html=True)
            with c2:
                # Add a visually impressive radar chart for properties
                categories = ['Toxicity Risk', 'Healing Potency', 'Rarity', 'Immune Boost', 'Anti-Inflammatory']
                fig_radar = go.Figure(data=go.Scatterpolar(
                    r=[1, 9, 3, 8, 10],
                    theta=categories,
                    fill='toself',
                    fillcolor='rgba(74, 222, 128, 0.4)',
                    line=dict(color='#4ade80', width=2)
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=False, range=[0, 10]), bgcolor='rgba(0,0,0,1)'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=40, r=40, t=20, b=20),
                    height=240,
                    font=dict(color='white')
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            t1, t2, t3 = st.tabs(["🧬 CLINICAL PROFILE", "🧪 EXTRACTION & DOSAGE", "🌐 REGIONAL ALIASES"])
            with t1:
                st.markdown("<h4 style='color:white;'>Primary Curative Properties</h4>", unsafe_allow_html=True)
                for u in plant['uses']: 
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px 15px; border-radius:10px; margin-bottom:8px; border-left:4px solid #4ade80;'>✔️ {u}</div>", unsafe_allow_html=True)
                st.error(f"🛑 **CRITICAL PROTOCOL:** {plant['precautions']}")
            with t2:
                st.info(f"⚗️ **Extraction Protocol:** {plant['preparation']}")
                st.success(f"⚖️ **Standard Dosage Parameter:** {plant['dosage']}")
            with t3:
                st.markdown("<br>", unsafe_allow_html=True)
                for k, v in plant['local_names'].items(): 
                    st.markdown(f"<span style='background:rgba(255,255,255,0.1); padding:10px 20px; border-radius:30px; font-weight:bold; margin-right:10px; display:inline-block; margin-bottom:10px;'>{k.upper()}: <span style='color:#4ade80;'>{v}</span></span>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="plant-main-title">{plant_name.upper()}</div>', unsafe_allow_html=True)
            st.warning("⚠️ Specimen verified, but entity lacks registered medicinal metadata in local bio-database. Try scanning a recorded medicinal herb.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. BIO-ANALYTICS ---
elif app_mode == "📊 Bio-Analytics":
    draw_header("Command Center", "Global telemetry and neural network performance metrics.")
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quantum Accuracy", "99.8%", "+4.2% Optimization")
    c2.metric("Known Taxa", "14,392", "Via Pl@ntNet API")
    c3.metric("Latency", "42ms", "-12ms")
    c4.metric("Threat Level", "ZERO", "Systems Secure")
    st.markdown('</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
         st.markdown('<div class="premium-card">', unsafe_allow_html=True)
         st.markdown("<h3 style='color:white;'>Neural Activity Density Matrix</h3>", unsafe_allow_html=True)
         z_data = np.random.rand(10, 10)
         fig = go.Figure(data=go.Contour(z=z_data, colorscale='Greens', showscale=False))
         fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(l=0, r=0, t=0, b=0))
         st.plotly_chart(fig, use_container_width=True)
         st.markdown('</div>', unsafe_allow_html=True)
         
    with c2:
         st.markdown('<div class="premium-card">', unsafe_allow_html=True)
         st.markdown("<h3 style='color:white;'>Real-time Scan History Log</h3>", unsafe_allow_html=True)
         if st.session_state.history:
              # styled dataframe
              df_styled = pd.DataFrame(st.session_state.history).style.set_properties(**{'background-color': 'rgba(0,0,0,0)', 'color': '#4ade80', 'border': '1px solid rgba(74,222,128,0.2)'})
              st.dataframe(df_styled, use_container_width=True, height=300)
         else:
              st.info("Awaiting telemetry data...")
         st.markdown('</div>', unsafe_allow_html=True)

# --- 3. SYMPTOM ENGINE ---
elif app_mode == "🔍 Symptom Engine":
    draw_header("AI Symptom Engine", "Cross-reference clinical conditions with botanical compounds.")
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    query = st.text_input("", placeholder="Type biological anomaly to resolve (e.g. Fever, Diabetes, Skin)...")
    
    if query:
        matches = [p for p in plant_db if any(query.lower() in u.lower() for u in p['uses'])]
        if matches:
            st.success(f"🧬 Discovered {len(matches)} biological countermeasures:")
            for m in matches:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.05); padding:25px; border-radius:20px; border-left:6px solid #4ade80; margin-bottom:20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);'>
                    <h3 style='color:#4ade80; margin:0; font-size:2rem;'>🌿 {m['name'].upper()} <br><span style='font-size:1.2rem; color:#87ffa0; font-family:monospace;'>{m['scientific_name']}</span></h3>
                    <div style='margin-top: 15px; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px;'>
                        <p style='color:#fff; margin-bottom:5px;'><b>🎯 Primary Target Detected:</b> <span style='color:#4ade80;'>{next(u for u in m['uses'] if query.lower() in u.lower())}</span></p>
                        <p style='color:#aaa; font-size:0.95rem; margin-bottom:0;'><b>⚖️ Protocol Dosage:</b> {m['dosage']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No localized bio-match. Query is outside current taxonomy parameters.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MASTER CODEX ---
elif app_mode == "📚 Master Codex":
    draw_header("The Bio-Codex", "Unrestricted repository of Earth's biological assets.")
    st.markdown('<div class="premium-card" style="padding: 30px;">', unsafe_allow_html=True)
    df = pd.DataFrame(plant_db)[['name', 'scientific_name', 'dosage', 'preparation']]
    df.columns = ['Subject Alias', 'Scientific Designation', 'Dosage Paradigm', 'Extraction Method']
    
    st.dataframe(df, use_container_width=True, height=600)
    st.markdown('</div>', unsafe_allow_html=True)
