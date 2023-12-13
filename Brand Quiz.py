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
        self.person_button.setFixedSize(250, 100)
        self.person_button.move(10, 10)
        self.person_button.clicked.connect(self.start_quiz_game)
        self.person_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.person_button)

        # '브랜드 퀴즈' 버튼 추가
        self.brand_button = QPushButton("브랜드 퀴즈", self.main_widget)
        self.brand_button.setFixedSize(250, 100)
        self.brand_button.move(170, 10)
        self.brand_button.clicked.connect(self.start_brand_quiz_game)
        self.brand_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.brand_button)

        # '속담 퀴즈' 버튼 추가
        self.proverb_button = QPushButton("속담 퀴즈", self.main_widget)
        self.proverb_button.setFixedSize(250, 100)
        self.proverb_button.move(330, 10)
        self.proverb_button.clicked.connect(self.start_proverb_quiz_game)
        self.proverb_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.proverb_button)

        # '4글자 퀴즈' 버튼 추가
        self.four_letter_button = QPushButton("4글자 퀴즈", self.main_widget)
        self.four_letter_button.setFixedSize(250, 100)
        self.four_letter_button.move(490, 10)
        self.four_letter_button.clicked.connect(self.start_four_letter_quiz_game)
        self.four_letter_button.setStyleSheet(button_style)
        quiz_buttons_layout.addWidget(self.four_letter_button)

        # '점수' 버튼 추가
        self.score_button = QPushButton("점수", self.main_widget)
        self.score_button.setFixedSize(200, 50)
        self.score_button.move(1650, 770)
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
        label = QLabel("Quiz Hub", self.main_widget)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label.setStyleSheet("font-size: 200px; color: #2E86AB;")  # 원하는 스타일로 조절

        main_layout.addWidget(quiz_buttons_container)
        main_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
