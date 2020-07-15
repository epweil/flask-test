#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.

import plotter
import planes
import os
import datetime
import rosbag_pandas2
import sys
#Indexes the bag and has csv files and base plots created
def newBag(bag,plane):
    planes.addPlanes(plane)
    cwd = os.getcwd()
    bagFilePath = cwd + "/bags/" +plane +"/" + bag 
    csvFilePath =  cwd + "/csvs/" + plane +"/"+bag[:len(bag)-4] +"/"
    if not os.path.exists(csvFilePath):
        os.makedirs(csvFilePath)
    rosbag_pandas2.startBag(csvFilePath,bagFilePath)
    plotter.makeBasePlots(csvFilePath,bag,plane)
if __name__ == "__main__":
    newBag(sys.argv[1], sys.argv[2])
