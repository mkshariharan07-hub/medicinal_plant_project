"""
Prediction script for testing the trained model
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import json
from PIL import Image
import matplotlib.pyplot as plt

class PlantPredictor:
    def __init__(self, model_path, class_indices_path):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to trained model (.h5 file)
            class_indices_path: Path to class indices JSON
        """
        self.model = keras.models.load_model(model_path)
        
        with open(class_indices_path, 'r') as f:
            self.class_names = json.load(f)
        
        self.img_size = 224
        
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        # Load and resize image
        img = Image.open(image_path).convert('RGB')
        img = img.resize((self.img_size, self.img_size))
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array, img
    
    def predict(self, image_path, top_k=5):
        """
        Predict plant species from image
        
        Args:
            image_path: Path to leaf image
            top_k: Number of top predictions to return
            
        Returns:
            List of tuples (class_name, probability)
        """
        # Preprocess image
        img_array, original_img = self.preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(img_array, verbose=0)
        
        # Get top K predictions
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            class_name = self.class_names[str(idx)]
            probability = predictions[0][idx]
            results.append((class_name, probability))
        
        return results, original_img
    
    def visualize_prediction(self, image_path, save_path='prediction_result.png'):
        """Visualize prediction with image and top predictions"""
        results, img = self.predict(image_path, top_k=5)
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Display image
        ax1.imshow(img)
        ax1.axis('off')
        ax1.set_title('Input Image', fontsize=14, fontweight='bold')
        
        # Display predictions
        plants = [r[0] for r in results]
        probabilities = [r[1] * 100 for r in results]
        colors = ['#2ecc71' if i == 0 else '#3498db' for i in range(len(plants))]
        
        bars = ax2.barh(range(len(plants)), probabilities, color=colors)
        ax2.set_yticks(range(len(plants)))
        ax2.set_yticklabels(plants)
        ax2.set_xlabel('Confidence (%)', fontsize=12)
        ax2.set_title('Top 5 Predictions', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 100)
        
        # Add percentage labels
        for i, (bar, prob) in enumerate(zip(bars, probabilities)):
            ax2.text(prob + 1, i, f'{prob:.1f}%', 
                    va='center', fontsize=10, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Prediction visualization saved to {save_path}")
        
        # Print results
        print(f"\n{'='*60}")
        print(f"PREDICTION RESULTS")
        print(f"{'='*60}")
        for i, (plant, prob) in enumerate(results, 1):
            print(f"{i}. {plant}: {prob*100:.2f}%")
        print(f"{'='*60}\n")
        
        return results


# Example usage
if __name__ == "__main__":
    # Initialize predictor
    predictor = PlantPredictor(
        model_path='medicinal_plant_model.h5',
        class_indices_path='class_indices.json'
    )
    
    # Test prediction (replace with your test image path)
    test_image = 'test_leaf.jpg'
    
    try:
        results = predictor.visualize_prediction(test_image)
        
        # Get the top prediction
        top_plant, confidence = results[0]
        
        print(f"\n✓ The leaf is identified as: {top_plant}")
        print(f"  Confidence: {confidence*100:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure you have a test image at the specified path")
