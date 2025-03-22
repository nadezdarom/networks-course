import socket, base64, sys, ssl


smtp_server = "smtp.yandex.ru"
port = 587


class MyEmailSender():
    def __init__(self, sender, password, smtp_server=smtp_server, smtp_port=port):
        self.sender = sender
        self.pswrd = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        print(self.smtp_server, self.smtp_port)
        self.server = socket.create_connection((self.smtp_server, self.smtp_port))

    def SendMessageAndCheckReply(self, msg, code = -1, noResponse = False):
        print(f"\nCommand: {msg}")
        self.server.send(msg.encode())

        if noResponse:
            return
        
        response = self.server.recv(1024).decode()
        print(f"Response: {response}")

        if code != -1 and response != None and not response.startswith(str(code)):
            raise Exception(f"код ответа {code} не получен от сервера. Response: {response}")


    def encode_to_64(self, text):
        return base64.b64encode(text.encode()).decode()


    def send_email(self, mail_to, subject, message):
        response = self.server.recv(1024).decode()

        if not response.startswith("220"):
            raise Exception("Код ответа 220 не получен от сервера.")
        
        self.SendMessageAndCheckReply(f"HELO {self.sender}\r\n", 250)

        self.SendMessageAndCheckReply("STARTTLS\r\n", 220)
        context = ssl.create_default_context()
        self.server = context.wrap_socket(self.server, server_hostname=self.smtp_server)

        self.SendMessageAndCheckReply(f"HELO {self.sender}\r\n", 250)

        self.SendMessageAndCheckReply(f"AUTH LOGIN\r\n", 334)

        self.SendMessageAndCheckReply(f"{self.encode_to_64(self.sender)}\r\n", 334)

        self.SendMessageAndCheckReply(f"{self.encode_to_64(self.pswrd)}\r\n", 235)

        self.SendMessageAndCheckReply(f"MAIL FROM: <{self.sender}>\r\n", 250)

        self.SendMessageAndCheckReply(f"RCPT TO: <{mail_to}>\r\n", 250)

        self.SendMessageAndCheckReply(f"DATA\r\n", 354)

        header = ""

        header += f"From: {self.sender}\r\n"
        header += f"To: {mail_to}\r\n"
        header += f"Subject: {subject}\r\n"

        self.SendMessageAndCheckReply(header, -1, True)

        sb = ""

        with open(message) as f:
            email_body = f.read()

        sb += email_body
        sb += "\r\n"

        self.SendMessageAndCheckReply(sb, -1, True)
        
        self.SendMessageAndCheckReply(".\r\n", 250)

        self.SendMessageAndCheckReply("QUIT\r\n", -1, True)

        response = self.server.recv(1024).decode()

        print(response)
        self.server.close()

mail_from = sys.argv[1]
password = sys.argv[2]
mail_to = sys.argv[3]
subject = sys.argv[4]
content = sys.argv[5]
MyMessage = MyEmailSender(mail_from, password, smtp_server, port)
        

MyMessage.send_email(mail_to, subject, content)