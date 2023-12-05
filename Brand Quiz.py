import tkinter as tk
from PIL import Image, ImageTk
import os
import random

class BrandLogoQuiz:
    def __init__(self, root, logo_directory):
        # (이전 코드 생략)

        # 로고 이미지 열기
        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)

        # 로고 이미지에서 자표에 해당하는 부분을 잘라냄
        self.coordinates = (100, 50, 300, 250)
        self.cropped_image = self.logo_image.crop(self.coordinates)

        # Tkinter PhotoImage 객체로 변환
        self.tk_cropped_image = ImageTk.PhotoImage(self.cropped_image)

        # 원본 로고 이미지 Tkinter PhotoImage 객체로 변환
        self.tk_original_image = ImageTk.PhotoImage(self.logo_image.resize(self.cropped_image.size))

        # (이후 코드 생략)

    def next_question(self):
        # 새로운 로고 퀴즈로 이동
        self.select_next_logo()
        self.logo_path = os.path.join(self.logo_directory, self.current_logo_file)
        self.logo_image = Image.open(self.logo_path)

        # 로고 이미지에서 자표에 해당하는 부분을 잘라냄
        self.cropped_image = self.logo_image.crop(self.coordinates)

        # Tkinter PhotoImage 객체로 변환
        self.tk_cropped_image = ImageTk.PhotoImage(self.cropped_image)

        self.logo_label.config(image=self.tk_cropped_image)  # 로고 이미지 업데이트

        self.entry.delete(0, tk.END)  # 텍스트 입력 상자 초기화

        # 7초 카운트 다운 시작
        self.root.after(0, self.countdown, 7)

# (이후 코드 생략)

# 특정 디렉토리에서 로고 이미지 파일로 퀴즈 생성
logo_directory = "image"  # 실제 디렉토리 경로로 대체
root = tk.Tk()
quiz_app = BrandLogoQuiz(root, logo_directory)
root.mainloop()
