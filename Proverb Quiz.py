dict_eng = {"가는 날이" : "장날이다", "싼 게" : "비지떡", "백지장도" : "맞들면 낫다", "계란으로" : "바위치기"}
for i in dict_eng:
    user_input = input(f"{i}")
    if user_input == dict_eng[i]:
        print("정답입니다")
    else:
        print(f"틀렸습니다. 정답은 {dict_eng[i]}입니다.")
