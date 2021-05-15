import unittest
from app import app
import os
from mongoengine import connect

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class EtlTests(unittest.TestCase):

  def setUp(self):
    connect(DB_NAME, host=f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin')

    self.app = app
    self.app.testing = True
    self.context = self.app.test_request_context()
    self.context.push()
    self.client = self.app.test_client()

  def test_index_status(self):
    request = self.client.get('http://0.0.0.0:8005/')
    self.assertEqual(200 , request.status_code)
      
  def test_index(self):
    request = self.client.get('http://0.0.0.0:8005/')
    self.assertEqual('ETL TSE!!! Devel' , request.data.decode())

  def test_fake_status(self):
      request = self.client.get('http://0.0.0.0:8005/not_exist')
      self.assertEqual(404 , request.status_code)

  def tearDown(self):
      self.context.pop()

if __name__=='__main__':
  unittest.main()