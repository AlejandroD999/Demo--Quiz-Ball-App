import tkinter as tk
import backend

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("QuizBall")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand= True)

        self.pages = {}
        for Page in (HomePage, ModeSelectionPage, QuizBallPage, ResultsPage):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(HomePage)

    
    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.config(bg='green', width=600, height=400)
        self.propagate(False)

        label = tk.Label(self, text="Home Page", fg='white', bg="black").pack(pady=20)


class ModeSelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="grey")

        label = tk.Label(self, text="Modes").pack(pady = 20)

class QuizBallPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='red')

class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="blue")


if __name__ == '__main__':
    app = App()
    app.mainloop()