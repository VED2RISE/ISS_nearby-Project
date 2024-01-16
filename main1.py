import requests as rq
from datetime import datetime
from twilio.rest import Client
import keys
import smtplib
import time

MY_LAT = 51.484170
MY_LONG = -3.181982
MY_EMAIL = "ivansmirnov9009@gmail.com"
PASSWORD = "quvvdrvncanvepxe"


def send_sms():
    try:
        client = Client(keys.account_sid, keys.auth_token)
        message = client.messages.create(
            body = "ISS is in the sky! Look up",
            from_ = keys.twilio_number,
            to = keys.target_number
        )
        print(message.body)
    except Exception as e:
        print(f"Error sending SMS: {e}")


def send_mail(email, parol):
    message = "Subject: Look up!\n\nHey! Look up, somewhere in the skies there is the ISS!"
    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=email, password=parol)
        connection.sendmail(from_addr=email, to_addrs=email, msg=message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.quit()

while True:

    parametrs = {
    "lat" : MY_LAT, 
    "lng": MY_LONG, 
    "formatted": 0
    }

    try:
        time_now = datetime.now().hour
        response = rq.get(url = "https://api.sunrise-sunset.org/json?", params = parametrs)
        response.raise_for_status()
        data = response.json()
        sunrise = int((data["results"]["sunrise"]).split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        response_iss = rq.get(url = "http://api.open-notify.org/iss-now.json")
        response_iss.raise_for_status()
        data_iss = response_iss.json()
        iss_lat = float(data_iss["iss_position"]["latitude"])
        iss_long = float(data_iss["iss_position"]["longitude"])


        if time_now > sunset and time_now < sunrise:
            latitude = MY_LAT - iss_lat    
            longitude = MY_LONG - iss_long

            if longitude < 0:
                longitude *= (-1)
            
            if latitude < 0:
                latitude *= (-1)

            if latitude <= 5 and longitude <= 5:
                send_sms()
                send_mail(MY_EMAIL, PASSWORD)

    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(60)

