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
     def show_question(self):
        if self.current_index < len(self.quiz_data):
            selected_quiz, answer = self.quiz_data[self.current_index], self.answer_data[self.current_index]
            two_letter = selected_quiz[:2]
            self.quiz_label.setText(f"퀴즈: {two_letter} ?")
            self.timer.start(6000)  # 6초 타이머 시작
        else:
            self.show_end_message()

    def handle_timeout(self):
        self.timer.stop()
        self.check_answer(timeout=True)
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
                QMessageBox.information(self, '정답', f'정답은 {self.answer_data[self.current_index]} 입니다.', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '오답', f'틀렸습니다. 정답은 {self.answer_data[self.current_index]} 입니다.', QMessageBox.Ok)
            restart = QMessageBox.question(self, '재시작', '다시 시작하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
            if restart == QMessageBox.Yes:
                self.total_score = 0
                self.current_index = 0
                self.show_question()
            else:
                self.show_end_message()
