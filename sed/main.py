from sed import settings
from sed import mixins
import os


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


class ResponseCreatorHTML(mixins.MessageResponseCreatorHTML,
                          mixins.MessageCreatorHTML,
                          ResponseCreator):
    def __init__(self, request_num, email_for_response, request_text=None):
        super(ResponseCreatorHTML, self).__init__(request_num,
                                                  email_for_response)
        self.request_text = request_text
        self.html_templates_path = os.path.join(settings.INTERNAL_DIR,
                                                'html_messages')
        self.html_no_reply_dir = os.path.join(self.html_templates_path,
                                              'no_reply')
        self.html_file_path = os.path.join(self.html_no_reply_dir,
                                           'index.html')


class IndividualRequestsMailWorker(SedInfo,
                                   mixins.IndividualMessageBodyCreator,
                                   MailWorker,
                                   mixins.IdentifierGenerator):
    def __init__(self, user_name, user_phone, user_email, user_text,
                 request_num, files_list, bill_num, auth, territory):
        self.user_name = user_name
        self.auth = auth
        self.user_phone = user_phone
        self.user_email = user_email
        self.user_text = user_text
        self.request_num = request_num
        self.territory = territory
        self.subject = f'Обращение физ.лица #{request_num}'
        self.attached_files = files_list
        self.email_to = settings.email_to_individual
        self.request_type = 'Ф'
        self.bill_num = bill_num
        self.request_identifier = self.get_request_identifier()


class EntityRequestsMailWorker(SedInfo,
                               mixins.EntityMessageBodyCreator,
                               MailWorker,
                               mixins.IdentifierGenerator):
    def __init__(self, company_inn, contact_person, contact_phone,
                 contact_email, request_num, user_text, bill_num,
                 files_list=None, auth=False, company_kpp=None,
                 company_name=None, territory=None):
        self.company_inn = company_inn
        self.company_kpp = company_kpp
        self.company_name = company_name
        self.auth = auth
        self.territory = territory
        self.contact_person = contact_person
        self.company_email = contact_email
        self.contact_phone = contact_phone
        self.request_num = request_num
        self.subject = f'Обращение юр. лица #{request_num}'
        self.attached_files = files_list
        self.user_text = user_text
        self.email_to = settings.email_to_juridical
        self.request_type = 'Ю'
        self.bill_num = bill_num
        self.request_identifier = self.get_request_identifier()


class EntityPointRequestsMailWorker(EntityRequestsMailWorker,
                                    mixins.IdentifierGenerator):
    """ Заявка на оформление новой точки от юридического лица"""

    def __init__(self, company_inn, contact_person, contact_phone,
                 contact_email, request_num, points):
        super().__init__(company_inn=company_inn,
                         contact_person=contact_person,
                         contact_phone=contact_phone,
                         contact_email=contact_email,
                         request_num=request_num,
                         bill_num=None,
                         user_text=None)
        self.subject = f'Заявка на оформление точки вывоза #{request_num}'
        self.points = points
        self.email_to = settings.email_to_juridical
        self.request_type = 'Ю'
        self.request_identifier = self.get_request_identifier()
        # Разбиваем список на множество списков по 2 элементов
        self.points = [self.points[i:i + 2] for i in
                       range(0, len(self.points), 2)]

    def get_msg_body(self):
        msg_body = super().get_msg_body()
        for point in self.points:
            msg_body += f'\nНазвание объекта - {point[0]}\n' \
                        f'Адрес объекта - {point[1]}\n '
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
