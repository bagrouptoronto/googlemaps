# -*- coding: utf-8 -*-
"""
Created Aug 2018

@author: rxr
Email rendelr97@gmail.com for support
(I dont bite I swear)

"""

# In[1]:
import pandas as pd
from tkinter import *
import tkinter as tk
from pymsgbox import *
import psycopg2

global street_list
global int_1
global int_2
global dataframe
global table_name
global int_select_1
global int_select_2
global reset_fcn
reset_fcn = False
int_select_1 = False
int_select_2 = False
street_list = []
int_1 = []
int_2 = []

# In[2]:
# Specify connection to SQL server. Change parameters as needed if Server gets moved to another computer.
conn = psycopg2.connect(host="10.1.2.165",database="TravelTime", user="postgres", password="postgres")

"""UNCOMMENT THIS SO YOU CAN SELECT FROM AN OPTION OF TABLES

#Provides a list of all table options in a database. 
#SQL = "select relname as table from  pg_stat_user_tables where schemaname = 'public'"
#table_list = pd.read_sql_query(SQL, conn)
#
##Converts dataframe column to a python list
#table_list = table_list['table'].tolist()    
"""

# In[3]: 
#Create Checkbar class to create the object in a menu later
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
    def state(self):
        return [var.get() for var in self.vars]  

""" These functions select distinct intersection names from the database and update the lists to include only relevant options"""

def int_selection_1(x, y, z):
    global intersection_1, table_name, int_2, int_select_1, int_select_2, reset_fcn
    if reset_fcn is False:
        intersection_1 = int_1_select.get()
        if int_select_2 is False and int_select_1 is False:
            #Creates a query that only selects the second intersections where the selected intersection exists.
            SQL = "Select distinct(Int2) from " + table_name + " where Int1 ILIKE '" + intersection_1 + "'"
            dataframe = pd.read_sql_query(SQL, conn)
            #Deletes current list of 2nd intersections and replaces it with relevant options.
            int_2_list.children["menu"].delete(0,"end")
            int_2 = dataframe['int2'].tolist()
            for i in int_2:
                int_2_list.children["menu"].add_command(label=i, command=lambda intersection=i: int_2_select.set(i))
            int_2_select.set(int_2[0])
            int_select_1 = True

def int_selection_2(x, y, z):
    global intersection_2, table_name, int_1, int_select_1, int_select_2, reset_fcn
    if reset_fcn is False:
        intersection_2 = int_2_select.get()
        if int_select_1 is False and int_select_2 is False:
            #Creates a query that only selects the first intersections where the selected intersection exists.
            SQL = "Select distinct(Int1) from " + table_name + " where Int2 ILIKE '" + intersection_2 + "'"
            dataframe = pd.read_sql_query(SQL, conn)
            #Deletes current list of 2nd intersections and replaces it with relevant options.
            int_1_list.children["menu"].delete(0,"end")
            int_1 = dataframe['int1'].tolist()
            for i in int_1:
                int_1_list.children["menu"].add_command(label=i, command=lambda intersection=i: int_1_select.set(i))
            int_1_select.set(int_1[0])
            int_select_2 = True
        
""" Creates Intersection 1 and 2 lists based on selected table, this contains all intersections in the database"""
def SelectTable():
    global int_1, int_2, table_name
    table_name = "intersection_selection_2018"
    SQL = "Select distinct(Int1) from " + table_name
    dataframe = pd.read_sql_query(SQL, conn)
    int_1 = dataframe['int1'].tolist()
    SQL = "Select distinct(Int2) from " + table_name
    dataframe = pd.read_sql_query(SQL, conn)
    int_2 = dataframe['int2'].tolist()
    SQL_Query.destroy()
    
""" Gets around limitation of the optionmenus. Once options are selected the lists won't go to their defaults
    unless this function is run"""
def ResetFunctions():
    global int_select_1, int_select_2, table_name, reset_fcn
    int_select_1 = False
    int_select_2 = False
    reset_fcn = True
    if int_select_2 is False and int_select_1 is False:
        SQL = "Select distinct(Int1) from " + table_name
        dataframe = pd.read_sql_query(SQL, conn)
       #Repopulates lists with original data from database.
        int_1_list.children["menu"].delete(0,"end")
        int_1 = dataframe['int1'].tolist()
        for i in int_1:
            int_1_list.children["menu"].add_command(label=i, command=lambda intersection=i: int_1_select.set(intersection))
            
        SQL = "Select distinct(Int2) from " + table_name
        dataframe = pd.read_sql_query(SQL, conn)
           
        int_2_list.children["menu"].delete(0,"end")
        int_2 = dataframe['int2'].tolist()
        for j in int_2:
            int_2_list.children["menu"].add_command(label=j, command=lambda intersection=j: int_2_select.set(intersection))

    int_1_select.set(int_1[0])
    int_2_select.set(int_2[0])
    reset_fcn = False
    alert(title='Reset', text='Reset', button='Ok')
    
