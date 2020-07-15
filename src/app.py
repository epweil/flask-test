#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.

from flask import Flask, render_template,url_for, redirect, request
import os
from os import path
import planes
import plotter
import csv
import pandas as pd
Path = os.getcwd()
app = Flask(__name__, template_folder="../templates")
# Screen to choose a plane 
@app.route('/')
def index():
    app.template_folder = "../templates"
    #File = Path+'/templates/planes.html'
    return render_template('planes.html')
#Screen to choose a bag
@app.route('/bags', methods=["POST"])
def bags(): 
    selected = request.form['button3'] 
    app.config['selectedPlane'] = selected
    filePath = Path
    filePath += "/bags/"+selected 
    app.config['bags'] = os.listdir(filePath)
    return render_template('rosbags.html')
#Screen to choose a plot 
@app.route('/plot', methods=["POST"])
def plot():
    selected = request.form['button'] 
    selected = selected[:len(selected)-4]
    fileName = Path
    fileName += "/templates/planes/"+ app.config['selectedPlane'] + "/" + selected
    app.config['plots'] = os.listdir((fileName))
    app.config['currentBag'] = selected
    return render_template('plots.html')
#Screen to see a plot 
@app.route('/seeMore',methods=["POST"])
def seeing():
    selected = request.form['button2'] 
    fileName = "planes/" +app.config['selectedPlane'] + "/"+app.config['currentBag'] +"/"+ selected
    return render_template(fileName)
#Screen to make a new plot 
#Generates option to choose from based on topics recorded in csv files 
@app.route('/newPlot', methods=["POST"])
def newPlot():
    options = []
    filePath = Path + "/csvs/"+app.config['selectedPlane']+"/"+app.config['currentBag']+"/"
    topics =  os.listdir(filePath)
    try:
        app.config['options'] = pd.read_csv(filePath+"canPlot.csv", index_col = 0).iloc[:, 0].values
    except:
        app.config['options'] = []
    return render_template('newPlot.html')
#New normal plot or new linked plot 
@app.route('/makeNewPlot', methods=["GET","POST"])
def whatToDo():
    if(request.form['Plot'] == "Plot"):
        return (makeNewPlot())
    else:
       return ( makeLinkedPlot())
#Normal plot 
def makeNewPlot():
    opperationsX =[]
    opperationsY = []
    y = request.form.getlist('checkboxY')
    x =  request.form.getlist('checkboxX')
    for i in y:
        opperationsY.append( request.form.getlist(i,type = int))
    for i in x:
        opperationsX.append( request.form.getlist(i,type = int))
    title = request.form['title']
    Path =  os.getcwd() + "/csvs/" + app.config['selectedPlane'] +"/"+app.config['currentBag'] +"/"
    plotter.makePlotFromList(y,x,Path,app.config['currentBag'],app.config['selectedPlane'],title, opperationsX, opperationsY)
    title.replace(" ","-")
    title = title+".html"
    title.replace(" ","_")
    clear()
    return render_template("planes/" +app.config['selectedPlane'] + "/"+app.config['currentBag'] +"/"+ title )
#Make a new linked plot
def makeLinkedPlot():
    opperationsY = []
    opperationsX = []
    y = (request.form.getlist('checkboxY'))
    x = (request.form.getlist('checkboxX'))
    app.config["plotY"].append(y)
    app.config["plotX"].append(x)
    for i in y:
        opperationsY.append( request.form.getlist(i))
    for i in x:
        opperationsX.append( request.form.getlist(i+"X"))
    app.config["opperationsX"].append(opperationsX)
    app.config["opperationsY"].append(opperationsY)
    app.config['title'].append(request.form['title'])
    return render_template('linkedPlot.html')
#Add another plot to the linked plot 
@app.route('/linkedPlot', methods=["GET","POST"])
def linkedPlot():
    opperationsY = []
    opperationsX = []
    y = (request.form.getlist('checkboxY' ))
    x = (request.form.getlist('checkboxX'))
    app.config["plotY"].append(y)
    app.config["plotX"].append(x)
    for i in y:
        opperationsY.append( request.form.getlist(i,type = int))
    for i in x:
        opperationsX.append( request.form.getlist(i,type = int))
    app.config["opperationsX"].append(opperationsX)
    app.config["opperationsY"].append(opperationsY)
    app.config['title'].append(request.form['title'])
    if( request.form['Do'] == "Done"):
        return saveLinkedPlot()
    else:
        return render_template('linkedPlot.html')
#Save and publish the linked plot 
def saveLinkedPlot():
    Path =  os.getcwd() + "/csvs/" + app.config['selectedPlane'] +"/"+app.config['currentBag'] +"/" 
    for i in range(len(app.config['title'])):
        app.config['title'][i].replace(" ","-")
    titleName = plotter.makeSubplotFromList(app.config['plotY'],app.config['plotX'],Path,app.config['currentBag'],app.config['selectedPlane'],app.config['title'],app.config["opperationsX"], app.config["opperationsY"])  
    clear()
    return render_template("planes/" +app.config['selectedPlane'] + "/"+app.config['currentBag'] +"/"+ titleName )
#Clear lists 
def clear():
    app.config['title'] = []
    app.config['legend'] = []
    app.config["plotY"] = []
    app.config["plotX"] = []
    app.config["xAxis"] = []
    app.config["yAxis"] = []
    app.config["opperationsX"] = []
    app.config["opperationsY"] = []
#Main
if __name__ == "__main__":
    cwd = os.getcwd()
    print(cwd+"/templates/planes/")
    if not os.path.exists(cwd+"/templates/planes/"):
        
        os.mkdir(cwd+"/templates/planes/")
    if not os.path.exists(cwd+"/csvs"):
        os.mkdir(cwd+"/csvs")
    if not os.path.exists(cwd+"/bags"):
        os.mkdir(cwd+"/bags")
    Path2 = Path + "/planes"
    app.config['planes'] = planes.getPlanes()
    app.config['title'] = []
    app.config['legend'] = []
    app.config["plotY"] = []
    app.config["plotX"] = []
    app.config["xAxis"] = []
    app.config["yAxis"] = []
    app.config["opperationsX"] = []
    app.config["opperationsY"] = []
    app.run()