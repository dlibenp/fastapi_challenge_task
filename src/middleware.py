import os
from fastapi import Request
import geocoder
import httpx
import crud, database

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

async def log_request(request: Request, call_next):
    hostname = request.client.host  # hostname of request
    if hostname in ['localhost', '127.0.0.1', '::1']:
        hostname = 'me'
    
    g = geocoder.ip(hostname)  # data from hostname
    # g.city g.state g.country
    country = g.country if g.country else "Unknown"  

    # Get the weather info
    weather_data = await get_weather(country)  
    # country, city, weather, temperature, humidity, wind_speed
    if weather_data:
        data = {**weather_data, 'hostname': hostname}
        db = database.SessionLocal()
        crud.create_weather(db, weather=data)  # save weather data in database

    response = await call_next(request)  
    return response  

async def get_weather(country: str):  
    async with httpx.AsyncClient() as client:  
        response = await client.get(  
            f"http://api.openweathermap.org/data/2.5/weather?q={country}&appid={API_KEY}&units=metric"  
        )

        if response.status_code == 200:  
            data = response.json()
            return {
                'country': data['sys']['country'],
                'city': data['name'],
                'weather': data['weather'][0]['description'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        return None