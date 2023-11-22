from PIL import Image, ImageTk
import os
import random
import tkinter as tk

def display_random_image_with_coordinates(directory_path):
    # 디렉토리 내 파일 리스트 얻기
    file_list = [f for f in os.listdir(directory_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    if not file_list:
        print("No valid image files found in the directory.")
        return

    # 랜덤하게 이미지 파일 선택
    random_image_file = random.choice(file_list)
    coordinates = (100, 50, 300, 250)
    
    # 이미지 열기
    image_path = os.path.join(directory_path, random_image_file)
    image = Image.open(image_path)
    
    # 좌표에 해당하는 부분을 잘라냄
    cropped_image = image.crop(coordinates)

    # Tkinter 창 생성
    root = tk.Tk()
    root.title("Random Cropped Image")

    # Tkinter PhotoImage 객체로 변환
    tk_image = ImageTk.PhotoImage(cropped_image)

    # 레이블에 이미지 표시
    image_label = tk.Label(root, image=tk_image)
    image_label.pack()

    # Tkinter 이벤트 루프 시작
    root.mainloop()

# 특정 디렉토리에서 랜덤 이미지 파일 및 좌표 표시
directory_path = "image"  # 실제 디렉토리 경로로 대체
display_random_image_with_coordinates(directory_path)
