from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime


class WeatherValues(BaseModel):
        cloudBase: float | None
        cloudCeiling: float | None
        cloudCover: float | None
        dewPoint: float | None
        evapotranspiration: float | None
        freezingRainIntensity: float | None
        humidity: float | None
        iceAccumulation: float | None
        #iceAccumulationLwe: float | None
        precipitationProbability: int | None
        pressureSurfaceLevel: float | None
        rainAccumulation: float | None
        #rainAccumulationLwe: float | None
        rainIntensity: float | None
        sleetAccumulation: float | None
        #sleetAccumulationLwe: float | None
        sleetIntensity: float | None
        snowAccumulation: float | None
        #snowAccumulationLwe: float | None
        #snowDepth: float | None
        snowIntensity: float | None
        temperature: float | None
        temperatureApparent: float | None
        #uvHealthConcern: int | None
        #uvIndex: int | None
        visibility: float | None
        weatherCode: int | None
        windDirection: float | None
        windGust: float | None
        windSpeed: float | None


class WeatherData(BaseModel):
    time: datetime
    values: WeatherValues 


class WeatherForecast(BaseModel):
    timelines: List[WeatherData]