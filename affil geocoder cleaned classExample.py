import csv
import json
import requests
import cPickle as pickle
import sys

##CHANGE THIS to something that makes sense for your own computer
yourPath = 'C:\Users\jbellmas\Documents\Kauffman drive\Code\\'
filename = 'Chai_affil.csv'

##CHANGE THESE to real keys
Key1 = ""
Key2 = ""
Key3 = ""
Key4 = ""
keys = [Key1, Key2, Key3, Key4]
keyNo = 0
#################################################################
print "Starting program..."

##Run at the very end to clean up messy unicode, like "/t/t/tAdele/t/t/t" --> "Adele"
def printer(cL):
    newLine = []
    for x in cL:
        if type(x) == unicode:
            x = x.strip()
        newLine.append(x)
    return newLine

###Open affil list
affilFile = csv.reader(open(filename, 'r'))
line1 = affilFile.next()

savePoint = False
headersNeeded = False

##load savePoint, otherwise manually define the first affilID
try:
    lastSavePoint = pickle.load(open("%s_lastSavePoint_Chai_ClassExample.p"%(yourPath), "rb"))
except:
    lastSavePoint = '109869028'
    savePoint = True
    headersNeeded = True

##Header for our csv file
header = ["affil ID", "affil Standardized Name", "affil Lat", "affil Lng"]

##Keeps track of where we are
counter = 0

with open("affil_geocoding_example.csv","ab") as f:
    w = csv.writer(f)
    
    ##Indicates we're on the first run for this batch, so we need to print a header
    if headersNeeded == True:
        w.writerow(line1+header)
        
    with requests.Session() as session:
        for row in affilFile:
            ourId = row[0]

            ##This gets us to the last place we geocoded, on previous runs of this script (previous days)
            if ourId == lastSavePoint:
                savePoint = True
                continue
            if savePoint == True:
                currentLine = []
                originalName = str(row[1])+" "+str(row[2])+" "+str(row[3])+" "+str(row[4])

                ##Do some basic data cleanup, so that the API can read the target
                locationToGeocode = originalName.replace(", all campuses", "")
                locationToGeocode = locationToGeocode.replace("&", " and ")
                locationToGeocode = locationToGeocode.replace("##", "")
                locationToGeocode = locationToGeocode.replace("#", "number ")
                locationToGeocode = unicode(locationToGeocode, errors='ignore')
                                
                ##Access the api for this target; load the response data into Python
                baseURL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
                endURL = "&key="

                ##This "while True" structure allows us to move onto the next key smoothly, if we hit the ratelimit
                while True:
                    key = keys[keyNo]
                    requestURL = baseURL+locationToGeocode+endURL+key
                    request = session.get(requestURL)
                    d = json.loads(request.text)
                    
                    ##If status != 'OK', the API has returned a bad response
                    if str(d['status']) == 'OK': 

                        ##Grab the lat/long and place name that the API thinks we want
                        lat = d['results'][0]['geometry']['location']['lat']
                        lng = d['results'][0]['geometry']['location']['lng']
                        standardizedName = d['results'][0]['name']
                        
                        ##To be printed later
                        currentLine = [ourId, standardizedName, str(lat), str(lng)]

                    ##This will happen if the API couldn't interpret the original string, and returned no results    
                    elif str(d['status']) == 'ZERO_RESULTS':
                        for x in header:
                            currentLine.append("Can't Geocode")
                            
                    ##Checking out what happens when we hit the rate limit
                    elif str(d['status']) == 'OVER_QUERY_LIMIT':
                        print d
                        keyNo += 1
                        if keyNo < len(keys):
                            print keyNo
                            continue
                        else:
                            f.close()
                            sys.exit()

                    ##This is for all other failed API responses, which only happens rarely (and usually means bad characters)
                    elif str(d['status']) == 'UNKNOWN_ERROR':
                        for x in header:
                            currentLine.append("UNKNOWN_ERROR")
     
                    else:
                        print str(d['status'])
                        print d
                        f.close()
                        sys.exit()

                    ##Add to the counter
                    counter += 1
                    
                    ##A bunch of clunky stuff to deal with bad unicode characters, like accents
                    currentLine = printer(currentLine)
                    ourRow = []
                    ourRow1 = []
                    for x in row:
                        y = unicode(x, errors='ignore')
                        ourRow1.append(y)
                    ourRow = ourRow1+currentLine

                    ##print to csv
                    w.writerow([unicode(s).encode("utf-8") for s in ourRow])

                    ##Saves: last line we printed out, so we know where to start next time
                    pickle.dump(ourId, open("%s_lastSavePoint_Chai_ClassExample.p"%(yourPath), "wb"))

                    ##Just keep track of where we are on the Python output Shell, so you know it's running
                    if counter != 0 and counter%100==0:
                        print counter
                    break
                    
f.close()
sys.exit()
            
                
