import linecache
import random

def generate_quiz():
    no = random.randint(1, 100)
    saying = linecache.getline('saying.txt', no).strip()
    return saying

def create_quiz(saying):
    words = saying.split()
    last_word = words[-1]
    words[-1] = '□' * len(last_word)  
    return " ".join(words), last_word

def main():
    total_score = 0
    best_score = 0

    while True:
        proverb = generate_quiz()
        quiz, answer = create_quiz(proverb)

        while True:
            user_input = input(f"현재 총점: {total_score}, 최고 점수: {best_score}, 다음 속담을 완성하세요: '{quiz}' ").strip()
            if len(user_input) == len(answer):
                break
            else:
                print(f"입력한 글자의 개수가 맞지 않습니다. 다시 입력하세요.")

        if user_input.replace(" ", "") == answer.replace(" ", ""):
            print("정답입니다!")
            total_score += 1
            if total_score > best_score:
                best_score = total_score
        else:
            print(f"틀렸습니다. 정답은 '{answer}'입니다.")

        if user_input.replace(" ", "") != answer.replace(" ", ""):
            retry = input("다시 시도하시려면 'r', 종료하시려면 'q'를 입력하세요: ")
            if retry.lower() == 'q':
                break

    print(f"퀴즈 종료! 총점: {total_score}, 최고 점수: {best_score}")

if __name__ == "__main__":
    main()
