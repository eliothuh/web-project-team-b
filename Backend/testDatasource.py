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

	def test_incorrect_state(self):
		self.assertRaises(TypeError, self.dataSource.checkState, 2000)
		self.assertRaises(ValueError, self.dataSource.checkState, "tiiio")

	def test_correct_state(self):
		self.assertTrue(self.dataSource.checkState("Florida"))
		
	def test_proper_state_query(self):
		list = [[[(None, "Delaware", 10.0, "Assault by other and unspecified firearm discharge", "X95", 17.0,
		774990.0, None), ("Total", "Delaware", 10.0, None, None, 24.0,
		774990.0, 3.1),  ("Total", "Delaware", 10.0, None, None, 23.0,
		783600.0, 2.9), [(None, "New Castle County, DE", 10003.0, "Assault by other and unspecified firearm discharge", "X95", 16.0,
		496079.0, None), ()]]]]
		results = self.dataSource.getStateQuery(1999, 1999, "Delaware")
		print(results)
		self.assertEqual(list, results)
		
if __name__ == '__main__':
	unittest.main()
