from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib
from transliterate import translit


class FilenameTranslator:
    def translate_ru(self, text):
        return translit(text, language_code='ru', reversed=True)


class MessageCreator(FilenameTranslator):
    subject = None
    message_body = None
    attached_file = None
    email_from = None
    filename = None

    def create_message(self):
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.email_from
        msg.attach(MIMEText(self.message_body))
        part = MIMEBase('application', "octet-stream")
        if self.attached_file:
            part.set_payload(self.attached_file)
            self.filename = self.translate_ru(self.filename)
            encoders.encode_base64(part)
            part['Content-Disposition'] = 'attachment; filename="%s"' % \
                                          self.filename
            msg.attach(part)
        return msg


class MessageBodyCreator:
    def get_msg_body(self):
        return ''


class IndividualMessageBodyCreator(MessageBodyCreator):
    user_name = None
    user_phone = None
    user_email = None
    user_text = None

    def get_msg_body(self):
        """ Создать тело сообщения для обращения от физ.лица """
        body = f'Имя - {self.user_name}\n' \
               f'Телефон - {self.user_phone}\n' \
               f'Email- {self.user_email}\n' \
               f'Запрос - {self.user_text}\n'
        return body


class EntityMessageBodyCreator(MessageBodyCreator):
    company_inn = None
    company_email = None
    contact_person = None
    contact_phone = None

    def get_msg_body(self):
        """ Создать тело сообщения для юр.лица """
        body = f'ИНН компании - {self.company_inn}\n\n' \
               f'Контактное лицо - {self.contact_person}\n' \
               f'Телефон контактного лица - {self.contact_phone}\n' \
               f'Email контактного лица - {self.company_email}\n'
        return body


class PersonalAccountGetRequest(MessageBodyCreator):
    user_phone = None
    user_email = None
    failed_address = None

    def get_msg_body(self):
        body = f'Номер пользователя - {self.user_phone}\n' \
               f'Email пользователя - {self.user_email}\n' \
               f'Адрес (лицевые счета не найдены) - {self.failed_address}'
        return body


class MessageSender:
    server_addr = None
    server_port = None
    email_login = None
    email_pass = None
    msg_to_send = None
    email_to = None

    def get_server(self):
        return smtplib.SMTP_SSL(self.server_addr, self.server_port, timeout=60)

    def auth_server(self, server):
        server.login(self.email_login, self.email_pass)

    async def send_mail(self, server, message):
        return server.sendmail(from_addr=self.email_login,
                               to_addrs=self.email_to,
                               msg=message)

    def get_server_auth(self):
        serv = self.get_server()
        self.auth_server(serv)
        return serv


class MailWorker(MessageCreator, MessageBodyCreator, MessageSender):

    def form_mail(self):
        self.message_body = self.get_msg_body()
        message = self.create_message()
        server = self.get_server_auth()
        return self.send_mail(server, message=message.as_string())
