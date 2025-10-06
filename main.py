from customtkinter import *
import tkinter as tk
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
        
        self.score = 0
        self.quiz_backend = backend.Quiz()
        self.quiz_backend.load_questions()

        self.load_widgets()

    def load_widgets(self):

        self.question_dict = self.question_handling()

        self.question_label = CTkLabel(self, text = self.question_dict["question"]["text"], font=("Times New Roman", 28),
                                        wraplength=450, fg_color="#00a8e8", width=550)

        self.choices_frame = CTkFrame(self, fg_color="#3b5c69", width=445, height=320)
        self.choices_frame.propagate(False)

        self.score_variable = tk.StringVar(self, value=f"Score: {self.score}")
        self.score_label = CTkLabel(self.choices_frame, textvariable = self.score_variable, font=("Times New Roman", 25),
                                anchor='w', fg_color="#3b5c69", text_color="#bfdbf7", width=345)

        self.choices_widgets = self.create_choices_widgets()

        
        self.question_label.pack(anchor = 'n', padx=(0, 0), pady=(15, 0))
        self.choices_frame.pack(anchor = 'w', padx=(30,0), pady=(35, 0))
        self.score_label.pack(anchor= 'w', padx=(15, 0), pady=(5, 0))
        
        #Pack choices widgets
        self.pack_choices_widgets()        

    def question_handling(self):
        question_attributes = {}

        question = self.quiz_backend.ask_question()
        correct_answer = self.quiz_backend._data[question["index"]]["correctAnswer"]
        choices_list = self.quiz_backend.get_possible_answers(question["index"])
        
        question_attributes = {"question": question, "correctAnswer": correct_answer, "all_choices": choices_list}

        return question_attributes

    def create_choices_widgets(self):
        widgets = {}
        
        for idx, label in enumerate(["A", "B", "C", "D"]):
            frame = CTkFrame(self.choices_frame, fg_color="#00a8e8", width=420, height=65)
            button = CTkButton(self.choices_frame, text=self.question_dict["all_choices"][idx], width=420, height=65)
            button._text_label.configure(wraplength=295)

            widgets[label] = {"frame": frame, "button": button}
        
        return widgets

    def pack_choices_widgets(self):

        for key in self.choices_widgets.keys():
            curr_button = self.choices_widgets[key]["button"]
            curr_button.pack(padx=(0, 0), pady=(3, 3))
            curr_button.configure(command=lambda k=key: self.check_answer(k))



    def check_answer(self, answer_frame):
        button = self.choices_widgets[answer_frame]["button"]
        answer_text = button.cget("text")

        if answer_text == self.question_dict["correctAnswer"]:
            self.increase_score()
            self.quiz_backend.asked_questions.add(self.question_dict["question"]["index"])
            self.question_dict = self.question_handling()
            self.update_question_widgets()

    def update_question_widgets(self):
        self.question_label.configure(text=self.question_dict["question"]["text"])
        
        for idx, letter in enumerate(["A", "B", "C", "D"]):
            self.choices_widgets[letter]["button"].configure(
                text=self.question_dict["all_choices"][idx]
            )

    def increase_score(self):
            self.score += 1
            self.score_variable.set(f"Score: {self.score}")



class ResultsPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color="#003459", corner_radius=0)
        self.propagate(False)

if __name__ == '__main__':
    app = App()
    app.mainloop()