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

class FourletterQuizGame(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.quiz_data, self.answer_data = self.load_quiz_data()
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)

        self.total_score = 0
        self.current_index = 0
        self.high_score = self.load_highest_score()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)

        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.timer_label = QLabel("", self)
        self.layout.addWidget(self.timer_label, alignment=Qt.AlignRight)

        self.layout.addSpacing(20)

        self.score_label = QLabel("", self)
        self.layout.addWidget(self.score_label, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.high_score_label = QLabel("", self)
        self.layout.addWidget(self.high_score_label, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.quiz_label = QLabel(self)
        self.layout.addWidget(self.quiz_label, alignment=Qt.AlignCenter)

        self.answer_input = QLineEdit(self)
        self.answer_input.returnPressed.connect(self.check_answer)
        self.layout.addWidget(self.answer_input, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.retry_game)
        self.layout.addWidget(self.retry_button, alignment=Qt.AlignCenter)

        self.layout.addSpacing(20)

        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_main_menu)
        self.layout.addWidget(self.main_button, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)
        self.show_question()
        self.high_score_label.setText(f'최고 점수: {self.high_score}')

    def load_highest_score(self):
        try:
            with open("highest_score4.json", "r") as file:
                data = json.load(file)
                return data.get("highest_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_highest_score(self):
        data = {"highest_score": self.high_score}
        with open("highest_score4.json", "w") as file:
            json.dump(data, file)

    def setup_styles(self):
        font_size = 30
        self.score_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; font-weight: bold; margin-bottom: 10px;"
        )
        self.timer_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; margin-bottom: 20px;"
        )
        self.high_score_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; font-weight: bold; margin-bottom: 10px;"
        )

        font_size = 70
        self.answer_input.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )
        font_size = 70
        self.quiz_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; background-color: #F9EBB2; padding: 20px; border-radius: 10px; margin-bottom: 20px;"
        )

        font_size = 24
        self.retry_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; border: 2px solid #FF595E; border-radius: 10px;"
        )
        self.main_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #2E86AB; color: #FFF; border: 2px solid #2E86AB; border-radius: 10px;"
        )

    def retry_game(self):
        self.timer.stop()
        self.timer_label.setText("")
        self.answer_input.clear()
        self.answer_input.setEnabled(True)
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.show_question()

    def show_main_menu(self):
        self.answer_input.setEnabled(True)
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)
        self.current_index = 0

        self.parent.show_main_menu_four()

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
            if self.total_score > self.high_score:
                self.high_score = self.total_score
                self.high_score_label.setText(f'최고 점수: {self.highest_score}')
                self.save_highest_score()

            self.show_main_menu()

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

                    if self.total_score > self.high_score:
                        self.high_score = self.total_score
                        self.high_score_label.setText(f'최고 점수: {self.high_score}')
                        self.save_highest_score()

                    self.current_index += 1
                    if self.current_index < len(self.quiz_data):
                        self.show_question()
                    else:
                        self.show_main_menu()
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

        # BGM 초기화
        self.bgm_player = QMediaPlayer()
        bgm_path = "bgm.mp3"  # 실제 BGM 파일 경로로 대체
        self.bgm_player.setMedia(QMediaContent(QUrl.fromLocalFile(bgm_path)))

        self.bgm_player.play()
        # 다양한 퀴즈 카테고리를 위한 버튼들 추가
        quiz_buttons_layout = QHBoxLayout()  # QHBoxLayout으로 변경

        button_style = (
            "QPushButton {"
            "   font-size: 30px;"
            "   padding: 10px;"
            "   border: 2px solid #2E86AB;"
            "   border-radius: 10px;"
            "   margin: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #2E86AB;"
            "   color: white;"
            "}"
        )

        # '인물 퀴즈' 버튼 추가
        self.person_button = QPushButton("인물 퀴즈", self.main_widget)
        self.person_button.setFixedSize(400, 200)
        self.person_button.move(10, 10)
        self.person_button.clicked.connect(self.start_quiz_game)
        self.person_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.person_button)

        # '브랜드 퀴즈' 버튼 추가
        self.brand_button = QPushButton("브랜드 퀴즈", self.main_widget)
        self.brand_button.setFixedSize(400, 200)
        self.brand_button.move(170, 10)
        self.brand_button.clicked.connect(self.start_brand_quiz_game)
        self.brand_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.brand_button)

        # '속담 퀴즈' 버튼 추가
        self.proverb_button = QPushButton("속담 퀴즈", self.main_widget)
        self.proverb_button.setFixedSize(400, 200)
        self.proverb_button.move(330, 10)
        self.proverb_button.clicked.connect(self.start_proverb_quiz_game)
        self.proverb_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.proverb_button)

        # '4글자 퀴즈' 버튼 추가
        self.four_letter_button = QPushButton("4글자 퀴즈", self.main_widget)
        self.four_letter_button.setFixedSize(400, 200)
        self.four_letter_button.move(490, 10)
        self.four_letter_button.clicked.connect(self.start_four_letter_quiz_game)
        self.four_letter_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.four_letter_button)

        # '점수' 버튼 추가
        self.score_button = QPushButton("점수", self.main_widget)
        self.score_button.setFixedSize(200, 50)
        self.score_button.move(1650, 770)
        self.score_button.clicked.connect(self.show_score)
        self.score_button.setStyleSheet(
            "QPushButton {"
            "   font-size: 20px;"
            "   padding: 5px;"
            "   background-color: #2E86AB;"
            "   color: white;"
            "   border: 2px solid #2E86AB;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #205170;"
            "}"
        )

        # '종료' 버튼 추가
        self.quit_button = QPushButton("종료", self.main_widget)
        self.quit_button.setFixedSize(200, 50)
        self.quit_button.move(1650, 830)
        self.quit_button.clicked.connect(self.close_application)
        self.quit_button.setStyleSheet(
            "QPushButton {"
            "   font-size: 20px;"
            "   padding: 5px;"
            "   background-color: #D32F2F;"
            "   color: white;"
            "   border: 2px solid #D32F2F;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #A52B2B;"
            "}"
        )
        # 퀴즈 버튼들을 담을 컨테이너 위젯 생성
        quiz_buttons_container = QWidget(self.main_widget)
        quiz_buttons_container.setLayout(quiz_buttons_layout)

        # 메인 레이아웃에 퀴즈 버튼 컨테이너와 "Quiz Hub" 라벨 추가
        main_layout = QVBoxLayout(self.main_widget)

        # 배경색 추가
        self.main_widget.setStyleSheet("background-color: #F9F6F2;")

        # QLabel을 생성하여 "Quiz Hub"를 가운데에 배치
        label = QLabel("QuizHub", self.main_widget)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label.setStyleSheet("font-size: 300px; color: #2E86AB;")  # 원하는 스타일로 조절

        main_layout.addWidget(quiz_buttons_container)
        main_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def start_quiz_game(self):
        pass

    def show_main_menu_person(self):
        pass

    def start_brand_quiz_game(self):
        pass

    def show_main_menu_brand(self):
        pass

    def start_proverb_quiz_game(self):
        pass

    def show_main_menu_proverb(self):
        pass
    def start_four_letter_quiz_game(self):
        self.four_letter_game = FourletterQuizGame(self)
        self.stack.addWidget(self.four_letter_game)
        self.stack.setCurrentIndex(1)

    def show_main_menu_four(self):
        # FourletterQuiz 스택에서 제거
        self.stack.removeWidget(self.four_letter_game)
        self.stack.setCurrentIndex(0)

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
            for quiz_number in range(1, 5):  # 1부터 4까지의 퀴즈 번호를 고려
                file_name = f"highest_score{quiz_number}.json"
                with open(file_name, "r") as file:
                    data = json.load(file)
                    highest_score = data.get("highest_score", 0)

                    if highest_score == 0:
                        score_message += f"{quiz_number}번 퀴즈: 기록 없음.\n"
                    else:
                        score_message += f"{quiz_number}번 퀴즈: {highest_score}\n"

            if score_message == "최고 점수:\n":
                custom_box = CustomMessageBox("점수", "기록 없음.")
            else:
                custom_box = CustomMessageBox("점수", score_message)

            custom_box.exec_()
        except Exception as e:
            custom_box = CustomMessageBox("에러", f"점수를 불러오는 중 오류가 발생했습니다: {str(e)}")
            custom_box.exec_()

    def close_application(self):
        # 종료 버튼 클릭 시 프로그램 종료
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
