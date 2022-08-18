import json
import random
import time
import tkinter
from tkinter import Label, Button, Entry, END, WORD, Text, messagebox


class TypingSpeed():
    def __init__(self):
        super().__init__()
        self.window = tkinter.Tk()
        self.window.title('Typing Speed Test')
        self.window.geometry('800x800')
        self.window.eval('tk::PlaceWindow . center')
        self.window.config(pady=50, padx=10, bg="white")

        ##VARIABLES
        self.typing_speed = 0
        self.correct_words = 0
        (self.hours, self.mins, self.secs) = (0, 0, 0)
        self.time_left = self._time_left_calc()
        self.tick = False
        self.t = 15
        self.random_paragraphs = self.get_paragrahs()

        ##ENTRY
        self.text_entry = Entry(self.window, width=75, state="disabled")
        self.text_entry.grid(column=0, row=3, columnspan=4, sticky='we', ipady=10)

        ##TEXTBOX
        self.text_box = Text(self.window, height=12, bg="lightgrey", pady=5, font=("Times", 12))
        self.text_box.grid(column=0, row=1, columnspan=4)
        self.text_box.insert(END, self.random_paragraphs)
        self.text_box.config(wrap=WORD)

        ###LABELS
        self.header_label = Label(self.window, text='Get your typing speed in words per minute(wpm)',
                                  font=("Bebas Neue", 15), bg="white")
        self.header_label.grid(column=0, row=0, columnspan=4)
        self.timer_label = Label(self.window, text=self.time_left, font=('Digital-7', 15, "bold"), fg="red", bg="white")
        self.timer_label.grid(column=2, row=2, columnspan=2, pady=10)
        self.high_score_label = Label(self.window, text=f"High Scores: {self._get_high_scores()}")
        self.high_score_label.grid(column=0, row=2, columnspan=2)
        self.speed_label = Label(text=f"WPM : {self.typing_speed} wpm", bg="white")
        self.speed_label.grid(column=1, row=4)
        self.correct_words_label = Label(text=f"CPM : {self.correct_words} wpm", bg="white")
        self.correct_words_label.grid(column=0, row=4)

        ###BUTTONS
        self.start_test_button = Button(text="Start the test", bg="white", highlightthickness=0,
                                        command=self._start_test)
        self.start_test_button.grid(column=0, row=5, columnspan=2, pady=10)
        self.reset_test_button = Button(text="Reset test", bg="white", highlightthickness=0, command=self._reset_test)
        self.reset_test_button.grid(column=2, row=5, columnspan=2, pady=10)

        ###ANALYSIS SECTION

        self.window.mainloop()

    def _start_test(self):
        self.tick = True
        self._countdown()
        if self.tick:
            text = self.text_entry.get()
            self._calculate_speed(text, 1)
            self._reset_test()
            self.window.update()

    def _calculate_speed(self, text, duration_in_minutes):
        length_of_text = len(text.split())
        self.typing_speed = int(length_of_text / duration_in_minutes)
        self._check_scores()

    def _countdown(self):
        """timer"""
        if self.tick:
            self.text_entry.config(state="normal")
            if self.t != -1:
                self._update_timer()
                self.t -= 1
                time.sleep(1)
                self.window.update()
                self._countdown()

    def _update_timer(self):
        self.mins, self.secs = divmod(self.t, 60)
        self.hours, self.mins = divmod(self.mins, 60)
        self.timer_label.config(text=self._time_left_calc())

    def _time_left_calc(self):
        return f"{self.hours:02d}:{self.mins:02d}:{self.secs:02d}"

    def _reset_test(self):
        self._reset_variables()
        self.high_score_label.config(text=f"High Scores: {self._get_high_scores()}")
        self.timer_label.config(text=self._time_left_calc())
        self.text_box.delete(1.0, END)
        self.text_box.insert(END, self.random_paragraphs)
        self.text_entry.delete(0, END)
        self.text_entry.config(state="disabled")

    def _check_scores(self):
        scores = self._get_high_scores()
        self._time_up_info(scores)
        if scores.count(self.typing_speed) > 0:
            return
        scores.append(self.typing_speed)
        scores.sort(reverse=True)
        scores = scores[0:3]
        with open("data.json", "rb") as data:
            user_data = json.load(data)
        user_data["scores"] = scores
        with open("data.json", "w") as f:
            json.dump(user_data, f)

    def _time_up_info(self, scores):
        if self.typing_speed > scores[0]:
            message = f"NEW HIGH SCORE!!\n\nYour typing speed was {self.typing_speed} WPM"
        else:
            message = f"Your typing speed was {self.typing_speed} WPM"
        messagebox.showinfo(title="Time up", message=message)
        self.speed_label.config(text=f"WPM : {self.typing_speed} wpm")

    def _reset_variables(self):
        self.tick = False
        (self.hours, self.mins, self.secs) = (0, 0, 0)
        self.correct_words = 0
        self.typing_speed = 0
        self.t = 60
        self.random_paragraphs = self.get_paragrahs()

    def _get_high_scores(self):
        with open("data.json", "rb") as data:
            high_scores = json.load(data)['scores']
            return high_scores

    def _compare_typed_text(self):
        print(self.random_paragraphs.split(" "))

        pass

    def get_paragrahs(self):
        with open("data.json", "rb") as data:
            return random.choice(json.load(data)['text'])


if __name__ == "__main__":
    ws = TypingSpeed()
