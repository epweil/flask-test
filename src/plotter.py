#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.

import math
import os
import matplotlib.pyplot as plt
import mpld3
import numpy as np
import obspy.signal.filter
import pandas as pd
from scipy import signal
import time
import arrayGetter
import planes
#Prepare plot to be published
def plot(fig, bag,  title,yAxis,xAxis,plane,legend):
    string2 =""
    plt.legend(legend, loc='best')
    plt.xlabel(xAxis)
    plt.title(title)
    plt.ylabel(yAxis)
    for i in range(len(title)):
        if(title[i:i+1] == " "):
            string2 += "-"
        else:
            string2+=title[i:i+1]
    title = string2
    title+=".html"
    if(".bag" in bag):
        bag = bag[:len(bag)-4]
    save(fig,plane,bag,title)
    plt.clf()
#Saves and publishes plot
def save(fig,plane,bag,title):
    filePath = os.getcwd() + "/templates/planes/" + plane +"/"+bag
    html = '<script type="text/javascript" src="https://mpld3.github.io/js/d3.v3.min.js"> \n </script> <script type="text/javascript" src="https://mpld3.github.io/js/mpld3.v0.3.js"></script>'
    fig = mpld3.fig_to_html(fig)
    fig = fig[fig.find("<style>"):]
    fig = html + fig
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    filePath +="/"+ title
    Html_file= open(filePath,"w")
    Html_file.write(fig)
    Html_file.close()
#Returns the name to parse the csv file for
def name(name):
    returnNames =[]
    for ii in range(len(name),0,-1):
            if(name[ii-1:ii] == "/"):
                returnNames.append(name[:ii-1])
                returnNames.append(name[ii:])
                return returnNames
    for ii in range(len(name),1,-2):
            if(name[ii-2:ii] == "__"):
                returnNames.append(name[:ii-2])
                returnNames.append(name[ii:])
                return returnNames
    return None
#Makes a plot from a list 
def makePlotFromList(listToPlot, x,  Path, bag,plane, title, opperationsX = None, opperationsY = None, yAxis = "Various", legend= None, topic = None, xAxis = "Time in Min", returnFig = False):
    plt.clf()
    if legend is None:
        legend = listToPlot
    toPlot = []
    if (len(x) > 0):
        xAxis = x[0]
        xNames = name(x)
        if(xNames is not None):
            x = xNames[1]
            topic = xNames[0]
        if(opperationsX is None):
            x = ( arrayGetter.get(x[0],  Path,topic))
        else:
            x = ( arrayGetter.get(x[0],  Path,topic, opperationsX[0]))
    else:
        x = None
    for i in range(len(listToPlot)):
        yNames = name(listToPlot[i])
        if(yNames is not None):
            listToPlot[i] = yNames[1]
            topic = yNames[0]
        if(opperationsY is None):
            y = ( arrayGetter.get(listToPlot[i],  Path,topic))
        else:
            y = ( arrayGetter.get(listToPlot[i],  Path,topic,opperationsY[i]))
        if(x is not None):
            plt.plot(y,x)
        else:
            if( y is not None):
                plt.plot(y.index,y.values)
    plot(plt.gcf(),bag,title,yAxis,xAxis,plane,legend)
