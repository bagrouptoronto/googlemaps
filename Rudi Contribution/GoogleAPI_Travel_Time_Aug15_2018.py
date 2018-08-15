
# coding: utf-8

# In[1]:


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


# In[2]:


#Connects to SQL Server with dbsettings credentials
def create_table():
    import sys
    import psycopg2
    import time
    import datetime
    import calendar
    conn = psycopg2.connect(host="localhost",database="TravelTime", user="postgres", password="postgres")
    year = datetime.datetime.today()
    year = year.year
    try:
        cur = conn.cursor()
        # After connecting to the SQL database this creates a table based on the year if it does not yet exist
        #Creates columns Intersection 1, 2, node 1,2, Month, date, day, travel time, distance and request time.
        sql = "CREATE TABLE IF NOT EXISTS Bloor_dundas_" + str(year) + "(ID REAL, Route_Number VARCHAR(80), Segment_Name VARCHAR(100), Route_Description VARCHAR(100), Int1 VARCHAR(70), Int2 VARCHAR(70), Node1 VARCHAR(150),Node2 VARCHAR(150), Month VARCHAR(50), Day VARCHAR(50), Date VARCHAR(50), Travel_Time REAL, Distance REAL, RTime TIME)"
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


# In[3]:


def csv_read():
    
    global travel_list
    import sys
    import time
    import csv
    import datetime
    import schedule
    
    
    #--------------------------------------------------------------------------------
    
    #Reads CSV with list of origins and destinations
    file = "C:/Users/rxr/Documents/Travel Times/Bloor and Dundas ODs.csv"
    
    with open(file, "r") as csvfile:
        
        csvreader = csv.reader(csvfile)
        # If your csv has a header keep this as true, otherwise set to false
        is_header = True
        #Goes through each CSV row and pulls a set of origins and destinations
        origin_list = []
        destination_list = []
        description_list = []
        nodeid_list = []
        linktype_list = []
        street_list = []
        inter1_list = []
        inter2_list = []
        for row in csvreader:
            if is_header:
                is_header = False
                continue
            else:
            #define origin and destination coordinates and description from the CSV file.
                origins = float(row[2].split(", ")[0]), float(row[2].split(", ")[1])
                destinations = float(row[3].split(", ")[0]), float(row[3].split(", ")[1])
                description = "NA"
                nodeid = row[0]
                linktype = "NA"
                street_name = row[1]
                inter1 = row[4]
                inter2 = row[5]
                origin_list.append(origins)
                destination_list.append(destinations)
                description_list.append(description)
                nodeid_list.append(nodeid)
                linktype_list.append(linktype)
                street_list.append(street_name)
                inter1_list.append(inter1)
                inter2_list.append(inter2)
    
#Returns lists of origins, destinations, and descriptions.
    return origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list


# In[4]:


def apicall(origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list):
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
    
    delay_time = 300
    
    conn = psycopg2.connect(host="localhost",database="TravelTime", user="postgres", password="postgres")
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

                travel_info['description'] = description_list[rowCounter]
                travel_info['day'] = day
                travel_info['date'] = date
                travel_info['month'] = month
                travel_info['id'] = nodeid_list[rowCounter]
                travel_info['linktype'] = linktype_list[rowCounter]
                travel_info['streetname'] = street_list[rowCounter]
                travel_info['inter1'] = inter1_list[rowCounter]
                travel_info['inter2'] = inter2_list[rowCounter]

                year = datetime.datetime.today()
                year = year.year

                cur = conn.cursor()
                    # execute the INSERT statement
                sql = "INSERT INTO Bloor_dundas_" + str(year) + "(ID, Route_Number, Segment_Name, Route_Description, Int1, Int2, Node1, Node2, Month, Day, Date, Travel_Time, Distance, RTime)                        VALUES(%(id)s, %(linktype)s, %(streetname)s, %(description)s, %(inter1)s, %(inter2)s, %(node1)s, %(node2)s,%(month)s, %(day)s, %(date)s, %(time)s, %(distance)s,%(rtime)s)"
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


create_table()
origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list = csv_read()
global rowCounter
global travel_list
import schedule
import datetime
import time
rowCounter = 0

#hour_stop = 17

#Schedule the code to run at a particular time for a particular day.
schedule.every().saturday.at("11:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 
schedule.every().sunday.at("11:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 

schedule.every().monday.at("16:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 
schedule.every().tuesday.at("16:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 
schedule.every().wednesday.at("16:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 
schedule.every().thursday.at("16:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 
schedule.every().friday.at("16:00").do(apicall, origin_list, destination_list, description_list, nodeid_list, linktype_list, street_list, inter1_list, inter2_list).tag('api') 



timer = datetime.datetime.today()
timer = timer.day

while timer < 35:
    schedule.run_pending()
    time.sleep(5)
    timer = datetime.datetime.today()
    timer = timer.day
    
schedule.clear('api')
cur.close()

#houston("reschedule")

print("Done")

