#!/usr/bin/env python3
'''
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

def getStateData(start, end, state):
	dataTable = {}
	
	fullList = dataSource.getStateQuery(start, end, state)
	dataTable["stateCrudeRate"] = getStateCrudeRate(fullList)
	dataTable["causesAndPercentages"] = getCausesAndPercentages(fullList)
	
	nationTotals = dataSource.getUSATotals(start, end)
	dataTable["nationalCrudeRate"] = getNationalCrudeRate(nationTotals)
	
	print(dataTable["stateCrudeRate"])
	print(dataTable["nationalCrudeRate"])
	print(dataTable["causesAndPercentages"])
	

		
	return dataTable


def getStateCrudeRate(list):
	averageDeaths = getAverageStateDeaths(list)
	averagePopulation = getAverageStatePopulation(list)
	print("average deaths (state): ")
	print(averageDeaths)
	print("average population (state): ")
	print(averagePopulation)
	return round(averageDeaths*100000/averagePopulation, 3)


def getAverageStateDeaths(list):
	tupleIndex = 0;
	stateTotal = 0;
	numYears = len(list)

	for year in list:
		tupleIndex = len(year) - 2
		if(tupleIndex > 0):
			stateTotal += year[tupleIndex][5]

	return stateTotal/numYears


def getAverageStatePopulation(list):
	numYears = len(list)
	total = 0

	for year in list:
		if(len(year) > 1):
			total += year[0][6]

	return total/numYears

def getNationalCrudeRate(list):
	averageDeaths = getNationalAverageDeaths(list)
	averagePopulation = getAverageNationalPopulation(list)
	print("average deaths (nation): ")
	print(averageDeaths)
	print("average population (nation): ")
	print(averagePopulation)

	return round(averageDeaths*100000/averagePopulation, 3)


def getNationalAverageDeaths(list):
	total = 0
	tupleIndex = 0
	numYears = len(list)

	for year in list:
		tupleIndex = len(year) - 1
		if(tupleIndex > 0):
			total += year[tupleIndex][5]

	return total/numYears

def getAverageNationalPopulation(list):
	numYears = len(list)
	total = 0
	tupleIndex = 0

	for year in list:
		tupleIndex = len(year) - 1
		if(tupleIndex > 0):
			total += year[tupleIndex][6]

	return total/numYears


def getCausesAndPercentages(list):
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
		
		for causeData in year:
			if(causeData[3] == cause):
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
		
		for causeData in year:
			if(causeData[3] == cause):
				totalDeaths += causeData[5]
		
	return totalDeaths


def getPercentOther(causesList, list):
	percentageKnown = 0

	for cause in causesList:
		percentageKnown += causesList[cause]
	
	return round(100 - percentageKnown, 3)
	
"""




	add total homicides, divide by avg population, multiply by 100,000
	Homicide average: total us homicides divide by avg population, multiply 100,000

	start w causes in first yr
	boolean valid
	array of year arrays
	year array: tuples for each cause of death, tuple for total, then array containing
	tuples for each county with causes"""


@app.route('/')
def homepage():
    return 'Hello, Citizen of CS257.'

@app.route('/home/', methods=['GET', 'POST'])
def getStateQueryResults():
	if (request.method == 'POST'):
		if(request.form.get('startYear') != None and request.form.get('endYear') != None
													and request.form.get('state')!= None):
			start = int(request.form.get('startYear'))
			end = int(request.form.get('endYear'))
			state = request.form.get('state')
			dataTable = getStateData(start, end, state)
		
			return render_template('Results.html', stateCrudeRate = dataTable["stateCrudeRate"],
											nationalCrudeRate = dataTable["nationalCrudeRate"], 
											causesAndPercentages = dataTable["causesAndPercentages"])

	else:

		return render_template('HomePage2.html')


@app.route('/greet/<person>/')
def greet(person):
    return render_template('greet.html',
                           person=person)

@app.route('/fruit')
def fruit():
    myFruit = [
        {'name': 'apple', 'rating': 7},
        {'name': 'banana', 'rating': 5},
        {'name': 'pear', 'rating': 4}
    ]

    return render_template('fruit.html',
                           fruits=myFruit)

@app.route('/fruitImg/')
def fruitImg():
    return render_template('fruitImg.html')

@app.route('/authors/<author>')
def get_author(author):
    ''' What a dopey function! But it illustrates a Flask route with a parameter. '''
    if author == 'Twain':
        author_dictionary = {'last_name':'Twain', 'first_name':'Mark'}
    elif author == 'Shakespeare':
        author_dictionary = {'last_name':'Shakespeare', 'first_name':'William'}
    else:
        author_dictionary = {'last_name':'McBozo', 'first_name':'Bozo'}
    return json.dumps(author_dictionary)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)

'''
def main():
	getStateData(1999, 2017, "New Hampshire")


main()
'''
