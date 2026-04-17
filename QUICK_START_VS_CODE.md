# 🚀 QUICK START GUIDE FOR VS CODE (STREAMLIT VERSION)

## ⚡ TEST THE APP IMMEDIATELY
**Time: 5 minutes**

This lets you test the web application with absolute minimal setup.

### Step 1: Install Python
- Ensure you have Python 3.9+ installed.
- Check version: `python --version`

### Step 2: Open in VS Code
1. **Open Project:**
   - File → Open Folder
   - Select `medicinal_plant_project`
2. **Install Extension:**
   - Open Extensions (Ctrl+Shift+X)
   - Install: "Python"

### Step 3: Install Dependencies
Open the VS Code Terminal (Ctrl+`) and run:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Web App
```bash
streamlit run app.py
```
The application will automatically open in your default web browser!

---

## 🤖 TRAINING THE ML MODEL (Advanced)
**Time: 2-4 hours (GPU recommended)**

If you want to re-train the model with your own dataset:

### Step 1: Prepare Your Data
1. Navigate to `ml_model/data/`
2. Create `train` and `validation` folders.
3. Inside each, create subfolders named after each plant (e.g., `Neem`, `Tulsi`, `Mint`).
4. Add 50-100 images per plant in the `train` folders.

### Step 2: Run Training Script
```bash
cd ml_model
python train_model.py
```
This will generate:
- `medicinal_plant_model.h5` (The full trained model)
- `class_indices.json` (The label mapping)

### Step 3: Deployment
To use your new model, move the generated files to the root directory or update the paths in `app.py`.

---

## ☁️ DEPLOYING TO THE CLOUD
**Time: 10 minutes**

### Via Streamlit Community Cloud (FREE)
1. **Upload to GitHub:** Push your project folder to a GitHub repository.
2. **Connect to Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Select your Repository, Branch, and `app.py` as the Main file path.
3. **Deploy!** Your app will be live at a public URL (e.g., `medicinal-plant-identifier.streamlit.app`).

---

## 🐛 COMMON ISSUES & FIXES

### Issue: "Streamlit command not found"
**Fix:** Ensure your python site-packages folder is in your system PATH, or use:
```bash
python -m streamlit run app.py
```

### Issue: "Model file not found"
**Fix:** The `app.py` script looks for the model in the root or `ml_model/` folder. Ensure the `.h5` file exists.

---

## 🎓 VS CODE SHORTCUTS
- `Ctrl + ` ` → Open/Close Terminal
- `Ctrl + Shift + P` → Command Palette (Type "Python: Select Interpreter" to ensure you're using the right version)
- `F5` → Run/Debug
- `Ctrl + C` → Stop the Streamlit server in the terminal

---

🎊 **Happy Coding!** 🎊
