# -*- coding: utf-8 -*-
"""
Created Aug 2018

@author: rxr
Email rendelr97@gmail.com for support
(I dont bite I swear)
"""

# In[2]:
import pandas as pd
from tkinter import *
import tkinter as tk
from pymsgbox import *
#Specify where to read CSV with all intersections from.
OD_list = pd.read_csv('R:/Modeling and Simulation (M&S - Vissim)/Google Maps Distance Matrix API/Intersection Shortened.csv')
OD_list['INTERSEC5'] = OD_list['INTERSEC5'].str.lower()

global coord_1_list
global coord_2_list
global id_1_list
global id_2_list
global inter_1_list
global inter_2_list
#Initialize lists
id_1_list = []
id_2_list = []

inter_1_list =[]
inter_2_list =[]

origin_list = []
destination_list = []

def savestreet():
    global street_name
    street_name = ent.get()
    Street.destroy()
    
def saveinter():
    global inter_1
    global inter_2
    #Find coordinates from CSV for relevant intersections
    inter_1 = int_1_list.get(ACTIVE)
    inter_2 = int_2_list.get(ACTIVE)
    coord_1 = float(streetlist.loc[streetlist['INTERSEC5']==inter_1, 'LATITUDE'].iloc[0]), float(streetlist.loc[streetlist['INTERSEC5']==inter_1, 'LONGITUDE'].iloc[0])
    coord_2 = float(streetlist.loc[streetlist['INTERSEC5']==inter_2, 'LATITUDE'].iloc[0]), float(streetlist.loc[streetlist['INTERSEC5']==inter_2, 'LONGITUDE'].iloc[0])
    id_1 = float(streetlist.loc[streetlist['INTERSEC5']==inter_1, 'OBJECTID_1'].iloc[0])
    id_2 = float(streetlist.loc[streetlist['INTERSEC5']==inter_2, 'OBJECTID_1'].iloc[0])
    #Appends id, intersection, and coordinates to relevant lists.
    id_1_list.append(id_1)
    id_2_list.append(id_2)
    inter_1_list.append(inter_1)
    inter_2_list.append(inter_2)
    origin_list.append(coord_1)
    destination_list.append(coord_2)
    #Checks if the two way option was selected.
    #If it was, then it takes the same results as before but flips the order
    if two_way_check.get() == 1:
        coord_2 = float(streetlist.loc[streetlist['INTERSEC5']==inter_1, 'LATITUDE'].iloc[0]), float(streetlist.loc[streetlist['INTERSEC5']==inter_1, 'LONGITUDE'].iloc[0])
        coord_1 = float(streetlist.loc[streetlist['INTERSEC5']==inter_2, 'LATITUDE'].iloc[0]), float(streetlist.loc[streetlist['INTERSEC5']==inter_2, 'LONGITUDE'].iloc[0])
        id_2 = float(streetlist.loc[streetlist['INTERSEC5']==inter_1, 'OBJECTID_1'].iloc[0])
        id_1 = float(streetlist.loc[streetlist['INTERSEC5']==inter_2, 'OBJECTID_1'].iloc[0])
        
        id_1_list.append(id_1)
        id_2_list.append(id_2)
        origin_list.append(coord_1)
        destination_list.append(coord_2)
        inter_1_list.append(inter_2)
        inter_2_list.append(inter_1)
    alert(title="Update", text="Appended!", button='OK')
    print(inter_1_list, inter_2_list)
""" Checks if request was of appropriate length and variable type.""" 
def request_length():
    global r_length
    r_length = ent.get()
    #If the length inputted was not a number, it throws the user an error
    if r_length.isdigit():    
        r_length = int(r_length)
        request_option.destroy()
    else:
        alert(title="Not Valid", text="Enter a valid number", button="OK")
    
