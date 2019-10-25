import psycopg2
import getpass

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self, connection):
        self.connection = connection

    def connect(user, password):
        '''
        Establishes a connection to the database with the following credentials:
		user - username, which is also the name of the database
		password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()
            return connection


    def USAAllYearsQuery(self):
        '''
        returns data for all the US over the full year range, using a special
        data set to get the highest quality data for this query

        RETURN:
            returns a list of data, with each entry for a certain state
        '''
        return []

    def USAQuery(self, startYear=1999, endYear=2017):
        '''
        returns a list of all states and their associated homicide data

        PARAMETERS:
            startYear - the first year of data to draw from
            endYear - the last year of data to draw from

        RETURN:
            a list of all of the states and associated homicide data for each
            year
        '''
        return []

    def USASingleYearQuery(self, year):
        '''
        returns a list of all states and thier associated homicide data

        PARAMETERS:
            year: the year of data to draw from

        RETURN:
            a list of all states and associated data
        '''
        return []

    def combineSingleYearQueries(self, queries):
        '''
        returns a list of states and their associated homicide data,
        averaged for all years the queries contianed

        PARAMETERS:
            queries: a list each entry of which is the results of a
            singleYearQuery

        RETURN:
            a list of data for each unit (states or counties) in the
            query, each entry is a list of the data for that unit
        '''
        return []

    def stateQuery(self, startYear, endYear, state):
        '''
        returns a list of data for the specified state, including both general
        data and data for each county

        PARAMETERS:
            startYear - the first year of data to draw from
            endYear - the last year of data to draw from
            state: the state to get data for

        RETURN:
            a list of data for the state, as a list of lists
        '''
        return []

    def stateSingleYearQuery(self, year, state):
        '''
        returns a list of data for the specified state, including both general
        data and data for each county, for a single year

        PARAMETERS:
            year: the year to get data for
            state: the state to get data for

        RETURN:
            a list of data for the state, as a list of lists.
        '''
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM HomicideUCODState{year} WHERE state = {state} ORDER BY Deaths DESC"
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None



    def CountyQuery(self,  startYear, endYear, county):
        '''
        returns a list of data for a specific county

        PARAMETERS:
            startYear - the first year to get data for
            endYear - the last year to get data for

        RETURN:
            a list of data for the county
        '''
        return []

    def countySingleYearQuery(self, year, county):
        '''
        returns county data for a single year

        PARAMETERS:
            year: the year to get data for
            county: the county to get data for
        '''
        return []


def main():
	# Replace these credentials with your own
    user = "knights3"
    password = getpass.getpass()

    # Connect to the database
    connection = psycopg2.connect(database=user, user=user, password=password)

    datasource = DataSource(connection)

    # Execute a simple query: how many earthquakes above the specified magnitude are there in the data?
    results = datasource.stateSingleYearQuery(2014, "Florida")

    if results is not None:
        print("Query results: ")
        for item in results:
            print(item)

    # Disconnect from database
    connection.close()

main()
