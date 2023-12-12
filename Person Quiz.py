import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PIL import Image
import sys


class QuizGame(QMainWindow):
    def __init__(self, directory_path, time_limit):
        super(QuizGame, self).__init__()

        # 초기화 작업
        self.directory_path = directory_path
        self.time_limit = time_limit
        self.score = 0
        self.current_timer = self.time_limit

        # GUI 초기화
        self.image_label = QLabel(self)
        self.name_input = QLineEdit(self)
        self.name_input.returnPressed.connect(self.check_answer)  # 엔터키 입력 시 check_answer 호출

        self.timer_label = QLabel(f'남은 시간: {self.current_timer}초', self)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignRight)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.load_random_image()

    def load_random_image(self):
        # 디렉토리에서 확장자가 '.jpeg'인 이미지 파일을 무작위로 선택하고 화면에 표시
        file_list = os.listdir(self.directory_path)
        image_files = [file for file in file_list if file.lower().endswith('.jpeg')]

        if not image_files:
            print("디렉토리에 .jpeg 확장자를 가진 이미지 파일이 없습니다.")
            sys.exit()

        random_image_file = random.choice(image_files)
        image_path = os.path.join(self.directory_path, random_image_file)

        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))

        # 정답 목록 설정
        self.correct_answers = [answer.lower() for answer in random_image_file.split(',')]

        # 입력창, 타이머 초기화 및 타이머 시작
        self.name_input.clear()
        self.current_timer = self.time_limit
        self.timer.start(1000)  # 1초마다 타이머 이벤트 발생

    def update_timer(self):
        # 타이머 갱신 및 시간 초과 체크
        self.current_timer -= 1
        self.timer_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            correct_answers_str = ', '.join(self.correct_answers)
            print("\n시간이 초과되었습니다. 정답은 ( {})입니다.".format(correct_answers_str.replace(".jpeg", "").replace(",", "")))
            self.show_result()

    def check_answer(self):
        # 사용자 입력을 받아 정답과 비교 후 처리
        entered_name = self.name_input.text().strip().lower()

        if any(entered_name == answer for answer in self.correct_answers):
            print("정답입니다.")
            self.score += 1
            self.load_random_image()
        else:
            correct_answers_str = ', '.join(self.correct_answers)
            print("오답입니다. 정답은 ( {})입니다.".format(correct_answers_str.replace(".jpeg", "").replace(",", "")))

            self.show_result()

    def show_result(self):
        # 최종 점수 출력 및 게임 종료
        print("최종 점수: {}".format(self.score))
        self.timer.stop()
        sys.exit()


if __name__ == '__main__':
    # 애플리케이션 실행
    app = QApplication(sys.argv)
    game = QuizGame(r"C:\Users\jung1\Documents\OSS-Project1\인물 퀴즈\인물 사진", 10)  # 디렉토리 경로와 시간 제한을 매개변수로 전달
    game.show()
    sys.exit(app.exec_())
