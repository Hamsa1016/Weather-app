import tkinter as tk
from PIL import Image, ImageTk
import requests
import geocoder
from io import BytesIO 

API_KEY = "9ff2d5887e38816fea1660e9ba0b1892"

def get_location_city():
    try:
        g = geocoder.ip('me')
        return g.city
    except:
        return None

def get_weather(city):
    url_current = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        current = requests.get(url_current).json()
        forecast = requests.get(url_forecast).json()

        if current.get("cod") != 200:
            result_label.config(text=f"City not found: {city}")
            return

        # Current Weather
        weather = current["weather"][0]["main"]
        icon_code = current["weather"][0]["icon"]
        temp = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        wind = current["wind"]["speed"]

        # Update icon
         

        # Update icon using BytesIO (no file saving needed)
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        img_data = requests.get(icon_url).content
        icon_img = Image.open(BytesIO(img_data)).resize((80, 80))
        icon_photo = ImageTk.PhotoImage(icon_img)
        weather_icon.config(image=icon_photo)
        weather_icon.image = icon_photo


        # Format current weather text
        result = f"{weather}\n{temp}°C\nHumidity: {humidity}%\nWind: {wind} m/s"
        result_label.config(text=result)

        # Forecast (display next 3 time slots)
        forecast_text = "\nForecast:\n"
        for i in range(0, 15, 5):  # Show 3 entries spaced apart
            day = forecast["list"][i]
            time = day["dt_txt"].split()[1][:5]
            temp_f = day["main"]["temp"]
            desc = day["weather"][0]["description"].capitalize()
            forecast_text += f"{time} - {temp_f}°C, {desc}\n"

        forecast_label.config(text=forecast_text)
    except:
        result_label.config(text="Failed to fetch weather data")

def fetch_weather():
    city = city_entry.get()
    if not city:
        city = get_location_city()
        if not city:
            result_label.config(text="Enter a city.")
            return
    get_weather(city)

# UI Setup
app = tk.Tk()
app.title("🌤️ Weather App")
app.geometry("400x500")
app.resizable(False, False)

# Background Image
bg_img = Image.open("background.jpg").resize((400, 500))  # Use any background image in same folder
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(app, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Input
city_entry = tk.Entry(app, font=("Arial", 14), justify="center")
city_entry.pack(pady=20)

tk.Button(app, text="Get Weather", font=("Arial", 12), command=fetch_weather).pack(pady=5)

# Weather Display
weather_icon = tk.Label(app, bg="#ffffff", bd=0)
weather_icon.pack(pady=10)

result_label = tk.Label(app, text="", font=("Arial", 13), bg="#ffffff", relief="solid", padx=10, pady=10)
result_label.pack(pady=10)

forecast_label = tk.Label(app, text="", font=("Arial", 11), bg="#ffffff", justify="left")
forecast_label.pack(pady=10)

app.mainloop()
