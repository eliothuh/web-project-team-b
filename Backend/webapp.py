#!/usr/bin/env python3
'''
webapp.py sends queries from the frontend to the backend.
It loads and updates pages and processes data in a form easy
for the html to present.

***We have only implemented the text field inputs! The buttons at the top do not work!***
'''

import flask
from flask import render_template, request
import json
import sys
from datasource import *
import psycopg2

app = flask.Flask(__name__)
connection = psycopg2.connect(database="huhe", user="huhe", password="tree695eye")
dataSource = DataSource(connection)


def getStateQueryData(startYear, endYear, state):
	'''
	Returns the average annual rate of homicide in a state (per 100,000 people),
	the national average annual rate of homicide (per 100,000 people),
	a line of Javascript code that stores the average annual rate of homicide during each year within the specified
	range in the state (per 100,000), another line of Javascript code storing a list of years within the
	specified range, and the causes of homicide along with the percentage of total homicides they
	contributed, if accurate data for each said cause is provided.

	PARAMETERS:
		startYear - the first year of data to draw from
		endYear - the last year of data to draw from
		state - the name of the state to draw data from

	RETURN:
		A dictionary containing the average annual rate homicide in the nation and
		state, Strings representing Javascript code to store the annual rate of homicide each year and
		a list of the years in the specified range, and another dictionary storing each cause and the percentage of
		homicides it was responsible for

	Calls getStateCrudeRate, getCausesAndPercentages, getStateSingleYearCrudeRates, getYearRange,
	and getNationalCrudeRate
	'''
	dataTable = {}
	fullList = dataSource.getStateQuery(startYear, endYear, state)

	if isinstance(fullList, Exception):
		raise fullList

	dataTable["yearRange"] = getYearRange(startYear, endYear)
	dataTable["singleYearCrudeRates"] = getStateSingleYearCrudeRates(startYear, endYear, state)

	dataTable["stateCrudeRate"] = getStateCrudeRate(fullList)
	dataTable["causesAndPercentages"] = getCausesAndPercentages(fullList)

	nationTotals = dataSource.getUSATotals(startYear, endYear)
	dataTable["nationalCrudeRate"] = getNationalCrudeRate(nationTotals)

	print("all done!")

	return dataTable


def getStateSingleYearCrudeRates(startYear, endYear, state):
	'''
	gets the rate of homicide over each year from startYear to endYear, places all of these
	crude rates into a list of ints, and then returns this data as a formatted String
	our Javascript file can parse.

    PARAMETERS:
    startYear: the first year to find the homicide crude rate for
    endYear: the last year to find the homicide crude rate for
    state: the state to find the homicide crude rate for

    RETURN:
    A String representation of our array of crude rates over the year range

    Calls getStateCrudeRate, formatSingleYearCrudeRates
    '''
	list = []
	rate = 0
	crudeRates = []

	for year in range (startYear, endYear + 1):
		list = dataSource.getStateQuery(year, year, state)
		rate = getStateCrudeRate(list)
		crudeRates.append(rate)

	variableName = "data"
	return formatJavascriptString(crudeRates, variableName)


def getStateCrudeRate(list):
	'''
	Returns the average annual rate of homicide in a state (per 100,000 people) over the
	specified year range

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		A String representing the average annual number of homicides in the user's
		requested state (per 100,000) rounded to 3 decimal places

	Calls getAverageStateDeaths, getAverageStatePopulation
	'''
	averageDeaths = getAverageStateDeaths(list)
	averagePopulation = getAverageStatePopulation(list)

	return round(averageDeaths*100000/averagePopulation, 3)


def getAverageStateDeaths(list):
	'''
	Returns the average annual number of homicides in a state (per 100,000 people)

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		The average annual number of homicides in the user's requested state (per 100,000)

	Calls getAverageStateDeaths, getAverageStatePopulation
	'''
	tupleIndex = 0;
	stateTotal = 0;
	numYears = len(list)

	for year in list:
		tupleIndex = len(year) - 2
		if(tupleIndex > 0):
			stateTotal += year[tupleIndex][5]

	return stateTotal/numYears


def getAverageStatePopulation(list):
	'''
	Returns the average annual population of the state over user's queried year range

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		The average annual population of the user's specified state over the user's
		specified year range
	'''
	numYears = len(list)
	total = 0

	for year in list:
		if(len(year) > 1):
			total += year[0][6]

	return total/numYears


def formatJavascriptString(list, variableName):
	'''
	takes in a list and a variable name and formats it into a string representing a line
	of Javascript code that assigns the inputted array to a variable with the specified name

	PARAMETERS:
	list: the list we want to store in Javascript
	variableName: the name of the variable we want to store the list in

	RETURN:
	A String representing the Javascript code that will store inputted list into
	a variable with our specified name in our Javascript file.
	'''
	javascriptString = "var " + variableName + " = "
	javascriptString += "[" + ', '.join([str(elem) for elem in list]) + "]"
	return javascriptString

