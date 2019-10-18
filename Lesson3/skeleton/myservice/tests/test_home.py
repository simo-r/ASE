import unittest
import json
from skeleton.myservice.app import app as aaaa


class TestSomething(unittest.TestCase):

    def test_my_view(self):
        app = aaaa.test_client()
        reply = app.get('/calc/sum?m=3&n=5')
        body = json.loads(str(reply.data, 'utf8'))
        self.assertEqual(body['result'], 8)
