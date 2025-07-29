# 🟢 EBE – Easy Broadcast Editor

EBE (Easy Broadcast Editor) is a desktop app + web overlay system that lets users create, style, and deploy live scoreboards powered by Google Sheets — without touching code.

This is the **centralized repo** that includes:
- `overlay/` → Live scoreboard HTML (deployed via GitHub Pages)
- `proxy/` → CORS-compatible data fetcher (deployed via Netlify)
- `gui/` → EBE desktop app (editable config, live preview, deploy buttons)

---

## 🚀 Features

✅ Live scoreboard powered by Google Sheets  
✅ Custom styling for font, colors, layout, and division names  
✅ Live HTML preview without pushing to production  
✅ One-click deploy to GitHub Pages and Netlify  
✅ Warning system for manual updates (Google Apps Script, sheet structure)  
🛠 Optional API integrations (future)

---

## 📁 Repo Structure

ebe-overlay/
├── overlay/ # GitHub Pages HTML overlay
│ └── index.html # Rendered scoreboard from config
│
├── proxy/ # Netlify CORS proxy for Google Apps Script
│ └── netlify.toml # Netlify settings
│ └── fetch.js # (or your current logic)
│
├── gui/ # Python desktop app (EBE)
│ ├── gui.py # GUI to configure overlay
│ ├── config.json # Style + layout options
│ ├── render.py # Jinja2 template renderer
│ └── template.html # HTML with {{ placeholders }}


---

## 🖥️ Running the GUI App

### 1. Clone this repo

```bash
git clone https://github.com/your-username/ebe-overlay.git
cd ebe-overlay/gui
```

### 2. Set up a Python environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```


### 3. Run the App
```bash
python gui.py
```

## 🛠 Deployment
GitHub Pages
The overlay/index.html is deployed using GitHub Pages

EBE pushes updates automatically if GitHub token or SSH is configured

Netlify
The proxy/ folder contains CORS logic deployed via Netlify

Manual or automatic deploy supported

## 🧠 Roadmap
 Template + config system

 GUI with live preview

 GitHub deploy integration

 Netlify deploy integration

 Google Apps Script helper

 Standalone installer packaging

## 📖 License
MIT or Custom — add your preferred license here.

## 🙋‍♀️ Maintainer
Created by Giulia Gallo – US National Champion & tech builder 💚
