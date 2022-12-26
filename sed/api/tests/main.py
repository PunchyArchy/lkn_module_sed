import unittest
import requests


class TestCase(unittest.TestCase):
    @unittest.SkipTest
    def test_phys_no_files(self):
        response = requests.post(
            'http://62.109.6.113:9002/create_individual_request/',
            params={
                'user_name': 'Arthur',
                'user_phone': '+79962947595',
                'user_text': 'Тестовое обращение от физ.лица',
                'request_num': 1},
            files=[])
        self.assertEqual(response.status_code, 200)

    @unittest.SkipTest
    def test_phys_multiple_files(self):
        files = [
            ('files_list', open('../../tests/pdf-test.pdf', 'rb')),
            ('files_list', open('../../tests/pdf-test.pdf', 'rb')),
        ]
        response = requests.post(
            'http://62.109.6.113:9002/create_individual_request/',
            params={
                'user_name': 'Arthur',
                'user_phone': '+79962947595',
                'user_text': 'Тестовое обращение от физ.лица',
                'request_num': 2},
            files=files)
        self.assertEqual(response.status_code, 200)

    @unittest.SkipTest
    def test_entity_multiple_files(self):
        files = [
            ('files_list', open('../../tests/pdf-test.pdf', 'rb')),
            ('files_list', open('../../tests/pdf-test.pdf', 'rb')),
        ]
        response = requests.post(
            'http://62.109.6.113:9002/create_entity_request/',
            params={'contact_person': 'Arthur',
                    'company_inn': '1241251',
                    'contact_email': 'ksmdrmvstchny@gmail.com',
                    'contact_phone': '+79962947595',
                    'user_text': 'Тестовое обращение',
                    'request_num': 999},
            files=files)
        self.assertEqual(response.status_code, 200)
        return response

    def test_entity_no_files(self):
        response = requests.post(
            'http://localhost:8000/create_entity_request/',
            params={'contact_person': 'Arthur',
                    'company_inn': '1241251',
                    'company_kpp': '6789',
                    'company_name': 'Umbrella',
                    'contact_email': 'ksmdrmvstchny@gmail.com',
                    'contact_phone': '+79962947595',
                    'user_text': 'Заявка на заключение договора на вывоз ТКО',
                    'request_num': 999},
            files=[])
        self.assertEqual(response.status_code, 200)
        return response

    def test_response_genereator(self):
        pass

if __name__ == '__main__':
    print("FFF")
    unittest.main()
