import smtplib
MY_EMAIL = "ivansmirnov9009@gmail.com"
PASSWORD = "quvvdrvncanvepxe"


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

send_mail(MY_EMAIL, PASSWORD)