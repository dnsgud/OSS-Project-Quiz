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
        self.countdown -= 1
        self.countdown_label.setText(f"남은 시간: {self.countdown}초")

        if self.countdown == 0:
            self.countdown_timer.stop()
            self.entry.setDisabled(True)  # 입력 창 비활성화
            self.submit_button.setDisabled(True)  # 제출 버튼 비활성화
            self.show_game_over()

    def reset_countdown(self):
        self.countdown = 5
        self.countdown_label.setText(f"남은 시간: {self.countdown}초")
        self.countdown_timer.start()

    def show_game_over(self):
        game_over_message = QMessageBox(self.root)
        game_over_message.setWindowTitle("게임 종료")
        game_over_message.setText(f"게임 종료! 최종 점수: {self.score}")
        game_over_message.exec_()
        self.app.quit()

if __name__ == "__main__":
    logo_directory = "image"  # 실제 디렉토리 경로로 대체
    quiz_app = BrandLogoQuiz(logo_directory)
