
# coding: utf-8

# In[28]:


#Google Maps Travel Time Output Tool

import googlemaps
import datetime
import calendar
import numpy
import pprint


maps_key = "AIzaSyBi5ERPxgzZEpMSQFmptFpg57aby2g76I0"
gmaps = googlemaps.Client(key=maps_key)


# In[29]:


#Define road segments and points - USER INPUT

#point list to be better organized

#Queen St
Title = 'Queen Street'
Direction = 'EW'
point1 = 43.65680, -79.35889,
point2 = 43.65886, -79.34982,
point3 = 43.66104, -79.34007,
point4 = 43.66324, -79.33020,

#Eastern Ave
#Title = 'Eastern Avenue'
#Direction = 'EW'
#point1 = 43.65381, -79.35860,
#point2 = 43.65663, -79.34890,
#point3 = 43.65837, -79.33896,
#point4 = 43.66155, -79.32947,

#Lake Shore Blvd E
#Title = 'Lake Shore Boulevard East'
#Direction = 'EW'
#point1 = 43.64919, -79.35711,
#point2 = 43.65112, -79.34724,
#point3 = 43.65507, -79.33766,
#point4 = 43.65917, -79.32857,

#Commissioners St
#Direction = 'EW'
#Title = 'Commissioners Street'
#point1 = 43.64539, -79.35230,
#point2 = 43.64851, -79.34510,
#point3 = 43.65260, -79.33549,
#point4 = 43.65649, -79.32641,

#Cherry St
#Direction = 'NS'
#Title = 'Cherry Street'
#point1 = 43.64536, -79.35259,
#point2 = 43.64890, -79.35603,
#point3 = 43.65368, -79.35856,
#point4 = 43.65676, -79.35888,

#Don Roadway
#Direction = 'NS'
#Title = 'Don Roadway'
#point1 = 43.64858, -79.34507,
#point2 = 43.65119, -79.34719,
#point3 = 43.65427, -79.34986,
#point4 = 43.65959, -79.35449,

#Carlaw Ave
#Direction = 'NS'
#Title = 'Carlaw Avenue'
#point1 = 43.65260, -79.33549,
#point2 = 43.65504, -79.33751,
#point3 = 43.65837, -79.33896,
#point4 = 43.66104, -79.34007,

#Leslie St
#Direction = 'NS'
#Title = 'Leslie Street'
#point1 = 43.65656, -79.32639,
#point2 = 43.65906, -79.32838,
#point3 = 43.66155, -79.32947,
#point4 = 43.66324, -79.33020,


# In[30]:


#definition for matrices, 'w' lists, each of 'h' items
#user input
w, h = 4, 4;

#Set origins and destinations
if w == 4:
    origins = [point1,point2,point3,point4]
    destinations = [point1,point2,point3,point4]
if w == 3:
    origins = [point1,point2,point3]
    destinations = [point1,point2,point3]

#Set direction text
if Direction == 'EW':
    Dir1 = 'Eastbound'
    Dir2 = 'Westbound'
if Direction == 'NS':
    Dir1 = 'Northbound'
    Dir2 = 'Southbound'


# In[31]:


#Convert Departure Time to seconds - USER INPUT

# January 18 2018 8:45 AM, Test 9:00 AM - 1516283100
# January 18 2018 5:30 PM - 1516314600

#user input
year = 2018
month = 1
day = 18
hour = 9
min = 0

#convert to datetime variable
fdate = datetime.datetime(year,month,day,hour,min,0)

#get timezone info
Time1 = gmaps.timezone(point1, fdate, language=None)
sec = calendar.timegm(fdate.timetuple()) - Time1['dstOffset'] - Time1['rawOffset']

#Time in seconds since Midnight of January 1 1970 UTC
deptime = sec

#Set Peak Hour based on time inputs
if hour < 12:
    TimeTitle = 'Morning (AM)'
else:
    TimeTitle = 'Afternoon (PM)'


# In[32]:


#Google Distance Matrix API Input and Output 

#Optimistic
Optimistic = gmaps.distance_matrix(
    (origins),
    (destinations),
    departure_time = deptime,
    mode = 'driving',
    traffic_model = 'optimistic',
    )

#Best Guess
BestGuess = gmaps.distance_matrix(
    (origins),
    (destinations),
    departure_time = deptime,
    mode = 'driving',
    traffic_model = 'best_guess',
    )

#Pessimistic
Pessimistic = gmaps.distance_matrix(
    (origins),
    (destinations),
    departure_time = deptime,
    mode = 'driving',
    traffic_model = 'pessimistic',
    )


# In[33]:


#Writes results to created travel time arrays

#Creates a list containing 'w' lists, each of 'h' items, all set to 0
#w, h = 4, 4;
otmat = [[0 for x in range(w)] for y in range(h)] 
btmat = [[0 for x in range(w)] for y in range(h)]
ptmat = [[0 for x in range(w)] for y in range(h)]

#Write to otmat, btmat and ptmat
for i in range (0, w):
    for j in range (0, h):
        otmat[i][j] = Optimistic['rows'][i]['elements'][j]['duration_in_traffic']['value']
        btmat[i][j] = BestGuess['rows'][i]['elements'][j]['duration_in_traffic']['value']
        ptmat[i][j] = Pessimistic['rows'][i]['elements'][j]['duration_in_traffic']['value']


# In[34]:


#Zero time entry correction

#find if zero is in this matrix thing?
for i in range (0, w):
    for j in range (0, h):
        if i == j:
            if otmat[i][j] == 0:
                otmat[i][j] = 1
            if btmat[i][j] == 0:
                btmat[i][j] = 1
            if ptmat[i][j] == 0:
                ptmat[i][j] = 1


