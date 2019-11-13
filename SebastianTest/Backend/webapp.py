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
connection = psycopg2.connect(database="knights3", user="knights3", password="seal894puppy")
dataSource = DataSource(connection)


def getStateQueryData(startYear, endYear, state):
	'''
	Returns the average annual rate of homicide in a state (per 100,000 people),
	the national average annual rate of homicide (per 100,000 people), and
	the causes of homicide along with the percentage of total homicides they
	contributed, if accurate data for each said cause is provided.

	PARAMETERS:
		startYear - the first year of data to draw from
		endYear - the last year of data to draw from
		state - the name of the state to draw data from

	RETURN:
		A dictionary with the average annual rate homicide in the nation and
		state, as well as another dictionary storing each cause and the percentage of
		homicides it was responsible for

	Calls getStateCrudeRate, getCausesAndPercentages, and getNationalCrudeRate
	'''
	dataTable = {}

	fullList = dataSource.getStateQuery(startYear, endYear, state)
	print(fullList)
	dataTable["stateCrudeRate"] = getStateCrudeRate(fullList)
	dataTable["causesAndPercentages"] = getCausesAndPercentages(fullList)

	nationTotals = dataSource.getUSATotals(startYear, endYear)
	dataTable["nationalCrudeRate"] = getNationalCrudeRate(nationTotals)

	return dataTable


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
	print(averageDeaths)
	print(averagePopulation)

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

def checkStartYear(startYear):
	if startYear == "":
		startYear = "1999"
	return startYear

def checkEndYear(endYear):
	if endYear == "":
		endYear = "2017"
	return endYear

def checkState(state):
	if state == "":
		state = "Alabama"
	return state

@app.route('/', methods=['GET', 'POST'])
def getStateQueryResults():
	'''
	Loads the homepage and returns a results page corresponding to the user's query. Directs
	user to an error page if the query was not formatted properly
	'''
	if (request.method == 'POST'):

		try:
			start = request.form.get('startYear')
			start = checkStartYear(start)
			start = int(start)

			end = request.form.get('endYear')
			end = checkEndYear(end)
			end = int(end)

			state = request.form.get('state')
			state = checkState(state)

			dataTable = getStateQueryData(start, end, state)

			return render_template('Results.html', stateCrudeRate = dataTable["stateCrudeRate"],
										nationalCrudeRate = dataTable["nationalCrudeRate"],
										causesAndPercentages = dataTable["causesAndPercentages"],
										state = state,
										startYear = start,
										endYear = end) 
		except Exception as e:

			return render_template('Error.html', error = e)
	else:

		return render_template('HomePage2.html')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)