import os
import random
from PIL import Image
directory_path = '"C:\Users\Desktop\인물 퀴즈\인물 사진"'  # 디렉토리 경로를 지정함.
def load_random_image(directory_path) :  # 지정된 경로에서 모든 파일 목록을 불러옴
    file_list = os.listdir(directory_path)
    image_files = [file for file in file_list if file.lower().endswith('.jpeg')]  # 확장자가 ‘jpeg’인 이미지파일만 불러옴

random_image_file = random.choice(image_files)  # 무작위로 이미지를 선택

image_path = os.path.join(directory_path, random_image_file)  # 선택된 이미지의 전체 경로를 작성함

image = Image.open(image_path)  # Pillow를 사용하여 이미지를 열음
image.show()  # 이미지를 화면에 표시