# In[35]:


#Writes results to created distance arrays

#Creates a list containing 'w' lists, each of 'h' items, all set to 0
#w, h = 4, 4;
odmat = [[0 for x in range(w)] for y in range(h)] 
bdmat = [[0 for x in range(w)] for y in range(h)]
pdmat = [[0 for x in range(w)] for y in range(h)]


#Write to otmat
for i in range (0, w):
    for j in range (0, h):
        odmat[i][j] = Optimistic['rows'][i]['elements'][j]['distance']['value']
        bdmat[i][j] = BestGuess['rows'][i]['elements'][j]['distance']['value']
        pdmat[i][j] = Pessimistic['rows'][i]['elements'][j]['distance']['value']


# In[36]:


#Copies travel times to another variable

#Creates a list containing 'w' lists, each of 'h' items, all set to 0
#w, h = 4, 4;
otmatsec = [[0 for x in range(w)] for y in range(h)] 
btmatsec = [[0 for x in range(w)] for y in range(h)]
ptmatsec = [[0 for x in range(w)] for y in range(h)]

for i in range (0, w):
    for j in range (0, h):
        otmatsec[i][j] = otmat[i][j]
        btmatsec[i][j] = btmat[i][j]
        ptmatsec[i][j] = ptmat[i][j]


# In[37]:


#Convert otmat, btmat and ptmat from seconds to hours
for i in range (0, w):
    for j in range (0, h):
        otmat[i][j] = otmat[i][j]/3600
        btmat[i][j] = btmat[i][j]/3600
        ptmat[i][j] = ptmat[i][j]/3600


# In[38]:


#Convert odmat, bdmat and pdmat from m to km
for i in range (0, w):
    for j in range (0, h):
        odmat[i][j] = odmat[i][j]/1000
        bdmat[i][j] = bdmat[i][j]/1000
        pdmat[i][j] = pdmat[i][j]/1000


# In[39]:


#Creates a list containing 'w' lists, each of 'h' items, all set to 0
#w, h = 4, 4;
osmat = [[0 for x in range(w)] for y in range(h)] 
bsmat = [[0 for x in range(w)] for y in range(h)] 
psmat = [[0 for x in range(w)] for y in range(h)] 

#Determine speed
for i in range (0, w):
    for j in range (0, h):
        osmat[i][j] = odmat[i][j]/otmat[i][j]
        bsmat[i][j] = bdmat[i][j]/btmat[i][j]
        psmat[i][j] = pdmat[i][j]/ptmat[i][j]


# In[40]:


if w == 4:
    print('{} Peak Hour' .format(TimeTitle))
    print("")
    print("")

    print('{} - {}' .format(Title,Dir1))
    print("")

    print('Point 1 to 2')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[0][1],osmat[0][1]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[0][1],bsmat[0][1]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[0][1],psmat[0][1]))
    print("")

    print('Point 2 to 3')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[1][2],osmat[1][2]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[1][2],bsmat[1][2]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[1][2],psmat[1][2]))
    print("")

    print('Point 3 to 4')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[2][3],osmat[2][3]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[2][3],bsmat[2][3]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[2][3],psmat[2][3]))
    print("")

    print('Point 1 to 4')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[0][3],osmat[0][3]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[0][3],bsmat[0][3]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[0][3],psmat[0][3]))

    print("")
    print("")

    print('{} - {}' .format(Title,Dir2))
    print("")

    print('Point 4 to 3')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[3][2],osmat[3][2]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[3][2],bsmat[3][2]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[3][2],psmat[3][2]))
    print("")

    print('Point 3 to 2')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[2][1],osmat[2][1]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[2][1],bsmat[2][1]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[2][1],psmat[2][1]))
    print("")

    print('Point 2 to 1')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[1][0],osmat[1][0]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[1][0],bsmat[1][0]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[1][0],psmat[1][0]))
    print("")

    print('Point 4 to 1')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[3][0],osmat[3][0]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[3][0],bsmat[3][0]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[3][0],psmat[3][0]))
    print("")

if w == 3:
    print('{} Peak Hour' .format(TimeTitle))
    print("")
    print("")

    print('{} - {}' .format(Title,Dir1))
    print("")

    print('Point 1 to 2')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[0][1],osmat[0][1]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[0][1],bsmat[0][1]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[0][1],psmat[0][1]))
    print("")

    print('Point 2 to 3')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[1][2],osmat[1][2]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[1][2],bsmat[1][2]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[1][2],psmat[1][2]))
    print("")
  
    print('Point 1 to 3')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[0][2],osmat[0][2]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[0][2],bsmat[0][2]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[0][2],psmat[0][2]))

    print("")
    print("")

    print('{} - {}' .format(Title.Dir2))
    print("")
 
    print('Point 3 to 2')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[2][1],osmat[2][1]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[2][1],bsmat[2][1]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[2][1],psmat[2][1]))
    print("")

    print('Point 2 to 1')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[1][0],osmat[1][0]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[1][0],bsmat[1][0]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[1][0],psmat[1][0]))
    print("")

    print('Point 3 to 1')
    print('Optimistic:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(otmatsec[2][0],osmat[2][0]))
    print('Best Guess:  \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(btmatsec[2][0],bsmat[2][0]))
    print('Pessimistic: \t\t Travel Time = {} secs  \t Speed = {} km/h' .format(ptmatsec[2][0],psmat[2][0]))
    print("")
    

