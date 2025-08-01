import sys
import json
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QSpinBox,
    QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox
)

class ScoresEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EBE – Scores Editor")
        self.setFixedSize(400, 500)

        with open("config.json") as f:
            self.config = json.load(f)

        self.scores = []
        self.layout = QVBoxLayout()

        self.div1_label = QLabel("Division 1:")
        self.div1_combo = QComboBox()
        self.div1_combo.addItems(self.config.get("divisions", []))
        self.layout.addWidget(self.div1_label)
        self.layout.addWidget(self.div1_combo)

        self.div2_label = QLabel("Division 2:")
        self.div2_combo = QComboBox()
        self.div2_combo.addItems(self.config.get("divisions", []))
        self.layout.addWidget(self.div2_label)
        self.layout.addWidget(self.div2_combo)

        self.match_label = QLabel("Match (e.g. Smith v Jones):")
        self.match_input = QLineEdit()
        self.layout.addWidget(self.match_label)
        self.layout.addWidget(self.match_input)

        self.ends_label = QLabel("Ends:")
        self.ends_input = QSpinBox()
        self.ends_input.setMinimum(1)
        self.layout.addWidget(self.ends_label)
        self.layout.addWidget(self.ends_input)

        score_layout = QHBoxLayout()
        self.score1_input = QSpinBox()
        self.score2_input = QSpinBox()
        score_layout.addWidget(QLabel("Score 1:"))
        score_layout.addWidget(self.score1_input)
        score_layout.addWidget(QLabel("Score 2:"))
        score_layout.addWidget(self.score2_input)
        self.layout.addLayout(score_layout)

        self.add_btn = QPushButton("Add Game")
        self.add_btn.clicked.connect(self.add_game)
        self.layout.addWidget(self.add_btn)

        self.games_list = QTextEdit()
        self.games_list.setReadOnly(True)
        self.layout.addWidget(QLabel("Games List:"))
        self.layout.addWidget(self.games_list)

        self.save_btn = QPushButton("Save scores.json")
        self.save_btn.clicked.connect(self.save_scores)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

        self.back_button = QPushButton("🔙 Back to Main Menu")
        self.back_button.clicked.connect(self.go_back_to_main)
        self.layout.addWidget(self.back_button)


    def add_game(self):
        game = {
            "division1": self.div1_combo.currentText(),
            "division2": self.div2_combo.currentText(),
            "match": self.match_input.text(),
            "ends": self.ends_input.value(),
            "score1": self.score1_input.value(),
            "score2": self.score2_input.value()
        }
        self.scores.append(game)
        self.games_list.append(f"{game['division1']} vs {game['division2']} - {game['match']} ({game['ends']} ends): {game['score1']}-{game['score2']}")
        self.match_input.clear()
        self.score1_input.setValue(0)
        self.score2_input.setValue(0)

    def save_scores(self):
        with open("nationals/scores.json", "w") as f:
            json.dump(self.scores, f, indent=2)
        QMessageBox.information(self, "Saved", "✅ scores.json saved successfully!")

    def go_back_to_main(self):
        self.close()
        subprocess.Popen(["python", "main.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScoresEditor()
    window.show()
    sys.exit(app.exec())