#Base plots
def makeBasePlots( Path,bag,plane):
    #vector nav status
    toPlot = []
    listOfThings = ["numSats","hDop","vDop"]
    makePlotFromList(listOfThings, [],  Path, bag,plane, "Vector-Nav-Status", yAxis = "Various", legend= ["Temp","nsats","Vdop","Hdop"] )
    #Als/AS
    toPlot = []
    listOfThings = ["airspeed_kn","altimeter_setting_in_hg","altitude_m","altitude"]
    makePlotFromList(listOfThings, [],  Path, bag,plane, "Alt and AS",opperationsY =  [[10,1,0,0],[],[],[]], yAxis = "kt and ft", legend= ["10*Airspeed","VN GPS Alt","G5 Air Alt","G5 Gps Alt"] )
    #Control SPs

    toPlot = []
    listOfThings = ["aileron_trim_pot","elevator_pot","elevator_trim_pot","rudder_pot","rudder_trim_pot","aileron_pot","maneuvering"]
    for i in listOfThings:
        [b,c]=signal.butter(5,0.05)
        a = arrayGetter.get(i,  Path)
        if(a is not None):
            plt.plot(a.index,signal.filtfilt(b,c,a,axis =0))
            #plt.plot(a.index,a.values)
    a = (arrayGetter.get("flap_indicator_b",  Path))
    if(a is not None):
            plt.plot(a.index,signal.filtfilt(b,c,a/2,axis =0))
            #plt.plot(a.index,a.values/2)
    plot(plt.gcf(),bag,"Control Surfaces (1 Hz)","Degs","Time in min",plane,["Aileron","A trim","elevator","E trim","Rudder","R Trim","FlapB/2"])
    #Steering Gear WOW
    toPlot = []
    listOfThings = ["lh_brake_pressure","rh_brake_pressure","gear_up","gear_down","weight_on_wheels","m"]
    makePlotFromList(listOfThings, [],  Path, bag,plane, "Brakes", yAxis = "Range and kpsi", legend= ["L Brake kpsi","R Brake kpsi","gearup","geardn","wow"])   
    #Throttle Control
    toPlot = []
    listOfThings =[ "rh_power_pot","lh_prop_pot","rh_prop_pot","lh_condition_pot","rh_condition_pot", "maneuvering"]
    makePlotFromList(listOfThings, [],  Path, bag,plane, "Throttle", yAxis = "%", legend= ["L Throt","R Throt","L Prop","R Prop","L Cond","R Cond"])
    #GPS
    toPlot = []
    toPlotX = []
    latMin = (arrayGetter.get("longitude_minuets", Path))
    lonMin = (arrayGetter.get("latitude_minutes",  Path,))
    if(lonMin is not None):
        lon = (arrayGetter.get("longitude_deg",  Path) + lonMin/60)  
    if(latMin is not None):
        lat = (arrayGetter.get("latitude_deg",  Path)+ latMin/60)
        if(lat is not None and lon is not None):
                plt.plot(lon,lat)
    Vlat = (arrayGetter.get("latitude",  Path))
    Vlon = (arrayGetter.get("longitude",  Path))
    if(Vlat is not None and Vlon is not None):
            plt.plot(Vlat,Vlon)
    plot(plt.gcf(),bag,"GPS","LAT","LON",plane,["G5","VN"])
    #Vectornav imu
    a = arrayGetter.get("quaternion_x",  Path, topic = "/vectornav/vn")
    b = arrayGetter.get("quaternion_y",  Path, topic = "/vectornav/vn")
    c = arrayGetter.get("quaternion_z",  Path, topic = "/vectornav/vn")
    d = arrayGetter.get("quaternion_w",  Path, topic = "/vectornav/vn")
    a = pd.to_numeric(a)
    b = pd.to_numeric(b)
    c = pd.to_numeric(c)
    d = pd.to_numeric(d)
    r2d = 180/math.pi
    toPlot = []
    ploter = r2d*np.arctan2((a**a-b**b-c**c+d**d),(2*a**b + 2*c**d))
    plt.plot(ploter)
    ploter = r2d*np.arctan2((a**a+b**b-c**c-d**d),(2*a**d + 2*c**b))+90
    plt.plot(ploter)
    ploter = -r2d*np.arcsin(2*b**d-2*a**c)
    plt.plot(ploter)
    plot(plt.gcf(),bag,"VectorNav Gyros","Acc","Time in Min",plane,["x","Y","Z"])
    #radalt
    listOfThings = ["current_distance","signal_quality"]
    makePlotFromList(listOfThings, [],  Path, bag,plane, "Radalt",opperationsY =  [[3.28084,1,0,0],[]], yAxis = "Ft", legend= ["Distance"] )
    #Tension
    lh_itt_chromel = arrayGetter.get("lh_itt_chromel",Path,  topic = "/labjack/labjack_slow")
    lh_itt_alumel = arrayGetter.get("lh_itt_alumel",Path, topic = "/labjack/labjack_slow")
    rh_itt_chromel = arrayGetter.get("rh_itt_chromel",Path,topic = "/labjack/labjack_slow")
    rh_itt_alumel = arrayGetter.get("rh_itt_alumel",Path, topic = "/labjack/labjack_slow")
    lh_itt_chromel = lh_itt_chromel - lh_itt_alumel
    rh_itt_chromel  = rh_itt_chromel - rh_itt_alumel
    [b,a] = signal.butter(5,0.0125)
    minv= 0.7
    maxv=1
    minout= 510
    maxout=520
    lh_itt_chromel=(lh_itt_chromel-minv)/(maxv-minv)*(maxout-minout)+minout
    minv= 0.7
    maxv=1
    minout= 510
    maxout= 520
    rh_itt_chromel= (rh_itt_chromel)/(maxv-minv)*(maxout-minout)+minout
    toPlot = []
    plt.plot(lh_itt_chromel.index,signal.filtfilt(b,a,lh_itt_chromel,axis =0))
    plt.plot(rh_itt_chromel.index,signal.filtfilt(b,a,rh_itt_chromel,axis =0))
    plot(plt.gcf(),bag,"ITT (0.25Hz)" ,"Degs C","Time in Min",plane,["L ITT C-A","R ITT C-A"])
    #Velociites
    toPlot = []
    listToPlot = ["aileron_pot","elevator_pot", "rudder_pot"]
    for i in listToPlot:
        array = arrayGetter.get(i,Path)
        f=1/(np.mean(np.diff(array))/1000000000)
        array = array*f
        plt.plot(array.index,array.values)
    plot(plt.gcf(),bag,"Control Surfaces Velocities (1 Hz)" ,"Degs/sec","Time in Min",plane,["Aileron","Elevator","Rudder"])
    """
    #Torque
    #TODO(Ethan Weilheimer) use downsample
    lh = 0
    rh =0
    lh = arrayGetter.get("lh_torque_pressure_c",Path)
    
    if(lh is not None):
        lh = obspy.signal.filter.envelope(lh,axis =0)
    
    minv= 3.95
    maxv=3.28
    minout= 100
    maxout= 270
    lh = (lh-minv)/(maxv-minv)*(maxout-minout)+minout
    plt.plot(lh.index,lh.values)
    lh = arrayGetter.get("rh_torque_pressure_c",Path)
    if(lh is not None):
        lh = obspy.signal.filter.envelope(lh,axis =0)
    minv= 3.91
    maxv = 3.06
    minout= 130
    maxout= 300
    lh = (lh-minv)/(maxv-minv)*(maxout-minout)+minout
    plt.plot(lh.index,lh.values)
    plot(plt.gcf(),bag,"Torque (Envelope)" ,"ft-lbs","Time in Min",plane,["L Torque c", "R Torque c"])
    """
    #Spectogram of Torque
    rh = arrayGetter.get4Specgram("rh_torque_pressure_c",Path)
    t = arrayGetter.get4Specgram("timestamp",Path, "/mcc_daq/fast", [1,1e9*60,0,0])
    if( t is not None):
        t =1/np.mean(np.diff((t-t.iloc[0])*60))
    if(rh is not None and t is not None):
        plt.specgram(rh,2048,t,window = np.hanning(2048), noverlap = 128)
        fig = plt.gcf()
        plot(fig,bag,"L Torque Spectogram","Freq (Hz)","Mission time (sec)",plane,[])
    """
    #Fuel Flow
    lh = 0
    rh =0
    a = arrayGetter.get("lh_fuel_flow_d",Path)
    if(a is not None):
        lh = obspy.signal.filter.envelope(a,axis =0)
    a = arrayGetter.get("rh_fuel_flow_d",Path)
    if(a is not None):
        rh = obspy.signal.filter.envelope(a,axis =0)
    minv= .825
    maxv=2.36
    minout= 86
    maxout= 141
    lh= (lh-minv)/(maxv-minv)*(maxout-minout)+minout
    minv= 0.79
    maxv=2.33
    minout= 86
    maxout= 141
    rh= (rh-minv)/(maxv-minv)*(maxout-minout)+minout
    plt.plot(lh.index,lh.values)
    plt.plot(rh.index,rh.values)
    plot(plt.gcf(),bag,"Fuel flow (Envelope)" ,"lb/hr","Time in Min",plane,["L FF d","R FF d"])
    """
    #fuel flow spec
    lh = arrayGetter.get4Specgram("rh_torque_pressure_c",Path)
    t = arrayGetter.get4Specgram("timestamp",Path,"/mcc_daq/fast", [1,1e9*60,0,0])
    if( t is not None):
        t =1/np.mean(np.diff((t-t.iloc[0])*60))
    if(lh is not None and t is not None):
        plt.specgram(lh,2048,t,window = np.hanning(2048), noverlap = 128)
        fig = plt.gcf()
        plot(fig,bag,"L FF D Spectogram","Freq (Hz)","Mission time (sec)",plane,[])
    """
    #oil
    b,a=signal.butter(5,0.025)
    roilp= arrayGetter.get("oil_pressure_right",Path)
    loilp= arrayGetter.get("oil_pressure_left",Path)
    minv= 1.68
    maxv=2.1
    minout= 65
    maxout= 80
    loilp= (loilp-minv)/(maxv-minv)*(maxout-minout)+minout
    minv= 1.68
    maxv=2.1
    minout= 65
    maxout= 80
    roilp= (roilp-minv)/(maxv-minv)*(maxout-minout)+minout
    plt.plot(loilp.index,signal.filtfilt(b,a,loilp,axis =0))
    plt.plot(roilp.index,signal.filtfilt(b,a,roilp,axis =0))
    plot(plt.gcf(),bag,"Oil P (0.5Hz)" ,"PSI","Time in Min",plane,["L oil p","R oil p"])
    """
    #spec of oil
    roilp=signal.filtfilt(b,a,arrayGetter.get4Specgram("oil_pressure_right",Path))
    ld= roilp 
    t = arrayGetter.get4Specgram("timestamp",Path,"/labjack/labjack_slow", [1,1e9*60,0,0])
    if( t is not None):
        t =1/np.mean(np.diff((t-t.iloc[0])*60))
    if(ld is not None and t is not None):
        plt.specgram(ld,2048,t,window = np.hanning(2048), noverlap = 128)
        fig = plt.gcf()
        plot(fig,bag,"R oil p Spectogram","Freq (Hz)","Mission time (sec)",plane,[])
    """
    #turbo tach
    lturb= np.argwhere(arrayGetter.get("lh_turbine_tach_a",Path))
    rturb= np.argwhere(arrayGetter.get("rh_turbine_tach_a",Path))
    minv=  38 
    maxv=53
    minout= 54.5
    maxout= 75
    lturb= (lturb-minv)/(maxv-minv)*(maxout-minout)+minout
    minv= 38
    maxv=53
    minout= 54.5
    maxout= 75
    rturb= (rturb-minv)/(maxv-minv)*(maxout-minout)+minout
    plt.plot(lturb.index,lturb.values)
    plt.plot(rturb.index,rturb.values)
    plot(plt.gcf(),bag,"Turbo Tach" ,"% RPM","Time in Min",plane,["L Turb","R Turb"])
    """
    #turbo tach spec
    ld = arrayGetter.get4Specgram("lh_turbine_tach_a",Path)
    t = arrayGetter.get4Specgram("timestamp",Path,"/mcc_daq/fast", [1,1e9*60,0,0])
    if( t is not None):
        t =1/np.mean(np.diff((t-t.iloc[0])*60))
    if(ld is not None and t is not None):
        plt.specgram(ld,2048,t,window = np.hanning(2048), noverlap = 128)
        fig = plt.gcf()
        plot(fig,bag,"L Turb Spectogram","Freq (Hz)","Mission time (sec)",plane,[])
    #prop tach
    #prop tach spec
