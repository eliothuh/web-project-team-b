from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
app = Flask(__name__)

def getStateDeathOverTimeLables(yearsStatesList):
	'''
	takes in a list of data for a specified state and returns a string contianing
	formated data for the javascript to us
	'''
	return 'var labels = ["1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017"]'


def getStateDeathOverTimeDeaths(yearsStatesList):
	'''
	takes in a list of data for the specified state and returns a string that will
	be evaluated by javascript to get all death counts
	'''
	return 'var data = [188, 59, 99, 150, 144, 135, 184, 195, 220, 232, 214, 217, 251, 277, 264, 239, 210, 228, 206]'


def getStateDeathCauses(stateDeathCausesDict):
	'''
	returns a string form of a list of all causes of death in the state
	'''
	return 'var labels = ["sharp object", "handgun", "other firearm", "other"]'


def getStateDeathCausesPercent(stateDeathCausesDict):
	'''
	returns a string form of a list of all percentages associated with causes of
	death by homicide in a state
	'''
	return 'var data = [30, 43, 91, 29]'


@app.route("/")
def chart():
	inputdata = getStateDeathOverTimeDeaths(0)
	inputlabels = getStateDeathOverTimeLables(0)
	inputtitle = 'var label = "New Hampshire Homicides, 1999 - 2017"'
	return render_template("basicline.html",
							inputdata=inputdata,
							inputlabels=inputlabels,
							inputtitle=inputtitle)


@app.route("/pie")
def pieChart():
	inputdata = getStateDeathCausesPercent(0)
	inputlabels = getStateDeathCauses(0)
	inputtitle = 'var label = "New Hampshire Homicides by type, 1999 - 2017"'
	return render_template("basicpie.html",
							inputdata=inputdata,
							inputlabels=inputlabels,
							inputtitle=inputtitle)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)
