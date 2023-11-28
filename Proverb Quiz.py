import linecache
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import linecache
import random

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.total_score = 0
        self.best_score = 0

        self.init_ui()

    def init_ui(self):
        self.proverb_label = QLabel("퀴즈 시작 버튼을 눌러주세요.")
        self.answer_input = QLineEdit()
        self.submit_button = QPushButton("정답 제출")
        self.retry_button = QPushButton("다시 시도")
        self.quit_button = QPushButton("종료")

        layout = QVBoxLayout()
        layout.addWidget(self.proverb_label)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.retry_button)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

        self.submit_button.clicked.connect(self.check_answer)
        self.retry_button.clicked.connect(self.retry_quiz)
        self.quit_button.clicked.connect(self.close_app)

        self.setWindowTitle('속담 퀴즈 앱')
        self.show()

    def generate_quiz(self):
        no = random.randint(1, 100)
        saying = linecache.getline('saying.txt', no).strip()
        return saying

    def create_quiz(self, saying):
        words = saying.split()
        last_word = words[-1]
        words[-1] = '□' * len(last_word)
        return " ".join(words), last_word

    def start_quiz(self):
        proverb = self.generate_quiz()
        self.quiz, self.answer = self.create_quiz(proverb)
        self.proverb_label.setText(f"현재 점수: {self.total_score}, 최고 점수: {self.best_score}, 다음 속담을 완성하세요: '{self.quiz}' ")

    def check_answer(self):
        user_input = self.answer_input.text().strip()

        if len(user_input) == len(self.answer):
            if user_input.replace(" ", "") == self.answer.replace(" ", ""):
                self.total_score += 1
                if self.total_score > self.best_score:
                    self.best_score = self.total_score
                self.start_quiz()
            else:
                self.proverb_label.setText(f"틀렸습니다. 정답은 '{self.answer}'입니다.")
        else:
            self.proverb_label.setText("입력한 글자의 개수가 맞지 않습니다. 다시 입력하세요.")

    def retry_quiz(self):
        self.total_score = 0
        self.start_quiz()

    def close_app(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    sys.exit(app.exec_())
