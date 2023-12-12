import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit,
    QPushButton, QHBoxLayout, QWidget
)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PIL import Image
import random

class BrandLogoQuiz(QMainWindow):
    def __init__(self, logo_directory, app):
        super().__init__()
        self.logo_directory = logo_directory
        self.app = app
        self.logo_files = [f for f in os.listdir(self.logo_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.logo_files:
            print("No valid logo image files found in the directory.")
            sys.exit()

        # BGM 초기화
        self.bgm_player = QMediaPlayer()
        bgm_path = "bgm.mp3"  # 실제 BGM 파일 경로로 대체
        self.bgm_player.setMedia(QMediaContent(QUrl.fromLocalFile(bgm_path)))

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #F9F6F2;
            }
            """
        )

        # BGM 재생
        self.bgm_player.play()
        self.setGeometry(100, 100, 700, 500)
        self.app.aboutToQuit.connect(self.bgm_player.stop)

        self.coordinates = (100, 50, 300, 250)
        self.current_logo_file = ""
        self.score = 0
        self.highest_score = self.load_highest_score()
        self.countdown = 5
        self.countdown_timer = QTimer()

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.logo_label = QLabel(central_widget)
        self.highest_score_label = QLabel(f"최고 점수: {self.highest_score}", central_widget)
        self.score_display_label = QLabel(f"score: {self.score}", central_widget)
        self.time_display_label = QLabel("", central_widget)
        self.result_label = QLabel(central_widget)

        self.entry = QLineEdit(central_widget)
        self.entry.returnPressed.connect(self.check_answer)

        self.submit_button = QPushButton("제출", central_widget)
        self.submit_button.clicked.connect(self.check_answer)

        self.restart_button = QPushButton("다시하기", central_widget)
        self.restart_button.clicked.connect(self.restart_quiz)

        self.main_menu_button = QPushButton("메인 메뉴", central_widget)
        self.main_menu_button.clicked.connect(self.return_to_main_menu)

        # 크기가 큰 폰트로 설정
        font = QFont()
        font.setPointSize(100)  # 원하는 폰트 크기로 조절

        self.score_display_label.setFont(font)
        self.highest_score_label.setFont(font)
        self.time_display_label.setFont(font)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.entry)
        h_layout.addWidget(self.submit_button)

        v_layout = QVBoxLayout(central_widget)
        v_layout.addWidget(self.highest_score_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        v_layout.addWidget(self.score_display_label, alignment=Qt.AlignCenter)
        v_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        v_layout.addWidget(self.time_display_label, alignment=Qt.AlignTop | Qt.AlignRight)

        # 추가된 버튼들을 수직 레이아웃에 추가
        h_button_layout = QHBoxLayout()
        h_button_layout.addWidget(self.restart_button, alignment=Qt.AlignCenter)
        h_button_layout.addWidget(self.main_menu_button, alignment=Qt.AlignCenter)

        v_layout.addLayout(h_button_layout)

        self.center_window()
        self.showMaximized()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

        self.start_new_question()

        self.setup_styles()  # 스타일 설정 함수 호출

        sys.exit(self.app.exec_())

    def setup_styles(self):
        # QLabel
        font_size = 50
        label_style = (
            f"font-size: {font_size}px; color: #2E86AB; background-color: #F9EBB2;"
            " padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #2E86AB;"
        )

        self.score_display_label.setStyleSheet(label_style)
        self.highest_score_label.setStyleSheet(label_style)
        self.result_label.setStyleSheet(label_style)
        self.time_display_label.setStyleSheet(label_style)

        # QLineEdit
        font_size = 70
        self.entry.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )

        # QPushButton
        font_size = 24
        self.submit_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; "
            "border: 2px solid #FF595E; border-radius: 10px;"
        )
        self.restart_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; "
            "border: 2px solid #FF595E; border-radius: 10px;"
        )
        self.main_menu_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; "
            "border: 2px solid #FF595E; border-radius: 10px;"
        )

    def center_window(self):
        window_width = 400
        window_height = 500
        screen_width = self.app.primaryScreen().geometry().width()
        screen_height = self.app.primaryScreen().geometry().height()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.setGeometry(x_position, y_position, window_width, window_height)

    def select_next_logo(self):
        remaining_logos = [logo for logo in self.logo_files if logo != self.current_logo_file]
        if remaining_logos:
            self.current_logo_file = random.choice(remaining_logos)
        else:
            print("All logos have been used. Restarting from the beginning.")
            self.current_logo_file = random.choice(self.logo_files)

    def pil_to_pixmap(self, image):
        # 이미지의 세로와 가로 길이를 변경
        new_width = 1900  # 원하는 가로 길이
        new_height = 400  # 원하는 세로 길이
        image = image.resize((new_width, new_height), Image.LANCZOS)
        image = image.convert("RGBA")
        width, height = image.size
        q_image = QImage(image.tobytes("raw", "RGBA"), width, height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)
        return pixmap

    def check_answer(self):
        user_input = self.entry.text().strip().lower()
        correct_answer = os.path.splitext(self.current_logo_file)[0].lower()

        if user_input == correct_answer:
            result_text = "정답입니다!"
            self.score += 1
            if self.score > self.highest_score:
                self.highest_score = self.score
                self.highest_score_label.setText(f"best: {self.highest_score}")
                self.save_highest_score()
            self.reset_countdown()
        else:
            result_text = f"틀렸습니다. 정답은 {correct_answer.capitalize()} 입니다."
            self.countdown_timer.stop()
            self.entry.setDisabled(True)
            self.submit_button.setDisabled(True)
            self.restart_button.setDisabled(False)
            self.main_menu_button.setDisabled(False)

        self.result_label.setText(result_text)
        self.score_display_label.setText(f"score: {self.score}")

    def start_new_question(self):
        self.select_next_logo()

        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)
        self.cropped_image = self.logo_image.crop(self.coordinates)
        self.q_pixmap = self.pil_to_pixmap(self.cropped_image)

        self.logo_label.setPixmap(self.q_pixmap)

        self.entry.clear()
        self.reset_countdown()
        self.entry.setDisabled(False)
        self.submit_button.setDisabled(False)
        self.restart_button.setDisabled(True)
        self.main_menu_button.setDisabled(True)

        self.countdown_timer.start()

    def restart_quiz(self):
        self.score = 0
        self.result_label.clear()
        self.restart_button.setDisabled(True)
        self.main_menu_button.setDisabled(True)
        self.start_new_question()

    def return_to_main_menu(self):
        self.close()

    def update_countdown(self):
        self.countdown -= 1
        self.time_display_label.setText(f"{self.countdown}초")

        if self.countdown == 0:
            self.countdown_timer.stop()
            self.entry.setDisabled(True)
            self.submit_button.setDisabled(True)
            self.restart_button.setDisabled(False)
            self.main_menu_button.setDisabled(False)
            self.result_label.setText("시간 초과!")
            self.result_label.setStyleSheet("color: red;")

    def reset_countdown(self):
        self.countdown = 5
        self.time_display_label.setText(f"{self.countdown}초")
        self.countdown_timer.start()

    def load_highest_score(self):
        try:
            with open("highest_score.json", "r") as file:
                data = json.load(file)
                return data.get("highest_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_highest_score(self):
        data = {"highest_score": self.highest_score}
        with open("highest_score.json", "w") as file:
            json.dump(data, file)

if __name__ == "__main__":
    logo_directory = "image"  # 실제 디렉토리 경로로 대체
    app = QApplication(sys.argv)
    quiz_app = BrandLogoQuiz(logo_directory, app)
    sys.exit(app.exec_())
