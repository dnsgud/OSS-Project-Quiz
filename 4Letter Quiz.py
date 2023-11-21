import random
import threading
import time

def load_quiz_data():
    with open("4letterquiz.txt", "r") as file:
        quiz_data = [line.strip() for line in file.readlines()]
    with open("4letteranswer.txt", "r") as file:
        answer_data = [line.strip() for line in file.readlines()]
    return quiz_data, answer_data

def get_user_input(timeout, default=None):
    result = [default]

    def user_input():
        result[0] = input()

    thread = threading.Thread(target=user_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    return result[0]

def play_quiz():
    quiz_data, answer_data = load_quiz_data()
    total_score = 0

    for index in range(len(quiz_data)):
        selected_quiz, answer = quiz_data[index], answer_data[index]
        twoletter = selected_quiz[:2]  # 앞 두 글자만 제시

        print(f"퀴즈: {twoletter} ?")

        # 6초 동안 사용자 입력 받기
        user_answer = get_user_input(6, default="timeout")

        if user_answer.lower() == "quit":
            print(f"종료! 총 점수: {total_score}")
            break

        if user_answer == answer:
            total_score += 1
            print(f"정답입니다! 현재 점수: {total_score}\n")
        else:
            if user_answer == "timeout":
                print("시간 초과! 오답으로 처리합니다.\n")
            else:
                print(f"오답입니다. 현재 점수: {total_score}\n")
            restart = input("다시 시작하시겠습니까? (yes/no): ")
            if restart.lower() != "yes":
                print(f"종료! 총 점수: {total_score}")
                break

if __name__ == "__main__":
    play_quiz()
