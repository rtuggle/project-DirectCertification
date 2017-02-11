# Create Scenario 1 
# Demographics #58% White, 17% Hispanic, 16% Black, 7% AAPI, 1 % Native, 1% Other
import os 
os.chdir('/Users/ryantuggle/Repositories/CNAAT/Python Scripts')
import pandas as pd
from records_generator import records_gen
from first_guess import first_guess
from last_guess import last_guess
from dob_guess import dob_guess
from typo import first_typo,last_typo,dob_typo
from both import first_both, last_both

race_weights = [0.58, 0.17, 0.16, 0.07, 0.01, 0.01]

#First Take 375 Kids and Put them on SNAP and School Rolls - ELIGIBLE, ENROLLED
#and no errors
counter = 0
n = 375
res = records_gen(race_weights, n)
snap_final = res.copy()
school_final = res.copy()
#Assign identifiers on both datasets
school_final["ELIGIBLE"] = True
school_final["ERRORS"] = False
school_final["ERROR TYPE"] = "None"

snap_final["SCHOOL_ID"] = range(0,n)
counter = n

#Now take 25 Kids and add in the guessing error
n = 10
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["First Name"] = first_guess(school["First Name"], n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Guessing-First Name"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)
n = 10
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["Last Name"] = last_guess(school["Last Name"], n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Guessing-Last Name"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)
n = 5
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["DOB"] = dob_guess(school["DOB"],n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Guessing-DOB"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)

#Now Take 25 kids and add in the typo error
n = 10
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["First Name"] = first_typo(school["First Name"], n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Typo-First Name"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)
n = 10
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["Last Name"] = last_typo(school["Last Name"], n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Typo-Last Name"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)
n = 5
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["DOB"] = dob_typo(school["DOB"],n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Typo-DOB"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)

#Now Take 10 kids and add in both errors
n = 5
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["First Name"] = first_both(school["First Name"], n)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Guess and Typo-First Name"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)
n = 5
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["Last Name"] = last_both(school["Last Name"], 5)
#Assign Identifiers
school["ELIGIBLE"] = True
school["ERRORS"] = True
school["ERROR TYPE"] = "Guess and Typo-Last Name"
snap["SCHOOL_ID"] = range(counter, (counter+n))
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)


#Now Take 3 Names, make birthday 01 and put them in the school and snap
n = 3
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
school["DOB"] = dob_guess(school["DOB"],3)
#Assign Identifiers

school["ELIGIBLE"] = False
school["ERRORS"] = True
school["ERROR TYPE"]  = "Ambiguity DOB"
snap["SCHOOL_ID"] = (-2)
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)

#Now Take 5 Names, make exact match and put them in the school and snap
n = 5
res = records_gen(race_weights, n)
snap = res.copy()
school = res.copy()
#Assign Identifiers

school["ELIGIBLE"] = False
school["ERRORS"] = True
school["ERROR TYPE"]  = "Ambiguity Exact"
snap["SCHOOL_ID"] = (-2)
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)

#Now take 4 names, make first name guessing&typo error and put them in snap, put original in 
# school
n = 4
res = records_gen(race_weights,n)
school = res.copy()
snap = res.copy()
snap["First Name"] = first_both(snap["First Name"], n)
#Assign Identifiers

school["ELIGIBLE"] = False
school["ERRORS"] = True
school["ERROR TYPE"]  = "Ambiguity First Name"
snap["SCHOOL_ID"] = (-2)
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)

#Now take 3 names, make last name guessing error and put them in snap, put original in 
n = 3
res = records_gen(race_weights,n)
school = res.copy()
snap = res.copy()
snap["Last Name"] = last_both(snap["Last Name"], n)
#Assign Identifiers

school["ELIGIBLE"] = False
school["ERRORS"] = True
school["ERROR TYPE"]  = "Ambiguity Last Name"
snap["SCHOOL_ID"] = (-2)
counter = counter+n
#Append
school_final = school_final.append(school, ignore_index = True)
snap_final = snap_final.append(snap, ignore_index = True)


# Now Put in 460 more kids in school 
n = 460
res = records_gen(race_weights,n)
school = res.copy()
#Assign Identifiers

school["ELIGIBLE"] = False
school["ERRORS"] = False
school["ERROR TYPE"]  = "None"
#Append
school_final = school_final.append(school, ignore_index = True)


#Now put in 10 more kids in SNAP 
n = 10
res = records_gen(race_weights,n)
snap = res.copy()
#Assign Identifiers
snap["SCHOOL_ID"] = (-1)
#Append
snap_final = snap_final.append(snap, ignore_index = True)

#Create a silver bullet 
ambiguity_index = [True if "Ambiguity" in x else False for x in school_final["ERROR TYPE"]]
n = sum(ambiguity_index)
res = records_gen(race_weights, n)
school_final.loc[ambiguity_index,"Street"] = list(res["Street"])
school_final.loc[ambiguity_index, "Guardian First"] = list(res["Guardian First"])

#Remove silver buller powers
from numpy import random
n = 10
silver_bullet_index = random.choice(range(0,375),n)
res = records_gen(race_weights, n)
school_final.loc[silver_bullet_index, "Street"] = list(res["Street"])
school_final.loc[silver_bullet_index, "Guardian First"] = list(res["Guardian First"])


#Change the extra address fields
school_final["City"] = "Cleantown"
snap_final["City"] = "Cleantown"

school_final["State"] = "ST"
snap_final["State"] = "ST"




#Save the data files
school_final.to_csv("school1_small.csv")
snap_final.to_csv("snap1_small.csv")




