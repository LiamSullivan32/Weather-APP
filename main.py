from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from datetime import datetime
from Data import WeatherData, WeatherForecast, WeatherValues
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)    

async def get_weather():
    """
    url = "https://api.tomorrow.io/v4/weather/forecast"
    params = {
        "location": "42.3478,-71.0466",
        "fields": [
            "temperature", "temperatureApparent", "windSpeed", "windGust", "windDirection",
            "pressureSurfaceLevel", "precipitationProbability", "precipitationType", "visibility",
            "cloudCover", "cloudBase", "cloudCeiling", "weatherCode"
        ],
        "units": "metric",
        "timesteps": ["1h"],
        "apikey": "2339V6rLQ1ASEieBy4iama9cZRe9n9MA"
    }
    """
    async with httpx.AsyncClient() as client:
        """
        response = await client.get(url, params=params)
        """
        with open('./fake_data.json', 'r') as file:
            data = json.load(file)
        timelines_data = data.get("timelines", [])['hourly']
        rows = []
        for i in timelines_data:
            vals = WeatherValues(
                cloudBase=i['values']['cloudBase'],
                cloudCeiling=i['values']['cloudCeiling'],
                cloudCover=i['values']['cloudCover'],
                dewPoint=i['values']['dewPoint'],
                evapotranspiration=i['values']['evapotranspiration'],
                freezingRainIntensity=i['values']['freezingRainIntensity'],
                humidity=i['values']['humidity'],
                iceAccumulation=i['values']['iceAccumulation'],
                #iceAccumulationLwe=i['values']['iceAccumulationLwe'],
                precipitationProbability=i['values']['precipitationProbability'],
                pressureSurfaceLevel=i['values']['pressureSurfaceLevel'],
                rainAccumulation=i['values']['rainAccumulation'],
                #rainAccumulationLwe=i['values']['rainAccumulationLwe'],
                rainIntensity=i['values']['rainIntensity'],
                sleetAccumulation=i['values']['sleetAccumulation'],
                #sleetAccumulationLwe=i['values']['sleetAccumulationLwe'],
                sleetIntensity=i['values']['sleetIntensity'],
                snowAccumulation=i['values']['snowAccumulation'],
                #snowAccumulationLwe=i['values']['snowAccumulationLwe'],
                #snowDepth=i['values']['snowDepth'],
                snowIntensity=i['values']['snowIntensity'],
                temperature=i['values']['temperature'],
                temperatureApparent=i['values']['temperatureApparent'],
                #uvHealthConcern=i['values']['uvHealthConcern'],
                #uvIndex=i['values']['uvIndex'],
                visibility=i['values']['visibility'],
                weatherCode=i['values']['weatherCode'],
                windDirection=i['values']['windDirection'],
                windGust=i['values']['windGust'],
                windSpeed=i['values']['windSpeed']
            )
            time = i['time']
            print(time)
            weather_data = WeatherData(time=time, values=vals)
            rows.append(weather_data)

        forcast = WeatherForecast(timelines=rows)
        #print(forcast.timelines[0].values)
        return forcast
    

@app.get("/weather-basic")
async def get_weather_basic():
    weather_data = await get_weather()
    return weather_data
    
@app.get("/days")
async def get_weather_basic():   
    weather = await get_weather()
    dates = set([i.time.date() for i in weather.timelines])
    return dates

@app.get("/by_day")
async def get_weather_basic(date):   
    weather = await get_weather()
    rows = []
    for i in weather.timelines:
        if str(i.time.date()) == str(date):
            rows.append(i)
    filtered_weather_data = WeatherForecast(timelines=rows)
    return filtered_weather_data


    
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)