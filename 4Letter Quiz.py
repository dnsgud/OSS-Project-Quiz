class FourletterQuizGame(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.quiz_data, self.answer_data = self.load_quiz_data()
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)

        self.total_score = 0
        self.current_index = 0
        self.high_score = self.load_highest_score()  # 최고점수 변수 추가

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

        # 최고점수를 표시
        self.high_score_label = QLabel("", self)  # 라벨 초기화 부분 추가
        self.layout.addWidget(self.high_score_label, alignment=Qt.AlignCenter)

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

        # 최고점수 초기값 설정
        self.high_score = 0
        self.high_score_label.setText(f'최고 점수: {self.high_score}')  # 초기값 표시 부분 추가

    def load_highest_score(self):
        try:
            with open("highest_score.json", "r") as file:
                data = json.load(file)
                return data.get("highest_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_highest_score(self):
        data = {"highest_score": self.highest_score}
        with open("highest_score.json", "w") as file:
            json.dump(data, file)
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
        self.total_score = 0  # 이 부분을 주석 처리 또는 삭제
        self.score_label.setText(f'현재 점수: {self.total_score}')
        self.show_question()

    def show_main_menu(self):
        self.answer_input.setEnabled(True)
        self.quiz_data, self.answer_data = self.shuffle_quiz_data(self.quiz_data, self.answer_data)
        self.current_index = 0

        # self.total_score 초기화를 제거
        # self.total_score = 0

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
            # 최고점수 업데이트
            if self.total_score > self.high_score:
                self.high_score = self.total_score
                self.high_score_label.setText(f'최고 점수: {self.high_score}')  # 최고점수 업데이트 부분 추가

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
                    # 최고점수 업데이트
                    if self.total_score > self.high_score:
                        self.high_score = self.total_score
                    # 최고점수 업데이트
                    self.high_score_label.setText(f'최고 점수: {self.high_score}')
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
 # '4글자 퀴즈' 버튼 추가
        self.four_letter_button = QPushButton("4글자 퀴즈", self.main_widget)
        self.four_letter_button.setFixedSize(400, 200)
        self.four_letter_button.move(490, 10)