""" Creates final Query that will be fed into SQL to produce results""" 

def FinishQuery():
    global table_name
    intersection_input_1 = int_1_select.get()
    intersection_input_2 = int_2_select.get()
    
    intersection_query = " WHERE Int1 ILIKE '" + intersection_input_1 + "' AND Int2 ILIKE '" + intersection_input_2 + "' "
    
    """ UNCOMMENT WHEN READY FOR MONTHS"""
    #Gets list of booleans of month checkboxes and compares it to a list of months.
#    selected_months = list(month_list.state())
#    months = ["'All'", "'January'", "'February'", "'March'", "'April'", "'May'", "'June'", "'July'", "'August'", "'September'", "'October'", "'November'", "'December'"]
#    month_input_list = []
#    j = 0
#    #Option 1 of the checkboxes is the "All" option, so if that option is true the query becomes "select all months"
#    if selected_months[j] == 1:
#        month_query = "AND month LIKE '%' "
#    else:
#        for i in selected_months:
#            if i == 1:
#                #Where the list contains a 1, it adds that month to the list for the query.
#                month_input_list.append(months[j])
#            j += 1
#                
#        month_query = "AND month IN (" + ', '.join(month_input_list) + ") "
#        print(month_query)
    #Depending on what time interval was chosen, a different query will be formed.
    selected_time =  time_select.get()
    if selected_time == 'AM':
        time_query = "AND rtime <'12:00:00' "
    elif selected_time == 'PM' :
        time_query = "AND rtime >'12:00:00' "
    elif selected_time == 'AMPeak' :
        time_query = "AND rtime between '07:00:00' and '09:00:00' "
    elif selected_time == 'PMPeak' :
        time_query = "AND rtime between '16:00:00' and '18:00:00' "
    elif selected_time == 'All' :
        time_query = ""
        
    """UNCOMMENT SQL LINE FOR MONTH QUERY"""
#    SQL = "SELECT * FROM " + table_name + intersection_query + month_query + time_query
    SQL = "SELECT * FROM " + table_name + intersection_query + time_query

    dataframe = pd.read_sql_query(SQL, conn)
    print(SQL)
    #If a query was chosen with no results, the user will be prompted to try again.
    if len(dataframe)> 0:
        print(dataframe)
        SQL_Query.destroy()
    else:
        alert(title='Warning!', text='Query Returned 0 Results', button='Try Again')
        
        
""" This function is leftover from a potential addition to include filtering by street.
    This is not available at the moment since our table only specifies intersections"""
#def street_change():
#    street_name = street_select.get()
#    SQL = "Select * from " + table_name + "where Int1 ILIKE " + street_name 
#    dataframe = pd.read_sql_query(SQL, conn)
#    street_list = []
#    street_selection.children["menu"].delete(0,"end")
#    street_list = street_list['Int1'].tolist()
#    for i in street_list:
#        street_selection.children["menu"].add_command(label=i, command=lambda street=i: selectedStreet.set(street))

# In[3]: 
#Create first windowed menu and give it dimensions.
SQL_Query = Tk()
SQL_Query.geometry("550x200")

table_select = StringVar()

""" Get rid of this temporary title when ready to add list of tables defined above"""
temporary_title = ["intersection_selection_2018"]
#Frames group certain buttons or entries together in a package. 
row = Frame(SQL_Query)
lab0 = Label(row, width=30, text="Private Vehicle 24h Travel Time:", anchor='w', font=("Helvetica", 12))

#Create an "Optionmenu" that contains all available tables
table_selection = OptionMenu(row, table_select, *temporary_title)
table_select.set(temporary_title[0])
row.pack(side=TOP, fill=X)
lab0.pack(side=LEFT)
table_selection.pack(side= RIGHT, fill=X)

row.pack(side=TOP, fill=X)
#
#
#row = Frame(SQL_Query)
#options_label1 = Label(row, width=80, text="Private Vehicle 24h Travel Time", anchor='w', font=("Helvetica", 12))
#row.pack(side=TOP, fill=X)
#options_label1.pack(side=LEFT, padx=8)
#
#row.pack(side=TOP, fill=X)
#

row = Frame(SQL_Query)
options_label2 = Label(row, width=80, text="Available", anchor='w', font=("Helvetica", 10))
row.pack(side=TOP, fill=X)
options_label2.pack(side=LEFT,padx=25)

