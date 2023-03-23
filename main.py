from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import *
from customtkinter import *
import pyttsx3 as ptx
import tkinter as tk
import threading
import os

PATH = os.path.dirname(os.path.realpath(__file__))
set_default_color_theme(PATH + "/files/dark-blue.json")
set_appearance_mode('dark')

class App(CTk):
    APP_NAME = "TEXT TO SPEECH"
    WIDTH = 600
    HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)
        image = Image.open(PATH + "/files/bg_gradient.jpg").resize((self.WIDTH, self.HEIGHT))
        self.bg_image = ImageTk.PhotoImage(image)
        self.image_label = CTkLabel(master=self, image=self.bg_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        icon = ImageTk.PhotoImage(file = PATH + "/files/mic.png")
        self.iconphoto(False, icon)
        self.upper_frame()
        self.lower_frame()
        
    def upper_frame(self):
        self.main_frame = CTkFrame(master=self, width=self.WIDTH, height=200)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=10, pady=10)

        self.open_file = self.load_image("/files/add-folder.png", 20, 20)

        
        self.title_label = CTkLabel(master=self.main_frame, text='TEXT TO SPEECH')
        self.title_label.place(x=220, y=10)

        self.t_input = StringVar()
        self.tinput = CTkEntry(master=self.main_frame, textvariable=self.t_input, placeholder_text=
                            'Input the words to converted to speech', placeholder_text_color='blue')
        self.tinput.configure(width=450)
        self.tinput.place(x=5, y=50)

        self.button = CTkButton(master=self.main_frame, text='CONVERT', height=32, compound='right',
                        command=self.convert_handler)
        self.button.place(x=100, y=140)

        self.browse_btn = CTkButton(master=self.main_frame, text='browse', height=32, compound='right',
            width=60, image=self.open_file, command=self.select_file)
        self.browse_btn.place(x=455, y=50)

        self.pb = CTkProgressBar(master=self.main_frame, orient='horizontal', mode='intermediate', width=450)
        self.pb.place(x=5, y=80)

        self.rate_label = CTkLabel(master=self.main_frame, text='Speech Rate: ')
        self.rate_label.place(x=0, y=100)

        self.r_input = StringVar()
        self.rate_input = CTkEntry(master=self.main_frame, textvariable=self.r_input, width=40)
        self.rate_input.place(x=120, y=100)

        self.voice_label = CTkLabel(master=self.main_frame, text='Voices: ', width=7)
        self.voice_label.place(x=0, y=100)
        self.voices_list = CTkComboBox(master=self.main_frame,
                values=['default', 'english', 'en-scottish', 'english-north',
'english_rp', 'english-us', 'en-westindies', 'swahili-test', 'english_rp+f3'])
        self.voices_list.place(x=45, y=100)

        self.save_as = CTkLabel(master=self.main_frame, text='Save AS: ', width=8)
        self.save_as.place(x=220, y=100)
        self.save_as_input = StringVar()
        self.saveas = CTkEntry(master=self.main_frame, textvariable=self.save_as_input)
        self.saveas.place(x=280, y=100)

        self.pb.set(0.001)
        self.voices_list.set("default")
        self.r_input.set(0.5)
        self.save_as_input.set("output")

    def lower_frame(self):
        self.lower_frame = CTkFrame(master=self, width=App.WIDTH, height=250)
        self.lower_frame.pack_propagate(False)
        self.lower_frame.pack(padx=10, pady=10)

    def select_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.')
        )
        filename = fd.askopenfilename(
            title='Select text file to convert' ,
            initialdir=PATH ,
            filetypes = filetypes
        )
        self.t_input.set(filename)
        return filename

    def convert(self):
        self.tts = ptx.init()
        rate = self.tts.getProperty('rate')
        selected_voice = self.voices_list.get()
        self.file_name = self.t_input.get()
        self.mp3_save = self.save_as_input.get()
        self.tts.setProperty('rate', rate - 0.3)
        self.tts.setProperty('voice', selected_voice)
        text_file = open(self.file_name, 'r+')
        text_input = text_file.read()
        self.tts.save_to_file(text_input, PATH + '/' + self.mp3_save + '.mp3')
        text_file.close()
        self.tts.runAndWait()

    def convert_handler(self):
        self.button['state'] = DISABLED
        self.convert_text = threading.Thread(target=self.convert)
        self.convert_text.start()
        self.monitor(self.convert_text)

    def monitor(self, thread):
        if thread.is_alive():
            self.after(1000, lambda: self.monitor(thread))
            self.pb.start()
        else:
            self.pb.stop()
            self.button['state'] = NORMAL
            self.convert_text.join()
    
    def load_image(self, path, image_size1, image_size2):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size1, image_size2)))

app = App()
app.mainloop()