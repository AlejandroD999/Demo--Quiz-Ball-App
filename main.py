import backend
from customtkinter import *
import os
import tkinter as tk


class App(CTk):

    def __init__(self):
        super().__init__()
        self.screen_with = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.geometry(f"{800}x{500}")
        self.resizable(1, 1)
        self.title("CogniTriv")
        self.background_color = "#161a1d"

        self.backend = backend.Quiz()
        self.container = CTkFrame(self, fg_color=self.background_color)
        self.container.pack(fill="both", expand= True)

        self.pages = {}
        for Page in (HomePage, LearnMorePage, ModeSelectionPage, QuizPage, ResultsPage):
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

        self.configure(width=800, height=800)
        self.propagate(False)

        self.load_widgets()

    def load_widgets(self):
        self.app_title = CTkLabel(self, text="CogniTriv", fg_color=self.controller.background_color, 
                                  text_color="#a4161a", font=("Calibri", 54, "bold")).pack(pady=(30, 0))

        self.start_button = CTkButton(self, text="Start", font=("Times New Roman", 31),
                                 text_color = "black", fg_color = '#ba181b', hover_color = '#a4161a',
                                 border_color="#d3d3d3", corner_radius = 3, border_width= 1,
                                 command= lambda: self.controller.show_page(QuizPage)).pack(pady=(100, 0))
        
        self.LearnMore_button = CTkButton(self, text="Learn More", font=("Times New Roman", 32),
                                 text_color = "black", fg_color = '#ba181b', hover_color = '#a4161a',
                                 border_color="#d3d3d3", corner_radius = 3, border_width=1,
                                 command=lambda: self.controller.show_page(LearnMorePage)).pack(pady=(20, 0))        

        self.exit_button = CTkButton(self, text="Exit", font=("Times New Roman", 31),
                                 text_color = "black", fg_color = '#ba181b', hover_color = '#a4161a',
                                 border_color="#d3d3d3", corner_radius = 3, border_width= 1,
                                 command=lambda: quit()).pack(pady=(20, 0))


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
        super().__init__(parent, fg_color="#161a1d", corner_radius=0)
        self.propagate(False)
        self.default_button_color = "#ba181b"
        self.default_hover_color = "#a4161a"
        self.default_button_text_color = "#d3d3d3"

        self.quiz_backend = self.controller.backend
        self.quiz_backend.load_questions()

        self.attempts = 0
        self.question_number = self.quiz_backend.total_questions_answered + 1
        
        self.load_widgets()

    def load_widgets(self):

        self.question_dict = self.question_handling()

        self.question_label = CTkLabel(self, text = self.question_dict["question"]["text"], font=("Times New Roman", 28),
                                        wraplength=650, fg_color=self.controller.background_color, text_color= self.default_button_text_color, 
                                        width=750)

        self.choices_frame = CTkFrame(self, fg_color="#0b090a", width=445, height=320)
        self.choices_frame.propagate(False)

        self.question_count_variable = tk.StringVar(self, value=f"Question #{self.question_number}")
        self.question_count_label = CTkLabel(self.choices_frame, textvariable = self.question_count_variable, font=("Times New Roman", 25),
                                anchor='w', fg_color="#0b090a", text_color="#d3d3d3", width=345)

        self.choices_widgets = self.create_choices_widgets()

        self.finish_button = CTkButton(self, text="Finish", font=("Times New Roman", 16), width=115, height=50,
                                       fg_color= "#ba181b", hover_color= "#660708", 
                                       state="disabled", command=self.prompt_for_results)

        #Pack widgets
        self.question_label.pack(anchor = 'n', padx=(0, 0), pady=(15, 0))

        self.choices_frame.place(x=30, y=155)
        self.question_count_label.pack(anchor= 'w', padx=(15, 0), pady=(5, 0))

        self.pack_choices_widgets()
        self.finish_button.place(x=650, y=420)

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
#            frame = CTkFrame(self.choices_frame, fg_color="#00a8e8", width=420, height=65)
            button = CTkButton(self.choices_frame, 
                               fg_color=self.default_button_color, hover_color=self.default_hover_color,
                               text_color=self.default_button_text_color,
                               text=self.question_dict["all_choices"][idx],
                               width=420, height=65)
            button._text_label.configure(wraplength=295)
            widgets[label] = {"button": button}
        
        return widgets

    def pack_choices_widgets(self):

        for key in self.choices_widgets.keys():
            curr_button = self.choices_widgets[key]["button"]
            curr_button.pack(padx=(0, 0), pady=(3, 3))
            curr_button.configure(command=lambda k=key: self.check_answer(k))

    def check_answer(self, answer_frame):
        incorrect_color = ["#850608", "#550C0E"]
        correct_color = ["#236E0D", "#016801"]

        
        button = self.choices_widgets[answer_frame]["button"]
        answer_text = button.cget("text")

        for key in self.choices_widgets:
            self.choices_widgets[key]["button"].configure(state="disabled")

        if answer_text == self.question_dict["correctAnswer"]:
            button.configure(fg_color= correct_color[0], hover_color = correct_color[1])
            self.attempts = 0
        
        else:
            self.attempts += 1
            button.configure(fg_color= incorrect_color[0], hover_color=incorrect_color[1])
            self.highlight_answer(correct_color[0], correct_color[1])

        self.after(1750, self.next_question)

    # Modifies color of button with correct answer
    def highlight_answer(self, color, hover_color):
            for key in self.choices_widgets.keys():
                correct_button = self.choices_widgets[key]["button"]

                if correct_button.cget("text") == self.question_dict["correctAnswer"]:
                    correct_button.configure(fg_color = color,
                                             hover_color = hover_color)
                    return

    #Updates window to show the next question
    def next_question(self):
        #Adjust values
        self.increase_score()
        self.quiz_backend.total_questions_answered += 1
        self.question_number = self.quiz_backend.total_questions_answered + 1
        self.quiz_backend.asked_questions.add(self.question_dict["question"]["index"])
        self.question_dict = self.question_handling()
        #Update values
        self.question_label.configure(text=self.question_dict["question"]["text"])
        self.question_count_variable.set(f"Question #{self.question_number}")
        self.attempts = 0
        
        for idx, letter in enumerate(["A", "B", "C", "D"]):
            btn = self.choices_widgets[letter]["button"]
            btn.configure(
                text=self.question_dict["all_choices"][idx],
                fg_color= self.default_button_color,
                hover_color = self.default_hover_color,
                state="normal"
            )
        self.finish_button.configure(state="normal")

    def increase_score(self):
            if self.attempts < 1:
                self.quiz_backend.score += 1

    def prompt_for_results(self):
        background_color = self.controller.background_color
        top = CTkToplevel()

        top.title("Finish Quiz")
        top.config(bg=background_color)
        top.geometry("350x100")
        top.resizable(False, False)

        label = CTkLabel(top, text="Do you want to finish?", font=("Times New Roman", 24),
                         bg_color=background_color, text_color="#f5f3f4")
        buttons_frame = CTkFrame(top, width=185, height= 10, fg_color=background_color)

        confirm_button = CTkButton(buttons_frame, text="Finish", width=90, command=lambda: self.prompt_confirm_action(top),
                                   fg_color=self.default_button_color, hover_color= self.default_hover_color,
                                   text_color="black")

        dismiss_button = CTkButton(buttons_frame, text="Dismiss", width=90, command=top.destroy,
                                   fg_color=self.default_button_color, hover_color= self.default_hover_color,
                                   text_color="black")

        label.pack()

        buttons_frame.pack(anchor="e", padx=(0, 10), pady=(35, 0))
        confirm_button.pack(side="right", padx=(5, 0))
        dismiss_button.pack(side="left")

        top.after(100, lambda: top.grab_set())

    def prompt_confirm_action(self, root):
        self.show_results_page()
        root.destroy()

    def show_results_page(self):
        self.controller.show_page(ResultsPage)
        return

class LearnMorePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color = controller.background_color)
        self.controller = controller
        self.propagate(False)


        self.load_widgets()

    def load_widgets(self):

        self.content = self.pull_file_content("learn_more.txt", "resources")
        
        self.content_frame = CTkScrollableFrame(self, 475, 500, fg_color = "#595a5c",
                                                border_width=3, border_color="#f5f3f4")

        self.content_label = CTkLabel(self.content_frame, text=self.content, font=("Times New Roman", 16),
                                      text_color = "#f5f3f4")

        self.content_frame.pack(anchor="e", pady=(0, 0))
        self.content_label.pack(anchor="w", padx=20, pady=(0, 0))



    def pull_file_content(self, file_name, folder):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        file_address = os.path.join(current_dir, folder, file_name)

        try:
            with open(file_address, "r") as file:
                content = file.read()

            return content

        except FileNotFoundError:
            raise FileNotFoundError("File was not found")

class ResultsPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color=self.controller.background_color, corner_radius=0)
        self.propagate(False)

        self.quiz_backend = self.controller.backend
        self.load_widgets()

    def load_widgets(self):
        self.results_title = CTkLabel(self, text="Results", fg_color=self.controller.background_color, text_color= "#ba181b",
                        font=("Times New Roman", 64, "italic")).pack(pady=(20, 5))
        
        self.load_results_button = CTkButton(self, text="Load Results", width=270, height=58, fg_color= "#a4161a",
                                             text_color= "#f5f3f4", hover_color = "#660708", border_width=4, border_color= "#d3d3d3",
                                             command=self.load_results)

        self.results_frame = CTkFrame(self, width= 562, height= 338, corner_radius= 2, border_width= 3,
                                      fg_color="#ba181b", border_color= "#ffffff")
        self.results_frame.propagate(False)

        self.load_results_button.pack()        


    def load_results(self):
        self.grade = self.get_grade()
        self.load_results_button.pack_forget()

        self.grade_label = CTkLabel(self.results_frame, text=f"{self.grade["grade"]}({self.grade["score"]}%)",
                                    font=("Times New Roman", 36), text_color= "#f5f3f4")

        self.passed_label = CTkLabel(self.results_frame, text="You nailed it! Keep up the great performance." if self.grade["passed"] else "Don’t be discouraged—every attempt is a step toward improvement.",
                                     font=("Times New Roman", 24, "italic"), text_color = "#ffffff",
                                     wraplength=540, justify="left")
        self.correct_answers_label = CTkLabel(self.results_frame, text=f"Total Correct Answers: {self.quiz_backend.score}",
                                              font=("Times New Roman", 24), text_color = "#d3d3d3")
        self.questions_answered_label = CTkLabel(self.results_frame, text=f"Total Questions Answered: {self.quiz_backend.total_questions_answered}",
                                           font=("Times New Roman", 24), text_color = "#d3d3d3")


        self.results_frame.pack()
        self.grade_label.pack(anchor="w", padx=(20, 0), pady=(5, 0))
        self.passed_label.pack(anchor="w", padx=(20, 0))
        self.correct_answers_label.pack(anchor="w", padx=(20, 0), pady=(25, 0))
        self.questions_answered_label.pack(anchor="w",padx=(20, 0))
        



    def get_grade(self):
        grades = {"F": 0, "D-": 52, "D": 60, "C": 70, "C+": 76.67, "B-": 80, "B": 83.33, "B+": 86.67, "A-": 90, "A": 93.33}
        self.score_percentage = round((float(self.quiz_backend.score / self.quiz_backend.total_questions_answered) * 100), 2)

        grade = ""
        for key in grades.keys():

            if grades[key] <= self.score_percentage:
                grade = key

        return {"score": self.score_percentage,
                "grade": grade,
                "passed": True if self.score_percentage >= 70 else False
                }





if __name__ == '__main__':
    app = App()
    app.mainloop()