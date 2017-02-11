import os
os.chdir('/Users/ryantuggle/Repositories/CNAAT/Make Results')
import pandas as pd
from vizmaker import vizmaker

#First Set the Parameters:
fname_func = "exact" # "exact" "jaro_winkler" "leven" "nysiis" "metaphone" "soundex"
lname_func = "exact"# "exact" "jaro_winkler" "leven" "nysiis" "metaphone" "soundex"
dob_func = "exact" # "exact" "dob_magic"
add_data = False
threshold = 90
threshold_label = "High" # "Low" "Medium" "High"
filename_prefix = "Results\\run2"

#Run the vizmaker on Cleantown and Oopstown
snap = pd.read_csv("snap1_small.csv", index_col = 0)
school = pd.read_csv("school1_small.csv", index_col = 0)
school_name = "Carefultown"
(fp1,fn1) = vizmaker(snap,school,school_name,fname_func,lname_func,dob_func,add_data,threshold,threshold_label,filename_prefix)
snap = pd.read_csv("snap2_small.csv", index_col = 0)
school = pd.read_csv("school2_small.csv", index_col = 0)
school_name = "Oopstown"
(fp2,fn2) = vizmaker(snap,school,school_name,fname_func,lname_func,dob_func,add_data,threshold,threshold_label,filename_prefix)

print "False Positive: Cleantown"
print fp1["ERROR TYPE"].value_counts()
print "False Positive: Oopstown"
print fp2["ERROR TYPE"].value_counts()
print "False Negative: Cleantown"
print fn1["ERROR TYPE"].value_counts()
print "False Negative: Oopstown"
print fn2["ERROR TYPE"].value_counts()