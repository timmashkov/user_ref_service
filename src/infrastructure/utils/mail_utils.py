import smtplib

from infrastructure.settings.config import base_config


async def send_email(receiver, message):
    sender = base_config.MAIL_FROM
    password = base_config.GOOGLE_PASS

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

        return "The message has been sent"
    except Exception as e:
        return {"error": e}
