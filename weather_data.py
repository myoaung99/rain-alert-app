import requests

API = '3244151f9f7031286a9b45b59763f091'
LAT = 21.803160
LON = 96.017548
END_POINT = 'https://api.openweathermap.org/data/2.5/onecall'

params = {
    'lat': LAT,
    'lon': LON,
    'appid': API,
    'exclude': 'current,minutely,daily,alerts',
}

response = requests.get(
    url=END_POINT, params=params)
response.raise_for_status()

data = response.json()

# with open('./data.py', 'w') as file:
#     file = file.write(f'{data}')


# def get_12_hour() -> None:
#     for i in range(0, 12):
#         condition_code = data['hourly'][i]['weather'][0]['id']


# get_12_hour()
# print(condition_code)

will_rain = False

twelve_hr_condition = data['hourly'][:12]

for hourly_data in twelve_hr_condition:
    condition_code = hourly_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    print('Bring your Umbrella.')
