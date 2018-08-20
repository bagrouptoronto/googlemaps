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
global dates
global months
reset_fcn = False
int_select_1 = False
int_select_2 = False
street_list = []
int_1 = []
int_2 = []
dates = []
# In[2]:
# Specify connection to SQL server. Change parameters as needed if Server gets moved to another computer.
conn = psycopg2.connect(host="10.1.2.165",database="BA_DATA", user="user", password="password")

#Provides a list of all table options in a database. 
SQL = "select relname as table from  pg_stat_user_tables where schemaname = 'public'"
table_list = pd.read_sql_query(SQL, conn)

#Converts dataframe column to a python list
table_list = table_list['table'].tolist()    


# In[3]: 
        
""" Creates Intersection, month, and date lists based on selected table, this contains all intersections in the database"""
def SelectTable():
    global int_1, int_2, table_name, date_list, months, dates
    table_name = table_select.get()
    
    SQL = "Select distinct(Int1) from " + table_name
    dataframe = pd.read_sql_query(SQL, conn)
    int_1 = dataframe['int1'].tolist()
    
    SQL = "Select distinct(Int2) from " + table_name
    dataframe = pd.read_sql_query(SQL, conn)
    int_2 = dataframe['int2'].tolist()
    
    SQL = "Select distinct(date) from " + table_name
    dataframe = pd.read_sql_query(SQL, conn)
    dates = dataframe['date'].tolist()
        
    SQL = "Select distinct(month) from " + table_name
    dataframe = pd.read_sql_query(SQL, conn)
    months = dataframe['month'].tolist()
    SQL_Query.destroy()
    
""" These functions select distinct intersection names from the database and update the lists to include only relevant options"""

def int_selection_1(x, y, z):
    global intersection_1, table_name, int_2, int_select_1, int_select_2, reset_fcn, month_select
    if reset_fcn is False:
        intersection_1 = int_1_select.get()
        if int_select_2 is False and int_select_1 is False:
            #Creates a query that only selects the second intersections where the selected intersection exists.
            SQL = "Select distinct(Int2) from " + table_name + " where Int1 ILIKE '" + intersection_1 + "'"
            dataframe = pd.read_sql_query(SQL, conn)
            if len(dataframe)<1:
                alert(title='Warning', text="Data doesn't exist for your selection", button="Try again")
            else:
            #Deletes current list of 2nd intersections and replaces it with relevant options.
                int_2_list.children["menu"].delete(0,"end")
                int_2 = dataframe['int2'].tolist()
                for i in int_2:
                    int_2_list.children["menu"].add_command(label=i, command=lambda intersection2=i: int_2_select.set(intersection2))
                int_2_select.set(int_2[0])
                
                SQL = "Select distinct(month) from " + table_name + " where Int1 ILIKE '" + intersection_1 + "'"
                dataframe = pd.read_sql_query(SQL, conn)
                month_list.children["menu"].delete(0, "end")
                months = dataframe['month'].tolist()
                for i in months:
                    month_list.children["menu"].add_command(label=i, command=lambda month=i: month_select.set(month))
                month_select.set(months[0])
                
                SQL = "Select distinct(date) from " + table_name + " where Int1 ILIKE '" + intersection_1 + "'"
                dataframe = pd.read_sql_query(SQL, conn)
                date_list.children["menu"].delete(0, "end")
                dates = dataframe['date'].tolist()
                for i in dates:
                    date_list.children["menu"].add_command(label=i, command=lambda date=i: date_select.set(date))
                date_select.set(dates[0])
                int_select_1 = True

def int_selection_2(x, y, z):
    global intersection_2, table_name, int_1, int_select_1, int_select_2, reset_fcn, months
    if reset_fcn is False:
        intersection_2 = int_2_select.get()
        if int_select_1 is False and int_select_2 is False:
            #Creates a query that only selects the first intersections where the selected intersection exists.
            SQL = "Select distinct(Int1) from " + table_name + " where Int2 ILIKE '" + intersection_2 + "'"
            dataframe = pd.read_sql_query(SQL, conn)
            if len(dataframe)<1:
                alert(title='Warning', text="Data doesn't exist for your selection", button="Try again")
            else:
            #Deletes current list of 2nd intersections and replaces it with relevant options.
                int_1_list.children["menu"].delete(0,"end")
                int_1 = dataframe['int1'].tolist()
                for i in int_1:
                    int_1_list.children["menu"].add_command(label=i, command=lambda intersection1=i: int_1_select.set(intersection1))
                int_1_select.set(int_1[0])
                
                SQL = "Select distinct(month) from " + table_name + " where Int2 ILIKE '" + intersection_2 + "'"
                dataframe = pd.read_sql_query(SQL, conn)
                month_list.children["menu"].delete(0, "end")
                months = dataframe['month'].tolist()
                for i in months:
                    month_list.children["menu"].add_command(label=i, command=lambda month=i: month_select.set(month))
                month_select.set(months[0])
                
                SQL = "Select distinct(date) from " + table_name + " where Int2 ILIKE '" + intersection_1 + "'"
                dataframe = pd.read_sql_query(SQL, conn)
                date_list.children["menu"].delete(0, "end")
                dates = dataframe['date'].tolist()
                for i in dates:
                    date_list.children["menu"].add_command(label=i, command=lambda date=i: date_select.set(date))
                date_select.set(dates[0])
                int_select_2 = True
            
