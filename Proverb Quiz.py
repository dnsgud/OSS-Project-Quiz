import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
import linecache
import random

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.total_score = 0
        self.best_score = 0
        self.time_limit = 7
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.setFixedSize(400, 200)

        self.score_label = QLabel("현재 점수: 0", self)
        self.score_label.setGeometry(10, 10, 150, 30)

        self.label = QLabel("", self)
        self.label.setGeometry(10, 50, 400, 30)

        self.entry = QLineEdit(self)
        self.entry.setGeometry(10, 90, 300, 30)

        self.button = QPushButton("제출", self)
        self.button.setGeometry(10, 130, 75, 30)
        self.button.clicked.connect(self.check_answer)

        self.generate_quiz()

    def generate_quiz(self):
        proverb = self.get_random_proverb()
        self.quiz, self.answer = self.create_quiz(proverb)
        self.label.setText(f"다음 속담을 완성하세요: '{self.quiz}'")
        self.entry.clear()

        self.remaining_time = self.time_limit
        self.update_time()

    def get_random_proverb(self):
        no = random.randint(1, 100)
        return linecache.getline('saying.txt', no).strip()

    def create_quiz(self, saying):
        words = saying.split()
        last_word = words[-1]
        words[-1] = '□' * len(last_word)
        return " ".join(words), last_word

    def check_answer(self):
        user_input = self.entry.text().strip()
        self.timer.stop()

        if user_input.replace(" ", "") == self.answer.replace(" ", ""):
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
            QMessageBox.information(self, "정답", "정답입니다!")
        else:
            retry = QMessageBox.question(self, "틀림", f"틀렸습니다. 정답은 '{self.answer}'입니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.No:
                self.close()
            else:
                self.total_score = 0
                self.best_score = 0

        self.score_label.setText(f"현재 점수: {self.total_score}")
        self.generate_quiz()

    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.label.setText(f"다음 속담을 완성하세요: '{self.quiz}' (남은 시간: {self.remaining_time}초)")
        elif self.remaining_time == 0:
            self.remaining_time = -1
            self.timer.stop()

            retry = QMessageBox.question(self, "시간 초과", "제한 시간이 초과되었습니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.No:
                self.close()
            else:
                self.total_score = 0
                self.best_score = 0
                self.generate_quiz()
        else:
            self.generate_quiz()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
