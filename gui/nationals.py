import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QLineEdit, QColorDialog, QComboBox, QTextEdit,
    QFileDialog, QMessageBox, QGroupBox, QGridLayout
)
import subprocess

from PyQt5.QtGui import QFont

CONFIG_FILE = "nationals/config.json"
SCORES_FILE = "nationals/scores.json"


class NationalsOverlayEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EBE – Nationals Overlay Editor")
        self.setMinimumSize(600, 500)

        self.config = {}
        self.scores = {}

        self.layout = QVBoxLayout()

        self.load_files()
        self.build_ui()

    def load_files(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.config = json.load(f)
        else:
            QMessageBox.warning(self, "Warning", f"{CONFIG_FILE} not found.")

        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as f:
                self.scores = json.load(f)
        else:
            QMessageBox.warning(self, "Warning", f"{SCORES_FILE} not found.")

    def build_ui(self):
        # Font settings
        self.layout = QVBoxLayout()
        font_box = QGroupBox("Font Settings")
        font_layout = QHBoxLayout()
        font_box.setLayout(font_layout)


        self.font_size_input = QLineEdit(str(self.config.get("font_size", 14)))
        self.font_family_input = QLineEdit(self.config.get("font_family", "Segoe UI"))
        font_layout.addWidget(QLabel("Font Size:"))
        font_layout.addWidget(self.font_size_input)
        font_layout.addWidget(QLabel("Font Family:"))
        font_layout.addWidget(self.font_family_input)

        # Division colors
        div_box = QGroupBox("Division Background Colors")
        div_layout = QGridLayout()
        div_box.setLayout(div_layout)

        self.division_inputs = {}
        for idx, div in enumerate(self.config.get("divisions", [])):
            color_btn = QPushButton(self.config.get(f"div{idx+1}_bg", "#cccccc"))
            color_btn.clicked.connect(lambda _, b=color_btn: self.choose_color(b))
            self.division_inputs[div] = color_btn
            div_layout.addWidget(QLabel(div), idx, 0)
            div_layout.addWidget(color_btn, idx, 1)

        # Scores viewer (not editable for now)
        scores_box = QGroupBox("Scores (View Only)")
        scores_layout = QVBoxLayout()
        scores_box.setLayout(scores_layout)
        label = QLabel("📋 Game Preview")
        label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.layout.addWidget(label)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont("Courier", 10))
        scores_layout.addWidget(self.preview)
        self.load_scores_preview()

        # Save button
        save_btn = QPushButton("💾 Save Changes")
        save_btn.clicked.connect(self.save_changes)


        # Add to layout
        self.layout.addWidget(font_box)
        self.layout.addWidget(div_box)
        self.layout.addWidget(scores_box)
        self.layout.addWidget(save_btn)

        # Go Back to Main Screen
        back_btn = QPushButton("⬅️ Return to Main Menu")
        back_btn.clicked.connect(self.go_back_to_main)
        self.layout.addWidget(back_btn)
        self.setLayout(self.layout)



    def choose_color(self, btn):
        color = QColorDialog.getColor()
        if color.isValid():
            btn.setText(color.name())
            btn.setStyleSheet(f"background-color: {color.name()};")

    def load_scores_preview(self):
        self.preview.clear()
        if not self.scores:
            self.preview.append("No scores available.")
            return

        for game in self.scores:
            div1 = game.get("division1", "Unknown")
            div2 = game.get("division2", "Unknown")
            match = game.get("match", "Match")
            ends = game.get("ends", "–")
            score1 = game.get("score1", "–")
            score2 = game.get("score2", "–")

            self.preview.append(
                f"<b>{div1} vs {div2}</b><br>{match} – Ends: {ends} | Score: {score1} - {score2}<br><br>"
            )



    def save_changes(self):
        self.config["font_size"] = int(self.font_size_input.text())
        self.config["font_family"] = self.font_family_input.text()
        for idx, (div, btn) in enumerate(self.division_inputs.items()):
            self.config[f"div{idx+1}_bg"] = btn.text()

        with open(CONFIG_FILE, "w") as f:
            os.makedirs("nationals", exist_ok=True)
            json.dump(self.config, f, indent=2)

        QMessageBox.information(self, "Saved", "✅ config.json saved successfully!")

    

    def go_back_to_main(self):
        self.close()
        subprocess.Popen(["python", "main.py"])

if __name__ == "__main__":
    app = QApplication([])
    editor = NationalsOverlayEditor()
    editor.show()
    app.exec()
