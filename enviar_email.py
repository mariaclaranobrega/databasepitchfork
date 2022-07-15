import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename


username = 'EMAIL_QUE_ENVIARA@gmail.com'
password = 'SENHA_DE_APP_GMAIL'
default_address = ['ENVIAR_PARA_ESSE_CASO_NAO_HAJA_REMETENTE@gmail.com']


def send_mail(send_from: str, subject: str, text: str,
              send_to: list, files=None):
    send_to = default_address if not send_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype=ext)
            attachedfile.add_header('content-disposition', 'attachment', filename=basename(f))
        msg.attach(attachedfile)

    smtp = smtplib.SMTP(host="smtp.gmail.com", port=587)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


send_mail(send_from=username, subject="Teste", text="Este é um email teste para enviar arquivos",
          send_to=["ENVIAR_PARA@gmail.com", ], files=["primeiro_pdf.pdf", ])
