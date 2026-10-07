import config
import sys
import requests
import textwrap
from tabulate import tabulate

def main():
    x = len(sys.argv)
    wapi_key = config.weather_api_key
    napi_key = config.news_api_key

    if (sys.argv[1].lower() == "weather"):
        if (x > 3):
            sys.exit("Too many arguments!")
        weather(wapi_key)
    
    if (sys.argv[1].lower() == "news"):
        if x != 3:
            sys.exit("Format must be python weathernews-informer.py news <phrase>")
        news(napi_key)


def weather(wapi_key):
    
        city = sys.argv[2]
        
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
        
        geo_params = {
            "q": city,
            "limit": 5,
            "appid": wapi_key
        }
        
        geo_response = requests.get(geo_url, params= geo_params)
        
        if geo_response.status_code == 200:
            data = geo_response.json()
            
            if not data:
                sys.exit(f"City '{city}' not found")
    
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            #print(f"\nlatitude is {lat} longitude is {lon}")
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
            
            table = [
                [f"\nThe weather today in {city} is {weather}\n"],
                [f"With a high of {temp_high}°C and a low of {temp_min}°C\n"]
                
            ]
               
            print(tabulate(
                table,
                tablefmt="grid"
            ))
            
        else:
            print(f"\nWeather API error: {w_response.status_code}\n")

def news(napi_key):
    phrases = sys.argv[2]
    
    n_params = {
        "q": phrases,
        "apiKey": napi_key,
        "sortBy": "relevancy"
    }
    
    n_response = requests.get("https://newsapi.org/v2/everything", params= n_params) 
    
    
    if n_response.status_code == 200:
        n_data = n_response.json()
        article = n_data["articles"][0]
        
        description = article["description"]
        
        description = textwrap.fill(description, width=80)
        
        table = [
            [description]
            
        ]
        
        
       

        print(tabulate(
            table,
            headers= [f'{article["publishedAt"][:10]}\n {article["title"]}'],
            tablefmt="grid"
        ))

    else:
        print(f"\nNews API error: {n_response.status_code}\n")



if __name__ == "__main__":
    main()