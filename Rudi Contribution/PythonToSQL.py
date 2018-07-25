# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 15:47:27 2018
Python to SQL Query
@author: rxr
"""

import psycopg2
import pandas as pd
import pandas.io.sql as psql 
import xlsxwriter
#Connect to SQL database using credentials
conn = psycopg2.connect(host="localhost",database="TravelTime", user="postgres", password="postgres")
cur = conn.cursor()

SQL = "select relname as table from  pg_stat_user_tables where schemaname = 'public'"
table_list = pd.read_sql_query(SQL, conn)
print("Database titles and index")
print(table_list)
#Execute SQL command to fetch list of tables in database

#Input title of table to use for query
while True:
    table_index = input('Enter database table index: ') 
    table_index = int(table_index)
    if table_index < len(table_list) and table_index > 0:    
        table_title = table_list.iloc[table_index]['table'] + " "
        break
    elif table_index >len(table_list) or table_index < 0:
        print("Enter a valid index")
        
print(table_title)
#Ask if the user wants to use Seasons to define their months or specify the months themselves
while True:
    seasonal_input = input('Do you want Seasonal data? Y/N: ')
    seasonal_input = seasonal_input.lower()
    if seasonal_input == 'y' or seasonal_input =='n':
        break
    else:
        print('Please try again')
        
month_input_list = []
#Checks to see if user asked for seasonal lists, if not they can specify their own months.
while True and seasonal_input == 'n':
    #Input has to be one month at a time
    month_input = input('Enter target months (January, february, etc.) one at a time or "All" (press enter on blank line when done): ')
    #Converts month to lower case to get rid of case sensitivity. 
    month_input =month_input.lower() 
    if month_input == 'january' or month_input == 'february' or month_input == 'march' or month_input == 'april' or month_input == 'may' or month_input == 'june' or month_input == 'july' or month_input == 'august' or month_input == 'september' or month_input == 'october' or\
     month_input == 'november' or month_input == 'december':
         #Checks to see if input is part of the list of months, then appends ' ' marks to beginning and end of month to be read by SQL
         month_input = "'" + month_input + "'"
         month_input_list.append(month_input)

    elif month_input == 'all':
        #If User selects ALL months the query will simply look at all months through % wildcard character
        month_sql_input = "WHERE month LIKE '%' "
        break
    elif month_input == '':
        #Once user has finished, they press enter on a blank command line and the query is compiled
        month_input_list = [month_input_list.title() for month_input_list in month_input_list]
        month_sql_input = "WHERE month IN (" + ', '.join(month_input_list) + ") "
        print(month_sql_input)
        break
    else:
        #If input is not part of the list it will prompt for a new input
        print('Please input month again')

while True and seasonal_input == 'y':
    #If the user asked for seasonal inputs they have to input the season they want
    season_input = input('Enter target season (spring, summer, fall, winter), working months(work) (excluding summmer), or "All": ')
    #Input is put into lowercase to avoid case sensitivity
    season_input = season_input.lower()
    #Depending on the season input it assigns a group of 3 months for the query
    if season_input == 'summer':
        month_input_list = ["'June'", "'July'", "'August'"]
        month_sql_input = "WHERE month IN (" + ', '.join(month_input_list) + ") "
        print(month_sql_input)

        break
    elif season_input == 'fall':
        month_input_list = ["'September'", "'October'", "'November'"]
        month_sql_input = "WHERE month IN (" + ', '.join(month_input_list) + ") "
        print(month_sql_input)

        break
    elif season_input == 'winter':
        month_input_list = ["'December'", "'January'", "'February'"]
        month_sql_input = "WHERE month IN (" + ', '.join(month_input_list) + ") "
        print(month_sql_input)

        break
    elif season_input == 'spring':
        month_input_list = ["'March'", "'April'", "'May'"]
        month_sql_input = "WHERE month IN (" + ', '.join(month_input_list) + ") "
        print(month_sql_input)

        break
    elif season_input == 'work':
        month_input_list = ["'June'", "'July'", "'August'"]
        month_sql_input = "WHERE month NOT IN (" + ', '.join(month_input_list) + ") "
        print(month_sql_input)

        break
    elif season_input == 'all':
        #If input is "all" then the month query is replaced with % wildcard
        month_sql_input = "WHERE month LIKE '%' "
        print(month_sql_input)

        break
    else:
        print('Please input season again')
        
while True:
    #Asks for time input as either an AM, PM or ALL input
    time_input = input('Enter AM (before noon), PM(after noon), AM Peak input ampeak (7-9), PM Peak input pmpeak (4-6)  or "All": ')
    time_input = time_input.lower()
    if time_input == 'am':
        #If input is AM it returns a query to specify request time < 12 (noon)
        time_input = "AND rtime <'12:00:00' "
        print(time_input)
        
        break
    elif time_input == 'pm':
        #If input is PM it returns a query to specify request time > 12 (noon)
        time_input = "AND rtime >'12:00:00' "
        print(time_input)

        break
    
    elif time_input == 'ampeak':
        #If input is PM it returns a query to specify request time > 12 (noon)
        time_input = "AND rtime between '07:00:00' and '09:00:00' "
        print(time_input)

        break
    elif time_input == 'pmpeak':
        #If input is PM it returns a query to specify request time > 12 (noon)
        time_input = "AND rtime between '16:00:00' and '18:00:00' "
        print(time_input)

        break
    elif time_input == 'all':
        time_input = ''
        print(time_input)

        break
    else: 
        print('Please input time again')

weekdays_list =[]
while True:
    #Works much the same as the month input. Checks input based on list of days, creates a list if user inputs multiple days.
    weekday_input = input('Enter desired weekday (monday, tuesday, wednesday etc), No weekend (enter weekday), weekend (enter weekend) or "All" (press enter on blank line when done): ')
    weekday_input = weekday_input.lower()
    #Input only allows one input per line
    if weekday_input == 'monday' or weekday_input == 'tuesday' or weekday_input == 'wednesday' or weekday_input == 'thursday' or weekday_input == 'friday' or weekday_input == 'saturday' or weekday_input == 'sunday':
        weekday_input = "'" + weekday_input + "'"
        weekdays_list.append(weekday_input)
    elif weekday_input == 'all':
        weekday_sql_input = ''
        break
    elif weekday_input == 'weekday':
        weekday_sql_input = "AND day NOT IN ('Saturday', 'Sunday') "
        break
    elif weekday_input == 'weekend':
        weekday_sql_input = "AND day IN ('Saturday', 'Sunday') "
        break
    elif weekday_input =='':
        #Joins list of inputs and creates DAY query.
        weekdays_list = [weekdays_list.title() for weekdays_list in weekdays_list]
        weekday_sql_input = "AND day IN (" + ', '.join(weekdays_list) + ") "
        print(weekday_sql_input)
        break
    else:
        print('Plese input weekday again')
        
        
#Joins all the queries and creates an SQL compatible query to execute.
SQL_input = "SELECT * FROM " + table_title + month_sql_input + weekday_sql_input + time_input + ";"
print(SQL_input)
    
#Puts SQL table into a Pandas Dataframe
df = pd.read_sql_query(SQL_input, conn)
dfstat = df[['travel_time']].describe(percentiles = [0.15, 0.25, 0.5, 0.7, 0.95])

excel_name = input("Input your desired file name: ")

print(dfstat)

excel_write = pd.ExcelWriter("C:/Users/rxr/Documents/Travel Times/" + excel_name + ".xlsx", engine='xlsxwriter')
dfstat.to_excel(excel_write, sheet_name='DataStats')
df.to_excel(excel_write, sheet_name='DataFrame')

excel_write.save()
conn.close()
