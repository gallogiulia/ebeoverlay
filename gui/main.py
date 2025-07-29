import sys
import json
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog, QMessageBox
)
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
        self.setFixedSize(440, 390)

        layout = QVBoxLayout()

        # Explanatory intro
        intro = QLabel(
            "👋 Welcome to EBE\n\n"
            "This app helps you build live scoreboard overlays.\n\n"
            "🆕 Create New Overlay: Creates a starter config.json (future version will allow GUI-based overlay creation).\n"
            "📁 Upload scores.json: Import a scores file. You'll need to reopen the Editor to apply it.\n"
            "🎨 Open Editor: Opens the current editor using config.json and scores.json from this folder."
        )
        intro.setFont(QFont("Segoe UI", 9))
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self.create_btn = QPushButton("🆕 Create New Overlay")
        self.create_btn.clicked.connect(self.create_new_overlay)
        layout.addWidget(self.create_btn)

        self.upload_btn = QPushButton("📁 Upload scores.json")
        self.upload_btn.clicked.connect(self.upload_scores)
        layout.addWidget(self.upload_btn)

        self.editor_btn = QPushButton("🎨 Open Editor")
        self.editor_btn.clicked.connect(self.open_editor)
        layout.addWidget(self.editor_btn)

        self.exit_btn = QPushButton("❌ Exit")
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

    def create_new_overlay(self):
        with open("config.json", "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        QMessageBox.information(
            self,
            "Overlay Created",
            "✅ A new config.json has been created in this folder.\n\n"
            "You can now click 'Open Editor' to customize it."
        )

    def upload_scores(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select scores.json", "", "JSON files (*.json)")
        if file_path:
            with open(file_path, "r") as src, open("scores.json", "w") as dest:
                dest.write(src.read())
            QMessageBox.information(
                self,
                "Scores Uploaded",
                "✅ scores.json has been uploaded.\n\n"
                "Please reopen the editor to see the updated scores."
            )

    def open_editor(self):
        if os.path.exists("gui.py"):
            subprocess.Popen(["python", "gui.py"])
        else:
            QMessageBox.critical(self, "Error", "❌ gui.py not found in this folder!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LandingScreen()
    window.show()
    sys.exit(app.exec())
