#import required packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from numpy import random

#This function takes as input a query string and webdriver, gets onto a SEO 
# website tools that provide a list of generated typos, scrapes the results 
# and sends it back to the calling function
def miskey(q,driver):
    #Get on the website
    driver.get("http://tools.seobook.com/spelling/keywords-typos.cgi")
    #Extract the elements of the page to be manipulated
    opt1 = driver.find_element_by_name("missed_key")
    opt2 = driver.find_element_by_name("inserted_key")
    opt3 = driver.find_element_by_name("double_letters")
    query = driver.find_element_by_name("user_input")
    #Got the xpath from a extension
    gen = driver.find_element_by_xpath("/html/body/div[@id='primer']/div[@id='binder']/div[@id='training']/div[@id='content']/form/input")
    
    #Fill out the fields and search
    query.send_keys(q)
    opt1.send_keys(Keys.SPACE)
    opt2.send_keys(Keys.SPACE)    
    opt3.send_keys(Keys.SPACE)
    gen.click()
    
    #Extract the results
    try:
        res = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[@id='primer']/div[@id='binder']/div[@id='training']/div[@id='content']/tt/textarea")))
    except:
        print "Fatal Error"
    res = str(res.text).rsplit(" ")
    
    #Postprocessing to remove results with digits
    def contains_digits(d):
        _digits = re.compile('\d')    
        return bool(_digits.search(d))
    
    tf = map(contains_digits,res)
    
    result = []
    for x in range(0,len(tf)):
        if tf[x]==0:
            result.append(res[x])
            
    #send back the list of strings with typo errors
    return random.choice(result,1)[0]

def first_typo(names, n):
    names = names.copy()
    index = random.choice(range(len(names)),n, replace = False)
    br = webdriver.Firefox()
    for i in index:
        names.loc[i] = miskey(names.loc[i],br)
    br.close()
    return names

def last_typo(names, n):
    names = names.copy()
    index = random.choice(range(len(names)),n, replace = False)
    br = webdriver.Firefox()
    for i in index:
        names.loc[i] = miskey(names.loc[i],br)
    br.close()
    return names

def dob_switch(st):
    s = st.split("-")
    st = s[0]+"-"+s[2]+"-"+s[1]
    return st

def dob_typo(dobs, n):
    dobs = dobs.copy()
    index = random.choice(range(len(dobs)),n, replace = False)
    for i in index:
        dobs.loc[i] = dob_switch(dobs.loc[i])
    return dobs

    
    
    

