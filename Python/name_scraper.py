import pandas as pd
import urllib2

#Create the SNAP Data or "Truth" for Scenario 1: The relevant parameters are as follows
#1. Demographics - 77% White,  
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#Scrape the most popular Boys names
url = 'http://names.mongabay.com/baby_names/boys-2014.html'
response = opener.open(url)

boys_names = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
boys_names.columns = ["Rank","Name","Population",""]
boys_names = boys_names.ix[1:len(boys_names)]
boys_names = boys_names[["Rank","Name","Population"]].reset_index(drop = True)

#Scrape the most popular Girls' names
url = 'http://names.mongabay.com//baby_names/girls-2014.html'
response = opener.open(url)

girls_names = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
girls_names.columns = ["Rank","Name","Population",""]
girls_names = girls_names.ix[1:len(girls_names)]
girls_names = girls_names[["Rank","Name","Population"]].reset_index(drop = True)

#Scrape Names on Ethnicities - White
url = 'http://names.mongabay.com/data/white.html'
response = opener.open(url)
white_surnames = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
white_surnames.columns = ["Surname","Pop_Sub","Rank_Sub","Percent_Sub","Rank", "Population"]
white_surnames = white_surnames.ix[1:len(white_surnames)].reset_index(drop = True)

#Scrape Names on Ethnicities - Black
url = 'http://names.mongabay.com/data/black.html'
response = opener.open(url)
black_surnames = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
black_surnames.columns = ["Surname","Pop_Sub","Rank_Sub","Percent_Sub","Rank", "Population"]
black_surnames = black_surnames.ix[1:len(black_surnames)].reset_index(drop = True)

#Scrape Names on Ethnicities - Hispanic
url = 'http://names.mongabay.com/data/hispanic.html'
response = opener.open(url)
hispanic_surnames = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
hispanic_surnames.columns = ["Surname","Pop_Sub","Rank_Sub","Percent_Sub","Rank", "Population"]
hispanic_surnames = hispanic_surnames.ix[1:len(hispanic_surnames)].reset_index(drop = True)

#Scrape Names on Ethnicities - Asian
url = 'http://names.mongabay.com/data/asian_pacific_islander.html'
response = opener.open(url)
aapi_surnames = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
aapi_surnames.columns = ["Surname","Pop_Sub","Rank_Sub","Percent_Sub","Rank", "Population"]
aapi_surnames = aapi_surnames.ix[1:len(aapi_surnames)].reset_index(drop = True)

#Scrape Names on Ethnicities - Native
url = 'http://names.mongabay.com/data/indians.html'
response = opener.open(url)
native_surnames = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
native_surnames.columns = ["Surname","Pop_Sub","Rank_Sub","Percent_Sub","Rank", "Population"]
native_surnames = native_surnames.ix[1:len(native_surnames)].reset_index(drop = True)

#Scrape Names on Ethnicities - Other
url = 'http://names.mongabay.com/data/two_race.html'
response = opener.open(url)
other_surnames = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
other_surnames.columns = ["Surname","Pop_Sub","Rank_Sub","Percent_Sub","Rank", "Population"]
other_surnames = other_surnames.ix[1:len(other_surnames)].reset_index(drop = True)


#Save all the data
#import pickle
#with open("C:\\Users\\571727\\Documents\\Projects\\USDA Name Matching\\CNAAT\\Data\\boys_names.p","wb") as f:
#    pickle.dump(boys_names, f)
#with open("C:\\Users\\571727\\Documents\\Projects\\USDA Name Matching\\CNAAT\\Data\\girls_names.p","wb") as f:
#    pickle.dump(girls_names, f)

url = 'http://names.mongabay.com/male_names.htm'
response = opener.open(url)

male_names = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
male_names.columns = ["Name","Percent_Freq","Population","Rank"]
male_names = male_names.ix[1:len(boys_names)]
male_names = male_names[["Rank","Name","Population"]].reset_index(drop = True)

url = 'http://names.mongabay.com/female_names.htm'
response = opener.open(url)

female_names = pd.read_html(response.read(), attrs={"id":"myTable"})[0]
female_names.columns = ["Name","Percent_Freq","Population","Rank"]
female_names = female_names.ix[1:len(boys_names)]
female_names = female_names[["Rank","Name","Population"]].reset_index(drop = True)


    