def month_selection(x, y, z):
    global months, dates, reset_fcn
    if reset_fcn is False:
        month = month_select.get()
        intersection_input_1 = int_1_select.get()
        intersection_input_2 = int_2_select.get()
        
        #Creates a query that only selects the first intersections where the selected intersection exists.
        SQL = "SELECT distinct(date) FROM " + table_name + " WHERE month ILIKE '" + month + "' AND int1 ILIKE '" + intersection_input_1 + "' AND int2 ILIKE '" + intersection_input_2 + "'"
        dataframe = pd.read_sql_query(SQL, conn)
        if len(dataframe)<1:
            alert(title='Warning', text="Data doesn't exist for your selection", button="Try again")
        else:
            date_list.children["menu"].delete(0, "end")
            dates = dataframe['date'].tolist()
            for i in dates:
                date_list.children["menu"].add_command(label=i, command=lambda date=i: date_select.set(date))
                date_select.set(dates[0])


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
            int_1_list.children["menu"].add_command(label=i, command=lambda intersection1=i: int_1_select.set(intersection1))
            
        SQL = "Select distinct(Int2) from " + table_name
        dataframe = pd.read_sql_query(SQL, conn)
           
        int_2_list.children["menu"].delete(0,"end")
        int_2 = dataframe['int2'].tolist()
        for j in int_2:
            int_2_list.children["menu"].add_command(label=j, command=lambda intersection2=j: int_2_select.set(intersection2))
        
        SQL = "Select distinct(month) from " + table_name
        dataframe = pd.read_sql_query(SQL, conn)
        month_list.children["menu"].delete(0, "end")
        months = dataframe['month'].tolist()
        for i in months:
            month_list.children["menu"].add_command(label=i, command=lambda month=i: month_select.set(month))
        
        SQL = "Select distinct(date) from " + table_name
        dataframe = pd.read_sql_query(SQL, conn)
        date_list.children["menu"].delete(0, "end")
        dates = dataframe['date'].tolist()
        for i in dates:
            date_list.children["menu"].add_command(label=i, command=lambda date=i: date_select.set(date))
    
    date_select.set(dates[0])
    month_select.set(months[0])
    int_1_select.set(int_1[0])
    int_2_select.set(int_2[0])
    reset_fcn = False
    alert(title='Reset', text='Reset', button='Ok')
    
""" Creates final Query that will be fed into SQL to produce results""" 

def FinishQuery():
    import os
    import sys
    global table_name, intersection_1, intersection_2
    
    intersection_input_1 = int_1_select.get()
    intersection_input_2 = int_2_select.get()
    
    intersection_query = " WHERE Int1 ILIKE '" + intersection_input_1 + "' AND Int2 ILIKE '" + intersection_input_2 + "' "
    
    selected_months = month_select.get()
    selected_date = date_select.get()

    month_query = "AND month LIKE '" + selected_months + "' "
    date_query = "AND date ILIKE '" + selected_date + "' "
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
    SQL = "SELECT * FROM " + table_name + intersection_query + month_query + time_query + date_query

    dataframe = pd.read_sql_query(SQL, conn, parse_dates={'rtime': '%H:%M:%S'},)
    print(dataframe)
    #If a query was chosen with no results, the user will be prompted to try again.
    if len(dataframe)> 0:
        newfn = "Output " + intersection_1.replace('/', '+') + " to " + intersection_2.replace('/', '+')
        print(newfn)
        srcfp = os.getcwd() + "/"
        srcfp = '/'.join(srcfp.split('\\'))
        pandasToExcel(dataframe, newfn, srcfp)
    else:
        alert(title='Warning!', text='Query Returned 0 Results', button='Try Again')
        
