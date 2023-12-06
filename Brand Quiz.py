import tkinter as tk
from PIL import Image, ImageTk
import os
import random

class BrandLogoQuiz:
    def __init__(self, root, logo_directory):
        self.root = root
        self.root.title("Brand Logo Quiz")

        # 디렉토리 내 파일 리스트 얻기
        self.logo_directory = logo_directory
        self.logo_files = [f for f in os.listdir(self.logo_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        if not self.logo_files:
            print("No valid logo image files found in the directory.")
            return

        # 랜덤하게 로고 파일 선택
        self.current_logo_file = ""
        self.select_next_logo()

        # 로고 이미지 열기
        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)

        # 로고 이미지에서 자표에 해당하는 부분을 잘라냄
        self.coordinates = (100, 50, 300, 250)
        self.cropped_image = self.logo_image.crop(self.coordinates)

        # Tkinter PhotoImage 객체로 변환
        self.tk_cropped_image = ImageTk.PhotoImage(self.cropped_image)

        # 로고 이미지 표시 레이블
        self.logo_label = tk.Label(root, image=self.tk_cropped_image)
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 텍스트 입력 상자 추가
        self.entry = tk.Entry(root, font=("Arial", 12))  # 폰트 크기를 동일하게 설정
        self.entry.grid(row=1, column=0, columnspan=2, pady=10)
        self.entry.bind("<Return>", lambda event: self.check_answer())  # 엔터 키에 대한 이벤트 설정

        # 제출 버튼 추가
        self.submit_button = tk.Button(root, text=">", command=self.check_answer, font=("Arial", 12))
        self.submit_button.grid(row=1, column=2, pady=10)  # 텍스트 입력 상자 옆에 배치

        # 결과 표시 레이블 추가
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=10)

        # 점수 관련 변수 초기화
        self.score = 0
        self.score_label = tk.Label(root, text=f"점수: {self.score}")
        self.score_label.grid(row=3, column=0, columnspan=2, pady=10)

        # 창 가운데에 위치하도록 설정
        self.center_window()

    def center_window(self):
        # 창의 크기 및 위치 계산
        window_width = 400
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # 창을 가운데로 이동
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def select_next_logo(self):
        # 새로운 로고 퀴즈로 이동
        remaining_logos = [logo for logo in self.logo_files if logo != self.current_logo_file]
        if remaining_logos:
            self.current_logo_file = random.choice(remaining_logos)
        else:
            print("All logos have been used. Restarting from the beginning.")
            self.current_logo_file = random.choice(self.logo_files)

    def check_answer(self):
        user_input = self.entry.get().strip().lower()
        correct_answer = os.path.splitext(self.current_logo_file)[0].lower()

        if user_input == correct_answer:
            result_text = "정답입니다!"
            self.score += 1  # 정답일 경우 점수 1 증가
        else:
            result_text = f"틀렸습니다. 정답은 {correct_answer.capitalize()} 입니다."

        # 결과 표시 및 점수 갱신
        self.result_label.config(text=result_text)
        self.score_label.config(text=f"점수: {self.score}")
        self.next_question()

    def next_question(self):
        # 새로운 로고 퀴즈로 이동
        self.select_next_logo()
        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)

        # 로고 이미지에서 자표에 해당하는 부분을 잘라냄
        self.cropped_image = self.logo_image.crop(self.coordinates)

        # Tkinter PhotoImage 객체로 변환
        self.tk_cropped_image.paste(self.cropped_image)

        self.entry.delete(0, tk.END)  # 텍스트 입력 상자 초기화

# 특정 디렉토리에서 로고 이미지 파일로 퀴즈 생성
logo_directory = "image"  # 실제 디렉토리 경로로 대체
root = tk.Tk()
quiz_app = BrandLogoQuiz(root, logo_directory)
root.mainloop()
