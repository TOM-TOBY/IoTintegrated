from flask import Flask
import pymysql
from datetime import datetime
from time import sleep
#from timeloop import Timeloop
#from datetime import timedelta

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
#Library to access external APIs (NOTE: This may not work with python3)
#from urllib.request import urlopen
#For Python3 only
import requests
#Read OpenWeatherMap API usage here - https://openweathermap.org/api/one-call-api
#Insert your OpenWeatherMap API here
OPEN_WEATHER_MAP_API_KEY = "725c333a25aff972c5d64b34616da787"
#give your Lattitude and Longitude
lat = '9.557270'
lon = '76.789436'
#Create openweathermap url
api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+"&lon="+str(lon)+"&exclude=hourly,daily,minutely,alerts+&appid="+OPEN_WEATHER_MAP_API_KEY+"&units=metric"
app = Flask(__name__)
@app.route('/fetchWeather')
def get_open_weather_map_data():
    #For Python2
    #response = urlopen(api_url).read()
    #For Python3
    #print("hi")
    response = requests.get(api_url).json()
    print(response)
    return response
#To save API response to mySQL
@app.route('/todb')
def todb():
    while(True):
        #receiving data from OpenWeather
        now = datetime.now()
        #tl = Timeloop()
        #@tl.job(interval=timedelta(seconds=300))
        ctime1 = now.strftime("%Y/%m/%d %H:%M:%S")
        ctime1 = ctime1.replace('/','-')
        response = requests.get(api_url).json()
        #Cleaning the data to make it look tidy
        currentWeather = response['current']
        key1 =['clouds', 'dew_point', 'dt', 'feels_like','humidity','temp','uvi']
        currentWeather = {key: currentWeather.get(key) for key in key1}
        currentWeather['uvi'] = ctime1
        #print(currentWeather)
        weatherReport = response['current']['weather']
        #print(weatherReport)
        key2 =['id', 'description', 'icon', 'main']
        weatherReport = {key: weatherReport[0].get(key) for key in key2}
        #print(weatherReport)
        #Connect to MySQL DB (Not tested, May have errors!)
        conn = pymysql.connect(database="WeatherDB",user="tom",password="iotassignment3",host="localhost")
        cur=conn.cursor()
        #Table 1 shows realtime weather
        cur.execute("INSERT INTO currentWeatherTable (time,clouds, dew_point, dt, feels_like, humidity, temp ) VALUES (%(uvi)s, %(clouds)s, %(dew_point)s, %(dt)s, %(feels_like)s, %(humidity)s, %(temp)s )",currentWeather)

        #Table 2 shows summary
        cur.execute("INSERT INTO weatherSummaryTable (id, description, icon, main) VALUES ( %(id)s, %(description)s, %(icon)s, %(main)s)",weatherReport)
        conn.commit()
        conn.close()
        return currentWeather
        sleep(60)     # sleep for 60seconds
        #return currentWeather
if __name__ == "__main__":
    #Application runs on port 6000
    app.run(host="0.0.0.0", port='1600', debug=1)
