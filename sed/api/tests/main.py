import unittest
import requests


class TestCase(unittest.TestCase):
    def test_upload_multiple_files(self):
        fobj = open('../../tests/pdf-test.pdf', 'rb')
        files = [
            ('files_list', fobj),
            ('files_list', fobj),
        ]
        response = requests.post(
            'http://127.0.0.1:8001/create_individual_request/',
            params={
                'user_name': 'Arthur',
                'user_phone': '+79962947595',
                'user_text': 'Тестовое обращение от физ.лица',
                'request_num': 145},
            files=files)
        self.assertEqual(response.status_code, 200)
        return response

    @unittest.SkipTest
    def test_entity_multiple_files(self):
        fobj = open('../../tests/pdf-test.pdf', 'rb')
        files = [
            ('files_list', fobj),
            ('files_list', fobj),
        ]
        response = requests.post(
            'http://127.0.0.1:8001/create_entity_request/',
            params={'contact_person': 'Arthur',
                    'company_inn': '1241251',
                    'contact_email': 'ksmdrmvstchny@gmail.com',
                    'contact_phone': '+79962947595',
                    'user_text': 'Тестовое обращение',
                    'request_num': 999},
            files=files)
        self.assertEqual(response.status_code, 200)
        return response


if __name__ == '__main__':
    unittest.main()
