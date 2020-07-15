#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.


import os
#Gets a list with the first index being a list of planes with number and the second having numbers removed
def getPlanes():
    if(not os.path.isfile('planes.txt')):
        f = open("planes.txt", "w")
        f.close()
    f = open("planes.txt", "r")
    planes = f.read().splitlines()
    f.close()
    for plane in planes:
        cwd = os.getcwd()
        if (not os.path.exists(cwd+"/templates/planes/"+plane)):
            os.mkdir(cwd+"/templates/planes/"+plane)
        if (not os.path.exists(cwd+"/csvs/"+plane)):
            os.mkdir(cwd+"/csvs/"+plane)
        if (not os.path.exists(cwd+"/bags/"+plane)):
            os.mkdir(cwd+"/bags/"+plane)
    return planes
#Adds a plane
def addPlanes(plane):
    planes = getPlanes()
    if(plane not in planes):
        f = open("planes.txt", "w")
        planes = getPlanes()
        for ii in planes:
            f.write("%s\n" % ii)
        f.write("%s\n" % plane)
        f.close()

