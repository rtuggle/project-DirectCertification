from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from numpy import random

def lastname(q,driver):
    #Get on the webpage 
    
    #driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME.copy())
    driver.get("http://www.namethesaurus.com/Thesaurus/")
    #Extract the elements of interest to be manipulated
    try:
        elem = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"ContentPlaceHolder1_Surname\"]")))
    except:
        print "Fatal Error"
    elem.send_keys(q)
    #Run the search
    driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_ButtonSearch\"]").click()
    
    try:
        res = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"ContentPlaceHolder1_LabelHitList\"]/table/tbody")))
    except:
        print "Fatal Error"
        return q
    
    result = res.text
    
    #Post-processing results to make them more useful
    a = result.split('\n')
    a = a[1:len(a)]
    lname = [0]*len(a)
    lscore = [0]*len(a)

    try:
    # Your code that enter data to database    
    #Separate the name and nameX score
        for i in range(0,len(a)):
            temp = str(a[i])
            temp2 = temp.split(' ')
            lname[i] = temp2[0]
            lscore[i] = temp2[1]
                
        lscore = map(int,lscore)
        lscore = [x - 90 for x in lscore]
        result_lname = []
        tf = map(lambda x: x>=0, lscore )
        
        for x in range(0,len(tf)):
            if tf[x]==1:
                result_lname.append(lname[x])
        
        result_lname = random.choice(result_lname,1)[0]
    except UnicodeEncodeError:
        return(q)        
        pass

    return(result_lname)

def last_guess(names, n):
    names = names.copy()
    index = random.choice(range(len(names)),n, replace = False)
    br = webdriver.Firefox()
    for i in index:
        names.loc[i] = lastname(names.loc[i],br)
    br.close()
    return names.map(str).map(str.upper)
    
