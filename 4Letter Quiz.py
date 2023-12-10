import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import random

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
        with open(r"C:\Users\user\PycharmProjects\pycharmhi\4letteranswer.txt", encoding="utf-8") as file:
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
        # 최종 점수 알림
        QMessageBox.information(self, '최종 점수', f'최종 점수: {self.total_score}', QMessageBox.Ok)
        # 점수 초기화
        self.total_score = 0
        self.score_label.setText(f'현재 점수: {self.total_score}')
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
        else:
            user_input = self.answer_input.text()

        matching_lines = [line for line in self.answer_data if line.endswith(user_input[-2:])]

        if not matching_lines:
            if timeout:
                self.timer_label.setText('시간 초과! 오답으로 처리합니다.')
            else:
                self.timer_label.setText(f'틀렸습니다. 정답은 {self.answer_data[self.current_index]} 입니다.')
        else:
            for line in matching_lines:
                if line[:2] == self.quiz_data[self.current_index][:2]:
                    self.total_score += 1
                    self.timer_label.setText(f'정답입니다! 현재 점수: {self.total_score}')
                    self.score_label.setText(f'현재 점수: {self.total_score}')
                    self.current_index += 1
                    self.show_question()
                    return

            self.timer_label.setText(f'틀렸습니다. 정답은 {self.answer_data[self.current_index]} 입니다.')

    def show_end_message(self):
        QMessageBox.information(self, '종료', f'게임 종료! 총 점수: {self.total_score}', QMessageBox.Ok)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = FourletterQuizGame()
    sys.exit(app.exec_())
