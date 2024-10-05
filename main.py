import yt_dlp
import os
import customtkinter as ctk
from tkinter import *
from PIL import Image
import shutil

class WidgetFact:
    def __init__(self ,coordinatex = 0,coordinatey =0,title = None, height = 15,
                 width = 50 ,text = "", type = "Label" ,command = None,values = None, font_size = "10",image_name = "",image_size_x = None,image_size_y= None):
        self.coordinatex = coordinatex
        self.coordinatey = coordinatey
        self.command = command
        self.height = height
        self.width = width
        self.text = text
        self.type = type
        self.title = title
        self.values = values
        self.font_size = int(font_size)
        self.image_name = image_name
        self.image_size_x = image_size_x
        self.image_size_y = image_size_y
        self.placewidget()
    #-------create a widget---------#
    def placewidget(self):
        #create a Label
        if self.type == "Label":
            self.widget = ctk.CTkLabel(root, text = self.text, height = self.height,width = self.width,font=("Bold",self.font_size))
        #create a Button
        elif self.type == "Button":
            self.widget = ctk.CTkButton(root, text=self.text, height=self.height, width=self.width,command= self.command)
        #create an Entry
        elif self.type == "Entry":
            self.widget = ctk.CTkEntry(root, height=self.height, width=self.width)
        #create a Tabview
        elif self.type == "TabView":
            self.widget = ctk.CTkTabview(root, height=self.height, width=self.width)
        #create a Combobox
        elif self.type == "ComboBox":
            self.widget = ctk.CTkComboBox(root,height=self.height,width=self.width,values= self.values,state="readonly",button_color="lightblue")
        elif self.type == "Frame":
            self.widget = ctk.CTkFrame(root, height=self.height, width=self.width)
        elif self.type == "Image":
            image = ctk.CTkImage(dark_image=Image.open(f"images/{self.image_name}"),size=(self.image_size_x,self.image_size_y))
            self.widget = ctk.CTkLabel(root, text="", image=image)
        #-------------place-widget------------------#


        self.widget.place(x = self.coordinatex, y = self.coordinatey)

class Windows:
    def __init__(self):
        self.main_window()
        root.geometry("600x500")
        ctk.set_appearance_mode("dark")
        root.mainloop()

    def main_window(self):
        for widget in root.winfo_children():
            widget.destroy()
        self.link_text = WidgetFact(50,50, text="Download your music now !",type="Label",font_size="20")
        WidgetFact(50, 90, text="Enter your youtube music link here :", type="Label", font_size="15")
        self.video_link = WidgetFact(50, 130, height=30, width=500, type="Entry")
        self.download_button = WidgetFact(250, 170, text="download", command=self.video_downloading, height=30, width=100, type="Button")
        WidgetFact(720,760,image_name="AngoLogo.png",type = "Image",image_size_x=70,image_size_y=20)

    def downloaded_page(self):
        self.link_text.widget.place(x= 50, y = 320)
        self.link_text.widget.configure(text=self.downloader.title)
        self.video_link.widget.place(x=50,y =350)
        self.download_button.widget.configure(command=self.main_window,text="Back")
        self.download_button.widget.place(x = 250, y = 390)
        WidgetFact(45, 30, image_name=self.downloader.title + ".webp", type="Image", image_size_x=128*4, image_size_y=72*4)

    def video_downloading(self):
        video_url = self.video_link.widget.get()
        if video_url == "":
            WidgetFact(250,210,height=40, width=100,text="It wont work bro",font_size="10",type= "Label")
        else:
            self.downloader = Downloader(video_url)
            self.downloaded_page()



class Downloader:
    def __init__(self,video_url):
        self.video_url = video_url
        if self.video_url != "":
            self.downloading()
            if f"{self.title}.webp" in os.listdir("images") :
                pass
            else:
                source = os.path.join(self.script_dir, 'downloaded', f'{self.title}.webp')
                destination = os.path.join(self.script_dir, 'images')
                print(source, destination)
                shutil.move(source, destination)
            if f"{self.title}.webp" in os.listdir("downloaded"):
                os.remove(f"downloaded/{self.title}.webp")




    def download(self):
        self.script_dir = os.path.dirname(__file__)

        # Construct the path to the ffmpeg binary in the project folder
        if os.name == 'nt':  # For Windows
            ffmpeg_path = os.path.join(self.script_dir, "bin",'ffmpeg', "ffmpeg","bin","ffmpeg.exe")


        ydl_opts = {
                'format': 'bestaudio/best',  # Download the best audio only
                'outtmpl': os.path.join(self.script_dir, 'downloaded', '%(title)s.%(ext)s'),  # Save file as title.extension
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Post-process to extract audio
                    'preferredcodec': 'mp3',  # Convert to mp3 format
                    'preferredquality': '192',  # Set audio quality

                }],
                'writethumbnail': "True",
                'ffmpeg_location': ffmpeg_path,  # Path to the bundled ffmpeg executable
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                #take the infos to use them later
                info_dict = ydl.extract_info(self.video_url, download=True)
                self.title = info_dict.get('title', None)


    def downloading(self):
        self.download()


if __name__ == "__main__":
    global root
    root = ctk.CTk()
    Windows()
