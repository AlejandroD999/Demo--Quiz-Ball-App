from customtkinter import CTkFrame, CTkButton, CTkLabel

class ResultsPage(CTkFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, fg_color=self.controller.background_color, corner_radius=0)
        self.propagate(False)


        self.quiz_backend = self.controller.backend
        self.load_widgets()

    def load_widgets(self):
        self.results_title = CTkLabel(self, text="Results", fg_color=self.controller.background_color, text_color= "#ba181b",
                        font=("Courier 10 Pitch", 64, "italic")).pack(pady=(20, 5))
        
        self.load_results_button = CTkButton(self, text="Load Results", width=270, height=58, fg_color= "#a4161a",
                                             text_color= "#f5f3f4", hover_color = "#660708", border_width=4, border_color= "#d3d3d3",
                                             command=self.load_results)

        self.results_frame = CTkFrame(self, width= 562, height= 338, corner_radius= 2, border_width= 3,
                                      fg_color="#595a5c", border_color= "#ffffff")
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

        self.retake_button = CTkButton(self.results_frame, text="Retake Quiz", width=115, height=50,
                                          fg_color=self.controller.default_button_color, hover_color=self.controller.default_hover_color,
                                            command=lambda: self.retake())

        results_frame_width = self.results_frame.winfo_reqwidth()
        results_frame_height = self.results_frame.winfo_reqheight()
        retake_button_width = self.retake_button.winfo_reqwidth()
        retake_button_height = self.retake_button.winfo_reqheight()


        self.results_frame.pack()
        self.grade_label.pack(anchor="w", padx=(20, 0), pady=(5, 0))
        self.passed_label.pack(anchor="w", padx=(20, 0))
        self.correct_answers_label.pack(anchor="w", padx=(20, 0), pady=(25, 0))
        self.questions_answered_label.pack(anchor="w",padx=(20, 0))
        self.retake_button.place(x=(results_frame_width - ((results_frame_width / 5) + (retake_button_width / 16))),
                                 y= (results_frame_height - ((results_frame_height / 8) + (retake_button_height / 3)))
                                 )

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

    def retake(self):
        self.controller.backend.reset()

        for page in self.controller.pages.values():
            page.destroy()

        self.controller.pages.clear()
        self.controller._init_pages()


        self.controller.show_page("HomePage")