import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import linecache
import random

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.total_score = 0
        self.best_score = 0
        self.time_limit = 10
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.setFixedSize(500, 350)

        self.score_label = QLabel("현재 점수: 0", self)
        self.score_label.setGeometry(10, 10, 150, 30)

        self.label = QLabel("", self)
        self.label.setGeometry(10, 50, 400, 50)
        self.label.setAlignment(Qt.AlignTop)

        self.entry = QLineEdit(self)
        self.entry.setGeometry(10, 110, 300, 30)

        self.button = QPushButton("제출", self)
        self.button.setGeometry(10, 150, 75, 30)
        self.button.clicked.connect(self.check_answer)

        self.entry.returnPressed.connect(self.button.click)

        self.used_proverbs = set()

        self.generate_quiz()

    def generate_quiz(self):
        while True:
            proverb = self.get_random_proverb()
            if proverb not in self.used_proverbs:
                break

        self.used_proverbs.add(proverb)

        self.quiz, self.answer = self.create_quiz(proverb)
        # 작은따옴표(') 제거
        self.quiz = self.quiz.replace("'", "")
        self.label.setText(f"속담을 완성하세요: {self.quiz}")
        self.entry.clear()

        self.remaining_time = self.time_limit
        self.update_time()
        self.timer.start(1000)

    def get_random_proverb(self):
        no = random.randint(1, 100)
        return linecache.getline('saying.txt', no).strip()

    def create_quiz(self, saying):
        words = saying.split()
        # 두 연속된 단어 중 하나 선택
        index_to_hide = random.randint(0, len(words) - 2)
        hidden_word1 = words[index_to_hide]
        hidden_word2 = words[index_to_hide + 1]
        words[index_to_hide] = '□' * len(hidden_word1)
        words[index_to_hide + 1] = '□' * len(hidden_word2)
        return " ".join(words), f"{hidden_word1} {hidden_word2}"

    def check_answer(self):
        user_input = self.entry.text().strip()
        self.timer.stop()

        if user_input == self.answer:
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
            self.label.setText(f"속담을 완성하세요: {self.quiz}\n(남은 시간: {self.remaining_time}초)")
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
