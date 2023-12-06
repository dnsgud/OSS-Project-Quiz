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
    def init_ui(self):
        self.layout = QVBoxLayout()

        self.quiz_label = QLabel(self)
        self.layout.addWidget(self.quiz_label)

        self.answer_input = QLineEdit(self)
        self.answer_input.returnPressed.connect(self.check_answer)  # Enter 키 누를 때 처리
        self.layout.addWidget(self.answer_input)

        self.setLayout(self.layout)

        self.show_question()
        self.show()
