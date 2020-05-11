from email.mime.text import MIMEText
import smtplib


def send_email(email, height, average_height, count):
    from_email = "anujnegi0513@gmail.com"
    from_password = "Anujnegi05@"
    to_email = email

    subject = "Height Data"
    message = f"Hey there, your height is <strong>{height}</strong><br>  The Average Height is :<strong>{average_height}</strong> (People : <strong>{count}</strong>) <br> Thanks :)"
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
