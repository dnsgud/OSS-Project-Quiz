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
    def load_quiz_data(self):
        with open(r"C:\Users\user\PycharmProjects\pycharmhi\4letterquiz.txt", encoding="utf-8") as file:
            quiz_data = [line.strip() for line in file.readlines()]
        with open(r"C:\Users\user\PycharmProjects\pycharmhi\4letteranswer.txt", encoding="utf-8") as file:
            answer_data = [line.strip() for line in file.readlines()]
        return quiz_data, answer_data
    def check_answer(self,timeout=False):
        if timeout:
            user_input = "timeout"
        else:
            user_input = self.answer_input.text()

        correct_answer = self.answer_data[self.current_index][2:]

        if user_input.lower() == "quit":
            self.show_end_message()
        elif user_input == self.answer_data[self.current_index][2:]:
            self.total_score += 1
            QMessageBox.information(self, '정답', f'정답입니다! 현재 점수: {self.total_score}', QMessageBox.Ok)
            self.current_index += 1
            self.show_question()
            self.answer_input.clear()  # 입력창 비우기
        else:
            if timeout:
                QMessageBox.information(self, '시간 초과', '시간 초과! 오답으로 처리합니다.', QMessageBox.Ok)
