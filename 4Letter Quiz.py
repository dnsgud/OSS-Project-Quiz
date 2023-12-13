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
    def __init__(self, parent, person_directory, time_limit):
        super(PersonQuiz, self).__init__(parent)

        self.person_directory = person_directory
        self.time_limit = time_limit
        self.total_score = 0
        self.best_score = 0
        self.current_timer = self.time_limit

        self.image_label = QLabel(self)
        self.name_input = QLineEdit(self)
        self.name_input.returnPressed.connect(self.check_answer)

        self.timer_label = QLabel(f'남은 시간: {self.current_timer}초', self)

        # 정답 여부와 현재 점수를 표시하는 레이블 추가
        self.correctness_label = QLabel("", self)
        self.score_label = QLabel("현재 점수: 0", self)
        self.score_label.setGeometry(10, 30, 150, 30)
        self.best_score_label = QLabel("최고 점수: 0", self)
        self.best_score_label.setGeometry(10, 30, 150, 30)

        # 다시하기 버튼과 메인화면 버튼 추가
        self.retry_button = QPushButton("다시하기", self)
        self.main_menu_button = QPushButton("메인화면", self)

        self.retry_button.clicked.connect(self.load_random_image)
        self.main_menu_button.clicked.connect(self.return_to_main_menu)

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
        button_layout.addWidget(self.main_menu_button)

        layout.addLayout(button_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.load_random_image()

    def load_random_image(self):
        file_list = os.listdir(self.person_directory)
        image_files = [file for file in file_list if file.lower().endswith('.jpeg')]

        if not image_files:
            print("디렉토리에 .jpeg 확장자를 가진 이미지 파일이 없습니다.")
            sys.exit()

        random_image_file = random.choice(image_files)
        image_path = os.path.join(self.person_directory, random_image_file)

        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))
        self.correct_answers = [answer.lower() for answer in random_image_file.split(',')]

        self.name_input.clear()
        self.correctness_label.clear()
        self.retry_button.hide()
        self.main_menu_button.hide()

        self.current_timer = self.time_limit
        self.timer.start(1000)

    def update_timer(self):
        self.current_timer -= 1
        self.timer_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            # 시간 초과 시 check_answer 메서드 호출
            self.check_answer()

        if self.current_timer == 0:
            correct_answers_str = ', '.join(self.correct_answers)
            correctness_text = "시간이 초과되었습니다. 정답은 ( {})입니다.".format(
                correct_answers_str.replace(".jpeg", "").replace(",", "")
            )
            print(correctness_text)
            self.correctness_label.setText(correctness_text)
            self.show_result()
        def check_answer(self):
        user_input = self.answer_input.text()
        matching_lines = [line for line in self.answer_data if line.endswith(user_input[-2:])]

        if not matching_lines:
            self.timer.stop()
            self.total_score = 0
            correct_answer = self.answer_data[self.current_index]
            self.timer_label.setText(f'틀렸습니다. 정답은 {correct_answer} 입니다.')
            self.show_result_buttons()
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
                        self.show_main_menu()
                    return

            self.timer.stop()
            self.total_score = 0
            correct_answer = self.answer_data[self.current_index]
            self.timer_label.setText(f'틀렸습니다. 정답은 {correct_answer} 입니다.')
            self.show_result_buttons()

    def show_result_buttons(self):
        # 시간 초과나 오답 시 버튼들을 보이도록 설정
        self.retry_button.show()
        self.main_button.show()
    def show_result(self):
        print("최종 점수: {}".format(self.score))

    def return_to_main_menu(self):
        # 현재 퀴즈 게임을 저장하고 제거
        current_quiz_game = self
        self.parent().stack.removeWidget(self)
        # 메인 메뉴로 돌아가기
        self.parent().stack.setCurrentIndex(0)

        # 저장된 퀴즈 게임을 메모리에서 지우지 않도록 함
        current_quiz_game.deleteLater()
