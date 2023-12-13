import json
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer
from PIL import Image
import sys
import linecache


class PersonQuiz(QMainWindow):
    def __init__(self, parent, directory_path, time_limit):
        super(PersonQuiz, self).__init__(parent)

        self.parent = parent

        # 퀴즈 디렉토리 경로, 시간 제한 등의 초기 설정
        self.directory_path = directory_path
        self.time_limit = time_limit
        self.total_score = 0
        self.best_score = 0
        self.current_timer = self.time_limit

        # UI 요소들을 나타내는 QLabel, QLineEdit, QPushButton 등의 초기화
        self.image_label = QLabel(self)
        self.name_input = QLineEdit(self)
        self.name_input.returnPressed.connect(self.check_answer)
        self.timer_label = QLabel(f'남은 시간: {self.current_timer}초', self)
        self.correctness_label = QLabel("", self)
        self.score_label = QLabel("현재 점수: 0", self)
        self.best_score_label = QLabel("최고 점수: 0", self)
        self.best_score_label.setGeometry(10, 30, 150, 30)
        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.retry_game)
        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_main_menu)

        # UI 초기화 함수 호출 및 타이머 설정
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.load_random_image()

    def init_ui(self):
        # UI 레이아웃 구성
        layout = QVBoxLayout()
        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.best_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.correctness_label)

        # 버튼들을 수평으로 정렬
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.retry_button)
        button_layout.addWidget(self.main_button)

        layout.addLayout(button_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def retry_game(self):
        # '다시하기' 버튼 클릭 시 퀴즈를 처음부터 다시 시작
        self.timer.stop()
        self.timer_label.setText("")
        self.name_input.clear()  # 수정된 부분
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.best_score_label.setText(f'최고 점수: {self.best_score}')  # 최고 점수 초기화 추가
        self.load_random_image()

    def show_main_menu(self):
        # '메인화면' 버튼 클릭 시 메인 메뉴로 이동
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.score_label.setText(f'최고 점수: {self.best_score}')
        self.parent.show_main_menu_person()

    def load_random_image(self):
        # 랜덤 이미지 로드 및 정답 초기화
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
        # 타이머 갱신 및 시간이 다 되면 check_answer 메서드 호출
        self.current_timer -= 1
        self.timer_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            # 시간 초과 시 check_answer 메서드 호출
            self.check_answer(timeout=True)

    def check_answer(self, timeout=False):
        # 정답 체크 함수
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
                # 정답일 때 처리
                correctness_text = "정답입니다."
                self.correctness_label.setText(correctness_text)

                self.total_score += 1
                if self.total_score > self.best_score:
                    self.best_score = self.total_score
                    self.best_score_label.setText(f"최고 점수: {self.best_score}")

                # 정답 여부를 일정 시간 동안 표시하고 다음 문제로 이동
                QTimer.singleShot(500, self.load_random_image)
            else:
                # 오답일 때 처리
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

    def return_to_main_menu(self):
        # 현재 퀴즈 게임을 저장하고 제거
        current_quiz_game = self
        self.parent().stack.removeWidget(self)

        # 메인 메뉴로 돌아가기
        self.parent().stack.setCurrentIndex(0)

        # 저장된 퀴즈 게임을 메모리에서 지우지 않도록 함
        current_quiz_game.deleteLater()

class BrandLogoQuiz(QMainWindow):
    def __init__(self, parent, logo_directory, app):
        super().__init__(parent)

        self.parent = parent
        self.app = app  # QApplication 객체 저장
        self.logo_directory = logo_directory

        # highest_score, score, countdown_timer, current_logo_file, coordinates 속성 초기화
        self.highest_score = self.load_highest_score()
        self.score = 0
        self.countdown_timer = QTimer(self)
        self.current_logo_file = None  # 초기값 설정
        self.coordinates = (100, 50, 300, 250)  # 초기값 설정

        self.logo_files = [f for f in os.listdir(self.logo_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.logo_files:
            print("디렉토리에서 유효한 로고 이미지 파일을 찾을 수 없습니다.")
            sys.exit()
        self.score_widget = QWidget(self)  # score_widget을 정의

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
        self.menu_button.clicked.connect(self.show_main_menu)

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

    def retry_game(self):
        # '다시하기' 버튼 클릭 시 퀴즈를 처음부터 다시 시작
        self.countdown_timer.stop()
        self.entry.clear()
        self.score = 0
        self.score_display_label.setText(f'현재 점수: {self.score}')
        self.highest_score_label.setText(f'최고 점수: {self.highest_score}')  # 최고 점수 초기화 추가
        self.start_new_question()  # 수정된 부분: 퀴즈를 처음부터 다시 시작

    def show_main_menu(self):
        self.score = 0
        self.score_display_label.setText(f'현재 점수: {self.score}')
        self.highest_score_label.setText(f'최고 점수: {self.highest_score}')
        self.parent.show_main_menu_brand()

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
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading highest score: {e}")
            return 0

    def save_highest_score(self):
        data = {"highest_score": self.highest_score}
        try:
            with open("highest_score.json", "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error saving highest score: {e}")

class ProverbQuiz(QMainWindow):
    def __init__(self, parent, time_limit):
        super(ProverbQuiz, self).__init__(parent)
        self.parent = parent

        # 초기화
        self.total_score = 0
        self.best_score = 0
        self.time_limit = time_limit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = self.time_limit
        # UI 요소 생성
        self.label = QLabel("", self)
        self.label.setGeometry(10, 70, 400, 50)
        self.label.setAlignment(Qt.AlignTop)

        self.result_label = QLabel("", self)
        self.result_label.setGeometry(10, 170, 400, 50)
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setStyleSheet(
            f"font-size: 20px; color: #FF595E; margin-bottom: 10px;"
        )

        self.setStyleSheet(
            "background-color: #F9F6F2;"
        )

        self.entry = QLineEdit(self)
        self.entry.setGeometry(10, 130, 300, 30)
        self.entry.returnPressed.connect(self.check_answer)

        self.total_score_label = QLabel("현재 점수: 0", self)
        self.best_score_label = QLabel("최고 점수: 0", self)

        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.retry_game)

        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_main_menu)

        self.retry_button.hide()
        self.main_button.hide()

        self.time_label = QLabel(f'남은 시간: {self.remaining_time}초', self)

        self.setup_styles()

        self.used_proverbs = set()

        # 레이아웃 구성
        layout = QVBoxLayout()
        layout.addWidget(self.total_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.best_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry, alignment=Qt.AlignCenter)
        layout.addWidget(self.result_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.retry_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.main_button, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 퀴즈 생성
        self.generate_quiz()

    def setup_styles(self):
        # UI 스타일 설정

        # QLabel
        font_size = 30
        self.total_score_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; font-weight: bold; margin-bottom: 10px;"
        )
        self.best_score_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; font-weight: bold; margin-bottom: 10px;"
        )
        self.label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; background-color: #F9EBB2; padding: 20px; border-radius: 10px; margin-bottom: 20px;"
        )
        self.time_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; margin-bottom: 20px;"
        )

        # QLineEdit
        font_size = 70
        self.entry.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )

        # QPushButton
        font_size = 24
        self.retry_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; border: 2px solid #FF595E; border-radius: 10px;"
        )
        self.main_button.setStyleSheet(  # 수정된 부분
            f"font-size: {font_size}px; padding: 10px; background-color: #2E86AB; color: #FFF; border: 2px solid #2E86AB; border-radius: 10px;"
        )

    def retry_game(self):
        # '다시하기' 버튼 클릭 시 퀴즈를 처음부터 다시 시작
        self.timer.stop()
        self.time_label.setText("")
        self.entry.clear()
        self.retry_button.hide()
        self.main_button.hide()
        self.total_score = 0
        self.total_score_label.setText(f'현재 점수: {self.total_score}')
        self.best_score_label.setText(f'최고 점수: {self.best_score}')  # 최고 점수 초기화 추가
        self.generate_quiz()

    def show_main_menu(self):
        self.total_score = 0
        self.total_score_label.setText(f'현재 점수: {self.total_score}')
        self.best_score_label.setText(f'최고 점수: {self.best_score}')
        self.parent.show_main_menu_proverb()

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.setText(f"남은 시간: {self.remaining_time}초")
        else:
            self.timer.stop()
            self.result_label.setText(f"시간초과입니다. 정답은 '{self.answer}'입니다.")
            QTimer.singleShot(2000, lambda: self.result_label.setText(""))  # 2초 후 메시지 지움
            self.show_buttons()  # 시간 초과 시 버튼 보이도록 추가
            self.check_answer()

    def generate_quiz(self):
        # 퀴즈 생성 및 타이머 시작
        self.remaining_time = self.time_limit
        self.timer.start(1000)
        while True:
            proverb = self.get_random_proverb()
            if proverb not in self.used_proverbs:
                break

        self.used_proverbs.add(proverb)

        self.quiz, self.answer = self.create_quiz(proverb)
        self.quiz = self.quiz.replace("'", "")
        self.label.setText(f"속담을 완성하세요: {self.quiz}")
        self.entry.clear()

        self.timer.start(1000)

    def get_random_proverb(self):
        # 랜덤 속담 얻기
        no = random.randint(1, 100)
        return linecache.getline('proverb Quiz.txt', no).strip()

    def create_quiz(self, saying):
        # 속담을 퍼즐로 변환
        words = saying.split()
        index_to_hide = random.randint(0, len(words) - 2)
        hidden_word1 = words[index_to_hide]
        hidden_word2 = words[index_to_hide + 1]
        words[index_to_hide] = '□' * len(hidden_word1)
        words[index_to_hide + 1] = '□' * len(hidden_word2)
        return " ".join(words), f"{hidden_word1} {hidden_word2}"

    def check_answer(self):
        # 사용자 답 확인 및 처리
        user_input = self.entry.text().strip()
        self.timer.stop()

        if user_input == self.answer:
            # 정답일 경우
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.best_score_label.setText(f"최고 점수: {self.best_score}")
            self.result_label.setText("정답입니다!")
            QTimer.singleShot(2000, lambda: self.result_label.setText(""))
            self.generate_quiz()
        else:
            # 오답일 경우
            self.result_label.setText(f"오답입니다. 정답은 '{self.answer}'입니다.")
            QTimer.singleShot(2000, lambda: self.result_label.setText(""))  # 2초 후 메시지 지움
            self.show_buttons()  # 오답 시 버튼 보이도록 추가

        self.total_score_label.setText(f"현재 점수: {self.total_score}")

    def show_buttons(self):
        # 버튼을 보이도록 설정
        self.retry_button.show()
        self.main_button.show()

