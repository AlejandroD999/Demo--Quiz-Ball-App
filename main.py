from customtkinter import *
from modules import backend, home, quiz, results
import os
from PIL import ImageTk, Image
import platform

class App(CTk):

    def __init__(self):
        super().__init__()
        self.window_width = int((self.winfo_screenwidth() // 2) + (self.winfo_screenwidth() / 25))
        self.window_height = int((self.winfo_screenheight() // 2) + (self.winfo_screenheight() / 9))
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))

        self.background_color = "#161a1d"
        self.default_button_color = "#ba181b"
        self.default_hover_color = "#a4161a"
        self.default_button_text_color = "#d3d3d3"

        self.geometry(f"{self.window_width}x{self.window_height}")
        self.configure(bg_color=self.background_color)
        self._set_appearance_mode("dark")


        self.set_icon()
        self.resizable(0, 0)
        self.title("CogniTriv")


        self.backend = backend.Quiz()
        self.container = CTkFrame(self, fg_color=self.background_color)
        self.container.pack(fill="both", expand= True)

        self.pages = {}
        self._init_pages()
        self.show_page("HomePage")

    def _init_pages(self):
        for PageClass in (home.HomePage, quiz.QuizPage, results.ResultsPage):
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky='nsew')
    
    def show_page(self, page_class):
        page = self.pages[page_class]
        page.lift()

    def set_icon(self):
        ico_address = os.path.join(self.curr_dir, "assets", "icon", "gui_icon.ico")
        png_address = os.path.join(self.curr_dir, "assets", "icon", "gui_icon.png")
        system = platform.system()

        try:
            if system == "Windows":
                self.iconbitmap(ico_address)
            else:
                self._icon_img = ImageTk.PhotoImage(Image.open(png_address))
                self.iconphoto(False, self._icon_img)
        except FileNotFoundError as fe:
            raise FileNotFoundError(f"File could not be found {fe}")

if __name__ == '__main__':
    app = App()
    app.mainloop()