
# coding: utf-8

# In[59]:


def GDistMat(reqtime, point1, w, h, origins, destinations, RName, timestamp, outfile):
    #Google Maps Travel Time Output Tool
    #No User Inputs Required

    import os
    import googlemaps
    import datetime
    import calendar
    import numpy
    import pprint

    maps_key = "AIzaSyCma3ToCjTI_7A5Wkq0HUeDtNtACS0IS20"
    gmaps = googlemaps.Client(key=maps_key)

    deptime = reqtime
    
    #Creates a list containing 'w' lists, each of 'h' items, all set to 0
    otmatsec = [[0 for x in range(w)] for y in range(h)] 
    btmatsec = [[0 for x in range(w)] for y in range(h)]
    ptmatsec = [[0 for x in range(w)] for y in range(h)]
    
    try:
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

        #Writes results to created travel time arrays
        #Write to otmat, btmat and ptmat
        for i in range (0, w):
            for j in range (0, h):
                otmatsec[i][j] = Optimistic['rows'][i]['elements'][j]['duration_in_traffic']['value']
                btmatsec[i][j] = BestGuess['rows'][i]['elements'][j]['duration_in_traffic']['value']
                ptmatsec[i][j] = Pessimistic['rows'][i]['elements'][j]['duration_in_traffic']['value']    

        #Zero time entry correction
        #find if zero is in this matrix thing?
        for i in range (0, w):
            for j in range (0, h):
                if i == j:
                    if otmatsec[i][j] == 0:
                        otmatsec[i][j] = 1
                    if btmatsec[i][j] == 0:
                        btmatsec[i][j] = 1
                    if ptmatsec[i][j] == 0:
                        ptmatsec[i][j] = 1

        #Calculate total travel times using individual times between points  
        if w == 2:
            OptTime = otmatsec[0][1]
            BestTime = btmatsec[0][1]
            PesTime = ptmatsec[0][1]
                
        if w == 3:
            OptTime = otmatsec[0][1] + otmatsec[1][2]
            BestTime = btmatsec[0][1] + btmatsec[1][2]
            PesTime = ptmatsec[0][1] + ptmatsec[1][2]
                
        if w == 4:
            OptTime = otmatsec[0][1] + otmatsec[1][2] + otmatsec[2][3]
            BestTime = btmatsec[0][1] + btmatsec[1][2] + btmatsec[2][3]
            PesTime = ptmatsec[0][1] + ptmatsec[1][2] + ptmatsec[2][3]   
            
    except:
        OptTime = "Er"
        BestTime = "Er"
        PesTime = "Er"
        houston("error",RName)
        
    #print(otmatsec[0][1],otmatsec[1][2],OptTime,otmatsec[0][2])
    #print(btmatsec[0][1],btmatsec[1][2],BestTime,btmatsec[0][2])
    #print(ptmatsec[0][1],ptmatsec[1][2],PesTime,ptmatsec[0][2])
       
    outfile.write("{},{},{},{},{}\n".format(RName,timestamp,OptTime,BestTime,PesTime))
    outfile.flush() 
    os.fsync(outfile.fileno())
    


# In[60]:


def houston(status,RName):
    
    import requests
    
    slack_token = "xoxb-300357605111-lSK0SxVQs1UfQKBZThBv3cfF"
    
    if status == "initialize":
        text = "GoogleDistanceMatrixAPI-{} Running".format(RName)
    if status == "success":
        text = "GoogleDistanceMatrixAPI-{} Complete".format(RName)
    if status == "fail":
        text = "GoogleDistanceMatrixAPI-{} Failed".format(RName)
    if status == "error":
        text = "GoogleDistanceMatrixAPI-{} Error".format(RName)
    
    channel = "#api_status"
    #Paremeters
    houstonparams = {"token": slack_token, "channel": channel, "as_user": "true", "text": text}

    #Slack message request line
    r1 = requests.get("https://slack.com/api/chat.postMessage?", params=houstonparams)
    r1.raise_for_status()


# In[61]:


def main():
    
    import time 
        
#--------------------------------------------------------------------------------
    
    #USER INPUT - Route Name
    RName = 'TestRoute'
    
    #USER INPUT - Coordinate Points
    point1 = 43.64316, -79.37791, #Origin
    point2 = 43.64311, -79.38056, #R1-1
    point3 = 43.64220, -79.38260, #Destination
        
    #USER INPUT - w and h are equal to the number of coordinate points
    w, h = 3, 3;
    
#--------------------------------------------------------------------------------  
    
    #definition for matrices, 'w' lists, each of 'h' items
    
    #Houston
    houston("initialize",RName)
    
    #Set origins and destinations
    if w == 4:
        origins = [point1,point2,point3,point4]
        destinations = [point1,point2,point3,point4]
    if w == 3:
        origins = [point1,point2,point3]
        destinations = [point1,point2,point3]
    if w == 2:
        origins = [point1,point2]
        destinations = [point1,point2]

#--------------------------------------------------------------------------------
    #USER INPUT
    #Number of rounds - currently set to run all day at 30 second intervals
    # Peak Hour 30 second intervals - rounds = 120
    # 30 second intervals - rounds = 2880
    # 60 second intervals - rounds = 1440
    
    rounds = 120
    interval = 30
#--------------------------------------------------------------------------------    
    
    #Sets counter to zero
    counter = 0
          
    # file date for naming of text file, day month year 
    filedate = time.strftime("%b-%d-%Y")
    
    with open('GDistMatOutput- {0} - {1}.txt' .format(RName, filedate), 'a') as outfile:
    
        outfile.write("{},{},{},{},{}\n".format("Route","Time","Optimistic Time","Best Guess Time","Pessimistic Time"))
    
        while counter < rounds:

            tic = time.time() #counter start       

            times = time.time() * 1000
            times = int(times)
            #reqtime = times + 30000 
            #print(tic)

            reqtime= "now"
            timestamp = time.strftime("%H:%M:%S")
            GDistMat(reqtime, point1, w, h, origins, destinations, RName, timestamp, outfile)

            counter = counter + 1
            #print(counter)

            toc = time.time() #counter end
            delay = (toc - tic) #function delay

            time.sleep(interval - delay)
            
        outfile.write("\n")
    
    outfile.close()
    
    houston("success",RName)
    


# In[63]:


main()

print("Done")

