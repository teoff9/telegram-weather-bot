#######################################################
# By Matteo Fava                                      #
# Created: 01/20/2022                                 #
# Finished: 01/25/2022                                #
# This code will contain functions used               #
# by the telegram bot                                 #
#######################################################

#imports
from requests import get
from json import loads

#api key from weatherapi.com
API_key="" #Insert here api key token


#define a functions to get the current weather for a location
# using its latitude and longitude (like 48.8567,2.3508) or name.
def getCurrent(city):
    url="http://api.weatherapi.com/v1/current.json?key={key}&q={city}&days=2".format(city=city,key=API_key)
    response= get(url)
    data= loads(response.text)
    return data


#define a functions to get the forecast/current for a location
# using its latitude and longitude (like 48.8567,2.3508, or name)
def getForecast(city,days):
    url="http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={d}".format(city=city,key=API_key,d=days)
    response= get(url)
    data= loads(response.text)
    return data


#define a function to output the current weather in a place
def Current(city):
    data = getCurrent(city)
    city=data["location"]["name"]
    region=data["location"]["region"]
    datetime=data["location"]["localtime"]
    datetime=datetime.split(' ')
    datetime="{date}, {time}".format(date=datetime[0],time=datetime[1])
    temp=data["current"]["temp_c"]
    feels=data["current"]["feelslike_c"]
    condition=data["current"]["condition"]["text"]
    wkph=data["current"]["wind_kph"]
    wdir=data["current"]["wind_dir"]
    wind="{wkph} K/h, from {wdir}".format(wkph=wkph, wdir=wdir)
    clouds=data["current"]["cloud"]
    humidity=data["current"]["humidity"]
    precip=data["current"]["precip_mm"]
    output="""
{city}, {region} ({date})
 - {condition}
 - Temp: {temp} C | Feels like: {feels} C
 - Clouds: {clouds}%
 - Precip: {precip}mm
 - Humidity: {humidity}%
 - Wind: {wind}""".format(city=city, region=region, date=datetime, temp=temp, feels=feels,condition=condition,clouds=clouds, precip=precip, humidity=humidity,wind=wind)
    return output


#define a function to output a forecast for the rest of the day
def outputForecastDay(city, days):
    data = getForecast(city, days)
    city=data["location"]["name"]
    region=data["location"]["region"]
    day=data["forecast"]["forecastday"][0]["day"]
    date=data["forecast"]["forecastday"][0]["date"]
    maxtemp=day["maxtemp_c"]
    mintemp=day["mintemp_c"]
    maxwind=day["maxwind_kph"]
    precipmm=day["totalprecip_mm"]
    avghumidity=day["avghumidity"]
    text=day["condition"]["text"]
    willsnow=day["daily_will_it_snow"]
    precip="snow"
    if willsnow==0:
        precip="rain"
    if precip=="snow":
        chance=day["daily_chance_of_snow"]
    elif precip=="rain":
        chance=day["daily_chance_of_rain"]
    output="""
{city}, {region} ({date})
 - {text}
 - Temp: {mintemp} to {maxtemp} C
 - Chance of {precip}: {chance}%
 - Precip: {precipmm}mm
 - Humidity: {avghumidity}%
 - Max Wind: {maxwind}kmh""".format(city=city, region=region, date=date, text=text, maxtemp=maxtemp, mintemp=mintemp,
                precip=precip, chance=chance, precipmm=precipmm, avghumidity=avghumidity, maxwind=maxwind)
    return output


#define a function to output a forecast for the next 2 days
def outputForecast(city, days):
    data = getForecast(city, days)
    city=data["location"]["name"]
    region=data["location"]["region"]
    datetime=data["location"]["localtime"]
    datetime=datetime.split(' ')
    datetime="{date}, {time}".format(date=datetime[0],time=datetime[1])
    tmp="{city}, {region} (as of {datetime}):".format(city=city, region=region, datetime=datetime)
    output=[]
    output.append(tmp)
    for i in range (1,3):
        sh=data['forecast']["forecastday"][i]['day']
        date=data['forecast']["forecastday"][i]["date"]
        maxtemp=sh["maxtemp_c"]
        mintemp=sh["mintemp_c"]
        maxwind=sh["maxwind_kph"]
        precipmm=sh["totalprecip_mm"]
        avghumidity=sh["avghumidity"]
        text=sh["condition"]["text"]
        willsnow=sh["daily_will_it_snow"]
        precip="snow"
        if willsnow==0:
            precip="rain"
        if precip=="snow":
            chance=sh["daily_chance_of_snow"]
        elif precip=="rain":
            chance=sh["daily_chance_of_rain"]
        tmp="""
{date}
 - {text}
 - Temp: {mintemp} to {maxtemp} C
 - Chance of {precip}: {chance}%
 - Precip: {precipmm}mm
 - Humidity: {avghumidity}%
 - Max Wind: {maxwind} kmh""".format(city=city, region=region, date=date, text=text, maxtemp=maxtemp, mintemp=mintemp,
            precip=precip, chance=chance, precipmm=precipmm, avghumidity=avghumidity, maxwind=maxwind)
        output.append(tmp)
    message="\n".join(output)
    return message