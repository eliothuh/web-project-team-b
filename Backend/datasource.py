import psycopg2
import getpass

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.

    grade these methods:
        - stateSingleYearQuery
        - countyQuery
        - countySingleYearQuery
    '''

    def __init__(self, connection):
        self.connection = connection
        self.stateDictionary = {
                "Alabama" : "AL",
                "Alaska" : "AK",
                "Arizona" : "AZ",
                "Arkansas" : "AR",
                "California" : "CA",
                "Colorado" : "CO",
                "Connecticut" : "CT",
                "Delaware" : "DE",
                "Florida" : "FL",
                "Georgia" : "GA",
                "Hawaii" : "HI",
                "Idaho" : "ID",
                "Illinois" : "IL",
                "Indiana" : "IN",
                "Iowa" : "IA",
                "Kansas" : "KS",
                "Kentucky" : "KY",
                "Louisiana" : "LA",
                "Maine" : "ME",
                "Maryland" : "MD",
                "Massachusetts" : "MA",
                "Michigan" : "MI",
                "Minnesota" : "MN",
                "Mississippi" : "MS",
                "Missouri" : "MO",
                "Montana" : "MT",
                "Nebraska" : "NE",
                "Nevada" : "NV",
                "New Hampshire" : "NH",
                "New Jersey" : "NJ",
                "New Mexico" : "NM",
                "New York" : "NY",
                "North Carolina" : "NC",
                "North Dakota" : "ND",
                "Ohio" : "OH",
                "Oklahoma" : "OK",
                "Oregon" : "OR",
                "Pennsylvania" : "PA",
                "Rhode Island" : "RI",
                "South Carolina" : "SC",
                "South Dakota" : "SD",
                "Tennessee" : "TN",
                "Texas" : "TX",
                "Utah" : "UT",
                "Vermont" : "VT",
                "Virgina" : "VA",
                "Washington" : "WA",
                "West Virgina" : "WV",
                "Wisconsin" : "WI",
                "Wyoming" : "WY",
                }


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
        Calls USASingleYearQuery
        '''
        return []

    def USASingleYearQuery(self, year):
        '''
        returns a list of all states and thier associated homicide data

        PARAMETERS:
            year: the year of data to draw from

        RETURN:
            a list of all states and associated data

        Calls stateSingleYearQuery
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

        Calls StateSingleYearQuery
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

        Grade this method
        '''

        self.checkValidYear(year)

        results = []

        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM states{year} WHERE statename = '{state}' ORDER BY Deaths DESC"
            cursor.execute(query)
            results.append(cursor.fetchall())
        except Exception as e:
            print("Something when wrong when excecuting the query (state)")


        countyPattern = self.getAllCountyPattern(state)

        countyData = self.countySingleYearQuery(year, countyPattern)

        results.append(countyData)

        return results

    def getAllCountyPattern(self, state):
        '''
        returns an pattern that will match for every county in the state

        PARAMETERS:
            state: the state to find the counties of

        RETURN:
            a pattern that will match all counties of the state with a LIKE operator

        '''
        return f"%{self.stateDictionary.get(state)}"




    def countyQuery(self,  startYear, endYear, county):
        '''
        returns a list of data for a specific county or list of counties (using LIKE)

        PARAMETERS:
            startYear - an integer, the first year to get data for
            endYear - an integer, the last year to get data for
            county - the expression defining which county names may be excepted
        RETURN:
            a list of data for the county

        Grade this method
        '''
        results = []

        self.checkValidRange(startYear, endYear)

        yearRange = endYear - startYear + 1

        try:
            for i in range(yearRange):
                currentYear = i + startYear
                results.append(self.countySingleYearQuery(currentYear, county))

            return results
        except Exception as e:
            print("Something went wrong when executing the query: " + str(e))
            return None

    def countySingleYearQuery(self, year, county):
        '''
        returns county data for a single year for one county or a list
        of counties (using LIKE)

        PARAMETERS:
            year - the year to get data for
            county -  the expression defining which county names may be excepted

        Grade this method
        '''
        self.checkValidYear(year)

        results = []


        cursor = self.connection.cursor()
        query = f"SELECT * FROM counties{year} WHERE county LIKE '{county}'"
        cursor.execute(query)
        results.append(cursor.fetchall())


        return results


    def checkValidYear(self, year):
        if(year < 1999 or year > 2017):
            print("invalid year")
            exit()

    def checkValidRange(self, startYear, endYear):
        if (startYear < 1999 or endYear > 2017 or startYear > endYear):
            print("invalid year range")
            exit()
            
            
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


def main():

    user = input("please enter your username: ")
    password = getpass.getpass()

    # Connect to the database
    #connection = psycopg2.connect(database=user, user=user, password=password)

    datasource = DataSource(connect(user, password))

    # Execute a simple query: how many earthquakes above the specified magnitude are there in the data?
    results = datasource.stateSingleYearQuery(2000, "Florida")
    print(results)
    results = datasource.countyQuery(2000, 2002, "Los Angeles County, CA")
    print(results)
    results = datasource.countyQuery(2000, 2020, "Los Angeles County, CA")

    if results is not None:
        print("Query results: ") 
        for item in results:
            print(item)

    print("Query complete")

    # Disconnect from database
    connection.close()

main()
