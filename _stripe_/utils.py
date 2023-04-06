import smtplib
from email.mime.text import MIMEText


def __send_email(to, content, subject):
    sender = "aroxan.999@gmail.com"
    # your password = "your password"
    password = ""

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(content, "html")
        msg["From"] = sender
        msg["To"] = to
        msg["Subject"] = subject
        server.sendmail(sender, to, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please! --errors"