class FourletterQuizGame(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.quiz_data, self.answer_data = self.load_quiz_data()
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)

        self.total_score = 0
        self.current_index = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # 시간 표시용
        self.timer_label = QLabel("", self)
        self.layout.addWidget(self.timer_label, alignment=Qt.AlignRight)

        self.layout.addSpacing(20)

        # 점수를 표시
        self.score_label = QLabel("", self)
        self.layout.addWidget(self.score_label, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.quiz_label = QLabel(self)
        self.layout.addWidget(self.quiz_label, alignment=Qt.AlignCenter)

        self.answer_input = QLineEdit(self)
        self.answer_input.returnPressed.connect(self.check_answer)
        self.layout.addWidget(self.answer_input, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        # 다시하기 버튼 추가
        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.retry_game)
        self.layout.addWidget(self.retry_button, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        # 메인 화면으로 돌아가는 버튼 추가
        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_main_menu)
        self.layout.addWidget(self.main_button, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)

        self.show_question()
        self.show()

    def retry_game(self):
        # '다시하기' 버튼 클릭 시 퀴즈를 처음부터 다시 시작
        self.timer.stop()
        self.timer_label.setText("")
        self.answer_input.clear()
        self.answer_input.setEnabled(True)
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.show_question()

    def load_quiz_data(self):
        with open(r"4letteranswer.txt", encoding="utf-8") as file:
            answer_data = [line.strip() for line in file.readlines()]
        return answer_data, answer_data

    def shuffle_quiz_data(self, quiz_data, answer_data):
        combined_data = list(zip(quiz_data, answer_data))
        random.shuffle(combined_data)
        shuffled_quiz_data, shuffled_answer_data = zip(*combined_data)
        return list(shuffled_quiz_data), list(shuffled_answer_data)

    def show_question(self):
        self.timer.stop()
        self.timer_label.setText("")
        self.quiz_label.setText("")
        self.answer_input.clear()

        if self.current_index < len(self.quiz_data):
            selected_quiz, answer = self.quiz_data[self.current_index], self.answer_data[self.current_index]
            two_letter = selected_quiz[:2]
            self.quiz_label.setText(f"퀴즈: {two_letter} ?")

            self.remaining_time = 6
            self.timer.start(1000)
        else:
            self.show_main_menu()

    def show_main_menu(self):
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.answer_input.setEnabled(True)
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)
        self.current_index = 0
        self.parent.show_main_menu_four()

    def handle_timeout(self):
        self.remaining_time -= 1
        self.timer_label.setText(f'남은 시간: {self.remaining_time}초')

        if self.remaining_time == 0:
            self.timer.stop()
            self.check_answer(timeout=True)

    def check_answer(self, timeout=False):
        if timeout:
            user_input = "timeout"
            self.answer_input.setEnabled(False)
        else:
            user_input = self.answer_input.text()

        matching_lines = [line for line in self.answer_data if line.endswith(user_input[-2:])]

        if not matching_lines:
            if timeout:
                self.timer_label.setText(f'시간 초과! 오답으로 처리합니다. 정답은 {self.answer_data[self.current_index]} 입니다.')
                self.timer.stop()
                self.answer_input.setEnabled(False)
                self.retry_button.setEnabled(True)
                self.main_button.setEnabled(True)
            else:
                self.timer_label.setText(f'틀렸습니다. 정답은 {self.answer_data[self.current_index]} 입니다.')
                self.timer.stop()
                self.answer_input.setEnabled(False)
                self.retry_button.setEnabled(True)
                self.main_button.setEnabled(True)

        else:
            for line in matching_lines:
                if line[:2] == self.quiz_data[self.current_index][:2]:
                    self.total_score += 1
                    self.timer_label.setText(f'정답입니다! 현재 점수: {self.total_score}')
                    self.score_label.setText(f'현재 점수: {self.total_score}')
                    self.current_index += 1
                    if self.current_index < len(self.quiz_data):
                        self.show_question()
                    else:
                        self.show_main_menu_four()
                    return

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
        quiz_buttons_layout = QHBoxLayout()  # QHBoxLayout으로 변경

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

        self.quit_button.clicked.connect(self.close_application)

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
        # quizgame 페이지를 스택에서 제거
        self.stack.removeWidget(self.quiz_game)
        self.stack.setCurrentIndex(0)

    def start_brand_quiz_game(self):
        # '브랜드 퀴즈' 게임 시작
        logo_directory = "image"  # 실제 디렉토리 경로로 대체해주세요
        self.brand_quiz_game = BrandLogoQuiz(self, logo_directory, app)
        self.stack.addWidget(self.brand_quiz_game)
        self.stack.setCurrentIndex(1)

    def show_main_menu_brand(self):
        # '브랜드 퀴즈' 페이지를 스택에서 제거
        self.stack.removeWidget(self.brand_quiz_game)
        self.stack.setCurrentIndex(0)

    def start_proverb_quiz_game(self):
        # '속담 퀴즈' 게임 시작
        self.proverb_quiz = ProverbQuiz(self, 8)
        self.stack.addWidget(self.proverb_quiz)
        self.stack.setCurrentIndex(1)

    def show_main_menu_proverb(self):
        # '속담 퀴즈' 페이지를 스택에서 제거
        self.stack.removeWidget(self.proverb_quiz)
        self.stack.setCurrentIndex(0)

    def start_four_letter_quiz_game(self):
        self.four_letter_game = FourletterQuizGame(self)
        self.stack.addWidget(self.four_letter_game)
        self.stack.setCurrentIndex(1)

    def show_main_menu_four(self):
        # FourletterQuizGame 페이지를 스택에서 제거
        self.stack.removeWidget(self.four_letter_game)
        self.stack.setCurrentIndex(0)

    def close_application(self):
        # 종료 버튼 클릭 시 프로그램 종료
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