try:
        
    streetlist = ""
    while len(streetlist)==0:
        Street = Tk()
        Street.geometry("500x100")
        street_name = StringVar()
        #Creates frames within the overall menu for formatting. Asks for user's input for relevant corridor.
        row = Frame(Street)
        lab = Label(row, width=30, text="Enter Corridor Name", anchor='w', font=("Helvetica", 10))
        ent = Entry(row, textvariable=street_name)
        ent.focus_set()
        
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        
        
        b1 = Button(Street, text='Submit', command=savestreet)
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(Street, text='Quit', command=Street.destroy)
        b2.pack(side=LEFT, padx=5, pady=5)
        
        Street.mainloop()
        streetlist = OD_list[OD_list['INTERSEC5'].str.contains(street_name.lower())]
        #If the street input does not exist the dataframe will have a length of 0 and return an error.
        if len(streetlist)==0:
            alert(title="Notice", text="Query returned 0 results", button="Try Again")
    
    
    #Once an appropriate street has been given it produces two lists of available intersections.
    int_1 = streetlist['INTERSEC5'].tolist()
    int_2 = streetlist['INTERSEC5'].tolist()
    
    intersections = Tk()
    intersections.geometry("800x500")
    row = Frame(intersections)
    two_way_check = IntVar()
    
    int_1_select = StringVar()
    int_2_select = StringVar()
    
    lab1 = Label(row, width=20, text="Intersection 1", anchor='w', font=("Helvetica", 10))
    
    scrollbar1 = Scrollbar(row, orient=VERTICAL)
    int_1_list = Listbox(row, yscrollcommand=scrollbar1.set)
    scrollbar1.config(command=int_1_list.yview)
    
    for item in int_1:
        int_1_list.insert(END, item)
    row.pack(side=TOP, fill=X)
    lab1.pack(side=LEFT)
    scrollbar1.pack(side=RIGHT, fill = Y)
    int_1_list.pack(side= RIGHT, fill=X, expand=YES)
    
    row = Frame(intersections)
    lab2 = Label(row, width=20, text="Intersection 2", anchor='w', font=("Helvetica", 10))
    
    scrollbar2 = Scrollbar(row, orient=VERTICAL)
    int_2_list = Listbox(row, yscrollcommand=scrollbar2.set)
    scrollbar2.config(command=int_2_list.yview)
    
    
    for item in int_2:
        int_2_list.insert(END, item)
    row.pack(side=TOP, fill=X)
    lab2.pack(side=LEFT)
    scrollbar2.pack(side=RIGHT, fill=Y)
    int_2_list.pack(side= RIGHT, fill=X, expand=YES)
    
    row.pack(side=TOP, fill=X)
    #Provides an option for people to request data in both directions.
    row = Frame(intersections)
    two_way_button = Checkbutton(row, text="Two Way", variable = two_way_check)
    row.pack(side=TOP, fill=X)
    two_way_button.pack(side=RIGHT)
    
    row.pack(side=TOP, fill=X)
    
    b1 = Button(intersections, text='Append', command=saveinter)
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(intersections, text='Finish', command=intersections.destroy)
    b2.pack(side=LEFT, padx=5, pady=5)
    intersections.mainloop()

except AttributeError:
    pass
#    
if len(origin_list)>0:
    while True:
        #Creates menu for user to enter the length of their study.
        request_option = Tk()
        row = Frame(request_option)
        r_length = IntVar()
        lab = Label(row, width=30, text="Enter Study Duration", anchor='w', font=("Helvetica", 10))
        ent = Entry(row, textvariable=r_length)
        
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=NO, fill=X)
        
        
        b1 = Button(request_option, text='Submit', command=request_length)
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(request_option, text='Quit', command=request_option.destroy)
        b2.pack(side=LEFT, padx=5, pady=5)
        request_option.mainloop()
        if isinstance(r_length, int) == True:
            break


print(origin_list)
# In[1]:


