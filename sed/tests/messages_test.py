from sed import mixins
import unittest


class TestCase(unittest.TestCase):
    def test_messages_send(self):
        mixins.send_individual_request(name='PunchyArchy',
                                       phone='7999999999',
                                       request_num=1337,
                                       text='Hello World',
                                       email='A@gmail.com',
                                       attached_file='pdf-test.pdf')


if __name__ == '__main__':
    unittest.main()
