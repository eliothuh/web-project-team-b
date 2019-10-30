import psycopg2
import unittest
from unittest import *


class DataSourceTester(unittest.TestCase):
	def setUp(self):
		connection = psycopg2.connect("huhe", "huhe", "tree695eye")
		self.dataSource = DataSource(connection)
		
	def check_incompatible_range(self, startYear, endYear):
		assertRaises(ValueError, self.dataSource.checkValidRange, (2000, 1999))
		assertRaises(ValueError, self.dataSource.checkValidRange, (1960, 1999))
		assertRaises(ValueError, self.dataSource.checkValidRange, (2017, 2020))
		assertRaises(TypeError, self.dataSource.checkValidRange, ('apple', 'banana'))
	
	def check_compatible_range(self, startYear, endYear):
		assertTrue(self.dataSource.checkValidRange(2000, 2002))
		
	if __name__ == '__main__':
		unittest.main()
