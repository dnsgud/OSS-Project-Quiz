import json
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import linecache



class ProverbQuiz(QMainWindow):
    def __init__(self, parent, time_limit):
        super(ProverbQuiz, self).__init__(parent)
         # 초기화
        self.total_score = 0
        self.best_score = self.load_highest_score()
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

        self.total_score_label = QLabel(f"현재 점수: {self.total_score}", self)
        self.best_score_label = QLabel(f"최고 점수: {self.best_score}", self)

        self.retry_button = QPushButton("다시하기", self)
        self.retry_button.clicked.connect(self.retry_game)

        self.main_button = QPushButton("메인화면", self)
        self.main_button.clicked.connect(self.show_main_menu)

        self.retry_button.hide()
        self.main_button.hide()

        self.time_label = QLabel(f'남은 시간: {self.remaining_time}초', self)

        self.setup_styles()

        self.used_proverbs = set()
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
        
        self.generate_quiz()    def check_answer(self):
        # 사용자 답 확인 및 처리
        user_input = self.entry.text().strip()
        self.timer.stop()

        if user_input == self.answer:
            # 정답일 경우
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.best_score_label.setText(f"최고 점수: {self.best_score}")
                self.save_highest_score()
            self.result_label.setText("정답입니다!")
            QTimer.singleShot(2000, lambda: self.result_label.setText(""))
            self.generate_quiz()
    def check_answer(self):
        # 사용자 답 확인 및 처리
        user_input = self.entry.text().strip()
        self.timer.stop()
        
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





    def save_highest_score(self):
        data = {"highest_score": self.best_score}
        with open("highest_score3.json", "w") as file:
            json.dump(data, file)
    def load_highest_score(self):
        try:
            with open("highest_score3.json", "r") as file:
                data = json.load(file)
                return data.get("highest_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
        if user_input == self.answer:
            # 정답일 경우
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.best_score_label.setText(f"최고 점수: {self.best_score}")
                self.save_highest_score()
            self.result_label.setText("정답입니다!")
            QTimer.singleShot(2000, lambda: self.result_label.setText(""))
                  else:
            # 오답일 경우
            self.result_label.setText(f"오답입니다. 정답은 '{self.answer}'입니다.")
            QTimer.singleShot(2000, lambda: self.result_label.setText(""))  # 2초 후 메시지 지움
            self.show_buttons()  # 오답 시 버튼 보이도록 추가

        self.total_score_label.setText(f"현재 점수: {self.total_score}")
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

    def load_highest_score(self):
        try:
            with open("highest_score3.json", "r") as file:
                data = json.load(file)
                return data.get("highest_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_highest_score(self):
        data = {"highest_score": self.best_score}
        with open("highest_score3.json", "w") as file:
            json.dump(data, file)
    def show_buttons(self):
        # 버튼을 보이도록 설정
        self.retry_button.show()
        self.main_button.show()
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

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
                # 기본 창 설정
        self.setGeometry(0, 0, 1900, 900)
        self.setWindowTitle("MainWindow")
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
        self.score_label.setStyleSheet(label_style)
        self.best_score_label.setStyleSheet(label_style)
        self.label.setStyleSheet(label_style)
        self.time_label.setStyleSheet(label_style)
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
    def get_random_proverb(self):
        # 랜덤 속담 얻기
        no = random.randint(1, 100)
        return linecache.getline('proverb Quiz.txt', no).strip()
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

        self.used_proverbs.add(proverb)

        self.quiz, self.answer = self.create_quiz(proverb)
        self.quiz = self.quiz.replace("'", "")
        self.label.setText(f"속담을 완성하세요: {self.quiz}")
        self.entry.clear()

        self.timer.start(1000)

        def show_main_menu(self):
        self.total_score = 0
        self.total_score_label.setText(f'현재 점수: {self.total_score}')
        self.best_score_label.setText(f'최고 점수: {self.best_score}')
        self.parent.show_main_menu_proverb()
    def create_quiz(self, saying):
        # 속담을 퍼즐로 변환
        words = saying.split()
        index_to_hide = random.randint(0, len(words) - 2)
        hidden_word1 = words[index_to_hide]
        hidden_word2 = words[index_to_hide + 1]
        words[index_to_hide] = '□' * len(hidden_word1)
        words[index_to_hide + 1] = '□' * len(hidden_word2)
        return " ".join(words), f"{hidden_word1} {hidden_word2}"

    def create_quiz(self, saying):
        words = saying.split()
        index_to_hide = random.randint(0, len(words) - 2)
        hidden_word1 = words[index_to_hide]
        hidden_word2 = words[index_to_hide + 1]
        words[index_to_hide] = '□' * len(hidden_word1)
        words[index_to_hide + 1] = '□' * len(hidden_word2)
        return " ".join(words), f"{hidden_word1} {hidden_word2}"

    def check_answer(self):
        user_input = self.entry.text().strip()
        self.timer.stop()

        if user_input == self.answer:
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
                self.best_score_label.setText(f"최고 점수: {self.best_score}")
            QMessageBox.information(self, "정답", "정답입니다!")
        else:
            retry = QMessageBox.question(self, "틀림", f"틀렸습니다. 정답은 '{self.answer}'입니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.No:
                self.close()
            else:
                self.total_score = 0

        self.score_label.setText(f"현재 점수: {self.total_score}")
        self.generate_quiz()

    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.setText(f"남은 시간: {self.remaining_time}초")
            self.label.setText(f"속담을 완성하세요: {self.quiz}")
        elif self.remaining_time == 0:
            self.remaining_time = -1
            self.timer.stop()

            retry = QMessageBox.question(self, "시간 초과", "제한 시간이 초과되었습니다.\n다시 시도하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.Yes:
                self.total_score = 0
                self.generate_quiz()
            else:
                self.close()
        else:
            self.generate_quiz()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.showMaximized()  # 전체 화면으로 표시
    sys.exit(app.exec_())
