import requests
from twilio.rest import Client

API = '3244151f9f7031286a9b45b59763f091'
LAT = 21.803160
LON = 96.017548
END_POINT = 'https://api.openweathermap.org/data/2.5/onecall'

test_lat = 44.434850
test_long = 7.589240

account_sid = "AC543d49d26bc5e60d64c3d3bd9fac8b90"
auth_token = "f132f6208656e5c65f3b4207b307e360"
my_phone = '+95 9 952 437129'


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

will_rain = False
weather_data = data['hourly'][:12]

for hourly_data in weather_data:
    condition_code = hourly_data['weather'][0]['id']
    print(condition_code)
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It is going to rain today. Don't forget to bring an ☔",
        from_='+12312723944',
        to=my_phone
    )
    print("It is going to rain.")


print(message.status)