#Makes subplot from list (For linked lists)
def makeSubplotFromList(listToPlotY, listToPlotX, Path, bag,plane,title, opperationsX, opperationsY, xAxis = "Time in min", yAxis = "Various",legend =[]):
    toPlot = []
    cols = 1
    rows = len(listToPlotY)
    for div in range (3,0,-1):
        if len(listToPlotY) % div ==0:
            cols = div
            rows /= div
            break
    for ii in range(len(listToPlotY)):
        plt.subplot(rows,cols,ii+1)
        toPlotY = []
        for i in range(len(listToPlotY[ii])):
            rNames = name(listToPlotY[ii][i])
            topic = None
            if(rNames is not None):
                listToPlotY[ii][i] = rNames[1]
                topic = rNames[0]
            y =  arrayGetter.get(listToPlotY[ii][i],  Path,topic,opperationsY[ii][i])
            if (len(listToPlotX[ii]) >0):
                x =  arrayGetter.get(listToPlotX[ii][0],  Path,topic,opperationsX[ii][0])
                #xAxis = listToPlotX[ii]
            else:
                x = None
            if(y is not None):
                if x is not None:
                    plt.plot(y,x)
                else:
                    plt.plot(y.index,y.values)
            #if (legend[ii] is None):
        if(len(legend) -1 <ii):
            legend.append(listToPlotY[ii])
        plt.legend(legend[ii], loc='best')
        plt.xlabel("Time in min")
        plt.title(title[ii])
        plt.ylabel("Various")
    plt.tight_layout()
    titleName = ""
    for i in range(len(title)):
        if i == len(title)-1:
            titleName += title[i]
        else:
            titleName += title[i] +"-&-"
    titleName+=".html"
    fig = plt.gcf()
    save(fig,plane,bag,titleName)
    return titleName
