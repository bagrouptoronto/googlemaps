
# coding: utf-8

# In[ ]:


def GDistMat(reqtime, origins, destinations, timestamp):
    #Google Maps Travel Time Output Tool
    #No User Inputs Required

    import os
    import googlemaps
    import datetime
    import calendar
    import numpy
    import pprint
    import time
    maps_key = "PLACEHOLDER"
    gmaps = googlemaps.Client(key=maps_key)

    deptime = reqtime
    
    #Pull information from the Google distance API. This currently pulls based on their "best guess algorithm"
    try:
        #Best Guess
        BestGuess = gmaps.distance_matrix(
            (origins),
            (destinations),
            departure_time = deptime,
            mode = 'driving',
            traffic_model = 'best_guess',
            )
        
        # BestGuess is a json of all the data pulled by the API
        #   Indexes json from google api to rows.
        data = BestGuess['rows']
        #Iterates through each "elements" dictionary in "data" 
        travel_list = {}
        travel_list['rtime'] = time.strftime("%H:%M:%S")
        for i in data:
            #Populates a dictionary called "Travel_list " 
            travel_list['node1'] = BestGuess['origin_addresses'][0]
            travel_list['node2'] = BestGuess['destination_addresses'][0]
            travel_list['time'] = i['elements'][0]['duration_in_traffic']['value']
            travel_list['distance'] = i['elements'][0]['distance']['value']
        
            
    except:
        print("error")
                
    #Returns the Travel_list dictionary to be used in function.
    return travel_list


# In[ ]:


#Connects to SQL Server with dbsettings credentials
def create_table():
    import sys
    import psycopg2
    import time
    import datetime
    import calendar
    conn = psycopg2.connect(host="10.1.2.165",database="BA_DATA", user="user", password="password")

    year = datetime.datetime.today()
    year = year.year
    try:
        cur = conn.cursor()
        # After connecting to the SQL database this creates a table based on the year if it does not yet exist
        #Creates columns Intersection 1, 2, node 1,2, Month, date, day, travel time, distance and request time.
        sql = "CREATE TABLE IF NOT EXISTS private_veh_traveltime (ID_1 REAL, ID_2 REAL, Int1 VARCHAR(70), Int2 VARCHAR(70), Month VARCHAR(50), Day VARCHAR(50), Date VARCHAR(50), Travel_Time REAL, Distance REAL, RTime TIME)"
        cur.execute(sql)
        # execute the Create statement
        
        # commit the changes to the database. Without this line nothing created will stay in the database.
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("error")
        #houston("error")
    finally:
        if conn is not None:
#Closes the connection to the database. Make sure to close this so the database won't get slowed down with extra connections.
            conn.close()


# In[ ]:


def csv_read(filename):
    
    global travel_list
    import sys
    import time
    import csv
    import datetime
    import schedule
    import pandas as pd
    
    #--------------------------------------------------------------------------------
    
    #Reads CSV with list of origins and destinations
    try:
        OD_list = pd.read_csv(filename)
        OD_list['int1'] = OD_list['int1'].str.lower()
        OD_list['int2'] = OD_list['int2'].str.lower()

        origin_list = []
        destination_list = []
        inter_1_list = []
        inter_2_list = []
        id_1_list = []
        id_2_list = []
        inter_1_list = OD_list['int1'].tolist()
        inter_2_list = OD_list['int2'].tolist()
        origin_list = OD_list['origin'].tolist()
        destination_list = OD_list['destination'].tolist()
        id_1_list = OD_list['OBJECTID_1'].tolist()
        id_2_list = OD_list['OBJECTID_2'].tolist()
    except ():
        print('Appropriate CSV not chosen')
#Returns lists of origins, destinations, and descriptions.
    return origin_list, destination_list, inter_1_list, inter_2_list, id_1_list, id_2_list


# In[ ]:


def apicall(origin_list, destination_list, inter_1_list, inter_2_list, id_1_list, id_2_list):
    #Calls google API caller, requests data for the list of OD pairs and prints that data into the table created in SQL. 
    global travel_list
    global rowCounter
    import psycopg2
    import time
    import csv
    import pprint
    import datetime
    import schedule
    
    #Define when you want the script to stop by time or by request limit. Time is in 24:00 format.
    #houston("initialize")
    
    limit = 50000
    
    delay_time = 0
    
    conn = psycopg2.connect(host="10.1.2.165",database="BA_DATA", user="user", password="password")

    timer = datetime.datetime.today()
    dateref = timer.date()
    
    #Pull date format from current day to input into SQL
    day = dateref.strftime("%A")
    date = dateref.strftime("%d")
    month = dateref.strftime("%B")

    
    #counter = 0
    #rounds = 1
    timer = datetime.datetime.today()
    timerh = timer.hour
    timerm = timer.minute
    timer = timerh*60 + timerm
    hour_stop = timerh*60 + timerm + 120

    requests = 0
        
    while timer <= hour_stop and requests <= limit:
        tic = time.clock()
        for i in range(rowCounter, len(origin_list)):
            if requests <=limit and timer <=hour_stop:
                #Defines which OD pair to pull from the long list
                origins = origin_list[rowCounter]
                destinations = destination_list[rowCounter]

                reqtime= "now"
                timestamp = time.strftime("%H:%M:%S")
                travel_info = GDistMat(reqtime, origins, destinations, timestamp)
                #Increase requests number by 1 for each request made. Stops the code if the requests gets above the limit.
                requests += 1

                travel_info['day'] = day
                travel_info['date'] = date
                travel_info['month'] = month
                travel_info['id1'] = id_1_list[rowCounter]
                travel_info['id2'] = id_2_list[rowCounter]
                travel_info['int1'] = inter_1_list[rowCounter]
                travel_info['int2'] = inter_2_list[rowCounter]

                year = datetime.datetime.today()
                year = year.year

                cur = conn.cursor()
                    # execute the INSERT statement
                sql = "INSERT INTO private_veh_traveltime (ID_1, ID_2, Int1, Int2, Month, Day, Date, Travel_Time, Distance, RTime)  VALUES(%(id1)s, %(id2)s, %(int1)s, %(int2)s, %(month)s, %(day)s, %(date)s, %(time)s, %(distance)s, %(rtime)s)"

                cur.execute(sql,travel_info)
                # commit the changes to the database
                conn.commit()
                timer = datetime.datetime.today()
                timerh = timer.hour
                timerm = timer.minute
                timer = timerh*60 + timerm
                if rowCounter < len(origin_list):
                    rowCounter += 1
            else:
                break
        if rowCounter == len(origin_list):
            rowCounter = 0
        toc = time.clock()
        delay = toc-tic
        sleepTime = delay_time - delay

        #Put the program to sleep for an interval. This will delay for your delay_time and subtract how long the program ran for.
        if sleepTime > 0 and requests < limit:
            time.sleep(sleepTime)
        #Return new hour to check if it's past the stop hour.
        
    conn.close
    #houston("success")
    
    #print(rowCounter)
    #return rowCounter


# In[ ]:

from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)
create_table()
origin_list, destination_list, inter_1_list, inter_2_list, id_1_list, id_2_list = csv_read(filename)
global rowCounter
import schedule
import datetime
import time
rowCounter = 0
schedule.every(2).minutes.do(apicall, origin_list, destination_list, inter_1_list, inter_2_list, id_1_list, id_2_list).tag('api')
dayCounter = 0

"""Checks to see if the current day is the same as the current day, otherwise it adds one to the counter.
    Keeps count of how many days the script has been running"""
while dayCounter < 1:
    schedule.run_pending()
    time.sleep(1)
schedule.clear('api')
print("Finish")

