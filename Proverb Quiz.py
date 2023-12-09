import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QMessageBox, QDesktopWidget, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
import linecache
import random


class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.total_score = 0
        self.best_score = 0
        self.time_limit = 8
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.setGeometry(100, 100, 700, 500)
        self.center_on_screen()

        self.setStyleSheet(
            "background-color: #282c35; color: #ffffff;"
        )

        self.score_label = QLabel("현재 점수: 0", self)
        self.best_score_label = QLabel("최고 점수: 0", self)
        self.label = QLabel("", self)
        self.time_label = QLabel("", self)
        self.entry = QLineEdit(self)
        self.entry.returnPressed.connect(self.check_answer)  # 엔터 키로 제출
        self.button = QPushButton("제출", self)
        self.button.clicked.connect(self.check_answer)

        # QLabel for displaying planet/star image
        self.image_label = QLabel(self)
        self.setup_image_label()

        self.setup_styles()

        self.used_proverbs = set()

        layout = QVBoxLayout()
        layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.best_score_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry, alignment=Qt.AlignCenter)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.generate_quiz()

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def setup_image_label(self):
        # Load planet/star image
        pixmap = QPixmap("planet_image.jpg")  # Replace "planet_image.jpg" with your image file
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

    def setup_styles(self):
        # Set Font
        font = QFont()
        font.setFamily("맑은 고딕")  # Adjust the font family as needed
        font.setPointSize(70)  # Adjust the font size as needed

        # QLabel
        label_style = (
            f"font-size: {font.pointSize()}px; background-color: #282c35; "
            "padding: 20px; border-radius: 10px; margin-bottom: 20px; color: #ffffff;"
        )
        self.score_label.setStyleSheet(label_style)
        self.best_score_label.setStyleSheet(label_style)
        self.label.setStyleSheet(label_style)
        self.time_label.setStyleSheet(f"font-size: {font.pointSize()}px; margin-bottom: 20px; color: #ffffff;")

        # QLineEdit
        self.entry.setStyleSheet(
            f"font-size: {font.pointSize()}px; padding: 10px; border: 2px solid #61afef; "
            "border-radius: 10px; margin-bottom: 20px; color: #ffffff;"
        )

        # QPushButton
        button_style = (
            f"font-size: {font.pointSize()}px; padding: 10px; background-color: #61afef; "
            "color: #282c35; border: 2px solid #61afef; border-radius: 10px;"
        )
        self.button.setStyleSheet(button_style)

    def generate_quiz(self):
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
        no = random.randint(1, 100)
        return linecache.getline('saying.txt', no).strip()

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
    window.show()
    sys.exit(app.exec_())
