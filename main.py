from customtkinter import *
import backend

class App(CTk):

    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.resizable(0, 0)

        self.title("QuizBall")
        self.background_color = "#00171f"

        self.container = CTkFrame(self)
        self.container.pack(fill="both", expand= True)

        self.pages = {}
        for Page in (HomePage, ModeSelectionPage, QuizBallPage, ResultsPage):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(ModeSelectionPage)

    
    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()


class HomePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color = controller.background_color, corner_radius=0)
        self.controller = controller

        self.configure(width=600, height=400)
        self.propagate(False)

        self.load_widgets()

    def load_widgets(self):
        self.app_title = CTkLabel(self, text="Project Name", fg_color=self.controller.background_color, text_color="#007ea7",
                         font=("Times New Roman", 48)).pack(pady=(35, 0))

        self.start_button = CTkButton(self, text="Start Quiz", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3).pack(pady=(100, 0))
        
        self.LearnMore_button = CTkButton(self, text="Learn More", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3).pack(pady=(20, 0))

        self.exit_button = CTkButton(self, text="Exit", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3, command=lambda: quit()).pack(pady=(20, 0))

class ModeSelectionPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color= controller.background_color, corner_radius=0)
        self.controller = controller
        self.propagate(False)

        self.load_widgets()


    def load_widgets(self):

        self.mode_label = CTkLabel(self, text="Select a Mode", font=("Times New Roman", 54), text_color = "#007ea7",
                                                 bg_color=self.controller.background_color).pack(pady=(60, 0))

        self.easy_button = CTkButton(self, text="Easy", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=3,
                                 border_color="black", corner_radius = 3).pack(side="left", padx=(60, 0), pady=(0, 45))

        self.medium_button = CTkButton(self, text="Medium", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=3,
                                 border_color="black", corner_radius = 3).pack(side="left", padx=(20, 0),pady=(0, 45))

        self.hard_button = CTkButton(self, text="Hard", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=3,
                                 border_color="black", corner_radius = 3).pack(side="left", padx=(20, 0),pady=(0, 45))

class QuizBallPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color=self.controller.background_color, corner_radius=0)
        self.propagate(False)


class ResultsPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#003459", corner_radius=0)
        self.propagate(False)

if __name__ == '__main__':
    app = App()
    app.mainloop()