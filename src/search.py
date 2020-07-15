#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.

import rosbag
import os
import csv
import pandas as pd
#Finds which topic the value key is in.
def find(looking,bag2,setTopic = None):
    if(".bag" not in bag2):
        bag2+=".bag"
    bag = rosbag.Bag(bag2)
    topics2 = bag.get_type_and_topic_info()[1].keys()

    for i in topics2:
        for topic, msg, t in bag.read_messages(i):
            message = msg
            messages = message.__slots__
            a = findSlots(messages,looking,message)
            if a == True :
                return i
            break
    return None
        
#Recursively searches the messages's submessages to check for the value key
def findSlots(find,looking,message):
    path = []
    for ii in find:
        path = []
        path.append(ii)
        if(ii == looking):
            return True
        try:
            message2 =getattr(message,ii)
            message3 = message2.__slots__
            a = findSlots(message3,looking,message2)
            if a: 
                return True
        except:
            pass

def findFromCsv(looking, Path,topic):
    possibleTopics =  os.listdir(Path)
    possibleChoices  = pd.read_csv(Path+"canPlot.csv", index_col = 0).iloc[:, 0].values
    for choice in possibleChoices:
        if(looking in choice):
            for topic in possibleTopics:
                if (topic.replace(".csv", "") in choice.replace("/","_")):
                    return [topic,choice]
    return None
