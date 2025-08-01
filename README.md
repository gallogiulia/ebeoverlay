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

---

## 🏆 Nationals Overlay Workflow

EBE now supports both **Playdowns** and **Nationals** overlays!

### 📋 How to Use the Nationals Editor

1. **🏆 Build Nationals Overlay**  
   Launch the Nationals Score Editor to create your `scores.json` file with all the inter-division matches.

2. **⚙️ Generate Nationals Config from Scores**  
   Parses the `scores.json`, extracts sections/divisions, and generates a valid `config.json`.

3. **🎨 Open Editor**  
   Launch the visual editor to style your overlay and preview live changes.

### 🧠 Tips & Guidance

- Each Nationals match is between two divisions (e.g. Central vs Northeast).
- You must complete the `scores.json` before generating the `config.json`.
- Once you’ve edited and rendered, your overlay (`output.html`) will be ready to publish or upload.

---

## 🔁 Navigation Tips

- All overlay tools now feature a **⬅️ Return to Main Menu** button.
- The main screen is divided into **Playdowns** and **Nationals** sections for clarity.

---

## 🖥️ Main Screen Buttons (New)

| Button | Purpose |
|--------|---------|
| 🆕 Create New Overlay | Resets `config.json` to default |
| 📁 Upload scores.json | Imports a scores structure file |
| 🏆 Build Nationals Overlay | Launch guided input for Nationals games |
| ⚙️ Generate Nationals Config | Builds `config.json` from the scores |
| 🎨 Open Editor | Customize and preview |
| ❌ Exit | Close the app |


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

### GitHub Pages
The overlay/index.html is deployed using GitHub Pages. EBE pushes updates automatically if GitHub token or SSH is configured

### Netlify 🌐 Netlify (CORS Proxy)
The proxy/ folder contains a simple CORS proxy that fetches JSON data from your deployed Google Apps Script and makes it readable for GitHub Pages (or any browser-based frontend).

#### 📦 Setup (First Time)

##### 1. Navigate to the folder:
```bash
cd proxy
```

##### 2. Install dependencies (if not done yet):
```bash
npm install
```
This installs:
- node-fetch – for making HTTP requests
- netlify-cli – for local dev and deploy (from devDependencies)

##### 3. Authenticate with Netlify (first time only):
```bash
npx netlify login
```
#### 🚀 Deploy to Netlify
To deploy your CORS proxy:
```bash
npm run deploy
```
This is a shortcut for:
```bash
npx netlify deploy --dir=. --prod
```

#### 🔁 Linking the Proxy to Your Overlay
In your overlay/index.html, make sure the fetch URL uses the Netlify-deployed CORS URL, like:
```js
const response = await fetch("https://your-netlify-url.netlify.app/your-endpoint");
```


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
