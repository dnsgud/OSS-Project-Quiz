def load_quiz_data():
    with open("4글자퀴즈.txt", "r") as file:
        quiz_data = [line.strip() for line in file.readlines()]
    with open("4글자퀴즈정답.txt", "r") as file:
        answer_data = [line.strip() for line in file.readlines()]
    return quiz_data, answer_data
  
def play_quiz():
    quiz_data, answer_data = load_quiz_data()

    for index in range(len(quiz_data)):
        selected_quiz, answer = quiz_data[index], answer_data[index]
        twoletter = selected_quiz[:2]  # 앞 두 글자만 제시

        print(f"퀴즈: {twoletter} ?")
        user_answer = input("정답을 입력하세요 (종료하려면 'quit' 입력): ")

        if user_answer == "quit":
            print("퀴즈 프로그램을 종료합니다.")
            break

        if user_answer == answer:
            print("정답입니다!\n")
        else:
            print("오답입니다!.\n")

if __name__ == "__main__":
    play_quiz()