def getYearRange(startYear, endYear):
	list = []

	for year in range(startYear, endYear + 1):
		list.append(year)

	variableName = "labels"

	return formatJavascriptString(list, variableName)


def getNationalCrudeRate(list):
	'''
	Returns the national average annual rate of homicide per 100,000 people

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		The national average annual rate of homicide per 100,000 people over the
		year range the user queried for

	Calls getNationalAverageDeaths and getAverageNationalPopulation
	'''
	averageDeaths = getNationalAverageDeaths(list)
	averagePopulation = getAverageNationalPopulation(list)

	return round(averageDeaths*100000/averagePopulation, 3)


def getNationalAverageDeaths(list):
	'''
	Returns the average annual number of homicides across the nation

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		The national average annual number of homicides
	'''
	total = 0
	tupleIndex = 0
	numYears = len(list)

	for year in list:
		tupleIndex = len(year) - 1
		if(tupleIndex > 0):
			total += year[tupleIndex][5]

	return total/numYears


def getAverageNationalPopulation(list):
	'''
	Returns the nation's average population over the user's specified year range

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		The national average population over the specified year range
	'''
	numYears = len(list)
	total = 0
	tupleIndex = 0

	for year in list:
		tupleIndex = len(year) - 1
		if(tupleIndex > 0):
			total += year[tupleIndex][6]

	return total/numYears


def getCausesAndPercentages(list):
	'''
	Returns a dictionary with each key being a cause of homicide and each value being the
	percentage of homicides the associated cause was responsible for

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		A dictionary with each key being a cause of homicide and each value being the
		percentage of homicides the associated cause was responsible for

	Calls isValidCause, getPercent, and getPercentOther
	'''
	lastIndex = len(list[0]) - 3
	causesList = {}

	for index in range(lastIndex):
		cause = list[0][index][3]
		if(isValidCause(cause, list)):
			causesList[cause] = getPercent(cause, list)

	causesList["Other"] = getPercentOther(causesList, list)

	return causesList


def isValidCause(cause, list):
	'''
	Determines whether the inputted cause has valid data. More specifically, this method
	checks whether the data for this cause was omitted in any of the specified years
	and does not regard it as valid in this case.

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		A True value if there was data for this cause every year and a False value otherwise
	'''
	foundAllYears = True

	for year in list:
		foundThisYear = False
		lastIndex = len(year) - 3

		for index in range(lastIndex):
			if(year[index][3] == cause):
				foundThisYear = True

		foundAllYears = foundAllYears and foundThisYear

	return foundAllYears


def getPercent(cause, list):
	'''
	Returns the percentage of total homicides the specified cause of homicide was responsible
	for

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		A String representing a number with at most 3 decimal places representing the percentage
		of deaths the specified cause was responsible for
	'''
	totalDeathsByCause = getTotalDeathsByCause(cause, list)
	numberOfYears = len(list)
	totalDeaths = getAverageStateDeaths(list)*numberOfYears

	return round(totalDeathsByCause * 100/totalDeaths, 3)


def getTotalDeathsByCause(cause, list):
	'''
	Returns the total number of deaths the specified cause was responsible for
	over the user's queried year range in the specified state

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		An integer representing the total number of homicides the specified cause contributed
	'''
	totalDeaths = 0

	for year in list:
		lastIndex = len(year) - 3

		for index in range(lastIndex):
			if(year[index][3] == cause):
				totalDeaths += year[index][5]

	return totalDeaths


def getPercentOther(causesList, list):
	'''
	Returns the percentage of homicides over the user's queried year range and specified state
	not caused by any of the valid causes already found

	PARAMETERS:
		list - an array of state homicide data for each year in the range the user queried

	RETURN:
		A String representation of a float rounded to 3 decimal places representing the
		percentage of homicides not caused by any of the specified causes
	'''
	percentageKnown = 0

	for cause in causesList:
		percentageKnown += causesList[cause]

	return round(100 - percentageKnown, 3)


def adjustYears(startYear, endYear):
	'''
	Adjusts the start and end years to be the same year if only one is specified
	and sets the start to 1999 and end to 2017 if neither is specified.

	PARAMETERS:
		startYear- the start year specified by the user
		endYear- the ending year specified by the user

	RETURN:
		An array of Strings, each specifying the start and end year
	'''
	if(startYear is None):
		startYear = "1999"
		endYear = "2017"
		return startYear, endYear

	startYear.strip()
	endYear.strip()

	if(startYear == "" and endYear == ""):
		startYear = "1999"
		endYear = "2017"

	elif(startYear == ""):
		startYear = endYear

	elif(endYear == ""):
		endYear = startYear

	return startYear, endYear


def setYearsToInts(startYear, endYear):
	'''
	Converts the inputted start year and end year to ints.

	PARAMETERS:
		startYear- the starting year for the query passed as a String
		endYear- the ending year for the query passed as a String

	RETURN:
		the start year String converted into and int and the end year String
		converted into an int
	'''

	startYear = int(startYear)
	endYear = int(endYear)

	return startYear, endYear


