import streamlit as st
import requests

# Replace with your OpenWeatherMap API key (free to get)
OPENWEATHER_API_KEY = "566109b2caa44a0c88cfaff12d9f9792"

def get_weather(city):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
        }
    else:
        return None

def get_dummy_events(city):
    # Simple dummy events - replace with real API if you want later
    return [
        f"{city} Food Festival - June 10",
        f"Outdoor Concert in {city} Park - June 12",
        f"Art Exhibition at {city} Gallery - June 15",
    ]

def packing_tip(temp):
    if temp < 10:
        return "Pack warm clothes 🧥 and a hat 🧢."
    elif temp < 20:
        return "Bring a jacket 🧥 and some layers."
    else:
        return "Light clothes 👕 and sunscreen 🧴 recommended."

st.title("🌍 Smart Travel Planner MVP")

city = st.text_input("Enter your travel city:")

if city:
    weather = get_weather(city)
    if weather:
        st.subheader(f"Current Weather in {city.title()}:")
        st.write(f"Temperature: {weather['temp']} °C")
        st.write(f"Condition: {weather['description'].title()}")
        st.write(f"Humidity: {weather['humidity']}%")

        st.subheader("Upcoming Local Events:")
        events = get_dummy_events(city.title())
        for event in events:
            st.write(f"- {event}")

        st.subheader("Packing Tip:")
        tip = packing_tip(weather['temp'])
        st.write(tip)
    else:
        st.error("Sorry, could not find weather data for that city.")
