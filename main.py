import tkinter as tk
import backend

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.title("QuizBall")

        self.widgets()

    def widgets(self):
        self.current_view = self.home_frame
        self.home_frame = tk.Frame(master = self)

    def show_home(self):

        self.current_view.pack_forget()
        self.home_frame.pack(self, bg="black")

    def show_other(self, current_view):
        pass


if __name__ == '__main__':
    app = App()
    app.mainloop()