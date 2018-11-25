import json
import datetime
import urllib2
import time
from random import randint
allgames =json.load(urllib2.urlopen('http://api.steampowered.com/ISteamApps/GetAppList/v0001/'))
#Get input 
appid=-1
price=-1
now = datetime.datetime.now()
saledatesstart=["0210","0620","1028","1115","1220"]
saledatesend=["0225","0705","1105","1130","1230"]
sett=[]
bigpubs = {'2K':61, 'Rockstar Games':17, 'Electronic Arts':65, 'Square Enix':116, 'Ubisoft':119, 'CAPCOM Co., Ltd.':52, 'CD PROJEKT RED':5, 'SEGA':154, 'Bethesda Softworks':59, 'Activision':219,'BANDAI NAMCO Entertainment':62,'XSEED Games':26,'Telltale Games':31,'Paradox Interactive':55,'Team17 Digital Ltd':40}
for t in allgames["applist"]["apps"]["app"]:
  if(randint(0, 1000)==69):
    appid=t["appid"]
    data = json.load(urllib2.urlopen('https://store.steampowered.com/api/appdetails?appids='+str(appid)))
    #Pull price out of data
    if "data" in data[str(appid)]:
      if data[str(appid)]["data"]["type"] == "game":
        dataToAddToSet=[]
        dataToAddToSet.append(appid)
        if "price_overview" in data[str(appid)]["data"]:
          dataToAddToSet.append(data[str(appid)]["data"]["price_overview"]["initial"])
        #If its not on sale, this is same as iniital
          dataToAddToSet.append(data[str(appid)]["data"]["price_overview"]["discount_percent"])
        else:
          dataToAddToSet.append(0)
          dataToAddToSet.append(0)
        #CHANGE TO HOW MANY GAMES THEYVE PUBLISHED FROM 0-8
        if(data[str(appid)]["data"]["publishers"][0]) in bigpubs:
          if bigpubs[str(data[str(appid)]["data"]["publishers"][0])]>100:
            dataToAddToSet.append(0)
          elif bigpubs[str(data[str(appid)]["data"]["publishers"][0])]>60:
            dataToAddToSet.append(2)
          elif bigpubs[str(data[str(appid)]["data"]["publishers"][0])]>40:
            dataToAddToSet.append(4)
          elif bigpubs[str(data[str(appid)]["data"]["publishers"][0])]>20:
            dataToAddToSet.append(6)
        else:
          dataToAddToSet.append(4)
      #Handle "Coming soon"
        releaseDate=data[str(appid)]["data"]["release_date"]["date"].split(', ')
        if len(releaseDate)>1:
          releaseDate=int(releaseDate[1])
          if now.year - releaseDate>=10:
            dataToAddToSet.append(8)
          elif now.year -releaseDate >=8:
            dataToAddToSet.append(7)
          elif now.year -releaseDate >=6:
            dataToAddToSet.append(6)
          elif now.year -releaseDate>=4:
            dataToAddToSet.append(5)
          elif now.year -releaseDate >=2:
            dataToAddToSet.append(4)
          elif now.year -releaseDate ==1:
            dataToAddToSet.append(3)
          else: 
            dataToAddToSet.append(2)
        else:
          dataToAddToSet.append(0)
        if "metacritic" in data[str(appid)]["data"]:
          mScore= data[str(appid)]["data"]["metacritic"]["score"]
          if mScore<=20:
            dataToAddToSet.append(8)
          elif mScore <=40:
            dataToAddToSet.append(6)
          elif mScore <=60:
            dataToAddToSet.append(4)
          elif mScore <=80:
            dataToAddToSet.append(2)
          else:
            dataToAddToSet.append(0)
        else:
          dataToAddToSet.append(4)
    #MAYBE save genres
    #print data[str(appid)]["data"]["genres"]
    #fix 
        if "dlc" in data[str(appid)]["data"]:
          dlc= data[str(appid)]["data"]["dlc"]
          mostRecent = 1990
          for x in dlc:
        #check if any are in future/just released 
            dlcData = json.load(urllib2.urlopen('https://store.steampowered.com/api/appdetails?appids='+str(x)))
            dlcDate=dlcData[str(x)]["data"]["release_date"]["date"].split(", ")
            if len(dlcDate)>1:
              dlcDate=int(dlcDate[1])
              if dlcDate > mostRecent:
                mostRecent = dlcDate
          if now.year - mostRecent<0:
            dataToAddToSet.append(8)
          elif (now.year - mostRecent) >0 and (now.year - mostRecent) <=1:
            dataToAddToSet.append(4)
          else:
            dataToAddToSet.append(0) 
        else:
          dataToAddToSet.append(0)
    #Pulls user reviews
        test=json.load(urllib2.urlopen('http://store.steampowered.com/appreviews/'+str(appid)+'?json=1'))
        if test["query_summary"]["review_score_desc"]=="Overwhelmingly Negative":
          dataToAddToSet.append(8)
        elif test["query_summary"]["review_score_desc"]=="Very Negative":
          dataToAddToSet.append(7)
        elif test["query_summary"]["review_score_desc"]=="Negative":
          dataToAddToSet.append(6)
        elif test["query_summary"]["review_score_desc"]=="Mostly Negative":
          dataToAddToSet.append(5)
        elif test["query_summary"]["review_score_desc"]=="Mixed":
          dataToAddToSet.append(4)
        elif test["query_summary"]["review_score_desc"]=="Mostly Positive":
          dataToAddToSet.append(3)
        elif test["query_summary"]["review_score_desc"]=="Positive":
          dataToAddToSet.append(2)
        elif test["query_summary"]["review_score_desc"]=="Very Positive":
          dataToAddToSet.append(1)
        elif test["query_summary"]["review_score_desc"]=="Overwhelmingly Positive":
          dataToAddToSet.append(0)
        else:
          dataToAddToSet.append(4)
    #print test["query_summary"]["review_score_desc"]
    #Use bundles to check if it has a recent sequel, hard to do this right now
    #https://store.steampowered.com/api/packagedetails?packageids=32848
        day=str(now.day)
        if now.day<10:
          day="0"+str(now.day)
        month=str(now.month)
        if now.month<10:
          month="0"+str(now.month)
        date=month+day
        i=0
    #Change this to work for the date they enter!!!!!
        q=False
        while i < len(saledatesstart):
            if date >saledatesstart[i] and date <saledatesend[i]:
              q=True
            i+=1
        if q:
          dataToAddToSet.append(8)
        else:
          dataToAddToSet.append(0)
        sett.append(dataToAddToSet)
for x in sett:
  print(x)
print(len(sett))
