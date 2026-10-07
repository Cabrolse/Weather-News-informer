import config
import sys
import requests

def main():
    x = len(sys.argv)
    wapi_key = config.weather_api_key
    
    if (x < 3):
        sys.exit("Too few arguments!")
    
    if (x > 3):
        sys.exit("Too many arguments!")
    
    if (sys.argv[1] == "weather"):
        weather(wapi_key)


def weather(wapi_key):
        city = sys.argv[2]
        
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={wapi_key}"
        
        geo_params = {
            "q": city,
            "appid": wapi_key
        }
        
        geo_response = requests.get(geo_url, params= geo_params)
        
        if geo_response.status_code == 200:
            data = geo_response.json()
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            print(f"\nlatitude is {lat} longitude is {lon}")
        else:
            print(f"Geo API error: {geo_response.status_code}")

            
        
        w_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": wapi_key,
            "units": "metric"
        }
        
        w_response = requests.get(w_url, params=weather_params)
        
        if w_response.status_code == 200:
            w_data = w_response.json()
            weather = w_data["weather"][0]["description"]
            temp_min = w_data["main"]["temp_min"]
            temp_high = w_data["main"]["temp_max"]
            print(f"\nThe weather today in {city} is {weather}\n")
            print(f"With a high of {temp_high}°C and a low of {temp_min}°C\n")
        else:
            print(f"\nWeather API error: {w_response.status_code}\n")
main()