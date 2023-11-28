import tkinter as tk
from tkinter import messagebox
import linecache
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Proverb Quiz")

        self.total_score = 0
        self.best_score = 0
        self.time_limit = 7  # 초기 제한 시간 (초)
        self.timer_id = None

        # 현재 점수를 표시할 Label 위젯
        self.score_label = tk.Label(master, text="현재 점수: 0", font=("Helvetica", 12))
        self.score_label.pack(side=tk.RIGHT, padx=10, pady=10)

        self.label = tk.Label(master, text="", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.entry = tk.Entry(master, font=("Helvetica", 12))
        self.entry.pack(pady=10)

        self.button = tk.Button(master, text="제출", command=self.check_answer)
        self.button.pack(pady=10)

        # 엔터 키와 'Return' 키를 눌렀을 때 check_answer 메서드를 호출하도록 설정
        self.master.bind('<Return>', lambda event=None: self.check_answer())

        self.generate_quiz()

    def generate_quiz(self):
        # 속담 퀴즈를 생성하고 화면에 표시합니다
        proverb = self.get_random_proverb()
        self.quiz, self.answer = self.create_quiz(proverb)
        self.label.config(text=f"다음 속담을 완성하세요: '{self.quiz}'")
        self.entry.delete(0, tk.END)  # Entry 위젯의 내용을 지웁니다

        # 초기 시간 설정
        self.remaining_time = self.time_limit
        self.update_time()

    def get_random_proverb(self):
        no = random.randint(1, 100)
        return linecache.getline('saying.txt', no).strip()

    def create_quiz(self, saying):
        words = saying.split()
        last_word = words[-1]
        words[-1] = '□' * len(last_word)
        return " ".join(words), last_word

    def check_answer(self, event=None):
        user_input = self.entry.get().strip()
        if self.timer_id:
            self.master.after_cancel(self.timer_id)  # 정답을 체크할 때 시간 멈춤
            self.timer_id = None

        if user_input.replace(" ", "") == self.answer.replace(" ", ""):
            self.total_score += 1
            if self.total_score > self.best_score:
                self.best_score = self.total_score
            messagebox.showinfo("정답", "정답입니다!")
        else:
            retry = messagebox.askquestion("틀림", f"틀렸습니다. 정답은 '{self.answer}'입니다.\n다시 시도하시겠습니까?")
            if retry == 'no':
                self.master.destroy()
            else:
                self.total_score = 0
                self.best_score = 0

        # 현재 점수를 업데이트하여 표시
        self.score_label.config(text=f"현재 점수: {self.total_score}")

        # 퀴즈 생성
        self.generate_quiz()

    def update_time(self):
        if self.remaining_time > 0:
            # 시간을 1초씩 줄이고 업데이트하는 메서드
            self.remaining_time -= 1
            self.label.config(text=f"다음 속담을 완성하세요: '{self.quiz}' (남은 시간: {self.remaining_time}초)")
            # 1초마다 업데이트
            self.timer_id = self.master.after(1000, self.update_time)
        elif self.remaining_time == 0:
            # 시간 초과 시
            self.remaining_time = -1
            if self.timer_id:
                self.master.after_cancel(self.timer_id)

            retry = messagebox.askquestion("시간 초과", "제한 시간이 초과되었습니다.\n다시 시도하시겠습니까?")
            if retry == 'no':
                self.master.destroy()
            else:
                self.total_score = 0
                self.best_score = 0
                self.generate_quiz()
        else:
            # 시간 초과 시에도 퀴즈 생성
            self.generate_quiz()

# Tkinter 애플리케이션을 시작합니다
root = tk.Tk()
app = QuizApp(root)
root.mainloop() 
