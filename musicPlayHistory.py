# Description: Fetch the last 50 song from a radio station.
# input: None
# output: A csv file with three columns (UNIX_GMT_Seconds_Timestamp, Artist, Song)
# output file format: musicPlayHistory_[RADIO_STATION]_GMT_DATE.csv

import requests
import time
import pprint
from xml.etree import ElementTree
import csv

#USER MODIFIABLE
DEBUG = False
#DEBUG = True
RADIO_STATION = "KCCNFM"

#DO NOT MODIFY
SONG_INFO = 3
ARTIST = 0
SONG = 1
TIME = 2
USECS_TO_SECS = 1000

#Reference
#http://playerservices.streamtheworld.com/public/nowplaying?mountName=KCCNFM&numberToFetch=15&eventType=track&request.preventCache=1399063172201

#Fetches the last 50 songs
BASEURL = "http://playerservices.streamtheworld.com/public/nowplaying?mountName={}&eventType=track".format(RADIO_STATION)

seed_resp = requests.get(BASEURL)   #type is 'request.models.Response'
text = seed_resp.text               #type is 'unicode' 
doc = ElementTree.fromstring(text)  #type is 'class xml.etree.ElementTree.Element'>

if DEBUG:
    for index, unit in enumerate(doc):
        if len(doc[index]) == SONG_INFO:
            print "Artist:{}".format(doc[index][ARTIST].text)
            print "Song:{}".format(doc[index][SONG].text)
            print "Time:{}".format(doc[index][TIME].text)
            print "---"
    
    # When ads play then there will be one entry instead of three
    for index, unit in enumerate(doc):
        if len(doc[index]) == 1:
            print "Ad:{}".format(doc[index][0].text)

gmtTime = time.strftime("%Y-%m-%d_%H%M" ,time.gmtime())

songFileName = "musicPlayHistory_{}_{}.csv".format(RADIO_STATION, gmtTime)
csvSongFile = csv.writer(open(songFileName, "wb")) 

#Change the time stamp to seconds
#Insert play history into csv file
for index, unit in enumerate(doc):
    if len(doc[index]) == SONG_INFO:
        localTime = int(doc[index][TIME].text)/USECS_TO_SECS
        csvSongFile.writerow([localTime, doc[index][ARTIST].text, doc[index][SONG].text])


#Returned data sample
'''
<nowplaying-info-list>
    <nowplaying-info mountName="KCCNFM" timestamp="1399318662" type="track">
        <property name="track_artist_name">
            <![CDATA[ Jimmy Weeks Project ]]>
        </property>
        <property name="cue_title">
            <![CDATA[ Home Grown ]]>
        </property>
        <property name="cue_time_start">
            <![CDATA[ 1399318662000 ]]>
        </property>
    </nowplaying-info>
    <nowplaying-info mountName="KCCNFM" timestamp="1399318447" type="track">
        <property name="track_artist_name">
            <![CDATA[ Anuhea ]]>
        </property>
        <property name="cue_title">
            <![CDATA[ Higher Than The Clouds ]]>
        </property>
        <property name="cue_time_start">
            <![CDATA[ 1399318447000 ]]>
        </property>
    </nowplaying-info>
'''