def cleanStateInput(state):
	'''
	if no state is provided, sets it to Alabama
	if the state starts with a lowercase letter, makes it a capital letter.
	'''
	state = state.strip()

	if state == "":
		state = "Alabama"

	correctedState = ""
	wordList = state.split(" ")

	for word in wordList:
		correctedWord = cleanIndividualWord(word)
		correctedState = correctedState + correctedWord + " "

	correctedState = correctedState.strip()

	return correctedState


def cleanIndividualWord(word):
	'''
	makes the first letter of the word a capital letter
	'''
	nonCapitalizedWords = ["a", "an", "for", "and", "or", "nor", "but", "yet", "so", "at",
	 "around", "by", "after", "along", "from", "of", "on", "to", "with", "without"]
	word = word.lower()
	if word not in nonCapitalizedWords:
		word = word[0].capitalize() + word[1:]

	return word


def getNationalQueryData(startYear, endYear):
	nationalQueryData = {}
	nationTotals = dataSource.getUSATotals(startYear, endYear)
	nationalQueryData["nationalCrudeRate"] = getNationalCrudeRate(nationTotals)
	nationalQueryData["mostDangerousState"], nationalQueryData["mostDangerousStateRate"] = getMostDangerousStateAndData(startYear, endYear)
	nationalQueryData["yearRange"] = getYearRange(startYear, endYear)
	nationalQueryData["singleYearCrudeRates"] = getNationalSingleYearCrudeRates(startYear, endYear)

	return nationalQueryData


def getMostDangerousStateAndData(startYear, endYear):
	crudeRate = 0
	currentStateRate = 0
	mostDangerousState = ""

	for state in dataSource.stateDictionary:
		currentStateRate = getStateCrudeRate(dataSource.getStateQuery(startYear, endYear, state))

		if (currentStateRate > crudeRate):
			crudeRate = currentStateRate
			mostDangerousState = state

	return mostDangerousState, crudeRate

def getNationalSingleYearCrudeRates(startYear, endYear):
	list = []
	rate = 0
	crudeRates = []

	for year in range (startYear, endYear + 1):
		list = dataSource.getUSATotals(year, year)
		rate = getNationalCrudeRate(list)
		crudeRates.append(rate)

	variableName = "data"
	return formatJavascriptString(crudeRates, variableName)


@app.route('/', methods = ['POST', 'GET'])
def getNationalQueryResults():
	'''
	Loads the homepage and returns a results page corresponding to the user's query. Directs
	user to an error page if the query was not formatted properly
	'''
	try:
		start = request.args.get('startYear')
		end = request.args.get('endYear')
		start, end = adjustYears(start, end)
		start, end = setYearsToInts(start, end)

		dataTable = getNationalQueryData(start, end)

		print(dataTable["singleYearCrudeRates"])
		print(dataTable["yearRange"])


		return render_template('HomePage2.html',
									inputdata = dataTable["singleYearCrudeRates"],
									inputlabels = dataTable["yearRange"],
									inputtitle = f"National Homicide Rate from {{start}} to {{end}}",
									nationalCrudeRate = dataTable["nationalCrudeRate"],
									startYear = start,
									endYear = end,
									mostDangerousState = dataTable["mostDangerousState"],
									mostDangerousStateRate = dataTable["mostDangerousStateRate"])

	except Exception as e:

		return render_template('Error.html', error = e)


@app.route('/stateQuery/')
def getMapQueryResults():
	'''
	Loads a resulting state query page if the user clicks on one of the states in the
	interactive map
	'''
	if(request.method == 'GET'):

		try:
			start = request.args.get('startYear')
			end = request.args.get('endYear')
			start, end = adjustYears(start, end)
			start, end = setYearsToInts(start, end)
			print(start)
			print(end)

			state = request.args.get('state')
			state = cleanStateInput(state)

			"""(inputlabels, inputdata, inputtitle)"""

			dataTable = getStateQueryData(start, end, state)

			return render_template('Results.html', stateCrudeRate = dataTable["stateCrudeRate"],
										nationalCrudeRate = dataTable["nationalCrudeRate"],
										causesAndPercentages = dataTable["causesAndPercentages"],
										state = state,
										startYear = start,
										endYear = end,
										inputdata = dataTable["singleYearCrudeRates"],
										inputlabels = dataTable["yearRange"],
										inputtitle = f"{state} Annual Crude Rates")

		except Exception as e:

			return render_template('Error.html', error = e)

	else:

		state = Alabama
		start = 1999
		end = 2017
		dataTable = getStateQueryData(start, end, state)

		return render_template('Results.html', stateCrudeRate = dataTable["stateCrudeRate"],
										nationalCrudeRate = dataTable["nationalCrudeRate"],
										causesAndPercentages = dataTable["causesAndPercentages"],
										state = state,
										startYear = start,
										endYear = end)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
		exit()

	host = sys.argv[1]
	port = sys.argv[2]
	app.run(host=host, port=port)
