from tkinter import *
import json
import datetime
import numpy
import matplotlib.pyplot as plt
from urllib.request import urlopen
from random import randint


def predict(features, weights):
  z = numpy.dot(features, weights)
  return 1.0 / (1 + numpy.exp(-z))

def classify(preds):
  answer=[]
  for x in preds:
  	#If we are 90% sure it is cancer
  	if x >=.80:
  		answer.append(1)
  	else:
  		answer.append(0)
  return answer

def showResult(gamex, datex):
	allgames =json.load(urlopen('http://api.steampowered.com/ISteamApps/GetAppList/v0001/'))

	appid=-1
	price=-1
	now = datetime.datetime.now()
#black friday(late novemeber), winter(late december) , halloween( late october), summer (late june), lunar new year(early feb)
	saledatesstart=["0210","0620","1028","1115","1220"]
	saledatesend=["0225","0705","1105","1130","1230"]
#Add mini sales 
#add training data for big publishers 
	dataToAddToSet=[]
	bigpubs = {'2K':61, 'Rockstar Games':17, 'Electronic Arts':65, 'Square Enix':116, 'Ubisoft':119, 'CAPCOM Co., Ltd.':52, 'CD PROJEKT RED':5, 'SEGA':154, 'Bethesda Softworks':59, 'Activision':219,'BANDAI NAMCO Entertainment':62,'XSEED Games':26,'Telltale Games':31,'Paradox Interactive':55,'Team17 Digital Ltd':40}
	pred_array = []
	answer_array = []
	labelArray=[]
