#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.

import pandas as pd
import numpy as np
import math
import search
#Get numpy array from csv files 
def get(X,Path,topic = None, opperations = [1,1,0,0] ):
    if opperations == []:
        opperations = [1,1,0,0]
    topics = search.findFromCsv(X,Path,topic)
    if(topics is None):
        return None
    topic = topics[0]
    topic.replace("/","_")
    look = topics[1]
    if(topic[0:1] != "_"):
        topic = "_"+topic
    try:
        df = pd.read_csv(Path+topics[0], index_col=0)
        a = getattr(df,look)
    except: 
        return None
    if (opperations[0] != 1):
        a  =  a * float(opperations[0]) 
    if (opperations[1] != 1):
        a =  a / float(opperations[1])
    if (opperations[2] != 0):
        a = a + float(opperations[2])
    if (opperations[3] != 0):
        a = a- float(opperations[3])
    return pd.DataFrame(data=a, index=df.index)
def get4Specgram(X,Path,topic = None, opperations = [1,1,0,0] ):
    if opperations == []:
        opperations = [1,1,0,0]
    topics = search.findFromCsv(X,Path,topic)
    if(topics is None):
        return None
    topic = topics[0]
    topic.replace("/","_")
    look = topics[1]
    if(topic[0:1] != "_"):
        topic = "_"+topic
    try:
        df = pd.read_csv(Path+topics[0], index_col=0)
        a = getattr(df,look)
    except: 
        return None
    if (opperations[0] != 1):
        a  =  a * float(opperations[0]) 
    if (opperations[1] != 1):
        a =  a / float(opperations[1])
    if (opperations[2] != 0):
        a = a + float(opperations[2])
    if (opperations[3] != 0):
        a = a- float(opperations[3])
    return a
    
    
    


    
   


