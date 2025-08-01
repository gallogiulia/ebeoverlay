import json
import os
import sys

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QColorDialog, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog
)
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from render import render_template
from PyQt5.QtWidgets import QComboBox

overlay_type = sys.argv[1] if len(sys.argv) > 1 else "playdowns"

class EBEGui(QWidget):
    def __init__(self, overlay_type="playdowns"):  # 👈 Add this parameter
        super().__init__()
        self.overlay_type = overlay_type
        self.setWindowTitle("EBE – Easy Broadcast Editor")
        self.resize(600, 800)
        self.load_config()
        self.init_ui()
        self.overlay_type = "playdowns"  # or "nationals" — passed in when calling the GUI


    def font_size_picker(self):
        layout = QHBoxLayout()
        label = QLabel("Font Size")
        box = QComboBox()
        for size in range(10, 33, 2):  # 10–32 pt
            box.addItem(str(size))
        box.setCurrentText(str(self.config.get("font_size", 14)))
        layout.addWidget(label)
        layout.addWidget(box)
        self.font_size_box = box
        return layout

    def font_family_picker(self):
        layout = QHBoxLayout()
        label = QLabel("Font Family")
        box = QComboBox()
        fonts = ["Segoe UI", "Verdana", "Arial", "Helvetica", "Tahoma", "Times New Roman"]
        for font in fonts:
            box.addItem(font)
        box.setCurrentText(self.config.get("font_family", "Segoe UI"))
        layout.addWidget(label)
        layout.addWidget(box)
        self.font_family_box = box
        return layout


    def load_config(self):
        with open(f"{self.overlay_type}/config.json") as f:
            self.config = json.load(f)

        with open(f"{self.overlay_type}/scores.json") as f:
            self.scores = json.load(f)


    def init_ui(self):
        layout = QVBoxLayout()

        # Font size & family
        layout.addLayout(self.font_size_picker())
        layout.addLayout(self.font_family_picker())

        # Colors
        layout.addLayout(self.color_picker("Score 1 Color", "score1_color"))
        layout.addLayout(self.color_picker("Score 2 Color", "score2_color"))
        layout.addLayout(self.color_picker("Ends Background", "ends_bg"))
        layout.addLayout(self.color_picker("Stars Background", "stars_bg"))
        layout.addLayout(self.color_picker("Stripes Background", "stripes_bg"))

        # Column widths
        layout.addLayout(self.labeled_input("Column 1 Width", "col1_width"))
        layout.addLayout(self.labeled_input("Column 2 Width", "col2_width"))
        layout.addLayout(self.labeled_input("Column 3 Width", "col3_width"))
        layout.addLayout(self.labeled_input("Column 4 Width", "col4_width"))

        # Google Apps Script URL
        layout.addLayout(self.labeled_input("Google Apps Script URL", "google_apps_script_url"))

        # Divisions
        layout.addWidget(QLabel("Divisions:"))
        self.division_list = QListWidget()
        for div in self.config["divisions"]:
            self.division_list.addItem(QListWidgetItem(div))
        layout.addWidget(self.division_list)

        btn_row = QHBoxLayout()
        self.add_div_btn = QPushButton("Add Division")
        self.remove_div_btn = QPushButton("Remove Selected")
        self.add_div_btn.clicked.connect(self.add_division)
        self.remove_div_btn.clicked.connect(self.remove_division)
        btn_row.addWidget(self.add_div_btn)
        btn_row.addWidget(self.remove_div_btn)
        layout.addLayout(btn_row)

        # Buttons
        self.render_btn = QPushButton("Render Preview")
        self.render_btn.clicked.connect(self.handle_render)
        layout.addWidget(self.render_btn)

        # Browser preview
        self.browser = QWebEngineView()
        self.browser.setMinimumHeight(400)
        layout.addWidget(self.browser)

        self.setLayout(layout)
        self.open_preview()  # Load initial

    
    def open_preview(self):
        preview_path = os.path.abspath("preview.html")
        preview_url = QUrl.fromLocalFile(preview_path)
        self.browser.load(preview_url)

    def labeled_input(self, label_text, config_key):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit(str(self.config.get(config_key, "")))
        layout.addWidget(label)
        layout.addWidget(input_field)
        setattr(self, f"input_{config_key}", input_field)
        return layout

    def color_picker(self, label_text, config_key):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        button = QPushButton(self.config.get(config_key, "#ffffff"))
        button.setStyleSheet(f"background-color: " + button.text())
        button.clicked.connect(lambda: self.pick_color(button, config_key))
        layout.addWidget(label)
        layout.addWidget(button)
        setattr(self, f"button_{config_key}", button)
        return layout

    def pick_color(self, button, config_key):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setText(color.name())
            button.setStyleSheet("background-color: " + color.name())
            self.config[config_key] = color.name()

    def add_division(self):
        new_div, ok = QInputDialog.getText(self, "Add Division", "Division name:")
        if ok and new_div.strip():
            self.division_list.addItem(new_div.strip())

    def remove_division(self):
        for item in self.division_list.selectedItems():
            self.division_list.takeItem(self.division_list.row(item))

    def handle_render(self):
        # Save inputs
        keys = [
            "col1_width", "col2_width",
            "col3_width", "col4_width", "google_apps_script_url"
        ]
        
        for key in keys:
            widget = getattr(self, f"input_{key}")
            val = widget.text().strip()
            if key == "font_size":
                try:
                    self.config[key] = int(val)
                except ValueError:
                    self.config[key] = 14
            else:
                self.config[key] = val

        # Save divisions
        self.config["divisions"] = [self.division_list.item(i).text() for i in range(self.division_list.count())]
        self.config["font_size"] = int(self.font_size_box.currentText())
        self.config["font_family"] = self.font_family_box.currentText()


        with open(f"{self.overlay_type}/config.json", "w") as f:
            json.dump(self.config, f, indent=2)

        render_template()
        self.open_preview()
        QMessageBox.information(self, "EBE", "✅ Preview has been rendered!")

if __name__ == "__main__":
    app = QApplication([])
    window = EBEGui(overlay_type)
    window.show()
    app.exec()