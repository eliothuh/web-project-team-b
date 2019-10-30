import psycopg2
import unittest
from datasource import *


class DataSourceTester(unittest.TestCase):
	def setUp(self):
		connection = psycopg2.connect(database="huhe", user="huhe", password="tree695eye")
		self.dataSource = DataSource(connection)
		
	def test_check_incompatible_range(self):
		self.assertRaises(ValueError, self.dataSource.checkValidRange, 2000, 1999)
		self.assertRaises(ValueError, self.dataSource.checkValidRange, 1960, 1999)
		self.assertRaises(ValueError, self.dataSource.checkValidRange, 2017, 2020)
		self.assertRaises(TypeError, self.dataSource.checkValidRange, 'apple', 'banana')
	
	def test_check_compatible_range(self):
		self.assertTrue(self.dataSource.checkValidRange(2000, 2002))
		
if __name__ == '__main__':
	unittest.main()
