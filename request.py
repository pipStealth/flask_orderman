import requests

def get_location():
    base_url = "https://ipinfo.io/json"
    response = requests.get(base_url)
    data = response.json()
    
    if response.status_code == 200:
        location = {
            'city': data.get('city')
        }
        return location
    else:
        return "Ошибка получения данных"

location = get_location()

def get_temperature(city):
    base_url = f"http://wttr.in/{city}"
    params = {
        'format': 'j1'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        temperature = data['current_condition'][0]['temp_C']
        return temperature
    else:
        return "Ошибка получения данных"

def take_temperature(city=get_location()):
    temperature = get_temperature(city)
    return temperature