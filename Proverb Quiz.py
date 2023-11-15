import random

proverb_kor = {"가는 날이": "장날이다", "싼 게": "비지떡", "백지장도": "맞들면 낫다", "계란으로": "바위치기"}

proverbs = list(proverb_kor.items())
random.shuffle(proverbs)

for i, (x, y) in enumerate(proverbs, start=1):
    user_input = input(f"{i}. {x} ")
    if user_input.strip() == y:  
        print("정답입니다")
    else:
        print(f"틀렸습니다. 정답은 {y}입니다.")

