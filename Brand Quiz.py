from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QFont, QTimer, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os
import random
from PIL import Image
import sys

class QuizGame(QMainWindow):
    def __init__(self, parent, directory_path, time_limit, app):
        super(QuizGame, self).__init__(parent)

        self.app = app
        self.directory_path = directory_path
        self.time_limit = time_limit
        self.retry_button = QPushButton("Retry", self)
        self.main_menu_button = QPushButton("Main Menu", self)
        self.total_score = 0
        self.best_score = 0
        self.current_timer = self.time_limit
        self.setGeometry(100, 100, 700, 500)
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
        self.logo_label = QLabel(central_widget)
        self.highest_score_label = QLabel(f"최고 점수: {self.best_score}", central_widget)
        self.score_display_label = QLabel(f"현재 점수: {self.total_score}", central_widget)
        self.time_display_label = QLabel("", central_widget)
        self.result_label = QLabel(central_widget)

        self.entry = QLineEdit(central_widget)
        self.entry.returnPressed.connect(self.check_answer)

        # 크기가 큰 폰트로 설정
        font = QFont()
        font.setPointSize(100)  # 원하는 폰트 크기로 조절

        self.score_display_label.setFont(font)
        self.highest_score_label.setFont(font)
        self.time_display_label.setFont(font)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.entry)

        v_layout = QVBoxLayout(central_widget)
        # 최고 점수와 현재 점수 라벨을 사진 바로 위 왼쪽에 위치하도록 조절
        v_layout.addWidget(self.highest_score_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        v_layout.addWidget(self.score_display_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        v_layout.addWidget(self.time_display_label, alignment=Qt.AlignCenter)
        v_layout.addWidget(self.logo_label, alignment=Qt.AlignTop | Qt.AlignCenter)
        # 입력창을 사진 바로 아래로 위치하도록 조절
        v_layout.addWidget(self.entry, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # 나머지는 그대로 유지
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.entry)

        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        v_layout.addWidget(self.time_display_label, alignment=Qt.AlignTop | Qt.AlignRight)

        self.center_window()
        self.showMaximized()
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)
        self.retry_button.clicked.connect(self.retry)
        
        self.main_menu_button.clicked.connect(self.return_to_main_menu)
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
        self.highest_score_label.setStyleSheet(label_style)
        self.score_display_label.setStyleSheet(label_style)
        self.time_display_label.setStyleSheet(label_style)

        # QLineEdit
        font_size = 50
        entry_style = (
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )
        self.entry.setStyleSheet(entry_style)
        self.entry.setFixedWidth(500)

    def center_window(self):
        window_width = 400
        window_height = 500
        screen_width = self.parent().width()
        screen_height = self.parent().height()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.setGeometry(x_position, y_position, window_width, window_height)

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

    def load_random_image(self):
        file_list = os.listdir(self.directory_path)
        image_files = [file for file in file_list if file.lower().endswith('.jpeg')]

        if not image_files:
            print("디렉토리에 .jpeg 확장자를 가진 이미지 파일이 없습니다.")
            sys.exit()

        random_image_file = random.choice(image_files)
        image_path = os.path.join(self.directory_path, random_image_file)

        pixmap = QPixmap(image_path)
        self.logo_label.setPixmap(pixmap.scaledToWidth(400))
        self.correct_answers = [answer.lower() for answer in random_image_file.split(',')]

        self.entry.clear()
        self.result_label.clear()
        self.retry_button.hide()
        self.main_menu_button.hide()

        self.current_timer = self.time_limit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.current_timer -= 1
        self.time_display_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            # 시간 초과 시 check_answer 메서드 호출
            self.check_answer()

    def check_answer(self):
        entered_name = self.entry.text().strip().lower()

        if any(entered_name == answer for answer in self.correct_answers):
            correctness_text = "정답입니다."
            self.result_label.setText(correctness_text)

            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.highest_score_label.setText(f"최고 점수: {self.best_score}")

            # 정답 여부를 일정 시간 동안 표시하고 다음 문제로 이동
            QTimer.singleShot(500, self.load_random_image)
        else:
            correctness_text = f"오답입니다. 정답은 ({', '.join(self.correct_answers)})입니다."
            print(correctness_text)
            self.result_label.setText(correctness_text)

            self.total_score = 0

            # 오답 시 버튼들을 보이도록 설정
            self.retry_button.show()
            self.main_menu_button.show()

            # 퀴즈가 더 진행되지 않도록 타이머를 멈춤
            self.timer.stop()

        self.score_display_label.setText(f"현재 점수: {self.total_score}")

    def show_result(self):
        print("최종 점수: {}".format(self.total_score))

    def return_to_main_menu(self):
        # 현재 퀴즈 게임을 저장하고 제거
        current_quiz_game = self
        self.parent().stack.removeWidget(self)

        # 메인 메뉴로 돌아가기
        self.parent().stack.setCurrentIndex(0)

        # 저장된 퀴즈 게임을 메모리에서 지우지 않도록 함
        current_quiz_game.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QuizGame(None, "your_directory_path", 60, app)
    sys.exit(app.exec_())
