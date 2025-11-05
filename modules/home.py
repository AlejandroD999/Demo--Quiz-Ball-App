import os
import webbrowser
from PIL import Image
from customtkinter import CTkButton, CTkLabel, CTkImage, CTkFrame

class HomePage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color = controller.background_color, corner_radius=0)
        self.controller = controller

        self.configure(width=self.controller.window_width, height=self.controller.window_height)
        self.propagate(False)

        self.load_widgets()

    def load_widgets(self):

        self.load_image()

        CTkLabel(self, text="CogniTriv", fg_color=self.controller.background_color, 
                                  text_color="#a4161a", font=("Courier 10 Pitch", 54)).pack(pady=(30, 0))

        CTkButton(self, text="Start", font=("Times New Roman", 31),
                        text_color = "black", fg_color = '#ba181b', hover_color = '#a4161a', height= int(self.controller.window_height / 12),
                        border_color="#d3d3d3", corner_radius = 3, border_width= 1,
                        command= lambda: self.controller.show_page("QuizPage")).pack(padx=(27, 0), pady=(80, 0))
        
        CTkButton(self, text="Learn More", font=("Times New Roman", 31), height= int(self.controller.window_height / 12),
                                 text_color = "black", fg_color = '#ba181b', hover_color = '#a4161a',
                                 border_color="#d3d3d3", corner_radius = 3, border_width=1,
                                 command=lambda: self.open_website("learn_more", "index.html")).pack(padx=(27, 0), pady=(20, 0))        

        CTkButton(self, text="Exit", font=("Times New Roman", 31), height= int(self.controller.window_height / 12), 
                                 text_color = "black", fg_color = '#ba181b', hover_color = '#a4161a',
                                 border_color="#d3d3d3", corner_radius = 3, border_width= 1,
                                 command=lambda: self.controller.destroy()).pack(padx=(27, 0), pady=(20, 0))

    def load_image(self):
        img_path = os.path.join(self.controller.curr_dir, "assets", "icon", "gui_icon.png")

        try:
            pil_image = Image.open(img_path)
        except FileNotFoundError:
            print("Error: 'gui_icon.png', could not be found")
        self._resized_image = pil_image.resize((100, 100), Image.LANCZOS)
        self._ctk_image = CTkImage(self._resized_image, self._resized_image,
                                   size=(100,100))

        image_label = CTkLabel(self, image=self._ctk_image, text='')
        image_label.place(x= 0, y=0)


    def open_website(self, file_parent, file_name):
        file_address = os.path.join(self.controller.curr_dir, file_parent, file_name)
    
        webbrowser.open(file_address)