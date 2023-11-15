from PIL import Image
import os
import random

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

    # 이미지 표시
    cropped_image.show()

# 특정 디렉토리에서 랜덤 이미지 파일 및 좌표 표시
directory_path = "image"  # 실제 디렉토리 경로로 대체
display_random_image_with_coordinates(directory_path)
