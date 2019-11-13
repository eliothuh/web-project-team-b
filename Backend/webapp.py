#!/usr/bin/env python3
'''
webapp.py sends queries from the frontend to the backend. 
It loads and updates pages and processes data in a form easy
for the html to present. 
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
	Returns the average annual number of homicides in a state (per 100,000 people),
	the national average annual number of homicides (per 100,000 people), and 
	The causes of homicide along with their percentages, if accurate
	data for each said cause is provided.

	PARAMETERS:
		startYear - the first year of data to draw from
		endYear - the last year of data to draw from
		state - the name of the state to draw data from

	RETURN:
		A dictionary with the average annual number of homicides in the nation and
		state, as well as another dictionary storing each cause and the percentage of
		homicides it was responsible for

	Calls getStateCrudeRate, getCausesAndPercentages, and getNationalCrudeRate
	'''
	dataTable = {}
	
	fullList = dataSource.getStateQuery(startYear, endYear, state)
	print(fullList)
	dataTable["stateCrudeRate"] = getStateCrudeRate(fullList)
	dataTable["causesAndPercentages"] = getCausesAndPercentages(fullList)
	
	nationTotals = dataSource.getUSATotals(start, end)
	dataTable["nationalCrudeRate"] = getNationalCrudeRate(nationTotals)
		
	return dataTable


def getStateCrudeRate(list):
	'''
	Returns the average annual number of homicides in a state (per 100,000 people)

	PARAMETERS:
		list - an array of data for each year the user queried 
			
	RETURN:
		The average annual number of homicides in the user's requested state (per 100,000)

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
		list - an array of data for each year the user queried 
			
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
		list - an array of data for each year the user queried 
			
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
		list - an array of data for each year in the range the user queried 
			
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
		list - an array of data for each year in the range the user queried 
			
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
		list - an array of data for each year in the range the user queried 
			
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
	Returns the nation's average population over the user's specified year range

	PARAMETERS:
		list - an array of data for each year in the range the user queried 
			
	RETURN:
		The national average population over the specified year range
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
	totalDeathsByCause = getTotalDeathsByCause(cause, list)
	numberOfYears = len(list)
	totalDeaths = getAverageStateDeaths(list)*numberOfYears
	
	return round(totalDeathsByCause * 100/totalDeaths, 3)
		

def getTotalDeathsByCause(cause, list):
	totalDeaths = 0 
	
	for year in list:
		lastIndex = len(year) - 3
		
		for index in range(lastIndex):
			if(year[index][3] == cause):
				totalDeaths += year[index][5]
		
	return totalDeaths


def getPercentOther(causesList, list):
	percentageKnown = 0

	for cause in causesList:
		percentageKnown += causesList[cause]
	
	return round(100 - percentageKnown, 3)


@app.route('/', methods=['GET', 'POST'])
def getStateQueryResults():
	if (request.method == 'POST'):
	
		try:
			start = int(request.form.get('startYear'))
			end = int(request.form.get('endYear'))
			state = request.form.get('state')
			dataTable = getStateData(start, end, state)
			
			return render_template('Results.html', stateCrudeRate = dataTable["stateCrudeRate"],
										nationalCrudeRate = dataTable["nationalCrudeRate"], 
										causesAndPercentages = dataTable["causesAndPercentages"])
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

