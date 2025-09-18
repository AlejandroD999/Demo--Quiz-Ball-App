import tkinter as tk
import backend
class QuizGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.title("QuizBall")

        self.widgets()

    def widgets(self):
        
        self.header_frame = tk.Frame(master = self)
        self.header_frame.pack()


root = QuizGUI()

root.mainloop()