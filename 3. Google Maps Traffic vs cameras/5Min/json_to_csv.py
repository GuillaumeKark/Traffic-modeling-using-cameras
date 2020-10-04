# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 15:48:02 2020
@author: Guillaume Karklins
Comment: This file queries Google Map the the required interval for a number of defined requests.
Careful with the input values as this is a paying service.
"""
#define used packages
import json
import urllib.request as urllib2
import time
import datetime
import pandas as pd


#WARNING: Remove Cloud key before sharing!
KEY = ""
INTERVAL = 30
TOTAL_REQUESTS = 10


#define variables and API url pre-defined on origins/destination
api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metrics&origins=40.896662,-72.396820&destinations=40.896611,-72.400175&mode=driving&departure_time=now&key=" + KEY
stack = []
output_list = []
nb_requests = 0

#time request loop
start_time = time.time()
for i in range(TOTAL_REQUESTS):
    #iterate every 30 seconds
    time.sleep(start_time + i*INTERVAL - time.time())
    
    #json_request
    json_request = json.load(urllib2.urlopen(api_url))
    
    #recover dictionnary inside json
    rows = json_request["rows"][0]["elements"][0]
    
    #add time to dictionnary
    date = datetime.datetime.now()
    rows.update({'time':date})
    
    #append to stack list
    stack.append(rows)
    
    #print for user the status
    nb_requests = nb_requests+1
    print("Request done " + str(i+1) + "/" + str(TOTAL_REQUESTS))
    

#keep useful information
for i in stack:
    distance = i["distance"]["value"]
    base_duration = i["duration"]["value"]
    traffic = i["duration_in_traffic"]["value"]
    dateh = i["time"]
    status = i["status"]
    whole = [distance,base_duration,traffic,dateh,status]
    output_list.append(whole)
 
#export list to csv
output = pd.DataFrame(output_list, columns=["distance","base_duration","duration_in_traffic","time","status"])
output.to_csv("output.csv",index=False)
