import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
from PIL import Image
import os
import pandas as pd
import time

# Set page config
st.set_page_config(
    page_title="EcoPlant | AI Medicinal Identifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a Premium, Modern Look (Glassmorphism & Nature Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1b5e20 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Card Styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        margin-bottom: 25px;
    }

    .header-text {
        color: #2e7d32;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }

    .sub-text {
        color: #4e342e;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: #2e7d32 !important;
        font-size: 2.5rem !important;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #2e7d32 0%, #43a047 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(46, 125, 50, 0.3);
        color: white;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
    }

    .plant-title {
        color: #1b5e20;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .scientific-name {
        color: #558b2f;
        font-size: 1.5rem;
        font-style: italic;
        margin-top: -10px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
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

# Paths
MODEL_PATH = os.path.join('ml_model', 'medicinal_plant_model.h5')
if not os.path.exists(MODEL_PATH): MODEL_PATH = 'medicinal_plant_model.h5'
INDICES_PATH = os.path.join('ml_model', 'class_indices.json')
if not os.path.exists(INDICES_PATH): INDICES_PATH = 'class_indices.json'
DB_PATH = os.path.join('dataset_info', 'medicinal_plants_database.json')

# Load Predictor and Data
predictor_data = load_predictor(MODEL_PATH, INDICES_PATH)
plant_db = load_database(DB_PATH)

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/clouds/200/leaf.png", width=150)
st.sidebar.title("EcoPlant AI")
st.sidebar.markdown("*Preserving Nature via Intelligence*")
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox("Navigate Menu", ["🌿 Identify Plant", "📚 Plant Library", "ℹ️ About System"])

# Enhancement: Demo Mode for users without model files
use_demo = st.sidebar.toggle("Virtual Demo Mode", value=predictor_data is None, help="Simulate AI identification if model is missing")

if app_mode == "🌿 Identify Plant":
    st.markdown('<div class="header-text">Medicinal Plant Identification</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Capture or upload a leaf image to unlock nature\'s secrets.</div>', unsafe_allow_html=True)

    # Tabs for Upload vs Camera
    input_tab1, input_tab2 = st.tabs(["📁 Upload Image", "📸 Real-time Camera"])
    
    uploaded_file = None
    with input_tab1:
        uploaded_file = st.file_uploader("Drop your leaf image here", type=["jpg", "jpeg", "png"])
    
    with input_tab2:
        camera_file = st.camera_input("Take a photo of the leaf")
        if camera_file:
            uploaded_file = camera_file

    if uploaded_file is not None:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            image = Image.open(uploaded_file).convert('RGB')
            st.image(image, caption='Input Sample', use_column_width=True, clamp=True)
        
        with col2:
            st.markdown("### AI Diagnostic Engine")
            with st.spinner('Deep feature extraction in progress...'):
                time.sleep(1.5) # Aesthetic delay
                
                if predictor_data and not use_demo:
                    model, class_names = predictor_data
                    img = image.resize((224, 224))
                    img_array = np.array(img) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    predictions = model.predict(img_array, verbose=0)
                    top_idx = np.argmax(predictions[0])
                    confidence = predictions[0][top_idx]
                    plant_name = class_names.get(str(top_idx), "Unknown")
                else:
                    # MOCK PREDICTION FOR DEMO
                    plant_name = "Neem" if use_demo else "Unknown"
                    confidence = 0.985 if use_demo else 0.0
                    if not use_demo: st.error("Model missing. Enable 'Demo Mode' in sidebar to test UI.")

                if confidence > 0.1 or use_demo:
                    st.metric("Top Classification", plant_name, f"{confidence*100:.1f}% Match")
                    st.progress(float(confidence))
                    st.success("Analysis Optimized!")
                else:
                    st.error("Could not identify. Please try a clearer leaf photo.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Show Plant Details if identified
        if (confidence > 0.4 or use_demo) and plant_name != "Unknown":
            plant_info = next((p for p in plant_db if p['name'].lower() in plant_name.lower() or plant_name.lower() in p['name'].lower()), None)
            
            if plant_info:
                st.markdown(f'<div class="plant-title">{plant_info["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="scientific-name">{plant_info["scientific_name"]}</div>', unsafe_allow_html=True)
                
                d_col1, d_col2 = st.columns([2, 1])
                
                with d_col1:
                    tabs = st.tabs(["🌱 Key Benefits", "🧪 Preparation", "💊 Dosage & Safety"])
                    with tabs[0]:
                        for use in plant_info['uses']:
                            st.write(f"✅ {use}")
                    with tabs[1]:
                        st.info(f"**Method:** {plant_info['preparation']}")
                    with tabs[2]:
                        st.success(f"**Dosage:** {plant_info['dosage']}")
                        st.warning(f"**Caution:** {plant_info['precautions']}")
                
                with d_col2:
                    st.markdown("#### Regional Names")
                    for lang, val in plant_info['local_names'].items():
                        st.write(f"**{lang.capitalize()}:** {val}")
                    
                    # Enhancement: Download report
                    report_text = f"Plant Analysis Report\n\nName: {plant_info['name']}\nScientific Name: {plant_info['scientific_name']}\n\nUses:\n" + "\n".join([f"- {u}" for u in plant_info['uses']])
                    st.download_button("📥 Download Report", report_text, file_name=f"{plant_info['name']}_Profile.txt")

elif app_mode == "📚 Plant Library":
    st.markdown('<div class="header-text">Botanical Repository</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Search Database (Common or Scientific Name)", "")
    
    filtered = [p for p in plant_db if search.lower() in p['name'].lower() or search.lower() in p['scientific_name'].lower()]
    
    # Grid using columns
    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(filtered):
                p = filtered[i+j]
                with cols[j]:
                    with st.container():
                        st.markdown(f"""
                        <div class="glass-card">
                            <h3 style='color:#1b5e20;margin-bottom:0;'>{p['name']}</h3>
                            <p style='color:#558b2f;font-style:italic;'>{p['scientific_name']}</p>
                            <p><b>Primary Use:</b> {p['uses'][0]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Full Details", key=f"det_{p['id']}"):
                            st.info(f"Full entry for {p['name']} is displayed in 'Identify Plant' after scanning.")

elif app_mode == "ℹ️ About System":
    st.markdown('<div class="header-text">Project Intelligence</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h3>AI-Powered Herbal Recognition</h3>
        <p>This system leverages <b>Deep Convolutional Neural Networks (MobileNetV2)</b> to automate the identification of medicinal flora. By training on high-resolution leaf datasets, we achieve clinical-grade accuracy in botanical classification.</p>
        <hr>
        <h4>System Architecture</h4>
        <ul>
            <li><b>Transfer Learning:</b> Pre-trained on ImageNet, fine-tuned on 100 medicinal species.</li>
            <li><b>Global Database:</b> Integrated JSON repository with multilingual metadata.</li>
            <li><b>Responsive Engine:</b> Optimized for both mobile and desktop browser deployment.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #1b5e20; font-weight: 600;'>🌿 EcoPlant v2.0 | Advanced Medicinal AI | © 2026</div>", unsafe_allow_html=True)
