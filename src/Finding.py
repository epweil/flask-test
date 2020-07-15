import rosbag
import csv
def find(bag2):
    bag = rosbag.Bag(bag2)
    topics2 = bag.get_type_and_topic_info()[1].keys()
    path = []
    for i in topics2:
        path = []
        path.append(i)
        for topic, msg, t in bag.read_messages(i):
            message = msg
        print(i)
        messages = message.__slots__
        a = findSlots(messages,message,1)
def findSlots(find,message,indent):
    for ii in find:
        for iii in range(indent):
            print("      "),
        print(ii)
        try:
            message2 =getattr(message,ii)
            message3 = message2.__slots__
            a = findSlots(message3,message2,indent +1)
        except:
            pass

def csvFile(filePath):
    with open(filePath, "rb") as f:
            reader = csv.reader(f)
            i = reader.next()
            rest = [row for row in reader]
            print(i)
