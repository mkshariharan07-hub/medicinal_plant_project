# 🚀 QUICK START GUIDE FOR VS CODE

## Option 1: DEMO MODE (Test Without Training) ⚡
**Time: 15 minutes**

This lets you test the app immediately without training the ML model.

### Step 1: Install Software

**A. Check Python:**
```bash
python --version
# Should be 3.8+, if not install from python.org
```

**B. Install Flutter:**
- Windows: Download from https://docs.flutter.dev/get-started/install/windows
- Mac/Linux: 
  ```bash
  git clone https://github.com/flutter/flutter.git -b stable ~/flutter
  export PATH="$PATH:$HOME/flutter/bin"
  ```

**C. Verify:**
```bash
flutter doctor
```

### Step 2: Open in VS Code

1. **Install VS Code Extensions:**
   - Open Extensions (Ctrl+Shift+X)
   - Install: "Flutter" and "Dart"

2. **Open Project:**
   - File → Open Folder
   - Select `medicinal_plant_project`

### Step 3: Setup Demo Mode

**In VS Code Terminal (Ctrl+`):**

```bash
# Navigate to flutter app
cd flutter_app

# Copy database file
# Windows:
copy ..\dataset_info\medicinal_plants_database.json assets\

# Mac/Linux:
# cp ../dataset_info/medicinal_plants_database.json assets/

# Install dependencies
flutter pub get
```

### Step 4: Use Demo Classifier

**Edit `lib/providers/plant_provider.dart`:**

Change line 3 from:
```dart
import '../services/plant_classifier.dart';
```

To:
```dart
import '../services/plant_classifier_demo.dart';
```

And change line 6 from:
```dart
final PlantClassifier _classifier = PlantClassifier();
```

To:
```dart
final PlantClassifierDemo _classifier = PlantClassifierDemo();
```

### Step 5: Run the App

```bash
# In flutter_app folder
flutter run
```

**That's it! The app will run in demo mode!** 🎉

---

## Option 2: FULL VERSION (With ML Model) 🤖
**Time: 1-2 days (includes dataset collection & training)**

### Step 1: Collect Dataset

You need leaf images for 100 plants:

**Quick Option - Start with 10 plants:**
1. Create folders in `ml_model/data/train/`:
   - Neem, Tulsi, Mint, Aloe Vera, Moringa, Turmeric, Ginger, Curry Leaves, Betel, Nochi

2. Download 50-100 images per plant from Google Images

3. Create same folders in `ml_model/data/validation/` with 10-20 images each

### Step 2: Install ML Dependencies

```bash
cd ml_model
pip install tensorflow keras numpy matplotlib pillow
```

### Step 3: Train Model

```bash
python train_model.py
```

**Time:** 2-4 hours (GPU) or 8-12 hours (CPU)

### Step 4: Copy Model to App

```bash
# Windows:
copy medicinal_plant_model.tflite ..\flutter_app\assets\model\
copy class_indices.json ..\flutter_app\assets\model\

# Mac/Linux:
# cp medicinal_plant_model.tflite ../flutter_app/assets/model/
# cp class_indices.json ../flutter_app/assets/model/
```

### Step 5: Run Full App

```bash
cd ../flutter_app
flutter pub get
flutter run
```

---

## 📱 Running on Different Devices

### Android Emulator:
```bash
# Install Android Studio
# Create AVD (Virtual Device)
# Start emulator
flutter run
```

### Real Android Phone:
1. Enable Developer Options (tap Build Number 7 times)
2. Enable USB Debugging
3. Connect phone
4. `flutter run`

### Build APK:
```bash
flutter build apk --release
# APK at: build/app/outputs/flutter-apk/app-release.apk
```

---

## 🎯 Recommended Approach

**For Quick Testing:**
1. Use Demo Mode (Option 1)
2. Get familiar with the app
3. Test all features

**For Complete Project:**
1. Start with 10-20 plants
2. Train a smaller model
3. Test and verify
4. Expand to 100 plants later

---

## 🐛 Common Issues & Fixes

### Issue: "Flutter not found"
**Fix:**
```bash
# Windows: Add to PATH via Environment Variables
# Mac/Linux: Add to ~/.bashrc:
export PATH="$PATH:$HOME/flutter/bin"
source ~/.bashrc
```

### Issue: "Android licenses not accepted"
**Fix:**
```bash
flutter doctor --android-licenses
# Press 'y' for all
```

### Issue: "No devices found"
**Fix:**
```bash
# Start Android emulator or connect phone
flutter devices
```

### Issue: "Asset not found"
**Fix:**
```bash
# Make sure files are in correct location:
flutter_app/
  assets/
    model/
      medicinal_plant_model.tflite
      class_indices.json
    medicinal_plants_database.json
```

---

## 📋 Checklist

**Before Running:**
- [ ] Python installed
- [ ] Flutter installed
- [ ] VS Code extensions installed
- [ ] Android Studio installed
- [ ] Emulator created OR phone connected
- [ ] Database JSON in assets/
- [ ] `flutter pub get` completed

**Demo Mode Additional:**
- [ ] plant_classifier_demo.dart created
- [ ] plant_provider.dart updated to use demo

**Full Mode Additional:**
- [ ] Dataset collected
- [ ] Model trained
- [ ] TFLite files copied to assets/model/

---

## 🎓 VS Code Tips

**Useful Shortcuts:**
- `Ctrl+` ` → Open Terminal
- `Ctrl+Shift+P` → Command Palette
- `F5` → Run/Debug
- `Ctrl+C` → Stop running app

**Flutter Commands in VS Code:**
1. Press `Ctrl+Shift+P`
2. Type "Flutter"
3. See all available commands

**Hot Reload:**
- When app is running, press `r` in terminal
- Changes reflect immediately!

---

## 🎬 Video Tutorial Steps

**Record these for your presentation:**

1. **Open Project** (0:00-0:30)
   - Show VS Code
   - Show project structure

2. **Explain Code** (0:30-2:00)
   - ML model architecture
   - Flutter app structure

3. **Run Demo** (2:00-4:00)
   - Start app
   - Scan a leaf (use gallery image)
   - Show results
   - Browse library
   - Check history

4. **Show Code** (4:00-5:00)
   - Main features
   - ML integration
   - Database

---

## 🚀 Next Steps

1. **Start with Demo Mode** - Get app running
2. **Collect Small Dataset** - 10 plants first
3. **Train Small Model** - Verify pipeline works
4. **Expand Dataset** - Add more plants
5. **Re-train** - Final model with 100 plants
6. **Polish** - Add features, improve UI
7. **Document** - Screenshots, results
8. **Present** - Demo to staff

**Good luck! You've got this! 💪🌿**
