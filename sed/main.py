import os
from sed import settings
from sed import mixins


class MailWorker(mixins.MessageCreator, mixins.MessageBodyCreator,
                 mixins.MessageSender):

    async def form_send_mail(self):
        self.message_body = self.get_msg_body()
        message = await self.create_message()
        server = self.get_server_auth()
        return await self.send_mail(server, message=message.as_string())


class SedInfo(MailWorker):
    email_login = settings.email_from
    email_from = email_login
    email_pass = settings.email_pass
    email_to = settings.email_to
    server_addr = 'smtp.yandex.ru'
    server_port = 465


class ResponseCreator(SedInfo,
                      mixins.MessageResponseCreator,
                      MailWorker):
    def __init__(self, request_num, email_for_response):
        self.request_identifier = request_num
        self.request_num = request_num
        self.subject = 'ЭКО-Сити. Ваше обращение принято в работу!'
        self.email_to = email_for_response


class IndividualRequestsMailWorker(SedInfo,
                                   mixins.IndividualMessageBodyCreator,
                                   MailWorker,
                                   mixins.IdentifierGenerator):
    def __init__(self, user_name, user_phone, user_email, user_text,
                 request_num, files_list, bill_num):
        self.user_name = user_name
        self.user_phone = user_phone
        self.user_email = user_email
        self.user_text = user_text
        self.request_num = request_num
        self.subject = f'Обращение физ.лица #{request_num}'
        self.attached_files = files_list
        self.email_to = settings.email_to_individual
        self.request_type = 'Ф'
        self.request_identifier = self.get_request_identifier()


class EntityRequestsMailWorker(SedInfo,
                               mixins.EntityMessageBodyCreator,
                               MailWorker,
                               mixins.IdentifierGenerator):
    def __init__(self, company_inn, contact_person, contact_phone,
                 contact_email, request_num, user_text, files_list=None,
                 bill_num=None):
        self.company_inn = company_inn
        self.contact_person = contact_person
        self.company_email = contact_email
        self.contact_phone = contact_phone
        self.request_num = request_num
        self.subject = f'Обращение юр. лица #{request_num}'
        self.attached_files = files_list
        self.user_text = user_text
        self.email_to = settings.email_to_juridical
        self.request_type = 'Ю'
        self.request_identifier = self.get_request_identifier()


class EntityPointRequestsMailWorker(EntityRequestsMailWorker,
                                    mixins.IdentifierGenerator):
    """ Заявка на оформление новой точки от юридического лица"""

    def __init__(self, company_inn, contact_person, contact_phone,
                 contact_email, request_num,
                 container_name, container_addr, container_type):
        super().__init__(company_inn=company_inn,
                         contact_person=contact_person,
                         contact_phone=contact_phone,
                         contact_email=contact_email,
                         request_num=request_num,
                         user_text=None)
        self.subject = f'Заявка на оформление точки вывоза #{request_num}'
        self.container_name = container_name
        self.container_addr = container_addr
        self.container_type = container_type
        self.email_to = settings.email_to_juridical
        self.request_type = 'Ю'
        self.request_identifier = self.get_request_identifier()

    def get_msg_body(self):
        msg_body = super().get_msg_body()
        msg_body += f'\nНазвание объекта - {self.container_name}\n' \
                    f'Адрес объекта - {self.container_addr}\n ' \
                    f'Тип контейнера - {self.container_type}\n'
        return msg_body


class PersonalAccountGetRequestMailWorker(SedInfo,
                                          mixins.PersonalAccountGetRequest,
                                          MailWorker,
                                          mixins.IdentifierGenerator):
    def __init__(self, user_phone, user_email, failed_address, request_num):
        self.user_phone = user_phone
        self.user_email = user_email
        self.failed_address = failed_address
        self.subject = f'Запрос на получение лицевого счета #{request_num}'
        self.email_to = settings.email_to_individual
        self.request_type = 'Ф'
        self.request_num = request_num
        self.request_identifier = self.get_request_identifier()
