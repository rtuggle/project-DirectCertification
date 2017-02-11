import pandas as pd
import fuzzy 
import Levenshtein as ln
from datetime import datetime
from functools import partial
from numpy import argmax


def soundex_score(string1,string2):
    string1 = str(string1)
    string2 = str(string2)

    matched = 0
    for i in range(1,11):
        soundex = fuzzy.Soundex(i)
        if(soundex(string1) == soundex(string2)):
            matched = i
    score = (matched/10.)*1.0
    return score

def metaphone_score(string1, string2):
    string1 = str(string1)
    string2 = str(string2)

    metaphone = fuzzy.DMetaphone()
    res1 = map(str,metaphone(string1))
    res2 = map(str,metaphone(string2))
    
    if(res1[0] == res2[0]):
        return(1.0)
    if((res1[0] in res2[0]) | (res2[0] in res1[0])):
        return(0.75)
    if((res1[1] != "None") & (res2[1] != "None")):
        if(res1[1]==res2[1]):
            return 0.5
        if((res1[1] in res2[1]) | (res2[1] in res1[1])):
            return(0.4)
    return 0.0

def nysiis_score(string1, string2):
    string1 = str(string1)
    string2 = str(string2)

    if(fuzzy.nysiis(string1) == fuzzy.nysiis(string2)):
        return(0.9)
    return 0.0
    
def leven_score(string1, string2):
    string1 = str(string1)
    string2 = str(string2)

    dist = ln.distance(string1,string2)
    score = 1 - (float(dist)/max(len(string1),len(string2)))
    return score

def jw_score(string1, string2):
    string1 = str(string1)
    string2 = str(string2)

    score = ln.jaro_winkler(string1,string2)
    return score
    
def dob_score(dob1,dob2):
    dob1 = str(dob1)
    dob2 = str(dob2)

    try:    
        d1 = datetime.strptime(dob1,  "%Y-%m-%d")
        d2 = datetime.strptime(dob2,  "%Y-%m-%d")
    except ValueError:
        return 0.0
    
    daydiff = abs((d1-d2).days)
    if(daydiff>=30):
        return 0.0
    score = 1-float(daydiff/30)
    return score

def exact_match(string1, string2):
    if(string1 == string2):
        return 1.0
    else:
        return 0.0


def matchmaker(snap,school, fname_func, lname_func, dob_func, add_data, threshold):
    f_dict = {"exact":exact_match,
              "dob_magic": dob_score,
              "jaro_winkler":jw_score,
              "leven":leven_score,
              "nysiis":nysiis_score,
              "metaphone":metaphone_score,
              "soundex":soundex_score
              }
    results = pd.DataFrame()
    counter = 0
    
    for row, obj in school.iterrows():
        f_name_school = obj["First Name"]
        l_name_school = obj["Last Name"]
        dob_school = obj["DOB"]        
        gf_name_school = obj["Guardian First"]
        gl_name_school = obj["Guardian Last"]
        street_school = obj["Street"]
        add_data_school = gf_name_school+gl_name_school+street_school
        
        
        part_func_fname = partial(f_dict.get(fname_func),f_name_school)
        part_func_lname = partial(f_dict.get(lname_func),l_name_school)
        part_func_dob = partial(f_dict.get(dob_func),dob_school)
        part_func_adddata = partial(f_dict.get("exact"),add_data_school)
        
        fname_score = (snap["First Name"].apply(str).apply(part_func_fname))*25
        lname_score = (snap["Last Name"].apply(str).apply(part_func_lname))*25
        d_score = (snap["DOB"].apply(str).apply(part_func_dob))*25
        
        if(add_data == True):
            add_data_score = ((snap["Guardian First"]+snap["Guardian Last"]+snap["Street"]).apply(str).apply(part_func_adddata))*25
        else:
            add_data_score = pd.Series(([25]*len(d_score)))
        
        combined_score = fname_score+lname_score+d_score+add_data_score
        
        predict = argmax(combined_score)
        if(combined_score[predict] < threshold):
            predict = -1
        
        results.loc[counter, "School Row"] = int(row)
        results.loc[counter, "SNAP Row"] = int(predict)
        counter = counter+1          
    return results
                        
            
        
    
    
    
    
    
    

