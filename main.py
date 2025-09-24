import customtkinter
import backend

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.title("QuizBall")
        self.background_color = "#00171f"

        self.container = customtkinter.CTkFrame(self)
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


class HomePage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):

        super().__init__(parent, fg_color = controller.background_color, corner_radius=0)
        self.controller = controller

        self.configure(width=600, height=400)
        self.propagate(False)

        app_title = customtkinter.CTkLabel(self, text="Project Name", fg_color=self.controller.background_color, text_color="#007ea7",
                         font=("Times New Roman", 48)).pack(pady=(35, 0))

        start_button = customtkinter.CTkButton(self, text="Start Quiz", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3).pack(pady=(100, 0))
        
        LearnMore_button = customtkinter.CTkButton(self, text="Learn More", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3).pack(pady=(20, 0))

        exit_button = customtkinter.CTkButton(self, text="Exit", font=("Times New Roman", 25),
                                 text_color = "black", fg_color = '#007ea7', hover_color = '#00a8e8',
                                 border_color="black", corner_radius = 3).pack(pady=(20, 0))

class ModeSelectionPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#003459")

        label = customtkinter.CTkLabel(self, text="Modes").pack(pady = 20)

class QuizBallPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color='#003459')

class ResultsPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#003459")


if __name__ == '__main__':
    app = App()
    app.mainloop()