row.pack(side=TOP, fill=X)


row = Frame(SQL_Query)
options_label3 = Label(row, width=80, text="Table: intersection_selection_2018", anchor='w', font=("Helvetica", 10))
row.pack(side=TOP, fill=X)
options_label3.pack(side=LEFT,padx=25)

row.pack(side=TOP, fill=X)


row = Frame(SQL_Query)
options_label4 = Label(row, width=80, text="Transit Vehicle Peak Hour Travel Time", anchor='w', font=("Helvetica", 12))
row.pack(side=TOP, fill=X)
options_label4.pack(side=LEFT,padx=8)

row.pack(side=TOP, fill=X)

row = Frame(SQL_Query)
options_label5 = Label(row, width=80, text="Coming Soon", anchor='w', font=("Helvetica", 10))
row.pack(side=TOP, fill=X)
options_label5.pack(side=LEFT,padx=25)

row.pack(side=TOP, fill=X)

b1 = Button(SQL_Query, text='Select', command=SelectTable)
b1.pack(side=LEFT, padx=5, pady=5)

SQL_Query.mainloop()
""" Leftover from version that included corridor selection"""
#row = Frame(SQL_Query)
#lab1 = Label(row, width=30, text="Corridor Selection", anchor='w')
#street_selection = OptionMenu(row, street_select, *street_list)
#
#street_select.trace('w', street_change)
#
#row.pack(side=TOP, fill=X)
#lab1.pack(side=LEFT)
#int_1_list.pack(side= RIGHT, fill=X)
#
#row.pack(side=TOP, fill=X)

if len(int_1)>0:
    #Create next windowed menu and give it dimensions
    SQL_Query = Tk()
    SQL_Query.geometry("1000x200")
    
    int_1_select = StringVar()
    int_2_select = StringVar()
    
    row = Frame(SQL_Query)
    lab2 = Label(row, width=30, text="Intersection 1:", anchor='w', font=("Helvetica", 10))
    int_1_list = OptionMenu(row, int_1_select, *int_1)
    int_1_select.set(int_1[0])
    #Trace changes to selection and when a change occurs run "int_selection_1" Function. 
    #This populates the second intersection list with only relevant options.
    int_1_select.trace('w', int_selection_1)
    
    row.pack(side=TOP, fill=X)
    lab2.pack(side=LEFT)
    int_1_list.pack(side= RIGHT)
    
    row.pack(side=TOP, fill=X)
    
    row = Frame(SQL_Query)
    lab3 = Label(row, width=30, text="Intersection 2:", anchor='w', font=("Helvetica", 10))
    int_2_list = OptionMenu(row, int_2_select, *int_2)
    int_2_select.set(int_2[0])
    
    #If user selects intersection 2 first it traces the change and populates first list with only relevant options.
    int_2_select.trace('w', int_selection_2)
    
    row.pack(side=TOP, fill=X)
    lab3.pack(side=LEFT)
    int_2_list.pack(side= RIGHT)
    
    row.pack(side=TOP, fill=X)
    
    """UNCOMMENT FOR SELECTION OF MONTHS"""
#    row = Frame(SQL_Query)
#    lab4 = Label(row, width=15, text="Months:", anchor='w', font=("Helvetica", 10))
#    #Creates a row of check boxes containing all months. User can select as many months as are relevant.
#    month_list = Checkbar(row, ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'])
#    row.pack(side=TOP, fill=X)
#    lab4.pack(side=LEFT)
#    month_list.pack(side= RIGHT)
#    
#    row.pack(side=TOP, fill=X)
#    
    #Creates a list of options for time selections
    time_options = ['All','AM', 'PM', 'AMPeak', 'PMPeak']
    time_select = StringVar()
    row = Frame(SQL_Query)
    lab5 = Label(row, width=30, text="Time:", anchor='w', font=("Helvetica", 10))
    
    time_list = OptionMenu(row, time_select, *time_options)
    time_select.set(time_options[0])
    row.pack(side=TOP, fill=X)
    lab5.pack(side=LEFT)
    time_list.pack(side= RIGHT)
    
    row.pack(side=TOP, fill=X)
    #Creates buttons to finish query or reset the intersection choices.
    b1 = Button(SQL_Query, text='Finish', command=FinishQuery)
    b1.pack(side=LEFT, padx=5, pady=5)
    
    b2 = Button(SQL_Query, text='Reset', command=ResetFunctions)
    b2.pack(side=LEFT, padx=5, pady=5)
    SQL_Query.mainloop()