def pandasToExcel(df, newfn, srcfp):
    """Query travel time data from Pandas Dataframe and export it to Excel."""
    global intersection_1, intersection_2
    import pandas as pd


    df.travel_time = df.travel_time.divide(24*3600)

    print("Pre-processing the dataframe...")

    writer = pd.ExcelWriter(srcfp + newfn + ".xlsx", engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Data')
    workbook = writer.book
    worksheet = writer.sheets['Data']
    chart = workbook.add_chart({'type': 'scatter'})
    chart.add_series({'categories': '=Data!$K$2:$K$' + str(len(df)),
                      'values':'=Data!$I$2:$I$' + str(len(df))})
#    chart.set_x_axis({'num_format': 'h:mm:ss'})
    chart.set_x_axis({'name':'Time of Day','minor_unit': 0.01666, 'major_unit': .083333, 'min':0, 'max':1, 'num_format':'h:mm:ss'})
    chart.set_y_axis({'name':'Travel Time (mins)'})
    chart.set_title({'name': 'Real-Time Travel Times from ' + intersection_1 + ' to ' + intersection_2})
    chart.set_size({'width': 800, 'height':500})
    chart.set_legend({'none':True})
    
    format1 = workbook.add_format({'num_format': 'mm:ss'})
    format2 = workbook.add_format({'num_format': 'h:mm:ss'})

    worksheet.insert_chart('M2', chart)
    worksheet.set_column('I:I', None, format1)
    worksheet.set_column('K:K', None, format2)
# =============================================================================
#         dfwkdy.to_excel(writer, 'Weekday')
#         dfwed.to_excel(writer, 'Wednesday')
#         dfthu.to_excel(writer, 'Thursday')
#         dfsat.to_excel(writer, 'Saturday')
#         dftue.to_excel(writer, 'Tuesday')
# =============================================================================
        
    writer.save()
    
    alert(title='Excel File', text='File created in ' + srcfp, button='Ok')
    
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
SQL_Query.geometry("550x400")

table_select = StringVar()


#Frames group certain buttons or entries together in a package. 
row = Frame(SQL_Query)
lab0 = Label(row, width=30, text="Data Selection:", anchor='w', font=("Helvetica", 14))

#Create an "Optionmenu" that contains all available tables
table_selection = OptionMenu(row, table_select, *table_list)
table_select.set(table_list[0])
row.pack(side=TOP, fill=X)
lab0.pack(side=LEFT)
table_selection.pack(side= RIGHT, fill=X)

row.pack(side=TOP, fill=X)


row = Frame(SQL_Query)
options_label1 = Label(row, width=80, text="Private Vehicle 24h Travel Time:", anchor='w', font=("Helvetica", 12))
row.pack(side=TOP, fill=X)
options_label1.pack(side=LEFT, padx=8)

row.pack(side=TOP, fill=X)


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
options_label4 = Label(row, width=80, text="Transit Vehicle Peak Hour Travel Time:", anchor='w', font=("Helvetica", 12))
row.pack(side=TOP, fill=X)
options_label4.pack(side=LEFT,padx=8)

row.pack(side=TOP, fill=X)

row = Frame(SQL_Query)
options_label5 = Label(row, width=80, text="Coming Soon", anchor='w', font=("Helvetica", 10))
row.pack(side=TOP, fill=X)
options_label5.pack(side=LEFT,padx=25)

row.pack(side=TOP, fill=X)

row = Frame(SQL_Query)
options_label6 = Label(row, width=80, text="Queue Data:", anchor='w', font=("Helvetica", 12))
row.pack(side=TOP, fill=X)
options_label6.pack(side=LEFT,padx=8)

row.pack(side=TOP, fill=X)

row = Frame(SQL_Query)
options_label7 = Label(row, width=80, text="Coming Soon", anchor='w', font=("Helvetica", 10))
row.pack(side=TOP, fill=X)
options_label7.pack(side=LEFT,padx=25)

row.pack(side=TOP, fill=X)

row = Frame(SQL_Query)
options_label8 = Label(row, width=80, text="TMDC Data:", anchor='w', font=("Helvetica", 12))
row.pack(side=TOP, fill=X)
options_label8.pack(side=LEFT,padx=8)

row.pack(side=TOP, fill=X)

row = Frame(SQL_Query)
options_label9 = Label(row, width=80, text="Coming Soon", anchor='w', font=("Helvetica", 10))
row.pack(side=TOP, fill=X)
options_label9.pack(side=LEFT,padx=25)

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
    month_select = StringVar()
    date_select = StringVar()
    row = Frame(SQL_Query)
    lab4 = Label(row, width=15, text="Months:", anchor='w', font=("Helvetica", 10))
    #Creates a row of check boxes containing all months. User can select as many months as are relevant.
    month_list = OptionMenu(row, month_select, *months)
    
    date_list = OptionMenu(row, date_select, *dates)
    
    month_select.trace('w',month_selection)
    
    row.pack(side=TOP, fill=X)
    lab4.pack(side=LEFT)
    month_list.pack(side= RIGHT)
    date_list.pack(side=RIGHT)
    
    row.pack(side=TOP, fill=X)

    #Creates a list of options for time selections
    time_options = ['All','AM', 'PM', 'AMPeak', 'PMPeak']
    time_select = StringVar()
    row = Frame(SQL_Query)
    lab6 = Label(row, width=30, text="Time:", anchor='w', font=("Helvetica", 10))
    
    time_list = OptionMenu(row, time_select, *time_options)
    time_select.set(time_options[0])
    row.pack(side=TOP, fill=X)
    lab6.pack(side=LEFT)
    time_list.pack(side= RIGHT)
    
    row.pack(side=TOP, fill=X)
    #Creates buttons to finish query or reset the intersection choices.
    b1 = Button(SQL_Query, text='Submit', command=FinishQuery)
    b1.pack(side=LEFT, padx=5, pady=5)
    
    b2 = Button(SQL_Query, text='Reset', command=ResetFunctions)
    b2.pack(side=LEFT, padx=5, pady=5)
    
    b3 = Button(SQL_Query, text='Finish', command=SQL_Query.destroy)
    b3.pack(side=LEFT, padx=5, pady=5)
    SQL_Query.mainloop()
