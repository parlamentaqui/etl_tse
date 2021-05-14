import unittest
from flask import url_for
from app import app


class EtlTests(unittest.TestCase):

  def setUp(self):
    self.app = app
    self.app.testing = True
    self.context = self.app.test_request_context()
    self.context.push()
    self.client = self.app.test_client()

  def test_index_status(self):
    request = self.client.get(url_for('/'))
    self.assertEqual(200 , request.status_code)
      
  def test_index(self):
    request = self.client.get(url_for('/'))
    self.assertEqual('ETL TSE!!! Devel' , request.data.decode())
      