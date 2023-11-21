import linecache
import random

def generate_quiz():
    # 'saying.txt' 파일에서 무작위로 한 줄을 읽어옵니다
    no = random.randint(1, 100)
    saying = linecache.getline('saying.txt', no).strip()
    return saying

def create_quiz(saying):
    # 속담에서 뒷부분을 네모 느낌의 빈칸으로 대체합니다
    words = saying.split()
    last_word = words[-1]
    words[-1] = '□' * len(last_word)  # 네모 느낌의 빈칸으로 대체합니다
    return " ".join(words), last_word

def main():
    total_score = 0
    best_score = 0

    while True:
        # 속담 퀴즈를 생성하고 사용자에게 제시합니다
        proverb = generate_quiz()
        quiz, answer = create_quiz(proverb)

        # 사용자에게 직접 입력을 받을 때 빈칸의 개수에 맞게 입력받도록 합니다
        while True:
            user_input = input(f"현재 총점: {total_score}, 최고 점수: {best_score}, 다음 속담을 완성하세요: '{quiz}' ").strip()
            if len(user_input) == len(answer):
                break
            else:
                print(f"입력한 글자의 개수가 맞지 않습니다. 다시 입력하세요.")

        # 정답을 체크하고 피드백을 제공합니다 (공백은 무시하여 비교)
        if user_input.replace(" ", "") == answer.replace(" ", ""):
            print("정답입니다!")
            total_score += 1
            if total_score > best_score:
                best_score = total_score
        else:
            print(f"틀렸습니다. 정답은 '{answer}'입니다.")

        # 다시 시도할지 종료할지 물어봅니다 (오답일 경우에만)
        if user_input.replace(" ", "") != answer.replace(" ", ""):
            retry = input("다시 시도하시려면 'r', 종료하시려면 'q'를 입력하세요: ")
            if retry.lower() == 'q':
                break

    print(f"퀴즈 종료! 총점: {total_score}, 최고 점수: {best_score}")

if __name__ == "__main__":
    main()
