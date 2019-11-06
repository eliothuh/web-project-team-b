import psycopg2
import unittest
from datasource import *


class DataSourceTester(unittest.TestCase):
	def setUp(self):
		connection = psycopg2.connect(database="huhe", user="huhe", password="tree695eye")
		self.dataSource = DataSource(connection)

	#Checks that getStateQuery raises appropriate errors on unusable year ranges.
	def test_check_invalid_range(self):
		self.assertIsNone(self.dataSource.getStateQuery(2000, 1999, "Delware"))
		self.assertIsNone(self.dataSource.getStateQuery(1960, 1999, "Delaware"))
		self.assertIsNone(self.dataSource.getStateQuery(2017, 2020, "Delaware"))
		self.assertIsNone(self.dataSource.getStateQuery('apple', 'banana', "Delaware"))

	#Call checkValidRange directly as getStateQuery does given there are no unittest assert
	#methods to check an error is NOT raised.
	def test_check_compatible_range(self):
		self.assertTrue(self.dataSource.checkValidRange(2000, 2002))

	#Checks that getStateQuery raises appropriate errors on invalid state names
	def test_invalid_state_name(self):
		self.assertRaises(TypeError, self.dataSource.getStateQuery, 1999, 2000, 2000)
		self.assertRaises(ValueError, self.dataSource.getStateQuery, 1999, 2000, "iiiii")

	#Checks no error is raised when checkValidState is called on an appropriate state name.
	#method called directly for same reason as in test_check_compatible_range
	def test_correct_state(self):
		self.assertTrue(self.dataSource.checkValidState("Florida"))

	#Checks getStateQuery returns a properly formatted set of state and county data
	def test_proper_state_query(self):
		list = [[(None, "Delaware", 10.0, "Assault by other and unspecified firearm discharge", "X95", 17.0,
		774990.0, None), ("Total", "Delaware", 10.0, None, None, 24.0,
		774990.0, 3.1), [(None, "New Castle County, DE", 10003.0, "Assault by other and unspecified firearm discharge", "X95", 16.0,
		496079.0, None)]], [("Total", "Delaware", 10.0, None, None, 23.0,
		783600.0, 2.9), []]]

		results = self.dataSource.getStateQuery(1999, 2000, "Delaware")
		self.assertEqual(list, results)

	#Checks getStateQuery does not return the wrong data set.
	def test_incorrect_state_query(self):
		incorrectList = [("incorrect")]
		results = self.dataSource.getStateQuery(1999, 2000, "Florida")
		self.assertNotEqual(list, results)

if __name__ == '__main__':
	unittest.main()
