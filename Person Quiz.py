import os
import random
from PIL import Image
import threading
import time

directory_path = r"C:\Users\jung1\Desktop\인물 퀴즈\인물 사진"  # 디렉토리 경로를 지정함
time_limit = 5  # 문제의 제한 시간

def get_user_input(timeout, default=None):
    result = [default]
    
    def user_input():
        result[0] = input("인물의 이름을 입력 : ")

    thread = threading.Thread(target=user_input)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("\n시간이 초과되었습니다.")
        return None
    else:
        return result[0]

def load_random_image(directory_path):
    # 지정된 경로에서 모든 파일 목록을 불러옴
    file_list = os.listdir(directory_path)

    # 확장자가 ‘.jpeg’인 이미지 파일만 불러옴
    image_files = [file for file in file_list if file.lower().endswith('.jpeg')]

    if not image_files:
        print("디렉토리에 .jpeg 확장자를 가진 이미지 파일이 없습니다.")
        return None

    score = 0  # 점수를 저장하는 변수

    for _ in range(len(image_files)):
        # 무작위로 이미지를 선택
        random_image_file = random.choice(image_files)

        # 선택된 이미지의 전체 경로를 작성함
        image_path = os.path.join(directory_path, random_image_file)

        # Pillow를 사용하여 이미지를 열음
        image = Image.open(image_path)
        image.show()

        # 인물의 이름 입력 받기
        person_name = get_user_input(time_limit)

        if person_name is None:
            break  # 시간 초과시 퀴즈 종료

        # 파일명과 입력 받은 이름이 일치하는지 확인
        if person_name.lower() in random_image_file.lower():
            print("정답입니다.")
            score += 1  # 정답일 경우 점수 1점 증가
        else:
            print("오답입니다. 정답은 {}입니다.".format(random_image_file.replace(".jpeg", "")))
            break  # 틀릴 경우 반복 종료

    print("점수: {}".format(score))

# 함수 호출
load_random_image(directory_path)
