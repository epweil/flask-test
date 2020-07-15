#!/usr/bin/env python

# Copyright 2020 Apollo Flight Research Inc. DBA Merlin Labs.
# All rights reserved.

import logging
import flatdict
import numpy as np
import pandas as pd
import rosbag
from rospy_message_converter.message_converter import convert_ros_message_to_dictionary
from datetime import datetime

class RosbagPandaException(Exception):
    pass
def topics_from_keys(keys):
    """
    Extracts the desired topics from specified keys
    :param Keys: List of desired keys
    :return: List of topics
    """
    topics = set()
    for key in keys:
        if not key.startswith("/"):
            key = "/" + key
        chunks = key.split("/")
        for i in range(2, len(chunks)):
            topics.add("/".join(chunks[0:i]))
    return list(topics)
bag = None
canPlot = []
def startBag(Path, bag_name):
    global bag
    global canPlot
    bag = rosbag.Bag(bag_name)
    topics = bag.get_type_and_topic_info()[1].keys()
    for topic in topics:
        topicNoSlash = topic.replace("/","_")
        Path2  = Path + topicNoSlash + ".csv"
        bag_to_CSV(Path2, topic)
    canPlot = pd.DataFrame(data = canPlot)
    canPlot.to_csv(Path + "canPlot.csv")
    bag.close()
def bag_to_CSV(Path2, include=None):
    first = True
    type_topic_info = bag.get_type_and_topic_info()
    topics = [include]
    index = []
    df_length = sum([type_topic_info.topics[t].message_count for t in topics])
    data_dict = {}
    for idx, (topic, msg, t) in enumerate(bag.read_messages(topics=topics)):
        if (first):
            startTime = t.to_sec()* 0.0166667
            first = False
        flattened_dict = _get_flattened_dictionary_from_ros_msg(msg)
        for key, item in flattened_dict.iteritems():
            data_key = topic + "/" + key
            if data_key not in data_dict:
                if isinstance(item, float) or isinstance(item, int):
                    data_dict[data_key] = np.empty(df_length)
                    data_dict[data_key].fill(np.NAN)
                else:
                    data_dict[data_key] = np.empty(df_length, dtype=np.object)
            data_dict[data_key][idx] = item
        index.append((t.to_sec()* 0.0166667)-startTime)
    # now we have read all of the messages its time to assemble the dataframe
    df = pd.DataFrame(data=data_dict, index=index)
    canPlot.extend(df.columns.tolist())
    df.to_csv(Path2)
def _get_flattened_dictionary_from_ros_msg(msg):

    return flatdict.FlatterDict(convert_ros_message_to_dictionary(msg), delimiter="/")



