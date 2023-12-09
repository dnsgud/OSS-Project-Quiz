import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPalette
from PyQt5.QtCore import QTimer, Qt
import linecache
import random

class ConsoleLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(self.font())
        painter.setPen(self.palette().color(QPalette.WindowText))
        painter.setBrush(QBrush(self.palette().color(QPalette.Window)))

        rect = self.contentsRect()
        painter.drawRect(rect)

        margin = 10
        rect.adjust(margin, margin, -margin, -margin)

        option = self.alignment()
        if option & Qt.AlignHCenter:
            option |= Qt.TextWordWrap

        metrics = painter.fontMetrics()
        text = self.text()
        if option & Qt.TextWordWrap:
            text = metrics.elidedText(text, Qt.ElideRight, rect.width())

        painter.drawText(rect, option, text)

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.total_score = 0
        self.best_score = 0
        self.time_limit = 8
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.setGeometry(100, 100, 700, 500)
        self.center_on_screen()  # 창을 화면 가운데로 이동

        self.setStyleSheet("background-color: #F5F5DC; font-size: 18px;")

        self.score_label = QLabel("현재 점수: 0", self)
        self.score_label.setStyleSheet("font-size: 24px;")

        self.best_score_label = QLabel("최고 점수: 0", self)
        self.best_score_label.setStyleSheet("font-size: 24px;")

        self.label = ConsoleLabel("", self)
        self.label.setAlignment(Qt.AlignCenter)  # 텍스트를 가운데로 정렬
        self.label.setStyleSheet("font-size: 24px;")
        self.label.setWordWrap(True)

        self.time_label = QLabel("", self)
        self.time_label.setAlignment(Qt.AlignCenter)  # 텍스트를 가운데로 정렬
        self.time_label.setStyleSheet("font-size: 24px;")

        self.entry = QLineEdit(self)
        self.entry.returnPressed.connect(self.check_answer)  # 엔터 키로 제출

        self.button = QPushButton("제출", self)
        self.button.clicked.connect(self.check_answer)

        self.used_proverbs = set()

        layout = QVBoxLayout()
        layout.addWidget(self.score_label)
        layout.addWidget(self.best_score_label)
        layout.addWidget(self.label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.entry)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.generate_quiz()

    def center_on_screen(self):
        # 창을 화면 가운데로 이동
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

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

        self.adjust_label_size()  # 라벨 크기 조정

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
            retry = QMessageBox.question(self, "틀림", f"틀렸습니다. 정답은 '{self.answer}'입니다.\n다시
