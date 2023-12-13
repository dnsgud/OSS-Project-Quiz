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
        self.score_widget = QWidget(self)  # score_widget을 정의
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

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.logo_label = QLabel(central_widget)
        self.highest_score_label = QLabel(f"최고 점수: {self.highest_score}", central_widget)
        self.score_display_label = QLabel(f"현재 점수: {self.score}", central_widget)
        self.time_display_label = QLabel("", central_widget)
        self.result_label = QLabel(central_widget)

        self.entry = QLineEdit(central_widget)
        self.entry.returnPressed.connect(self.check_answer)

        # 다시하기 버튼
        self.retry_button = QPushButton("다시하기", central_widget)
        self.retry_button.clicked.connect(self.retry_game)

        # 메인 메뉴로 돌아가기 버튼
        self.menu_button = QPushButton("메인 메뉴", central_widget)
        self.menu_button.clicked.connect(self.return_to_menu)

        # 크기가 큰 폰트로 설정
        font = QFont()
        font.setPointSize(100)  # 원하는 폰트 크기로 조절

        self.score_display_label.setFont(font)
        self.highest_score_label.setFont(font)
        self.time_display_label.setFont(font)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.entry)

        v_layout = QVBoxLayout(central_widget)

       # 최고 점수와 시간 표시, 현재 점수 라벨 모두 가운데에 위치
        v_layout.addWidget(self.highest_score_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        v_layout.addWidget(self.score_display_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        v_layout.addWidget(self.time_display_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # 로고 라벨을 가운데에 위치
        v_layout.addWidget(self.logo_label, alignment=Qt.AlignTop | Qt.AlignCenter)

        # 입력창을 사진 바로 아래로 위치하도록 조절
        v_layout.addWidget(self.entry, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # 나머지는 그대로 유지
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.retry_button)
        h_layout.addWidget(self.menu_button)
        v_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        v_layout.addLayout(h_layout)


        self.center_window()
        self.showMaximized()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

        self.start_new_question()

        self.setup_styles()  # 스타일 설정 함수 호출

        sys.exit(self.app.exec_())

    def setup_styles(self):
        # QLabel
        font_size = 60
        label_style = (
            f"font-size: {font_size}px; color: #2E86AB;"
            " padding: 20px;"
        )

        self.score_display_label.setStyleSheet(label_style)
        self.highest_score_label.setStyleSheet(label_style)
        self.time_display_label.setStyleSheet(label_style)

        # QLineEdit
        font_size = 50
        entry_style = (
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )
        self.entry.setStyleSheet(entry_style)
        self.entry.setFixedWidth(500)

        # QPushButton
        button_style = (
            "font-size: 30px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin: 10px;"
        )
        self.retry_button.setStyleSheet(button_style)
        self.menu_button.setStyleSheet(button_style)

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
        new_width = 600  # 원하는 가로 길이
        new_height = 200  # 원하는 세로 길이
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
            result_style = (
                "font-size: 40px; color: #FF0000;" if self.countdown == 0 else "font-size: 40px; color: #FFA500;"
            )
            result_text = f"<span style='{result_style}'>{result_text}</span>"
            self.score += 1
            if self.score > self.highest_score:
                self.highest_score = self.score
                self.highest_score_label.setText(f"best: {self.highest_score}")
                self.save_highest_score()
            self.reset_countdown()
            self.start_new_question()
        else:
            result_text = f"정답은 {correct_answer.capitalize()} 입니다."
            self.countdown_timer.stop()
            self.entry.setDisabled(True)
            self.retry_button.show()
            self.menu_button.show()
            result_style = (
                "font-size: 40px; color: #FF0000;" if self.countdown == 0 else "font-size: 40px; color: #FFA500;"
            )
            result_text = f"<span style='{result_style}'>{result_text}</span>"
        self.result_label.setText(result_text)
        self.result_label.show() 
        self.score_display_label.setText(f"현재 점수: {self.score}")

    def retry_game(self):
        self.result_label.hide()  # result_label 숨기기
        self.score = 0
        self.highest_score_label.setText(f"최고 점수: {self.highest_score}")
        self.score_display_label.setText(f"현재 점수: {self.score}")
        self.start_new_question()

    def start_new_question(self):
        self.retry_button.hide()
        self.menu_button.hide()
        self.result_label.hide() 
        self.select_next_logo()

        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)
        self.cropped_image = self.logo_image.crop(self.coordinates)
        self.q_pixmap = self.pil_to_pixmap(self.cropped_image)

        self.logo_label.setPixmap(self.q_pixmap)

        self.entry.clear()
        self.reset_countdown()
        self.entry.setDisabled(False)
        self.countdown_timer.start()

    def update_countdown(self):
        self.countdown -= 1
        self.time_display_label.setText(f"{self.countdown}초")

        if self.countdown == 0:
            self.countdown_timer.stop()
            self.entry.setDisabled(True)
            self.check_answer()

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

    def retry_game(self):
        self.score = 0
        self.highest_score_label.setText(f"최고 점수: {self.highest_score}")
        self.score_display_label.setText(f"현재 점수: {self.score}")
        self.start_new_question()

    def return_to_menu(self):
        self.score = 0
        self.highest_score = self.load_highest_score()
        self.highest_score_label.setText(f"최고 점수: {self.highest_score}")
        self.score_display_label.setText(f"현재 점수: {self.score}")
        self.retry_button.hide()
        self.menu_button.hide()
        self.start_new_question()


if __name__ == "__main__":
    logo_directory = "image"  # 실제 디렉토리 경로로 대체
    app = QApplication(sys.argv)
    quiz_app = BrandLogoQuiz(logo_directory, app)
    sys.exit(app.exec_())
