import os
import unittest
from sed import main
from sed import settings


class TestCase(unittest.TestCase):
    @unittest.SkipTest
    def test_individual_requests(self):
        inst = main.IndividualRequestsMailWorker(
            user_name='TEST_NAME',
            user_phone='+7999312341',
            user_email='test_mail@gmail.com',
            user_text='Hello world!',
            request_num='1337',
            filepath='pdf-test.pdf')
        inst.form_send_mail()

    @unittest.SkipTest
    def test_entity_requests(self):
        inst = main.EntityRequestsMailWorker(
            company_inn='123',
            contact_phone='88005553535',
            contact_person='Иван Михайлович',
            contact_email='test_mail@gmail.com',
            request_num='1009')
        inst.form_send_mail()

    @unittest.SkipTest
    def test_entity_point_requests(self):
        inst = main.EntityPointRequestsMailWorker(
            company_inn='123',
            contact_phone='88005553535',
            contact_person='Сергей Владимирович',
            contact_email='point_test@gmail.com',
            request_num='12312',
            container_name='Точка вывоза #1',
            container_type='1.2 м.',
            container_addr='Улица Пушкина, дом Колотушкина'
        )
        inst.form_send_mail()

    def test_request_account(self):
        inst = main.PersonalAccountGetRequestMailWorker(
            user_phone='3312',
            user_email='12@gmail.com',
            failed_address='Улица Пушкина, дом Колотушкина',
            request_num='0044'
        )
        inst.form_send_mail()


if __name__ == '__main__':
    unittest.main()
