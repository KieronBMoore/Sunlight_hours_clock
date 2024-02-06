from tkinter import *
import requests
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv("locked.env")

class DraggableWindow:
    def __init__(self, master):
        self.master = master
        master.geometry("100x100")
        
        #-----------retrieve api key from .env-----------------
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        
        #----------------------Load the image-------------------
        self.background_image = PhotoImage(file="img/Clock.png")

        #----Create a label for the image and set it as the background----
        self.background_label = Label(master, image=self.background_image)
        #----Make image background black and set black to transparent------
        self.background_label.config(bg="black")
        master.wm_attributes("-transparentcolor", "black")

        self.background_label.place(relwidth=1, relheight=1)

        #--------Make the window borderless------
        master.overrideredirect(True)

        #-----Set the window always on top-------
        master.wm_attributes("-topmost", 1)

        #-------------Handling dragging events----------------
        self.background_label.bind("<Button-1>", self.start_drag)
        self.background_label.bind("<B1-Motion>", self.drag)

        #----------Handling right-click to close the window--------
        self.background_label.bind("<Button-3>", self.close_window)

        #--------------Create labels for sunrise and sunset----------------
        self.sunrise_label = Label(master, text="", font=("Helvetica", 8), bg="black", fg="white")
        self.sunset_label = Label(master, text="", font=("Helvetica", 8), bg="black", fg="white")

        #----------Place the labels over the background image--------
        self.sunrise_label.place(relx=0.5, rely=0.1, anchor="center")
        self.sunset_label.place(relx=0.5, rely=0.9, anchor="center")

        #-----Update sunrise and sunset labels-------
        self.update_sunrise_sunset()

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        x_root, y_root = event.x_root, event.y_root
        self.master.geometry(f"+{x_root - self.x}+{y_root - self.y}")

    def close_window(self, event):
        self.master.destroy()

    #---------Retrieve sunrise & sunset from OpenWeather API-------
    def get_sunrise_sunset(self):
        LAT = 53.832980
        LNG = 7.421540
        

        parameters = {
            "lat": LAT,
            "lon": LNG,
            "appid": self.api_key,
        }

        response = requests.get("https://api.openweathermap.org/data/2.5/weather?", params=parameters)
        data = response.json()
        

        sunrise = int(data["sys"]["sunrise"])
        sunrise_GMT = sunrise + 3600
        sunset = int(data["sys"]["sunset"])
        sunset_GMT = sunset + 3600 #adds 1 hour to get GMT time

        sunrise_format = datetime.utcfromtimestamp(sunrise_GMT).strftime('%I:%M %p')
        sunset_format = datetime.utcfromtimestamp(sunset_GMT).strftime('%I:%M %p')

        return sunrise_format, sunset_format

    def update_sunrise_sunset(self):
        sunrise, sunset = self.get_sunrise_sunset()
        self.sunrise_label.config(text=f"Sunrise: {sunrise}")
        self.sunset_label.config(text=f"Sunset: {sunset}")
        # self.master.after(6000000, self.update_sunrise_sunset)





if __name__ == "__main__":
    root = Tk()

    draggable_window = DraggableWindow(root)
    
    root.mainloop()