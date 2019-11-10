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
	fullList = dataSource.getStateQuery(start, end, state)
	stateCrudeRate = getStateCrudeRate(fullList)
	nationTotals = dataSource.getUSATotals(start, end)
	nationalCrudeRate = getNationalCrudeRate(nationTotals)
	causesAndPercentages = getCausesAndPercentages(fullList)
	print(stateCrudeRate)
	print(nationalCrudeRate)
	
	
def getStateCrudeRate(list):
	total = getStateTotal(list)
	averagePopulation = getAveragePopulation(list)
	
	return total*100000/averagePopulation
		
		
def getStateTotal(list):
	tupleIndex = 0;
	stateTotal = 0;
	
	for year in list: 
		tupleIndex = len(year) - 2;
		stateTotal += year[tupleIndex][5]
		
	return stateTotal
	
	
def getAveragePopulation(list):
	numYears = len(list)
	total = 0
	
	for year in list:
		total += year[0][6]
		
	return total/numYears 
	
	
def getNationalCrudeRate(list):
	total = getNationalTotal(list)
	averagePopulation = getAveragePopulation(list)
	
	return total*100000/averagePopulation


def getNationalTotal(list):
	total = 0
	
	for year in list:
		total += year[50][5]
		
	return total 
	
	
def getCausesAndPercentages(list):
	lastIndex = len(list[0]) - 3 
	
	if(lastIndex < 0):
		causeAndPercent
		causeAndPercent["Other"] = 100 
		return causeAndPercent
	
	causeAndPercent = getStartingCauses(list, lastIndex)
	causeAndPercent = addPercentages(causeAndPercent, list)
	return None	
	
	
def getStartingCauses(list, lastIndex):
	causeAndPercent = {}
	
	for cause in range(lastIndex):
		causeAndPercent[list[0][cause][3]] = list[0][cause][5]
	
	return causeAndPercent 

"""def addPercentages(causeAndPercent, list): 
	for cause in causeAndPercent"""
		
		 
	
	
""""	add total homicides, divide by avg population, multiply by 100,000 
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
		start = request.form.get('startYear')
		end = request.form.get('endYear')
		state = request.form.get('state')
		list = getStateData(start, end, state)

	return render_template("results.html", start, end, state)

@app.route('/home/')
def boring():
    return render_template('Homepage.html')

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

"""if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)"""
    
def main():
	getStateData(1999, 2016, "Florida")
	

main()