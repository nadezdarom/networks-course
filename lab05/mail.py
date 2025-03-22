import smtplib, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "smtp.yandex.ru"
port = 587


def send_email(mail_to, subject, message, is_html = False):
    msg = MIMEMultipart("alternative")
    with open(message) as f:
        content = MIMEText(f.read(), "html" if is_html else "plain")

    msg['Subject'] = subject
    msg['From'] = main_email
    msg['To'] = mail_to

    msg.attach(content)

    s = smtplib.SMTP(smtp_server, port)
    s.starttls()
    s.login(main_email, main_password)
    s.sendmail(main_email, mail_to, msg.as_string())
    s.quit()


main_email = sys.argv[1]
main_password = sys.argv[2]
mail_to = sys.argv[3]
subject = sys.argv[4]
content = sys.argv[5]
content_type = content.split('.')[1]
is_html = False

if content_type == "html":
    is_html = True

send_email(mail_to, subject, content, is_html)


