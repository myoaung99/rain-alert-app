import smtplib
import requests
import imghdr
from email.message import EmailMessage


API = '3244151f9f7031286a9b45b59763f091'
LAT = 21.803160
LON = 96.017548
END_POINT = 'https://api.openweathermap.org/data/2.5/onecall'

USER = 'your mail'
PASS = 'your pass()'

msg = EmailMessage()
msg['Subject'] = 'မိုးသတိပေးချက် ⚠️'
msg['From'] = USER
msg['To'] = USER
msg.set_content(
    'ဒီနေ့ နောက်(၁၂)နာရီအတွင်းမိုးရွာဖို့ ရှိတယ်နော် အပြင်သွားရင် ☔ ယူသွားဖို့ မမေ့ပါနဲ့')

with open('alert.png', 'rb') as file:
    file_data = file.read()
    file_type = imghdr.what(file.name)
    file_name = file.name


msg.add_attachment(file_data, maintype='image',
                   subtype=file_type, filename=file_name)


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
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    connection = smtplib.SMTP(host="smtp.gmail.com")
    connection.starttls()
    connection.login(user=USER, password=PASS)
    connection.send_message(msg)
    connection.close()
    print("It is going to rain.")
