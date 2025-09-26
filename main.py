from customtkinter import *
import backend

class App(CTk):

    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.resizable(0, 0)

        self.title("CogniTriv")
        self.background_color = "#00171f"

        self.container = CTkFrame(self, fg_color=self.background_color)
        self.container.pack(fill="both", expand= True)

        self.pages = {}
        for Page in (HomePage, ModeSelectionPage, QuizPage, ResultsPage):
            page = Page(self.container, self)
            self.pages[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(HomePage)

    
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
        self.app_title = CTkLabel(self, text="CogniTriv", fg_color=self.controller.background_color, text_color="#007ea7",
                         font=("Times New Roman", 48)).pack(pady=(35, 0))

        self.start_button = CTkButton(self, text="Start Quiz", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3, command = self.start_quiz).pack(pady=(100, 0))
        
        self.LearnMore_button = CTkButton(self, text="Learn More", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3).pack(pady=(20, 0))

        self.exit_button = CTkButton(self, text="Exit", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3, command=lambda: quit()).pack(pady=(20, 0))

    def start_quiz(self):
        self.controller.show_page(QuizPage)

class ModeSelectionPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color= controller.background_color, corner_radius=0)
        self.controller = controller
        self.propagate(False)

        self.load_widgets()


    def load_widgets(self):

        self.buttons_frame = CTkFrame(self, fg_color=self.controller.background_color)

        self.mode_label = CTkLabel(self, text="Select a Mode", font=("Times New Roman", 54), text_color = "#007ea7",
                                                 bg_color=self.controller.background_color).pack(pady=(60, 0))

        self.buttons_frame.pack(pady=(35, 0)) 

        self.easy_button = CTkButton(self.buttons_frame, text="Easy", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=3,
                                 border_color="black", corner_radius = 3).pack(side="left",padx=10, pady=20)

        self.medium_button = CTkButton(self.buttons_frame, text="Medium", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=3,
                                 border_color="black", corner_radius = 3).pack(side="left", padx=(20, 10))

        self.hard_button = CTkButton(self.buttons_frame, text="Hard", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=3,
                                 border_color="black", corner_radius = 3).pack(side="left", padx=(20, 10))

        self.random_button = CTkButton(self, text="Random", font=("Times New Roman", 35),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 height=2,
                                 border_color="black", corner_radius = 3).pack()


class QuizPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color="#007ea7", corner_radius=0)
        self.propagate(False)

        self.quiz_backend = backend.Quiz()
        self.quiz_backend.load_questions()

        self.load_widgets()

    def load_widgets(self):

        self.question_handling()

        self.question_label = CTkLabel(self, text = self.question["text"], font=("Times New Roman", 28),
                                        wraplength=400, fg_color="#00a8e8", width=500)

        self.choices_frame = CTkFrame(self, fg_color="#00a8e8", width=300, height=212)
        self.choices_frame.propagate(False)

        #Frame A
        self.frame_a = CTkFrame(self.choices_frame, fg_color="#00a8e8",
                                width=300, height=46)
        self.frame_a.propagate(False)
        #Frame B
        self.frame_b = CTkFrame(self.choices_frame, fg_color="#00a8e8",
                                width=300, height=46)
        self.frame_b.propagate(False)
        #Frame C
        self.frame_c = CTkFrame(self.choices_frame, fg_color="#00a8e8",
                                width=300, height=46)
        self.frame_c.propagate(False)
        #Frame D
        self.frame_d = CTkFrame(self.choices_frame, fg_color="#00a8e8",
                                width=300, height=46)
        self.frame_d.propagate(False)


        self.a_button = CTkButton(self.frame_a, text="A", width=24, height=1)
        self.b_button = CTkButton(self.frame_b, text="B", width=24, height=1)
        self.c_button = CTkButton(self.frame_c, text="C", width=24, height=1)
        self.d_button = CTkButton(self.frame_d, text="D", width=24, height=1)        

        self.question_label.pack(anchor = 'n', padx=(0, 0), pady=(25, 0))
        self.choices_frame.pack(anchor = 'w', padx=(30,0), pady=(65, 0))

        self.frame_a.pack(pady=(6, 1))
        self.frame_b.pack(pady=(1, 0))
        self.frame_c.pack(pady=(1, 0))
        self.frame_d.pack(pady=(1, 6))

        self.a_button.pack(side="left", padx=(5, 2))
        self.b_button.pack(side="left", padx=(5, 2))
        self.c_button.pack(side="left", padx=(5, 2))
        self.d_button.pack(side="left", padx=(5, 2))

    def question_handling(self):
        self.question = self.quiz_backend.ask_question()

        self.choices_list = self.quiz_backend.get_possible_answers(self.question["index"])




class ResultsPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color="#003459", corner_radius=0)
        self.propagate(False)

if __name__ == '__main__':
    app = App()
    app.mainloop()