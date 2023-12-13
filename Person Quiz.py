import json
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PIL import Image
import sys
import linecache

class PersonQuiz(QMainWindow):
    def __init__(self, parent, directory_path, time_limit):
        super(PersonQuiz, self).__init__(parent)

        self.parent = parent

        self.directory_path = directory_path
        self.time_limit = time_limit
        self.total_score = 0
        self.high_score = self.load_highest_score()
        self.current_timer = self.time_limit

        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.load_random_image()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.image_label = QLabel(central_widget)
        self.name_input = QLineEdit(central_widget)
        self.name_input.returnPressed.connect(self.check_answer)
        self.timer_label = QLabel(f'남은 시간: {self.current_timer}초', central_widget)
        self.correctness_label = QLabel("", central_widget)
        self.score_label = QLabel("현재 점수: 0", central_widget)
        self.high_score_label = QLabel(f'최고 점수: {self.high_score}')
        self.high_score_label.setGeometry(10, 30, 150, 30)
        self.retry_button = QPushButton("다시하기", central_widget)
        self.retry_button.clicked.connect(self.retry_game)
        self.main_button = QPushButton("메인화면", central_widget)
        self.main_button.clicked.connect(self.show_main_menu)

        font_size = 30
        label_style = f"font-size: {font_size}px; color: #2E86AB; padding: 20px;"
        button_style = "font-size: 20px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin: 10px;"

        self.score_label.setStyleSheet(label_style)
        self.high_score_label.setStyleSheet(label_style)
        self.timer_label.setStyleSheet(label_style)
        self.correctness_label.setStyleSheet(label_style)

        self.name_input.setStyleSheet(
            f"font-size: 20px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;")
        self.retry_button.setStyleSheet(button_style)
        self.main_button.setStyleSheet(button_style)

        font_size = 30
        self.name_input.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 10px;"
        )

        layout = QVBoxLayout()
        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.high_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.timer_label, alignment=Qt.AlignRight)
        layout.addWidget(self.correctness_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.retry_button)
        button_layout.addWidget(self.main_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def retry_game(self):
        # '다시하기' 버튼 클릭 시 퀴즈를 처음부터 다시 시작
        self.timer.stop()
        self.timer_label.setText("")
        self.name_input.clear()
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.high_score_label.setText(f'최고 점수: {self.high_score}')  # 최고 점수 초기화 추가
        self.load_random_image()

    def show_main_menu(self):
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.score_label.setText(f'최고 점수: {self.best_score}')
        self.parent.show_main_menu_person()

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
        self.correctness_label.clear()
        self.retry_button.hide()
        self.main_button.hide()

        self.current_timer = self.time_limit
        self.timer.start(1000)

    def update_timer(self):
        self.current_timer -= 1
        self.timer_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            # 시간 초과 시 check_answer 메서드 호출
            self.check_answer(timeout=True)

    def check_answer(self, timeout=False):
        if timeout:
            # 시간 초과일 때 처리
            correct_answers_str = ', '.join(self.correct_answers)
            correctness_text = "시간이 초과되었습니다. 정답은 ( {})입니다.".format(
                correct_answers_str.replace(".jpeg", "").replace(",", "")
            )
            print(correctness_text)
            self.correctness_label.setText(correctness_text)
            self.show_result()

        else:
            entered_name = self.name_input.text().strip().lower()

            if any(entered_name == answer for answer in self.correct_answers):
                correctness_text = "정답입니다."
                self.correctness_label.setText(correctness_text)

                self.total_score += 1
                if self.total_score > self.best_score:
                    self.best_score = self.total_score
                    self.best_score_label.setText(f"최고 점수: {self.best_score}")

                # 정답 여부를 일정 시간 동안 표시하고 다음 문제로 이동
                QTimer.singleShot(500, self.load_random_image)
            else:
                correct_answers_str = ', '.join(self.correct_answers)
                correctness_text = "오답입니다. 정답은 ( {})입니다.".format(
                    correct_answers_str.replace(".jpeg", "").replace(",", "")
                )
                print(correctness_text)
                self.correctness_label.setText(correctness_text)

                self.total_score = 0

                # 오답 시 버튼들을 보이도록 설정
                self.retry_button.show()
                self.main_button.show()

                # 퀴즈가 더 진행되지 않도록 타이머를 멈춤
                self.timer.stop()

            self.score_label.setText(f"현재 점수: {self.total_score}")

    def show_result(self):
        # 시간초과일 때도 버튼들을 보이도록 설정
        self.retry_button.show()
        self.main_button.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 기본 창 설정
        self.setGeometry(0, 0, 1900, 900)
        self.setWindowTitle("MainWindow")

        # 스택 위젯 생성
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 메인 화면
        self.main_widget = QWidget()
        self.stack.addWidget(self.main_widget)

        # 다양한 퀴즈 카테고리를 위한 버튼들 추가
        quiz_buttons_layout = QHBoxLayout()
        
        # '인물 퀴즈' 버튼 추가
        self.person_button = QPushButton("인물 퀴즈", self.main_widget)
        self.person_button.setFixedSize(250, 100)
        self.person_button.move(10, 10)
        self.person_button.clicked.connect(self.start_quiz_game)
        quiz_buttons_layout.addWidget(self.person_button)

        # '브랜드 퀴즈' 버튼 추가
        self.brand_button = QPushButton("브랜드 퀴즈", self.main_widget)
        self.brand_button.setFixedSize(250, 100)
        self.brand_button.move(170, 10)
        self.brand_button.clicked.connect(self.start_brand_quiz_game)
        quiz_buttons_layout.addWidget(self.brand_button)

        # '속담 퀴즈' 버튼 추가
        self.proverb_button = QPushButton("속담 퀴즈", self.main_widget)
        self.proverb_button.setFixedSize(250, 100)
        self.proverb_button.move(330, 10)
        self.proverb_button.clicked.connect(self.start_proverb_quiz_game)
        quiz_buttons_layout.addWidget(self.proverb_button)

        # '4글자 퀴즈' 버튼 추가
        self.four_letter_button = QPushButton("4글자 퀴즈", self.main_widget)
        self.four_letter_button.setFixedSize(250, 100)
        self.four_letter_button.move(490, 10)
        self.four_letter_button.clicked.connect(self.start_four_letter_quiz_game)
        quiz_buttons_layout.addWidget(self.four_letter_button)

        # '점수' 버튼 추가
        self.score_button = QPushButton("점수", self.main_widget)
        self.score_button.setFixedSize(200, 50)
        self.score_button.move(1650, 770)

        # '종료' 버튼 추가
        self.quit_button = QPushButton("종료", self.main_widget)
        self.quit_button.setFixedSize(200, 50)
        self.quit_button.move(1650, 830)

        # 퀴즈 버튼들을 담을 컨테이너 위젯 생성
        quiz_buttons_container = QWidget(self.main_widget)
        quiz_buttons_container.setLayout(quiz_buttons_layout)

        # 메인 레이아웃에 퀴즈 버튼 컨테이너 추가
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.addWidget(quiz_buttons_container)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def start_quiz_game(self):
        # '인물 퀴즈' 게임 시작
        self.quiz_game = PersonQuiz(self, r"인물 퀴즈\인물 사진", 7)
        self.stack.addWidget(self.quiz_game)
        self.stack.setCurrentIndex(1)

    def show_main_menu_person(self):
        # '인물 퀴즈' 페이지를 스택에서 제거
        self.stack.removeWidget(self.quiz_game)
        self.stack.setCurrentIndex(0)

    def start_brand_quiz_game(self):
        pass

    def start_proverb_quiz_game(self):
        pass

    def start_four_letter_quiz_game(self):
        pass
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
