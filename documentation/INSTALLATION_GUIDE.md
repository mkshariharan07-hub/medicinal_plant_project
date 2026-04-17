# INSTALLATION & SETUP GUIDE

## Step-by-Step Installation

### PART 1: Python & ML Setup (15-30 minutes)

#### 1. Install Python
```bash
# Check if Python is installed
python --version  # Should be 3.8 or higher

# If not installed, download from python.org
```

#### 2. Install ML Dependencies
```bash
cd ml_model
pip install -r requirements.txt --break-system-packages

# Verify installation
python -c "import tensorflow as tf; print(tf.__version__)"
```

### PART 2: Flutter Setup (30-45 minutes)

#### 1. Install Flutter

**Linux/Mac:**
```bash
# Download Flutter
git clone https://github.com/flutter/flutter.git -b stable ~/flutter

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$HOME/flutter/bin"

# Verify
flutter doctor
```

**Windows:**
1. Download Flutter SDK from flutter.dev
2. Extract to C:\src\flutter
3. Add to PATH: C:\src\flutter\bin
4. Run `flutter doctor` in cmd

#### 2. Install Android Studio

1. Download from developer.android.com/studio
2. Install Android SDK
3. Accept licenses:
   ```bash
   flutter doctor --android-licenses
   ```
4. Create an AVD (Android Virtual Device)

### PART 3: Project Setup (10 minutes)

#### 1. Prepare Model Files
```bash
# Train the model first (or use pre-trained)
cd ml_model
python train_model.py

# Files generated:
# - medicinal_plant_model.tflite
# - class_indices.json
```

#### 2. Setup Flutter Project
```bash
cd ../flutter_app

# Copy model files
cp ../ml_model/medicinal_plant_model.tflite assets/model/
cp ../ml_model/class_indices.json assets/model/
cp ../dataset_info/medicinal_plants_database.json assets/

# Install dependencies
flutter pub get
```

#### 3. Run the App
```bash
# Check connected devices
flutter devices

# Run on emulator/device
flutter run

# Or build APK
flutter build apk --release
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] TensorFlow installed successfully
- [ ] Flutter SDK installed
- [ ] Android Studio setup complete
- [ ] Model files in assets/model/
- [ ] Database JSON in assets/
- [ ] `flutter doctor` shows no errors
- [ ] App runs successfully

## Common Issues & Solutions

### Issue 1: TensorFlow Installation Fails
**Solution:**
```bash
# Try with specific version
pip install tensorflow==2.13.0 --break-system-packages

# Or use conda
conda install tensorflow
```

### Issue 2: Flutter Doctor Shows Errors
**Solution:**
```bash
# Android licenses
flutter doctor --android-licenses

# Update Flutter
flutter upgrade

# Clear cache
flutter clean
```

### Issue 3: Model Files Not Found
**Solution:**
```bash
# Verify file locations
ls -la flutter_app/assets/model/

# Should show:
# - medicinal_plant_model.tflite
# - class_indices.json

# Check pubspec.yaml asset paths
```

### Issue 4: Camera Permission Denied
**Solution:**
Edit `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

### Issue 5: Build Fails
**Solution:**
```bash
flutter clean
flutter pub get
flutter pub upgrade
flutter build apk
```

## Dataset Collection Tips

### Where to Get Leaf Images:

1. **Your Own Collection**
   - Use smartphone camera
   - Take 50-100 images per plant
   - Various lighting conditions
   - Different angles

2. **Online Sources**
   - Kaggle datasets
   - Google Images (check licenses)
   - PlantNet database
   - iNaturalist

3. **Image Requirements**
   - Minimum 224x224 pixels
   - JPG or PNG format
   - Clear, focused images
   - Variety of backgrounds

### Dataset Organization:

```
data/
├── train/
│   ├── Neem/
│   │   ├── neem_001.jpg
│   │   ├── neem_002.jpg
│   │   └── ... (50+ images)
│   ├── Tulsi/
│   │   └── ... (50+ images)
│   └── ... (98 more folders)
└── validation/
    ├── Neem/
    │   └── ... (10+ images)
    └── ...
```

## Time Estimates

| Task | Time Required |
|------|---------------|
| Python setup | 10 min |
| Flutter setup | 30 min |
| Dataset collection | 5-10 hours |
| Model training | 2-4 hours (GPU) / 8-12 hours (CPU) |
| App development | Already complete! |
| Testing | 1-2 hours |
| **Total** | **1-2 days** |

## Hardware Requirements

### Minimum:
- 4GB RAM
- 20GB free disk space
- Intel Core i3 or equivalent
- Integrated graphics

### Recommended:
- 8GB+ RAM
- 50GB free disk space
- Intel Core i5/i7 or equivalent
- NVIDIA GPU (for training)

## Next Steps After Installation

1. **Collect/Download Dataset** (if training from scratch)
2. **Train Model** or use pre-trained weights
3. **Test Model** with sample images
4. **Run Flutter App**
5. **Test on Real Device**
6. **Build Release APK**
7. **Document Results** for project report

## Getting Help

If you encounter issues:

1. Check the COMPLETE_GUIDE.md
2. Read error messages carefully
3. Google the specific error
4. Check Flutter documentation
5. Stack Overflow (flutter, tensorflow tags)

## Success Indicators

You'll know setup is successful when:

✅ `flutter doctor` shows all green checkmarks
✅ Model training completes without errors
✅ App runs on emulator/device
✅ Camera opens and captures images
✅ Plant identification works
✅ Results display correctly

Good luck! 🍀
