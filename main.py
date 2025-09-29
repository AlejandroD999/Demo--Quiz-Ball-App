from customtkinter import *
import backend

class App(CTk):

    def __init__(self):
        super().__init__()

        self.geometry("800x500")
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

        self.configure(width=800, height=500)
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
                                        wraplength=450, fg_color="#00a8e8", width=550)

        self.choices_frame = CTkFrame(self, fg_color="#3b5c69", width=445, height=300)
        self.choices_frame.propagate(False)

        self.choices_widgets = {}

        for idx, label in enumerate(["A", "B", "C", "D"]):
            frame = CTkFrame(self.choices_frame, fg_color="#00a8e8", width=420, height=65)
            button = CTkButton(frame, text=label, width=28, height=2)
            label = CTkLabel(frame, text=self.choices_list[idx], font=("Times New Roman", 20), wraplength=295)

            self.choices_widgets[label] = {"frame": frame, "button": button, "label": label}
        
        self.question_label.pack(anchor = 'n', padx=(0, 0), pady=(25, 0))
        self.choices_frame.pack(anchor = 'w', padx=(30,0), pady=(40, 0))

        for key in self.choices_widgets.keys():
            curr_frame = self.choices_widgets[key]["frame"]
            curr_frame.propagate(False)
            curr_frame.pack(padx = (5, 5), pady = (5, 5))

            curr_button = self.choices_widgets[key]["button"]
            curr_button.pack(side="left", padx=(5, 0))

            curr_label = self.choices_widgets[key]["label"]
            curr_label.pack(side="left", padx=(10, 0))


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