class BrandLogoQuiz(QWidget):
    def __init__(self, logo_directory):
        super().__init__()
        self.logo_directory = logo_directory
        self.logo_files = [f for f in os.listdir(self.logo_directory) if
                           f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.logo_files:
            print("No valid logo image files found in the directory.")
            sys.exit()

        self.coordinates = (100, 50, 300, 250)
        self.current_logo_file = ""
        self.total_score = 0
        self.best_score = 0
        self.countdown = 5
        self.countdown_timer = QTimer()

        self.setup_ui()

    def setup_ui(self):
        self.select_next_logo()

        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)
        self.cropped_image = self.logo_image.crop(self.coordinates)
        self.q_pixmap = self.pil_to_pixmap(self.cropped_image)

        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(self.q_pixmap)

        self.entry = QLineEdit(self)
        self.entry.returnPressed.connect(self.check_answer)

        self.submit_button = QPushButton("제출", self)
        self.submit_button.clicked.connect(self.check_answer)

        self.result_label = QLabel(self)

        self.score_label = QLabel("현재 점수: 0", self)
        self.best_score_label = QLabel("최고 점수: 0", self)
        self.best_score_label.setGeometry(10, 30, 150, 30)

        self.countdown_label = QLabel("", self)

        # 크기가 큰 폰트로 설정
        font = QFont()
        font.setPointSize(13)  # 원하는 폰트 크기로 조절

        self.result_label.setFont(font)
        self.score_label.setFont(font)
        self.best_score_label.setFont(font)
        self.countdown_label.setFont(font)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.entry)
        h_layout.addWidget(self.submit_button)

        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.logo_label)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.result_label)
        v_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        v_layout.addWidget(self.best_score_label, alignment=Qt.AlignCenter)
        v_layout.addWidget(self.countdown_label)

        self.setLayout(v_layout)

        self.center_window()
        self.show()

        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def center_window(self):
        window_width = 400
        window_height = 500
        screen_width = QApplication.primaryScreen().geometry().width()
        screen_height = QApplication.primaryScreen().geometry().height()

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
        new_width = 400  # 원하는 가로 길이
        new_height = 300  # 원하는 세로 길이
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
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.best_score_label.setText(f"최고 점수: {self.best_score}")
            self.reset_countdown()
        else:
            result_text = f"틀렸습니다. 정답은 {correct_answer.capitalize()} 입니다."
            self.countdown_timer.stop()
            self.entry.setDisabled(True)  # 입력 창 비활성화
            self.submit_button.setDisabled(True)  # 제출 버튼 비활성화

            self.total_score = 0

        self.result_label.setText(result_text)
        self.score_label.setText(f"현재 점수: {self.total_score}")

        if user_input == correct_answer:
            self.next_question()

    def next_question(self):
        self.select_next_logo()

        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)
        self.cropped_image = self.logo_image.crop(self.coordinates)
        self.q_pixmap = self.pil_to_pixmap(self.cropped_image)

        self.logo_label.setPixmap(self.q_pixmap)

        self.entry.clear()
        self.reset_countdown()
        self.entry.setDisabled(False)  # 입력 창 활성화
        self.submit_button.setDisabled(False)  # 제출 버튼 활성화
        self.countdown_timer.start()

    def update_countdown(self):
        correct_answer = os.path.splitext(self.current_logo_file)[0].lower()
        self.countdown -= 1
        self.countdown_label.setText(f"남은 시간: {self.countdown}초")

        if self.countdown == 0:
            self.countdown_timer.stop()
            self.entry.setDisabled(True)  # 입력 창 비활성화
            self.submit_button.setDisabled(True)  # 제출 버튼 비활성화
            self.result_label.setText(f"시간 초과! 정답은 {correct_answer.capitalize()} 입니다.")

    def reset_countdown(self):
        self.countdown = 5
        self.countdown_label.setText(f"남은 시간: {self.countdown}초")
        self.countdown_timer.start()
