from tkinter import *
import requests
import json
import threading
from PIL import ImageTk, Image

# Global constants
key = open('./weather.env', 'r').read()
s = "https://api.openweathermap.org/data/2.5/weather?"

def fahrenheit(celsius):
    return round((9/5)*celsius + 32, 2)


def rain_percent(humi):
    if humi < 50:
        return 'Not likely'
    elif humi < 70:
        return 'Likely'
    else:
        return 'Strong'
def skycast(city):
    req = requests.get(f'{s}q={city}&appid={key}&units=metric').json()
    main = req['weather'][0]['main']
    desc = req["weather"][0]["description"]
    temp = req["main"]["temp"]
    humidity = req["main"]["humidity"]
    wind_speed = req["wind"]["speed"]
    print(req)
    return {'Description': desc, "Main": main, "Temp": temp, "Humi": humidity, "Wind": wind_speed, "FTemp": fahrenheit(temp)}

def update_city(city):
    result = skycast(city)
    temp_celsius.config(text=f"{result['Temp']}°C")
    temp_fahrenheit.config(text=f"{result['FTemp']}°F")
    main_desc = result["Main"]
    weather_string = ''
    if main_desc == 'Clear':
        weather_string = 'clear.png'
    elif main_desc == 'Clouds':
        weather_string = 'clouds.png'
    elif main_desc == "Mist":
        weather_string = 'mist.png'
    elif main_desc == 'Haze':
        weather_string = 'fog.png'
    elif main_desc == 'Rain':
        if result['Description'].split()[0] == 'moderate':
            weather_string = 'mod_rain.png'
        else:
            weather_string = 'storm.png'
    change = ImageTk.PhotoImage(Image.open("images/"+weather_string).resize((360, 340)))
    location_label.grid(row=0, column=0, padx=10, pady=10)
    logoLabel.config(image=change)
    logoLabel.image = change
    city_label.config(text=city.capitalize())
    wind_label.config(text=f"Wind: {result['Wind']} m/s")
    humidity_label.config(text=f"Humidity: {result['Humi']}%")
    rain_label.config(text=f"Rain Probability: {rain_percent(result['Humi'])}")  # Update with actual rain probability

def retrieve_temperature():
    city = city_entry.get()
    threading.Thread(target=update_city, args=(city,)).start()

if __name__ == "__main__":
    root = Tk()
    root.geometry('360x620')
    app = Frame(root, bg='light blue', width=360, height=720)
    app.pack()

    # Location and City Name
    location_icon = ImageTk.PhotoImage(Image.open("images/location.png").resize((30, 30)))
    location_label = Label(app, image=location_icon, bg='light blue')
    city_label = Label(app, text="", font=('Helvetica', 20), bg='light blue')
    city_label.place(x=150, y=10)
    # Weather Image
    logo = ImageTk.PhotoImage(Image.open("images/logo.png").resize((360, 340)))
    logoLabel = Label(app, image=logo)
    logoLabel.grid(row=1, column=0, columnspan=2, pady=10)

    # Temperature Columns
    temp_frame = Frame(app, bg='light blue')
    temp_frame.grid(row=2, column=0, columnspan=2, pady=7)
    temp_celsius = Label(temp_frame, font=('Geraldine', 24), text="", bg='light blue')
    temp_celsius.grid(row=0, column=0, padx=3)
    temp_fahrenheit = Label(temp_frame, font=('Geraldine', 24), text="", bg='light blue')
    temp_fahrenheit.grid(row=0, column=1, padx=3)

    # Other Weather Information Columns
    weather_info_frame = Frame(app, bg='light blue')
    weather_info_frame.grid(row=3, column=0, columnspan=2, padx=10)
    wind_label = Label(weather_info_frame, text="", font=('Helvetica', 12), bg='light blue')
    wind_label.grid(row=0, column=0, sticky=W, pady=5)
    humidity_label = Label(weather_info_frame, text="", font=('Helvetica', 12), bg='light blue')
    humidity_label.grid(row=1, column=0, sticky=W, pady=5)
    rain_label = Label(weather_info_frame, text="", font=('Helvetica', 12), bg='light blue')
    rain_label.grid(row=2, column=0, sticky=W, pady=5)

    # Search Bar and Submit Button
    search_frame = Frame(app, bg='light blue')
    search_frame.grid(row=4, column=0, columnspan=2, pady=10)
    city_entry = Entry(search_frame)
    city_entry.pack(side=LEFT, padx=10)
    submit_button = Button(search_frame, text='Submit', font=('Helvetica', 12), command=retrieve_temperature, bg='light green')
    submit_button.pack(side=LEFT)

    root.mainloop()
