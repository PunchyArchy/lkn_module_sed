from fastapi import FastAPI, Query, File, UploadFile
from sed import main as main_workers
from sed.logger.main import logger
from typing import List, Union

logger.info('Инициализация API')

app = FastAPI(title='ЛКН. Модуль для работы с СЭД',
              description='Модуль предназначен для взаимодействия с '
                          'СЭД (Система Электронного Документооборота) '
                          'РО "Эко-Сити" в рамках разработки ЛКН.',
              contact={'name': 'Qodex.PunchyArchy',
                       'url': 'http://about.qodex.tech/'},
              version='0.1.0')


@app.post('/create_individual_request', tags=['Обращения'])
async def create_individual_request(
        user_name=Query(None, description='Имя пользователя'),
        user_phone=Query(..., description='Телефон пользователя'),
        user_email=Query(None, description='Email пользователя'),
        user_text=Query(..., description='Текст обращения пользователя'),
        request_num=Query(...,
                          description='Номер обращения (из нашей системы)'),
        files_list: List[UploadFile] = File(None,
                                            description='Загружаемые файлы')):
    """ Создать обращение от физического лица """
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


@app.post('/create_entity_request', tags=['Обращения'])
async def create_entity_request(
        company_inn=Query(None, description='ИНН компании'),
        contact_person=Query(None, description='Контактное лицо (имя)'),
        contact_phone=Query(..., description='Телефон для связи'),
        contact_email=Query(None, description='Email для связи'),
        request_num=Query(..., description='Номер обращения'),
        user_text=Query(..., description='Текст обращения'),
        files_list: List[UploadFile] = File(None,
                                            description='Загружаемые файлы')):
    """ Создать обращение от юридического лица """
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


@app.post('/create_entity_new_point_request', tags=['Точки вывозов'])
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


@app.post('/create_personal_account_request', tags=['Лицевые счета'])
async def create_personal_account_request(
        user_phone=Query(..., description='Номер пользователя'),
        user_email=Query(None, description='Email пользователя'),
        failed_address=Query(None,
                             description='Адрес, по которому юзер пытался'
                                         'получить лицевой счет'),
        request_num=Query(..., description='Номер обращения')):
    logger.info(f'Создание запроса на получение лицевого счета ({locals()})')
    inst = main_workers.PersonalAccountGetRequestMailWorker(
        user_phone=user_phone,
        user_email=user_email,
        failed_address=failed_address,
        request_num=request_num
    )
    return await inst.form_send_mail()
