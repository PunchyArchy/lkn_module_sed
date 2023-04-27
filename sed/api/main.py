from fastapi import FastAPI, Query, File, UploadFile
from sed import main as main_workers
from sed.logger.main import logger
from typing import List

app = FastAPI(title='ЛКН. Модуль для работы с СЭД',
              description='API взаимодействия с СЭД РО "Эко-сити". '
                          'Суть АПИ в том, что дергая нижеописанные ручки, мы '
                          'отправляем соответсвующие запросы на мыло "Эко-Сити".'
                          '\nТам эти запросы будут оформлены как заявки для '
                          'исполнения менеджерами.'
                          '\nНомер заявки мы должны генерить с нашей стороны, '
                          'это число-буквенный номер, но при дергании ручки '
                          'передаем только числа, и уже под капотом сгенерится '
                          'правильный номер. Т.е. передаешь 148, на выходе '
                          'будет что-то типа "02-Ю-В-148"',
              contact={'name': 'Qodex.PunchyArchy',
                       'url': 'http://about.qodex.tech/'},
              version='0.1.0')


@app.post('/create_individual_request', tags=['Физ. лица'])
async def create_individual_request(
        user_name=Query(None, description='Имя пользователя'),
        user_phone=Query(..., description='Телефон пользователя'),
        user_email=Query(None, description='Email пользователя'),
        user_text=Query(..., description='Текст обращения пользователя'),
        request_num=Query(...,
                          description='Номер обращения (из нашей системы)'),
        files_list: List[UploadFile] = File(None,
                                            description='Загружаемые файлы'),
        bill_num=Query('Не указан', description='Номер лицевого счета'),
        auth=Query(False, description='Авторизованный пользователь'),
        territory=Query(None, description='Территория (необязательно)')):
    """ Создать произвольное обращение от физического лица """
    logger.info(f'Создание запроса для физ.лица ({locals()})')
    inst = main_workers.IndividualRequestsMailWorker(
        user_name=user_name,
        user_phone=user_phone,
        user_email=user_email,
        user_text=user_text,
        request_num=request_num,
        files_list=files_list,
        bill_num=bill_num,
        territory=territory,
        auth=auth)
    response = await inst.form_send_mail()
    return inst.get_request_identifier()


@app.post('/create_entity_request', tags=['Юр. лица'])
async def create_entity_request(
        company_inn=Query(None, description='ИНН компании'),
        company_kpp=Query(None, description='КПП компании'),
        company_name=Query(None, description='Название компании'),
        contact_person=Query(None, description='Контактное лицо (имя)'),
        contact_phone=Query(..., description='Телефон для связи'),
        contact_email=Query(None, description='Email для связи'),
        request_num=Query(..., description='Номер обращения'),
        user_text=Query(..., description='Текст обращения'),
        files_list: List[UploadFile] = File(None,
                                            description='Загружаемые файлы'),
        bill_num=Query('Не указан', description='Номер лицевого счета'),
        auth=Query(False, description='Авторизованный пользователь'),
        territory=Query(None, description='Территория (необязательно)')):
    """ Создать произвольное обращение от юридического лица """
    logger.info(f'Создание запроса для юр.лица ({locals()})')
    inst = main_workers.EntityRequestsMailWorker(
        company_name=company_name,
        company_inn=company_inn,
        company_kpp=company_kpp,
        contact_person=contact_person,
        contact_phone=contact_phone,
        contact_email=contact_email,
        request_num=request_num,
        user_text=user_text,
        files_list=files_list,
        bill_num=bill_num,
        auth=auth,
        territory=territory
    )
    response = await inst.form_send_mail()
    return inst.get_request_identifier()


@app.post('/create_entity_new_point_request', tags=['Точки вывозов',
                                                    'Юр. лица'])
async def create_entity_new_point_request(
        company_inn=Query(None, description='ИНН компании'),
        contact_person=Query(None, description='Контактное лицо (имя)'),
        contact_phone=Query(..., description='Телефон для связи'),
        contact_email=Query(None, description='Email для связи'),
        request_num=Query(..., description='Номер обращения'),
        points: List = Query([],
                             description='Точки вывозов (список, в котором '
                                         'элемент #0 - это название (вывеска), '
                                         '#1 - адрес точки..'
                                         '#2 - Название второй точки, #-3 адрес второй точки и тд. т.е список [0,1,  2,3,  4,5]')):
    """ Создать обращение с просьбой зарегистрировать новую О\очку вывоза """
    logger.info(f'Создание запроса для создания точки от юр.лица ({locals()})')
    inst = main_workers.EntityPointRequestsMailWorker(
        company_inn=company_inn,
        contact_person=contact_person,
        contact_phone=contact_phone,
        contact_email=contact_email,
        request_num=request_num,
        points=points)
    response = await inst.form_send_mail()
    return inst.get_request_identifier()



@app.post('/create_personal_account_request', tags=['Лицевые счета',
                                                    'Физ. лица', 'Юр. лица'])
async def create_personal_account_request(
        user_phone=Query(..., description='Номер пользователя'),
        user_email=Query(None, description='Email пользователя'),
        failed_address=Query(None,
                             description='Адрес, по которому юзер пытался'
                                         'получить лицевой счет'),
        request_num=Query(..., description='Номер обращения')):
    """ Создать запрос на получение номера лицевого счета """
    logger.info(f'Создание запроса на получение лицевого счета ({locals()})')
    inst = main_workers.PersonalAccountGetRequestMailWorker(
        user_phone=user_phone,
        user_email=user_email,
        failed_address=failed_address,
        request_num=request_num
    )
    return await inst.form_send_mail()


@app.post('/create_user_response', tags=['Лицевые счета',
                                         'Физ. лица', 'Юр. лица'])
async def create_user_response(email_to=Query(...,
                                              description='Email куда слать ответ'),
                               request_num=Query(...,
                                                 description='Номер обращения')):
    inst = main_workers.ResponseCreator(email_for_response=email_to,
                                        request_num=request_num)
    return await inst.form_send_mail()


@app.post('/create_user_response_html', tags=['Лицевые счета',
                                              'Физ. лица', 'Юр. лица'])
async def create_user_response_html(email_to=Query(...,
                                                   description='Email куда слать ответ'),
                                    request_num=Query(...,
                                                      description='Номер обращения'),
                                    request_text=Query(None,
                                                      description='Текст обращения'
                                                      )):
    inst = main_workers.ResponseCreatorHTML(email_for_response=email_to,
                                            request_num=request_num,
                                            request_text=request_text)
    return await inst.form_send_mail()
