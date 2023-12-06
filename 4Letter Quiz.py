import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
import random

class QuizGame(QWidget):
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

        self.quiz_label = QLabel(self)
        self.layout.addWidget(self.quiz_label)

        self.answer_input = QLineEdit(self) #답 입력 버튼임
        self.answer_input.returnPressed.connect(self.check_answer)  # Enter 키 누를 때 처리
        self.layout.addWidget(self.answer_input)

        self.setLayout(self.layout)

        self.show_question()
        self.show()

    def load_quiz_data(self):
        with open(r"C:\Users\user\PycharmProjects\pycharmhi\4letterquiz.txt", encoding="utf-8") as file:
            quiz_data = [line.strip() for line in file.readlines()]
        with open(r"C:\Users\user\PycharmProjects\pycharmhi\4letteranswer.txt", encoding="utf-8") as file:
            answer_data = [line.strip() for line in file.readlines()]
        return quiz_data, answer_data

    def shuffle_quiz_data(self, quiz_data, answer_data):
        combined_data = list(zip(quiz_data, answer_data))
        random.shuffle(combined_data) #랜덤으로 나와야하니까 문제 섞기기
        shuffled_quiz_data, shuffled_answer_data = zip(*combined_data)
        return list(shuffled_quiz_data), list(shuffled_answer_data)

    def show_question(self):
        if self.current_index < len(self.quiz_data):
            selected_quiz, answer = self.quiz_data[self.current_index], self.answer_data[self.current_index]
            two_letter = selected_quiz[:2]
            self.quiz_label.setText(f"퀴즈: {two_letter} ?")
            self.timer.start(6000)  # 6초 타이머 시작
        else:
            self.show_end_message()

    def handle_timeout(self):
        self.timer.stop()
        self.check_answer(timeout=True)

    # def check_answer(self,timeout=False):
    #     if timeout: #답 입력 시간초과
    #         user_input = "timeout"
    #     else:
    #         user_input = self.answer_input.text()

    #     correct_answer = self.answer_data[self.current_index][2:]

    #     if user_input.lower() == "quit":
    #         self.show_end_message()
    #     elif user_input == self.answer_data[self.current_index][2:]:
    #         self.total_score += 1
    #         QMessageBox.information(self, '정답', f'정답입니다! 현재 점수: {self.total_score}', QMessageBox.Ok)
    #         self.current_index += 1
    #         self.show_question()
    #         self.answer_input.clear()  # 입력창 비우기
    #     else:
    #         if timeout:
    #             QMessageBox.information(self, '시간 초과', '시간 초과! 오답으로 처리합니다.', QMessageBox.Ok)
    #             QMessageBox.information(self, '정답', f'정답은 {self.answer_data[self.current_index]} 입니다.', QMessageBox.Ok)
    #         else:
    #             QMessageBox.information(self, '오답', f'틀렸습니다. 정답은 {self.answer_data[self.current_index]} 입니다.', QMessageBox.Ok)

    #         restart = QMessageBox.question(self, '재시작', '다시 시작하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
    #         if restart == QMessageBox.Yes:
    #             self.total_score = 0
    #             self.current_index = 0
    #             self.show_question()
    #         else:
    #             self.show_end_message()
    def check_answer(self, timeout=False):
    if timeout:
        user_input = "timeout"
    else:
        user_input = self.answer_input.text()

    # 텍스트 파일에서 뒤 두 글자가 일치하는지 확인
    matching_lines = [line for line in self.answer_data if line.endswith(user_input[-2:])]

    if not matching_lines:
        # 오답 처리
        if timeout:
            QMessageBox.information(self, '시간 초과', '시간 초과! 오답으로 처리합니다.', QMessageBox.Ok)
            QMessageBox.information(self, '정답', f'정답은 {self.answer_data[self.current_index]} 입니다.', QMessageBox.Ok)
        else:
            else:
            for line in matching_lines:
                if line[:2] == self.quiz_data[self.current_index][:2]:
                    self.total_score += 1
                    self.correct_count += 1  # 정답일 경우 정답 횟수 증가
                    QMessageBox.information(self, '정답', f'정답입니다! 현재 점수: {self.total_score}', QMessageBox.Ok)
                    self.current_index += 1
                    self.show_question()
                    self.answer_input.clear()
                    return

            QMessageBox.information(self, '오답', f'틀렸습니다. 정답은 {self.answer_data[self.current_index][2:]} 입니다.', QMessageBox.Ok)
            restart = QMessageBox.question(self, '재시작', '다시 시작하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
            if restart == QMessageBox.Yes:
                self.total_score = 0
                self.current_index = 0
                self.show_question()
            else:
                self.show_end_message()

        


    def check_user_answer(self, user_input, correct_answer):
        # 사용자가 입력한 답이 뒷 두 글자와 일치하고, 앞 두 글자도 일치하는지 확인
        return user_input[-2:] == correct_answer[-2:] and user_input[:2] == self.quiz_data[self.current_index][:2]
    def show_end_message(self):
        QMessageBox.information(self, '종료', f'게임 종료! 총 점수: {self.total_score}', QMessageBox.Ok)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = QuizGame()
    sys.exit(app.exec_())