class FourletterQuizGame(QWidget):
    def __init__(self):
        super().__init__()

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
        self.layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignRight)

        self.layout.addSpacing(20)

        # 점수를 표시
        self.score_label = QLabel("", self)
        self.layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(20)

        self.quiz_label = QLabel(self)
        self.layout.addWidget(self.quiz_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.answer_input = QLineEdit(self)
        self.answer_input.returnPressed.connect(self.check_answer)
        self.layout.addWidget(self.answer_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(20)

        # 메인 화면으로 돌아가는 버튼 추가
        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.show_main_menu)
        self.layout.addWidget(self.retry_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addSpacing(20)

        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_question)
        self.layout.addWidget(self.main_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.show_question()
        self.show()

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
        QMessageBox.information(self, '최종 점수', f'최종 점수: {self.total_score}', QMessageBox.Ok)
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.answer_input.setEnabled(True)
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)
        self.current_index = 0
        self.show_question()

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
                        self.show_main_menu()
                    return

            self.timer_label.setText(f'틀렸습니다. 정답은 {self.answer_data[self.current_index]} 입니다.')
    def show_end_message(self):
        QMessageBox.information(self, '종료', f'게임 종료! 총 점수: {self.total_score}', QMessageBox.Ok)
        self.close()

class ProverbQuiz(QMainWindow):
    def __init__(self, parent, time_limit):
        super(ProverbQuiz, self).__init__(parent)

        # 초기화
        self.total_score = 0
        self.best_score = 0
        self.time_limit = 8
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer2)

        # UI 요소 생성
        self.label = QLabel("", self)
        self.label.setGeometry(10, 70, 400, 50)
        self.label.setAlignment(Qt.AlignTop)

        self.setStyleSheet(
            "background-color: #F9F6F2;"
        )

        self.entry = QLineEdit(self)
        self.entry.setGeometry(10, 130, 300, 30)
        self.entry.returnPressed.connect(self.check_answer)

        self.button = QPushButton("제출", self)
        self.button.setGeometry(10, 170, 75, 30)
        self.button.clicked.connect(self.check_answer)

        self.score_label = QLabel("현재 점수: 0", self)
        self.best_score_label = QLabel("최고 점수: 0", self)
        self.best_score_label.setGeometry(10, 30, 150, 30)

        self.time_label = QLabel("", self)
        self.setup_styles()

        self.used_proverbs = set()

        # 레이아웃 구성
        layout = QVBoxLayout()
        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.best_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 퀴즈 생성
        self.generate_quiz()

    def setup_styles(self):
        # UI 스타일 설정

        # QLabel
        font_size = 30
        self.score_label.setStyleSheet(
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
        self.button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; border: 2px solid #FF595E; border-radius: 10px;"
        )

    def generate_quiz(self):
        # 퀴즈 생성 및 타이머 시작
        self.remaining_time = self.time_limit
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
            QMessageBox.information(self, "정답", "정답입니다!")
        else:
            # 오답일 경우
            retry = QMessageBox.question(self, "틀림", f"틀렸습니다. 정답은 '{self.answer}'입니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.No:
                self.parent().return_to_main_menu()
                return
            else:
                self.total_score = 0

        self.score_label.setText(f"현재 점수: {self.total_score}")
        self.generate_quiz()

    def update_timer2(self):
        # 타이머 업데이트
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.setText(f"남은 시간: {self.remaining_time}초")
            self.label.setText(f"속담을 완성하세요: {self.quiz}")
        elif self.remaining_time == 0:
            self.remaining_time = -1
            self.timer.stop()

            # 시간 초과 시 텍스트를 직접 화면에 출력하고 결과 버튼들을 보이도록 설정
            self.label.setText(f"시간이 초과되었습니다. 정답은 '{self.answer}'입니다.\n다시 시도하려면 제출 버튼을 클릭하세요.")
            self.show_result_buttons()
        else:
            self.timer.stop()

            # 시간 초과 시 텍스트를 직접 화면에 출력하고 결과 버튼들을 보이도록 설정
            self.label.setText(f"시간이 초과되었습니다. 정답은 '{self.answer}'입니다.\n다시 시도하려면 제출 버튼을 클릭하세요.")
            self.show_result_buttons()

    def show_result_buttons(self):
        # 시간 초과나 오답 시 버튼들을 보이도록 설정
        self.retry_button.show()
        self.main_menu_button.show()

        # 퀴즈가 더 진행되지 않도록 타이머를 멈춤
        self.timer.stop()

class PersonQuiz(QMainWindow):
    def __init__(self, parent, person_directory, time_limit):
        super(PersonQuiz, self).__init__(parent)

        self.person_directory = person_directory
        self.time_limit = time_limit
        self.total_score = 0
        self.best_score = 0
        self.current_timer = self.time_limit

        self.image_label = QLabel(self)
        self.name_input = QLineEdit(self)
        self.name_input.returnPressed.connect(self.check_answer)

        self.timer_label = QLabel(f'남은 시간: {self.current_timer}초', self)

        # 정답 여부와 현재 점수를 표시하는 레이블 추가
        self.correctness_label = QLabel("", self)
        self.score_label = QLabel("현재 점수: 0", self)
        self.score_label.setGeometry(10, 30, 150, 30)
        self.best_score_label = QLabel("최고 점수: 0", self)
        self.best_score_label.setGeometry(10, 30, 150, 30)

        # 다시하기 버튼과 메인화면 버튼 추가
        self.retry_button = QPushButton("다시하기", self)
        self.main_menu_button = QPushButton("메인화면", self)

        self.retry_button.clicked.connect(self.load_random_image)
        self.main_menu_button.clicked.connect(self.return_to_main_menu)

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
        button_layout.addWidget(self.main_menu_button)

        layout.addLayout(button_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.load_random_image()

    def load_random_image(self):
        file_list = os.listdir(self.person_directory)
        image_files = [file for file in file_list if file.lower().endswith('.jpeg')]

        if not image_files:
            print("디렉토리에 .jpeg 확장자를 가진 이미지 파일이 없습니다.")
            sys.exit()

        random_image_file = random.choice(image_files)
        image_path = os.path.join(self.person_directory, random_image_file)

        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaledToWidth(400))
        self.correct_answers = [answer.lower() for answer in random_image_file.split(',')]

        self.name_input.clear()
        self.correctness_label.clear()
        self.retry_button.hide()
        self.main_menu_button.hide()

        self.current_timer = self.time_limit
        self.timer.start(1000)

    def update_timer(self):
        self.current_timer -= 1
        self.timer_label.setText(f'남은 시간: {self.current_timer}초')

        if self.current_timer == 0:
            # 시간 초과 시 check_answer 메서드 호출
            self.check_answer()

        if self.current_timer == 0:
            correct_answers_str = ', '.join(self.correct_answers)
            correctness_text = "시간이 초과되었습니다. 정답은 ( {})입니다.".format(
                correct_answers_str.replace(".jpeg", "").replace(",", "")
            )
            self.correctness_label.setText(correctness_text)
            self.show_result()

    def check_answer(self):
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
            self.correctness_label.setText(correctness_text)

            self.total_score = 0

            # 오답 시 버튼들을 보이도록 설정
            self.retry_button.show()
            self.main_menu_button.show()

            # 퀴즈가 더 진행되지 않도록 타이머를 멈춤
            self.timer.stop()

        self.score_label.setText(f"현재 점수: {self.total_score}")

    def show_result(self):
        print("최종 점수: {}".format(self.score))

    def return_to_main_menu(self):
        # 현재 퀴즈 게임을 저장하고 제거
        current_quiz_game = self
        self.parent().stack.removeWidget(self)

        # 메인 메뉴로 돌아가기
        self.parent().stack.setCurrentIndex(0)

        # 저장된 퀴즈 게임을 메모리에서 지우지 않도록 함
        current_quiz_game.deleteLater()

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

    def start_brand_quiz_game(self):
        # '브랜드 퀴즈' 게임 시작
        logo_directory = "image"  # 실제 디렉토리 경로로 대체해주세요
        self.brand_quiz_game = BrandLogoQuiz(logo_directory)

        # BrandLogoQuiz 클래스의 객체를 스택에 추가하고 현재 인덱스를 변경하여 UI를 표시
        self.stack.addWidget(self.brand_quiz_game)
        self.stack.setCurrentIndex(self.stack.indexOf(self.brand_quiz_game))

    def start_proverb_quiz_game(self):
        # '속담 퀴즈' 게임 시작
        self.proverb_quiz = ProverbQuiz(self, 8)
        self.stack.addWidget(self.proverb_quiz)
        self.stack.setCurrentIndex(2)

    def start_four_letter_quiz_game(self):
        self.four_letter_game = FourletterQuizGame()
        self.stack.addWidget(self.four_letter_game)
        self.stack.setCurrentIndex(3)
    def show_score(self):
        class CustomMessageBox(QDialog):
            def __init__(self, title, message, parent=None):
                super(CustomMessageBox, self).__init__(parent)
                self.setWindowTitle(title)

                layout = QVBoxLayout()

                # 메시지를 나타내는 레이블 추가
                label = QLabel(message)
                label.setAlignment(Qt.AlignCenter)

                # 레이블 디자인 설정
                label.setStyleSheet("""
                    QLabel {
                        font-family: 'Arial';
                        font-size: 80px;
                        font-weight: bold;
                        color: #0078d4;  /* 텍스트 색상 */
                        background-color: #f0f0f0;  /* 배경색 */
                        border: 2px solid #999;  /* 경계선 */
                        border-radius: 5px;  /* 테두리 모서리 둥글게 */
                        padding: 10px;  /* 안쪽 여백 */
                    }
                """)

                layout.addWidget(label)

                # 확인 버튼 추가
                ok_button = QPushButton("확인")
                ok_button.clicked.connect(self.accept)
                layout.addWidget(ok_button)

                self.setLayout(layout)

                # 다이얼로그의 크기 설정
                self.setMinimumWidth(800)
                self.setMinimumHeight(400)

        try:
            score_message = "최고 점수:\n"
            for quiz_number in range(1, 5):  # 1~4 퀴즈번호
                file_name = f"highest_score{quiz_number}.json"
                with open(file_name, "r") as file:
                    data = json.load(file)
                    highest_score = data.get("highest_score", 0)

                    if highest_score == 0:
                        score_message += f"{quiz_number}번 퀴즈: 아직 기록된 최고 점수가 없습니다.\n"
                    else:
                        score_message += f"{quiz_number}번 퀴즈: {highest_score}\n"

            if score_message == "최고 점수:\n":
                custom_box = CustomMessageBox("점수", "아직 기록된 최고 점수가 없습니다.")
            else:
                custom_box = CustomMessageBox("점수", score_message)

            custom_box.exec_()
        except Exception as e:
            custom_box = CustomMessageBox("에러", f"점수를 불러오는 중 오류가 발생했습니다: {str(e)}")
            custom_box.exec_()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
