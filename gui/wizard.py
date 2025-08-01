import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QListWidget, QListWidgetItem, QMessageBox
)

DIVISION_OPTIONS = [
    "Central", "Northeast", "Northwest", "PIMD",
    "Southwest Stars", "Southwest Stripes",
    "Southeast", "Southcentral"
]

class Wizard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧙 Overlay Builder Wizard")
        self.setFixedSize(400, 500)
        self.section_count = 1
        self.division_lists = []

        layout = QVBoxLayout()

        self.step1_label = QLabel("Step 1: Choose number of sections (e.g. Men/Women)")
        layout.addWidget(self.step1_label)

        self.section_selector = QComboBox()
        self.section_selector.addItems(["1", "2"])
        self.section_selector.currentIndexChanged.connect(self.update_sections)
        layout.addWidget(self.section_selector)

        self.step2_label = QLabel("Step 2: Select up to 4 divisions per section")
        layout.addWidget(self.step2_label)

        self.division_widgets = []
        for i in range(2):  # max 2 sections
            section_label = QLabel(f"Section {i + 1}")
            layout.addWidget(section_label)

            division_list = QListWidget()
            division_list.setSelectionMode(QListWidget.MultiSelection)
            for d in DIVISION_OPTIONS:
                item = QListWidgetItem(d)
                division_list.addItem(item)
            division_list.setDisabled(i != 0)
            layout.addWidget(division_list)
            self.division_widgets.append(division_list)

        self.create_btn = QPushButton("🛠 Create config.json")
        self.create_btn.clicked.connect(self.create_config)
        layout.addWidget(self.create_btn)

        self.setLayout(layout)

    def update_sections(self):
        self.section_count = int(self.section_selector.currentText())
        for i, widget in enumerate(self.division_widgets):
            widget.setDisabled(i >= self.section_count)

    def create_config(self):
        sections = []
        for i in range(self.section_count):
            selected = [item.text() for item in self.division_widgets[i].selectedItems()]
            if not (1 <= len(selected) <= 4):
                QMessageBox.warning(self, "Error", f"Section {i+1} must have 1-4 divisions.")
                return
            sections.append(selected)

        flat_divisions = [div for sec in sections for div in sec]
        config = {
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
            "division1_name": sections[0][0],
            "division2_name": sections[1][0] if len(sections) > 1 else "",
            "div1_bg": "#333399",
            "div2_bg": "#cc3333",
            "divisions": flat_divisions
        }
        os.makedirs("nationals", exist_ok=True)  # 👈 Add this line before writing the file
        with open("nationals/config.json", "w") as f:
            json.dump(config, f, indent=2)

        QMessageBox.information(self, "Done", "✅ config.json created successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = Wizard()
    wizard.show()
    sys.exit(app.exec_())