def GDistMat(reqtime, origins, destinations, RName, timestamp):
    #Google Maps Travel Time Output Tool
    #No User Inputs Required

    import os
    import googlemaps
    import datetime
    import calendar
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
#            travel_list['node1'] = BestGuess['origin_addresses'][0]
#            travel_list['node2'] = BestGuess['destination_addresses'][0]
            travel_list['time'] = i['elements'][0]['duration_in_traffic']['value']
            travel_list['distance'] = i['elements'][0]['distance']['value']
        
            
    except:
        BestTime = "Er"
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
    conn = psycopg2.connect(host="10.1.2.165",database="TravelTime", user="postgres", password="postgres")
    year = datetime.datetime.today()
    year = year.year
    try:
        cur = conn.cursor()
        # After connecting to the SQL database this creates a table based on the year if it does not yet exist
        #Creates columns Intersection 1, 2, node 1,2, Month, date, day, travel time, distance and request time.
        sql = "CREATE TABLE IF NOT EXISTS Intersection_Selection_" + str(year) + "(ID_1 REAL, ID_2 REAL, Int1 VARCHAR(70), Int2 VARCHAR(70), Month VARCHAR(50), Day VARCHAR(50), Date VARCHAR(50), Travel_Time REAL, Distance REAL, RTime TIME)"
        cur.execute(sql)
        # execute the Create statement

        # commit the changes to the database. Without this line nothing created will stay in the database.
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
#Closes the connection to the database. Make sure to close this so the database won't get slowed down with extra connections.
            conn.close()


# In[4]:


def apicall(origin_list, destination_list, inter_1_list, inter_2_list, id_1_list, id_2_list):
    #Calls google API, requests data for the list of OD pairs and prints that data into the table created in SQL. 
    global travel_list
    global rowCounter
    import psycopg2
    import time
    import datetime
    import schedule
    
    #Define when you want the script to stop by time or by request limit. Time is in 24:00 format.
    
    limit = 10000
    
    delay_time = 0
    
    RName = 'TestRoute'
    conn = psycopg2.connect(host="10.1.2.165",database="TravelTime", user="postgres", password="postgres")
    timer = datetime.datetime.today()
    dateref = timer.date()
    
    #Pull date format from current day to input into SQL
    day = dateref.strftime("%A")
    date = dateref.strftime("%d")
    month = dateref.strftime("%B")

    
    counter = 0
    rounds = 1
    timer = datetime.datetime.today()
    timer = timer.hour
    hour_stop = timer
    
    requests = 0
    
    while counter < rounds and requests <= limit:
        tic = time.clock()
        for i in range(rowCounter, len(origin_list)):
            if requests <=limit:
                #Defines which OD pair to pull from the long list
                origins = origin_list[rowCounter]
                destinations = destination_list[rowCounter]

                reqtime= "now"
                timestamp = time.strftime("%H:%M:%S")
                travel_info = GDistMat(reqtime, origins, destinations, RName, timestamp)
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
                sql = "INSERT INTO Intersection_Selection_" + str(year) + "(ID_1, ID_2, Int1, Int2, Month, Day, Date, Travel_Time, Distance, RTime)                        VALUES(%(id1)s, %(id2)s, %(int1)s, %(int2)s, %(month)s, %(day)s, %(date)s, %(time)s, %(distance)s, %(rtime)s)"
                cur.execute(sql,travel_info)
                # commit the changes to the database
                conn.commit()
                if rowCounter < len(origin_list):
                    rowCounter += 1
            else:
                break
            counter += 1
        if rowCounter == len(origin_list):
            rowCounter = 0
        toc = time.clock()
        delay = toc-tic
        sleepTime = delay_time - delay

        #Put the program to sleep for an interval. This will delay for your delay_time and subtract how long the program ran for.
        if sleepTime > 0 and requests < limit:
            time.sleep(sleepTime)
        #Return new hour to check if it's past the stop hour.
        timer = datetime.datetime.today()
        timer = timer.hour
    conn.close
    
    #print(rowCounter)
    #return rowCounter


# In[8]:

try:
    create_table()
    global rowCounter
    import schedule
    import datetime
    import time
    rowCounter = 0
    schedule.every(2).minutes.do(apicall, origin_list, destination_list, inter_1_list, inter_2_list, id_1_list, id_2_list).tag('api')
    dayCounter = 0
    day_index = datetime.datetime.today()
    day_check = day_index.day
    
    while dayCounter < r_length:
        schedule.run_pending()
        time.sleep(1)
        day_test = datetime.datetime.today()
        day_check = day_test.day
        if day_check != day_index.day:
            dayCounter +=1
            day_index = datetime.datetime.today()
    schedule.clear('api')
    alert(title="Note!", text="Done!", button="OK")
except (NameError):
    alert(title='Error', text='Request not made', button='OK')
