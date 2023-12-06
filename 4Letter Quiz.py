import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
import random
class QuizGame(QWidget):
    def __init__(self):
        super().__init__()

        self.quiz_data, self.answer_data = self.load_quiz_data()
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)

        self.total_score = 0
        self.current_index = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)

        self.init_ui()
