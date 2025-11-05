from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkToplevel
from tkinter import StringVar

class QuizPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color="#161a1d", corner_radius=0)
        self.propagate(False)

        self.quiz_backend = self.controller.backend
        self.quiz_backend.load_questions()

        self.attempts = 0
        self.question_number = self.quiz_backend.total_questions_answered + 1
        
        self.load_widgets()

    def load_widgets(self):

        self.question_dict = self.question_handling()

        self.question_label = CTkLabel(self, text = self.question_dict["question"]["text"], font=("Times New Roman", 28),
                                        wraplength=650, fg_color=self.controller.background_color, text_color= self.controller.default_button_text_color, 
                                        width=750)

        self.choices_frame = CTkFrame(self, fg_color="#0b090a", width=445, height=320)
        self.choices_frame.propagate(False)

        self.question_count_variable = StringVar(self, value=f"Question #{self.question_number}")
        self.question_count_label = CTkLabel(self.choices_frame, textvariable = self.question_count_variable, font=("Times New Roman", 25),
                                anchor='w', fg_color="#0b090a", text_color="#d3d3d3", width=345)

        self.choices_widgets = self.create_choices_widgets()

        self.finish_button = CTkButton(self, text="Finish", font=("Times New Roman", 16), width=115, height=50,
                                       fg_color= "#ba181b", hover_color= "#660708", 
                                       state="disabled", command=self.prompt_for_results)

        #Pack widgets
        self.question_label.pack(anchor = 'n', padx=(0, 0), pady=(15, 0))

        self.choices_frame.place(x=self.controller.window_width - (self.controller.window_width * .97),
                                 y=self.controller.window_height - (self.controller.window_height * .70))
        self.question_count_label.pack(anchor= 'w', padx=(15, 0), pady=(5, 0))

        self.pack_choices_widgets()
        self.finish_button.place(x=(self.controller.window_width - 130), y=(self.controller.window_height - 60))

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
                               fg_color=self.controller.default_button_color, hover_color=self.controller.default_hover_color,
                               text_color=self.controller.default_button_text_color,
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
                fg_color= self.controller.default_button_color,
                hover_color = self.controller.default_hover_color,
                state="normal"
            )
        self.finish_button.configure(state="normal")

    def increase_score(self):
            if self.attempts < 1:
                self.quiz_backend.score += 1

    def prompt_for_results(self):
        width = int(self.winfo_screenwidth() / 4)
        height = int(self.winfo_screenheight() / 8)

        background_color = self.controller.background_color
        top = CTkToplevel()

        top.title("Finish Quiz")
        top.config(bg=background_color)
        top.geometry(f"{width}x{height}")
        top.resizable(False, False)

        label = CTkLabel(top, text="Do you want to finish?", font=("Times New Roman", 24),
                         bg_color=background_color, text_color="#f5f3f4")
        buttons_frame = CTkFrame(top, width=185, height= 10, fg_color=background_color)

        confirm_button = CTkButton(buttons_frame, text="Finish", width=90, command=lambda: self.prompt_confirm_action(top),
                                   fg_color=self.controller.default_button_color, hover_color= self.controller.default_hover_color,
                                   text_color="black")

        dismiss_button = CTkButton(buttons_frame, text="Dismiss", width=90, command=top.destroy,
                                   fg_color=self.controller.default_button_color, hover_color= self.controller.default_hover_color,
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
        self.controller.show_page("ResultsPage")
        return