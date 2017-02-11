from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from numpy import random

def firstname(q,driver):
    #Get on the webpage 
    
    #driver = webdriver.Remote("http://localhost:9515", webdriver.DesiredCapabilities.CHROME.copy())
    driver.get("http://www.namethesaurus.com/Thesaurus/")
    #Extract the elements of interest to be manipulated
    try:
        elem = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"ContentPlaceHolder1_Forename\"]")))
    except:
        print "Fatal Error"
    elem.send_keys(q)
    #Run the search
    driver.find_element_by_xpath("//*[@id=\"ContentPlaceHolder1_Button1\"]").click()
    
    try:
        res = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"ContentPlaceHolder1_LabelHitList\"]/table/tbody")))
    except:
        print "Fatal Error"
        return q
    
    result = res.text
    
    #Post-processing results to make them more useful
    a = result.split('\n')
    a = a[2:len(a)]
    fname = [0]*len(a)
    fscore = [0]*len(a)

    #Separate the name and nameX score
    for i in range(0,len(a)):
        temp = str(a[i])
        temp2 = temp.split()
        fname[i] = temp2[0]
        fscore[i] = temp2[1]
        
    fscore = map(int,fscore)
    fscore = [x - 93 for x in fscore]


    result_fname = []
    
    tf = map(lambda x: x>=0, fscore )
    
    for x in range(0,len(tf)):
        if tf[x]==1:
            result_fname.append(fname[x])
    try:
        result_fname = random.choice(result_fname,1)[0]
    except ValueError:
        print result_fname
        return q
        
    #Return the results
    return(result_fname)

def first_guess(names, n):
    names = names.copy()
    index = random.choice(range(len(names)),n)
    br = webdriver.Firefox()
    for i in index:
        names.loc[i] = firstname(names.loc[i],br)
    br.close()
    return names
