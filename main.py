import smtplib
import requests
import imghdr
import os
import data
from data_model import DataModel
from email.message import EmailMessage


API = 'API from Open Weather Map'
USER = os.environ.get("EMAIL_USER")
PASS = os.environ.get("EMAIL_PASSWORD")

msg = EmailMessage()
msg['Subject'] = 'မိုးသတိပေးချက် ⚠️'
msg['From'] = USER
msg.set_content(
    'ဒီနေ့ နောက်(၁၂)နာရီအတွင်းမိုးရွာဖို့ ရှိတယ်နော် အပြင်သွားရင် ☔ ယူသွားဖို့ မမေ့ပါနဲ့')


with open('alert.png', 'rb') as file:
    file_data = file.read()
    file_type = imghdr.what(file.name)
    file_name = file.name


msg.add_attachment(file_data, maintype='image',
                   subtype=file_type, filename=file_name)

users = data.user_data

for user in users:
    user_data = DataModel(user["lat"], user["lon"], user["email"])

    LAT = user_data.latitude
    LON = user_data.longitude
    END_POINT = 'https://api.openweathermap.org/data/2.5/onecall'
    msg['To'] = user_data.email

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
    # Get a list of next 12 hour weather condition
    weather_data = data['hourly'][:12]

    for hourly_data in weather_data:
        condition_code = hourly_data['weather'][0]['id']
        if int(condition_code) < 700:
            will_rain = True

    if will_rain:
        connection = smtplib.SMTP(host="smtp.gmail.com")
        connection.starttls()
        connection.login(user=USER, password=PASS)
        connection.send_message(msg)
        connection.close()
        del msg['To']
        print("It is going to rain.")
    print('complete')
