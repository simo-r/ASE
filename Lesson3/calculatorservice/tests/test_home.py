import unittest
import json
from calculatorservice.app import app as aaaa


class TestSomething(unittest.TestCase):

    def test_my_view(self):
        app = aaaa.test_client()
        reply = app.get('/calc/sum?m=3&n=5')
        body = json.loads(reply.data)
        self.assertEqual(body['result'], 8)
