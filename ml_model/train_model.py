"""
Medicinal Plant Leaf Classification Model
This script trains a CNN model to identify 100 different medicinal plant leaves
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
NUM_CLASSES = 100  # 100 different medicinal plants

class MedicinalPlantClassifier:
    def __init__(self, data_dir, num_classes=100):
        """
        Initialize the classifier
        
        Args:
            data_dir: Path to dataset directory with train/validation subdirectories
            num_classes: Number of plant species to classify
        """
        self.data_dir = data_dir
        self.num_classes = num_classes
        self.model = None
        self.history = None
        
    def create_data_generators(self):
        """Create data augmentation and generators for training"""
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Load training data
        self.train_generator = train_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'train'),
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        # Load validation data
        self.validation_generator = val_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'validation'),
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical'
        )
        
        # Save class indices for later use
        self.class_indices = self.train_generator.class_indices
        self.class_names = {v: k for k, v in self.class_indices.items()}
        
        return self.train_generator, self.validation_generator
    
    def build_model(self):
        """Build CNN model using transfer learning with MobileNetV2"""
        # Load pre-trained MobileNetV2 (without top layer)
        base_model = MobileNetV2(
            input_shape=(IMG_SIZE, IMG_SIZE, 3),
            include_top=False,
            weights='imagenet'
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Build model
        self.model = keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.5),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'top_k_categorical_accuracy']
        )
        
        return self.model
    
    def train(self, epochs=EPOCHS):
        """Train the model"""
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                'best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        self.history = self.model.fit(
            self.train_generator,
            validation_data=self.validation_generator,
            epochs=epochs,
            callbacks=callbacks
        )
        
        return self.history
    
    def fine_tune(self, epochs=20):
        """Fine-tune the model by unfreezing some layers"""
        # Unfreeze the base model
        base_model = self.model.layers[0]
        base_model.trainable = True
        
        # Freeze all layers except the last 20
        for layer in base_model.layers[:-20]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=1e-5),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'top_k_categorical_accuracy']
        )
        
        # Continue training
        history_fine = self.model.fit(
            self.train_generator,
            validation_data=self.validation_generator,
            epochs=epochs,
            callbacks=[
                keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                keras.callbacks.ModelCheckpoint('best_model_finetuned.h5', save_best_only=True)
            ]
        )
        
        return history_fine
    
    def save_model(self, model_path='medicinal_plant_model.h5', 
                   tflite_path='medicinal_plant_model.tflite'):
        """Save model in H5 and TFLite formats"""
        # Save full model
        self.model.save(model_path)
        print(f"Model saved to {model_path}")
        
        # Convert to TFLite for mobile deployment
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()
        
        with open(tflite_path, 'wb') as f:
            f.write(tflite_model)
        print(f"TFLite model saved to {tflite_path}")
        
        # Save class indices
        with open('class_indices.json', 'w') as f:
            json.dump(self.class_names, f, indent=2)
        print("Class indices saved to class_indices.json")
    
    def plot_training_history(self):
        """Plot training history"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        axes[0].plot(self.history.history['accuracy'], label='Train Accuracy')
        axes[0].plot(self.history.history['val_accuracy'], label='Val Accuracy')
        axes[0].set_title('Model Accuracy')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot loss
        axes[1].plot(self.history.history['loss'], label='Train Loss')
        axes[1].plot(self.history.history['val_loss'], label='Val Loss')
        axes[1].set_title('Model Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        print("Training history saved to training_history.png")
        
    def evaluate(self):
        """Evaluate model on validation data"""
        results = self.model.evaluate(self.validation_generator)
        print(f"\nValidation Accuracy: {results[1]*100:.2f}%")
        print(f"Top-5 Accuracy: {results[2]*100:.2f}%")
        return results


# Main execution
if __name__ == "__main__":
    # Initialize classifier
    # NOTE: You need to organize your dataset in the following structure:
    # data/
    #   train/
    #     plant_name_1/
    #       image1.jpg
    #       image2.jpg
    #     plant_name_2/
    #       ...
    #   validation/
    #     plant_name_1/
    #       ...
    
    DATA_DIR = "data"  # Change this to your dataset path
    
    print("Initializing Medicinal Plant Classifier...")
    classifier = MedicinalPlantClassifier(DATA_DIR, num_classes=100)
    
    print("\nCreating data generators...")
    train_gen, val_gen = classifier.create_data_generators()
    
    print(f"\nFound {len(classifier.class_indices)} plant classes")
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")
    
    print("\nBuilding model...")
    model = classifier.build_model()
    model.summary()
    
    print("\nStarting training...")
    history = classifier.train(epochs=EPOCHS)
    
    print("\nFine-tuning model...")
    classifier.fine_tune(epochs=20)
    
    print("\nEvaluating model...")
    classifier.evaluate()
    
    print("\nSaving model...")
    classifier.save_model()
    
    print("\nPlotting training history...")
    classifier.plot_training_history()
    
    print("\n✓ Training completed successfully!")
    print("Files generated:")
    print("  - medicinal_plant_model.h5 (Full Keras model)")
    print("  - medicinal_plant_model.tflite (TFLite model for Flutter)")
    print("  - class_indices.json (Class names mapping)")
    print("  - training_history.png (Training plots)")
