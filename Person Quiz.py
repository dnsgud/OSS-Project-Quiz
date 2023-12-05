import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys

class QuizGame(QMainWindow):
    def __init__(self, parent, directory_path, time_limit):
        super(QuizGame, self).__init__(parent)

        self.directory_path = directory_path
        self.time_limit = time_limit
        self.score = 0
        self.current_timer = self.time_limit

        self.image_label = QLabel(self)
        self.name_input = QLineEdit(self)
        self.name_input.returnPressed.connect(self.check_answer)

        self.timer_label = QLabel(f'남은 시간: {self.current_timer}초', self)

        # 정답 여부와 현재 점수를 표시하는 레이블 추가
        self.correctness_label = QLabel("", self)
        self.score_label = QLabel(f'현재 점수: {self.score}', self)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.correctness_label)
        layout.addWidget(self.score_label)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.load_random_image()

    def load_random_image(self):
        file_list = os.listdir(self.directory_path)
        image_files = [file for file in file_list if file.lower().endswith('.jpeg')]

        if not image_files:
            print("디렉토리에 .jpeg 확장자를 가진 이미지 파일이 없습니다.")
            sys.exit()

        random_image_file = random.choice(image_files)
        image_path = os.path.join(self.directory_path, random_image_file)

        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))
        self.correct_answers = [answer.lower() for answer in random_image_file.split(',')]

        self.name_input.clear()
        self.current_timer = self.time_limit
        self.timer.start(1000)

    def update_timer(self):
        self.current_timer -= 1
        self.timer_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            correct_answers_str = ', '.join(self.correct_answers)
            correctness_text = "시간이 초과되었습니다. 정답은 ( {})입니다.".format(
                correct_answers_str.replace(".jpeg", "").replace(",", "")
            )
            print(correctness_text)
            self.correctness_label.setText(correctness_text)
            self.show_result()

    def check_answer(self):
        entered_name = self.name_input.text().strip().lower()

        if any(entered_name == answer for answer in self.correct_answers):
            correctness_text = "정답입니다."
            print(correctness_text)
            self.correctness_label.setText(correctness_text)

            self.score += 1
            self.score_label.setText(f'현재 점수: {self.score}')

            self.load_random_image()
        else:
            correct_answers_str = ', '.join(self.correct_answers)
            correctness_text = "오답입니다. 정답은 ( {})입니다.".format(
                correct_answers_str.replace(".jpeg", "").replace(",", "")
            )
            print(correctness_text)
            self.correctness_label.setText(correctness_text)

            self.show_result()

    def show_result(self):
        print("최종 점수: {}".format(self.score))
        self.timer.stop()
        self.parent().stack.setCurrentIndex(0)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(0, 0, 725, 600)
        self.setWindowTitle("MainWindow")

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.main_widget = QWidget()
        self.stack.addWidget(self.main_widget)

        self.quiz_button = QPushButton("인물 퀴즈", self.main_widget)
        self.quiz_button.setGeometry(10, 10, 131, 111)
        self.quiz_button.clicked.connect(self.start_quiz_game)

    def start_quiz_game(self):
        self.quiz_game = QuizGame(self, r"C:\Users\jung1\Desktop\인물 퀴즈\인물 사진", 7)
        self.stack.addWidget(self.quiz_game)
        self.stack.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
