import sys
import json
import subprocess
import os
import sys


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog, QMessageBox, QGroupBox,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFont

DEFAULT_CONFIG = {
    "font_size": 14,
    "font_family": "Segoe UI",
    "score1_color": "#cc0000",
    "score2_color": "#0055cc",
    "score1_bg": "#ffffff",
    "score2_bg": "#ffffff",
    "ends_bg": "#f0f0f0",
    "score1_font_color": "#ffffff",
    "score2_font_color": "#ffffff",
    "ends_font_color": "#000000",
    "stars_bg": "#333399",
    "stripes_bg": "#cc3333",
    "col1_width": "120px",
    "col2_width": "40px",
    "col3_width": "60px",
    "col4_width": "60px",
    "google_apps_script_url": "https://ebeoverlay.netlify.app/.netlify/functions/scores",
    "division1_name": "Stars",
    "division2_name": "Stripes",
    "div1_bg": "#333399",
    "div2_bg": "#cc3333",
    "divisions": ["Stars", "Stripes"]
}


class LandingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Easy Broadcast Editor (EBE)")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        title = QLabel("🎬 Easy Broadcast Editor (EBE)")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #333333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)


        intro = QLabel("👋 Welcome to EBE\n\nThis app helps you build live scoreboard overlays.")
        intro.setFont(QFont("Segoe UI", 11))
        intro.setWordWrap(True)
        layout.addWidget(intro)

        # 👉 Playdowns Section
        playdowns_box = QGroupBox("🏅 Playdowns Tools")
        playdowns_layout = QVBoxLayout()
        self.create_btn = QPushButton("🆕 Create New Overlay")
        self.create_btn.clicked.connect(self.create_new_overlay)
        playdowns_layout.addWidget(self.create_btn)

        self.upload_btn = QPushButton("📁 Upload scores.json")
        self.upload_btn.clicked.connect(self.upload_scores)
        playdowns_layout.addWidget(self.upload_btn)

        self.editor_btn = QPushButton("🎨 Open Editor")
        self.editor_btn.clicked.connect(self.open_editor)
        playdowns_layout.addWidget(self.editor_btn)
        playdowns_box.setLayout(playdowns_layout)
        layout.addWidget(playdowns_box)

        # Spacer
        layout.addSpacing(10)

        # 👉 Nationals Section
        nationals_box = QGroupBox("🏆 Nationals Tools")
        nationals_layout = QVBoxLayout()
        self.nat_score_btn = QPushButton("🧾 Build Nationals Overlay")
        self.nat_score_btn.clicked.connect(self.build_nationals_scores)
        nationals_layout.addWidget(self.nat_score_btn)

        self.nat_cfg_btn = QPushButton("Generate Nationals Config from Scores")
        self.nat_cfg_btn.clicked.connect(self.generate_nationals_config)
        nationals_layout.addWidget(self.nat_cfg_btn)

        self.nat_editor_btn = QPushButton("🛠️ Open Nationals Overlay Editor")
        self.nat_editor_btn.clicked.connect(self.open_nationals_editor)
        nationals_layout.addWidget(self.nat_editor_btn)
        nationals_box.setLayout(nationals_layout)
        layout.addWidget(nationals_box)

        # Spacer
        layout.addSpacing(20)

        # ❌ Exit
        self.exit_btn = QPushButton("❌ Exit")
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)


        # Dark Mode Toggle
        self.darkmode_btn = QPushButton("🌙 Toggle Dark Mode")
        self.darkmode_btn.clicked.connect(self.toggle_dark_mode)
        layout.addWidget(self.darkmode_btn)

        self.setStyleSheet("""
    QWidget {
        background-color: #f6f8fa;
    }
    QGroupBox {
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        border-radius: 12px;
        margin-top: 20px;
        padding: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 3px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px;
        font-size: 13px;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #388e3c;
    }
""")

        self.setLayout(layout)


    def generate_nationals_config(self):
        try:
            with open("scores.json") as f:
                scores = json.load(f)
            
            sections = {}
            for match in scores:
                sec1 = match.get("division1")
                sec2 = match.get("division2")
                sections.setdefault("Section1", set()).add(sec1)
                sections.setdefault("Section2", set()).add(sec2)

            divisions = list(sections["Section1"]) + list(sections["Section2"])
            config = DEFAULT_CONFIG.copy()
            config["division1_name"] = "Section1"
            config["division2_name"] = "Section2"
            config["div1_bg"] = "#003399"
            config["div2_bg"] = "#990000"
            config["divisions"] = divisions

            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)

            QMessageBox.information(self, "EBE", "✅ config.json generated from scores.json!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Failed to generate config.json\n{str(e)}")

    def create_new_overlay(self):
        os.makedirs("playdowns", exist_ok=True)
        with open("playdowns/config.json", "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)

        QMessageBox.information(self, "EBE", "✅ New overlay config.json created!")

    def upload_scores(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select scores.json", "", "JSON files (*.json)")
        if file_path:

            with open(file_path, "r") as src, open("playdowns/scores.json", "w") as dest:

                dest.write(src.read())
            QMessageBox.information(self, "EBE", "✅ scores.json uploaded!")

    def open_editor(self):
        if os.path.exists("gui.py"):
            subprocess.Popen(["python", "gui.py", "playdowns"])
        else:
            QMessageBox.critical(self, "Error", "❌ gui.py not found!")

    def launch_nationals(self):
        if os.path.exists("nationals.py"):
            subprocess.Popen(["python", "nationals.py"])
        else:
            QMessageBox.critical(self, "Error", "❌ nationals.py not found!")

    def create_scores(self):
        if os.path.exists("scores_editor.py"):
            subprocess.Popen(["python", "scores_editor.py"])
        else:
            QMessageBox.critical(self, "Error", "❌ scores_editor.py not found!")


    def launch_builder(self):
        if os.path.exists("wizard.py"):
            subprocess.Popen(["python", "wizard.py"])
        else:
            QMessageBox.critical(self, "Error", "❌ wizard.py not found!")

    def build_nationals_scores(self):
        subprocess.Popen(["python", "wizard.py"])

    def generate_nationals_config(self):
        subprocess.Popen(["python", "scores_editor.py"])

    def open_nationals_editor(self):
        subprocess.Popen(["python", "nationals.py"])
    
    def toggle_dark_mode(self):
        dark_palette = self.palette()
        dark_palette.setColor(self.backgroundRole(), Qt.black)
        dark_palette.setColor(self.foregroundRole(), Qt.white)
        self.setPalette(dark_palette)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LandingScreen()
    window.show()
    sys.exit(app.exec())
