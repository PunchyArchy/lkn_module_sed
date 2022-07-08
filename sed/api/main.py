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
                                            description='Загружаемые файлы')):
    """ Создать произвольное обращение от физического лица """
    logger.info(f'Создание запроса для физ.лица ({locals()})')
    inst = main_workers.IndividualRequestsMailWorker(
        user_name=user_name,
        user_phone=user_phone,
        user_email=user_email,
        user_text=user_text,
        request_num=request_num,
        files_list=files_list)
    response = await inst.form_send_mail()
    return response


@app.post('/create_entity_email_failed_request', tags=['Юр. лица'])
async def create_entity_email_failed_request(
        inn=Query(..., description='ИНН компании'),
        failed_email=Query(...,
                           description='ИНН из БД (не прошедший валидацию)', ),
        request_num=Query(..., description='Номер заявки (только цифры)')):
    """ Дергать, когда валидация email из БД не прошла. В СЭД упадет заявка,
    что бы менеджер скорректировал email юр.лица """
    logger.info(f'Создание запроса на восстановление доступа по ИНН')
    inst = main_workers.EntityRequestsMailWorker(
        company_inn=inn,
        contact_email=failed_email,
        contact_phone='Неизвестно',
        contact_person='Неизвестно',
        request_num=request_num,
        user_text='Пользователь не смог авторизоваться по ИНН, '
                  'поскольку в базе неверно указан email: {failed_email}')
    response = await inst.form_send_mail()
    return response


@app.post('/create_entity_request', tags=['Юр. лица'])
async def create_entity_request(
        company_inn=Query(None, description='ИНН компании'),
        contact_person=Query(None, description='Контактное лицо (имя)'),
        contact_phone=Query(..., description='Телефон для связи'),
        contact_email=Query(None, description='Email для связи'),
        request_num=Query(..., description='Номер обращения'),
        user_text=Query(..., description='Текст обращения'),
        files_list: List[UploadFile] = File(None,
                                            description='Загружаемые файлы')):
    """ Создать произвольное обращение от юридического лица """
    logger.info(f'Создание запроса для юр.лица ({locals()})')
    inst = main_workers.EntityRequestsMailWorker(
        company_inn=company_inn,
        contact_person=contact_person,
        contact_phone=contact_phone,
        contact_email=contact_email,
        request_num=request_num,
        user_text=user_text,
        files_list=files_list
    )
    response = await inst.form_send_mail()
    return response


@app.post('/create_entity_new_point_request', tags=['Точки вывозов',
                                                    'Юр. лица'])
async def create_entity_new_point_request(
        company_inn=Query(None, description='ИНН компании'),
        contact_person=Query(None, description='Контактное лицо (имя)'),
        contact_phone=Query(..., description='Телефон для связи'),
        contact_email=Query(None, description='Email для связи'),
        request_num=Query(..., description='Номер обращения'),
        container_name=Query(..., description='Имя объекта'),
        container_addr=Query(..., description='Адрес объекта'),
        container_type=Query(..., description='Тип контейнера')):
    """ Создать обращение с просьбой зарегистрировать новую точку вывоза """
    logger.info(f'Создание запроса для создания точки от юр.лица ({locals()})')
    inst = main_workers.EntityPointRequestsMailWorker(
        company_inn=company_inn,
        contact_person=contact_person,
        contact_phone=contact_phone,
        contact_email=contact_email,
        request_num=request_num,
        container_name=container_name,
        container_addr=container_addr,
        container_type=container_type)
    return await inst.form_send_mail()


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
