import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
from PIL import Image
import os
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Medicinal Plant Identifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        background-image: linear-gradient(135deg, #f5f7f9 0%, #e0e8ee 100%);
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7d32, #1b5e20);
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #388e3c;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .result-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #2e7d32;
    }
    .plant-header {
        color: #2e7d32;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .scientific-name {
        font-style: italic;
        color: #558b2f;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
    }
    .section-title {
        color: #2e7d32;
        font-weight: bold;
        margin-top: 1rem;
        border-bottom: 1px solid #ddd;
        padding-bottom: 0.2rem;
    }
    .confidence-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .info-label {
        font-weight: bold;
        color: #333;
    }
</style>
""", unsafe_content_allowed=True)

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
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_data
def load_database(db_path):
    try:
        with open(db_path, 'r') as f:
            data = json.load(f)
        return data['medicinal_plants_database']
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return []

# Paths
MODEL_PATH = os.path.join('ml_model', 'medicinal_plant_model.h5')
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = 'medicinal_plant_model.h5' # Fallback to root

INDICES_PATH = os.path.join('ml_model', 'class_indices.json')
if not os.path.exists(INDICES_PATH):
    INDICES_PATH = 'class_indices.json' # Fallback to root

DB_PATH = os.path.join('dataset_info', 'medicinal_plants_database.json')

# Load Model and Data
predictor_data = load_predictor(MODEL_PATH, INDICES_PATH)
plant_db = load_database(DB_PATH)

# App Sidebar
st.sidebar.image("https://img.icons8.com/color/96/000000/leaf.png", width=100)
st.sidebar.title("🌿 EcoPlant")
st.sidebar.markdown("---")
st.sidebar.info(
    "Identify medicinal plants instantly using Artificial Intelligence. "
    "Our model is trained on 100 different plant species with 95% accuracy."
)

app_mode = st.sidebar.selectbox("Navigate", ["Identify Plant", "Plant Library", "About"])

if app_mode == "Identify Plant":
    st.title("🌿 Medicinal Plant Identity")
    st.markdown("Upload a clear photo of a plant leaf to identify it and learn about its medicinal properties.")

    if predictor_data is None:
        st.warning("⚠️ ML Model files not found. Please ensure 'medicinal_plant_model.h5' and 'class_indices.json' are in the root or 'ml_model' folder.")
        st.info("You can still browse the Plant Library.")
    else:
        model, class_names = predictor_data
        
        uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                image = Image.open(uploaded_file).convert('RGB')
                st.image(image, caption='Uploaded Leaf', use_column_width=True)
            
            with col2:
                with st.spinner('Analysing leaf patterns...'):
                    # Preprocess
                    img = image.resize((224, 224))
                    img_array = np.array(img) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    
                    # Predict
                    predictions = model.predict(img_array, verbose=0)
                    top_idx = np.argmax(predictions[0])
                    confidence = predictions[0][top_idx]
                    
                    # Map to class name
                    # Handle indices as strings in JSON
                    plant_name = class_names.get(str(top_idx), class_names.get(top_idx, "Unknown"))
                    
                    st.success(f"Identification Complete!")
                    st.metric("Top Match", plant_name, f"{confidence*100:.2f}% Confidence")
                    
                    # Progress bar for confidence
                    st.progress(float(confidence))

            # Find in Database
            plant_info = next((p for p in plant_db if p['name'].lower() == plant_name.lower()), None)
            
            if plant_info:
                st.markdown("---")
                st.markdown(f'<div class="plant-header">{plant_info["name"]}</div>', unsafe_content_allowed=True)
                st.markdown(f'<div class="scientific-name">{plant_info["scientific_name"]}</div>', unsafe_content_allowed=True)
                
                tab1, tab2, tab3 = st.tabs(["Medicinal Uses", "Preparation & Dosage", "Local Names"])
                
                with tab1:
                    st.markdown('<div class="section-title">Medicinal Uses</div>', unsafe_content_allowed=True)
                    for use in plant_info['uses']:
                        st.markdown(f"- {use}")
                    
                    st.markdown('<div class="section-title">Precautions</div>', unsafe_content_allowed=True)
                    st.warning(plant_info['precautions'])
                
                with tab2:
                    st.markdown('<div class="section-title">Preparation Method</div>', unsafe_content_allowed=True)
                    st.info(plant_info['preparation'])
                    
                    st.markdown('<div class="section-title">Recommended Dosage</div>', unsafe_content_allowed=True)
                    st.success(plant_info['dosage'])
                
                with tab3:
                    st.markdown('<div class="section-title">Regional Names</div>', unsafe_content_allowed=True)
                    for lang, name in plant_info['local_names'].items():
                        st.markdown(f"**{lang.capitalize()}**: {name}")
            else:
                st.info(f"Identified as **{plant_name}**, but detailed info is missing from the database.")

elif app_mode == "Plant Library":
    st.title("📚 Medicinal Plant Library")
    st.markdown("Browse our database of 100 medicinal plants.")
    
    search_query = st.text_input("Search plants by name or scientific name...", "")
    
    filtered_plants = [p for p in plant_db if search_query.lower() in p['name'].lower() or search_query.lower() in p['scientific_name'].lower()]
    
    if not filtered_plants:
        st.write("No plants found matching your search.")
    else:
        # Display as cards in a grid
        cols = st.columns(3)
        for i, plant in enumerate(filtered_plants):
            with cols[i % 3]:
                with st.expander(f"🌿 {plant['name']}"):
                    st.markdown(f"**Scientific Name:** *{plant['scientific_name']}*")
                    st.markdown("**Primary Uses:**")
                    for use in plant['uses'][:3]:
                        st.markdown(f"- {use}")
                    if st.button(f"View Details", key=f"btn_{plant['id']}"):
                        st.session_state.selected_plant = plant
                        # We can redirect or show details in a modal/sidebar if needed
                        # For now, just show a message or expand info
                        st.info(f"Navigate to 'Identify' and upload an image to see full AI details, or click 'View Details' to see full text info below.")

elif app_mode == "About":
    st.title("About the Project")
    st.markdown("""
    ### 🌿 Medicinal Plant Identification System
    This project uses Deep Learning to bridge the gap between traditional herbal knowledge and modern technology.
    
    #### Technologies Used:
    - **Frontend:** Streamlit (Python)
    - **Machine Learning:** TensorFlow, Keras (MobileNetV2)
    - **Dataset:** 100 Species of Western Ghats & Indian Medicinal Plants
    - **Accuracy:** ~95% Training Accuracy
    
    #### Developers:
    - Developed for College Mini Project / Research Application.
    
    #### Disclaimer:
    This application is for educational and identification purposes only. Always consult with a qualified Ayurvedic practitioner or medical professional before using any medicinal plants for treatment.
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #777;'>© 2026 Medicinal Plant AI Identification System | Built with ❤️ using Streamlit</div>", unsafe_content_allowed=True)
