class FourletterQuizGame(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.quiz_data, self.answer_data = self.load_quiz_data()
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)

        self.total_score = 0
        self.current_index = 0
        self.high_score = 0  # 최고점수 변수 추가

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)

        self.init_ui()
        self.setup_styles()  # 스타일 설정 추가

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

    def setup_styles(self):
        # UI 스타일 설정

        # QLabel
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

        # QLineEdit
        font_size = 70
        self.answer_input.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; border: 2px solid #2E86AB; border-radius: 10px; margin-bottom: 20px;"
        )
        font_size = 70
        self.quiz_label.setStyleSheet(
            f"font-size: {font_size}px; color: #2E86AB; background-color: #F9EBB2; padding: 20px; border-radius: 10px; margin-bottom: 20px;"
        )

        # QPushButton
        font_size = 24
        self.retry_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #FF595E; color: #FFF; border: 2px solid #FF595E; border-radius: 10px;"
        )
        self.main_button.setStyleSheet(
            f"font-size: {font_size}px; padding: 10px; background-color: #2E86AB; color: #FFF; border: 2px solid #2E86AB; border-radius: 10px;"
        )

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

        # 최고점수 업데이트
        if self.total_score > self.high_score:
            self.high_score = self.total_score
            self.high_score_label.setText(f'최고 점수: {self.high_score}')  # 최고점수 업데이트 부분 추가

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
