import tkinter as tk

class QuizGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.title("QuizBall")

    def widgets(self):
        pass


root = QuizGUI()

root.mainloop()