#total = 0
#if int(lines[2]) > 0:
#  total = total + 1
#if int(lines[1]) > 0:
	for x in allgames["applist"]["apps"]["app"]:
		if str(x["name"])==gamex:
			appid= x["appid"]
			dataToAddToSet.append(x["name"])

	data = json.load(urlopen('https://store.steampowered.com/api/appdetails?appids='+str(appid)))
	if appid!=-1:
   		if "data" in data[str(appid)]:
   			if data[str(appid)]["data"]["type"] == "game":
   				dataToAddToSet.append(appid)
   				if "price_overview" in data[str(appid)]["data"]:
   					dataToAddToSet.append(data[str(appid)]["data"]["price_overview"]["initial"])
   					dataToAddToSet.append(data[str(appid)]["data"]["price_overview"]["discount_percent"])
   				else:
   					dataToAddToSet.append(0)
   					dataToAddToSet.append(0)
   				if(data[str(appid)]["data"]["publishers"][0]) in bigpubs:
   					dataToAddToSet.append(0)
   				else:
   					dataToAddToSet.append(8)
   				releaseDate=data[str(appid)]["data"]["release_date"]["date"].split(', ')
   				if len(releaseDate)>1:
   					releaseDate=int(releaseDate[1])
   					if int(datex) - releaseDate>=10:
   						dataToAddToSet.append(8)
   					elif int(datex) -releaseDate >=8:
   						dataToAddToSet.append(7)
   					elif int(datex) -releaseDate >=6:
   						dataToAddToSet.append(6)
   					elif int(datex) -releaseDate>=4:
   						dataToAddToSet.append(5)
   					elif int(datex) -releaseDate >=2:
   						dataToAddToSet.append(4)
   					elif int(datex) -releaseDate ==1:
   						dataToAddToSet.append(3)
   					else: 
   						dataToAddToSet.append(0)
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
   				if "dlc" in data[str(appid)]["data"]:
   					dlc= data[str(appid)]["data"]["dlc"]
   					mostRecent = 1990
   					for x in dlc:
   						dlcData = json.load(urlopen('https://store.steampowered.com/api/appdetails?appids='+str(x)))
   						dlcDate=dlcData[str(x)]["data"]["release_date"]["date"].split(", ")
   						if len(dlcDate)>1:
   							dlcDate=int(dlcDate[1])
   							if dlcDate > mostRecent:
   								mostRecent = dlcDate
   					if int(datex) - mostRecent<0:
   						dataToAddToSet.append(8)
   					elif int(datex) - mostRecent==1:
   						dataToAddToSet.append(4)
   					else:
   						dataToAddToSet.append(0) 
   				else:
   					dataToAddToSet.append(0)
   				test=json.load(urlopen('http://store.steampowered.com/appreviews/'+str(appid)+'?json=1'))
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
   				day=str(now.day)
   				if now.day<10:
   					day="0"+str(now.day)
   				month=str(now.month)
   				if now.month<10:
   					month="0"+str(now.month)
   				date=month+day
   				i=0
   				q=False
   				while i < len(saledatesstart):
   					if date >saledatesstart[i] and date <saledatesend[i]:
   						q=True
   					i+=1
   				if q:
   					dataToAddToSet.append(8)
   				else:
   					dataToAddToSet.append(0)

   		weights=[2.48304924e+01, 0.00000000e+00, 8.67424242e-02, 9.28030303e-02, 3.78787879e-03, 8.12500000e-02, 0.00000000e+00]
   		temp = dataToAddToSet[1]
   		dataToAddToSet[1] = dataToAddToSet[2]
   		dataToAddToSet[2] = temp
   		prob=predict(dataToAddToSet[3::],weights)
   		pred_array.append(prob)
   		dataToAddToSet = []
	counter = 0
	answer_array = classify(pred_array)
	for items in answer_array:
		if items == 1:
			counter = counter + 1
	correct=[1.0, 0.6112244656079482, 1.0, 1.0, 1.0, 0.5861582283280572, 1.0, 1.0, 1.0, 1.0, 1.0, 0.739463473275115, 1.0, 1.0, 0.739463473275115, 1.0, 1.0, 1.0, 1.0, 1.0, 0.6272540480391376, 0.6673474163108982, 0.6673474163108982, 0.6673474163108982, 0.771476412711551, 1.0, 1.0, 0.739463473275115, 1.0, 1.0, 0.6303484883596477, 1.0, 1.0, 0.6673474163108982, 1.0, 0.739463473275115, 1.0, 1.0, 0.7224083463904427, 1.0, 1.0, 0.755824917990191, 1.0, 0.6673474163108982, 0.7224083463904427, 1.0, 1.0, 1.0, 1.0, 0.7069634906080505, 1.0, 1.0, 0.7224083463904427, 1.0, 0.7224083463904427, 1.0, 1.0, 1.0, 1.0, 0.739463473275115, 0.739463473275115, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.7705066517264872, 1.0, 0.6919157486866386, 0.6673474163108982, 1.0, 1.0, 0.6112244656079482, 1.0, 0.6673474163108982, 1.0, 1.0, 1.0, 0.739463473275115, 1.0, 0.7548098475464379, 1.0, 1.0, 0.6886765683018528, 1.0, 1.0, 1.0, 0.6919157486866386, 1.0, 0.7224083463904427, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
	incorrect=[]
	fig =plt.figure()
	axis = fig.add_subplot(111)
	axis.scatter([i for i in range(len(correct))], correct, c='g')
	axis.scatter([i for i in range(len(incorrect))], incorrect,  c='r')
	axis.set_ylabel('Predicted probability of going on sale')
	qwop.set(str(prob))
	z.set(gamex)
	plt.axhline(.8, color='black')
	plt.show()
#font = {'weight' : 'bold',
#        'size'   : 6}

#fig, ax = plt.subplots()
#fig.set_title("Features vs Effect they had")
#index = numpy.arange(6)
#bar_width = 0.35
#plt.rc('font', **font)
#opacity = 0.4
#error_config = {'ecolor': '0.3'}


#rects1 = ax.bar(index, dataToAddToSet[3::], bar_width,
#                alpha=opacity, color='b',
#                error_kw=error_config,
#                label='Features')
#ax.set_xlabel('Features')
#ax.set_ylabel('Scores (Higher means effects likelyhood of sale more)')
#ax.set_title('How each factor effected our result')
#ax.set_xticks(index + bar_width / 2)
#ax.set_xticklabels(('Publisher', 'Release Date', 'Metacritic', 'Recent DLC', 'User Reviews','Date'))
#ax.legend()

#fig.tight_layout()
#plt.show()


def sendit():
	text = searchField.get()
	date = dateField.get()
	showResult(text, date)		
	
master = Tk()
z = StringVar()
qwop = StringVar()
gameNames = []
with open("namefinal") as fp:
	line = fp.readline()
	line = line.replace("\n", "")
	gameNames.append(line)
	while line:
		line = fp.readline()
		line = line.replace("\n", "")
		gameNames.append(line)

text1 = Label(master, textvariable=z)
text2 = Label(master, textvariable=qwop)
text1.place(x=200, y = 60)	
text2.place(x=200, y = 120)
newDate = ""
searchLabel = Label(master, text="Game:")
searchLabel.place(x=10, y=30)
gameLabel = Label(master, text="Game:")
gameLabel.place(x=200, y=30)
probLabel = Label(master, text="Probability of sale:")
probLabel.place(x=200, y=90)
dateLabel = Label(master, text="Year to Check:")
dateLabel.place(x=10, y=90)
searchField = Entry(master)
dateField = Entry(master)
searchField.place(x=10, y=60)
dateField.place(x=10, y=120)
searchButton = Button(master, text="Search", command=sendit)
searchButton.place(x=10, y=150)
master.title("Steam Game Price Predictor")
master.geometry("400x300")
mainloop()
