from records_generator import records_gen
#Create Scenario 1 Truth DataSet 
#58% White, 17% Hispanic, 16% Black, 7% AAPI, 1 % Native, 1% Other
race_weights = [0.58, 0.17, 0.16, 0.07, 0.01, 0.01]
n = 10

res = records_gen(race_weights, n)

filename='/tmp/shelve.out'

pickle.dump()

with open("boys_names.pkl","wb") as filename:
    pickle.dump(boys_names, filename)
    
with open("girls_names.pkl","wb") as filename:
    pickle.dump(girls_names, filename)
    
with open("male_names.pkl","wb") as filename:
    pickle.dump(male_names, filename)
    
with open("female_names.pkl","wb") as filename:
    pickle.dump(female_names, filename)
    
with open("hispanic_surnames.pkl","wb") as filename:
    pickle.dump(hispanic_surnames, filename)
    
with open("black_surnames.pkl","wb") as filename:
    pickle.dump(black_surnames, filename)
    
with open("native_surnames.pkl","wb") as filename:
    pickle.dump(native_surnames, filename)
    
with open("other_surnames.pkl","wb") as filename:
    pickle.dump(other_surnames, filename)
      
with open("white_surnames.pkl","wb") as filename:
    pickle.dump(white_surnames, filename)

with open("aapi_surnames.pkl","wb") as filename:
    pickle.dump(aapi_surnames, filename)

with open("address_master.pkl","wb") as filename:
    pickle.dump(address_master, filename)


import os
os.chdir('C:\\Users\\571727\\Documents\\Projects\\USDA Name Matching\\CNAAT\\Python Scripts')
import pandas as pd
from records_generator import records_gen
#Create Scenario 1 Truth DataSet 
#58% White, 17% Hispanic, 16% Black, 7% AAPI, 1 % Native, 1% Other
race_weights = [0.58, 0.17, 0.16, 0.07, 0.01, 0.01]
snap_final = pd.read_csv("snap1.csv", index_col = 0)
school_final = pd.read_csv("school1.csv", index_col = 0)
messy_index = [x!=x for x in school_final["Guardian First"]]
n = sum(messy_index)
res = records_gen(race_weights, n)
school_final.loc[messy_index, "Street"] = list(res["Street"])
school_final.loc[messy_index, "Guardian First"] = list(res["Guardian First"])
school_final.to_csv("school1.csv")
snap_final.to_csv("snap1.csv")

#School 2
snap_final = pd.read_csv("snap2.csv", index_col = 0)
school_final = pd.read_csv("school2.csv", index_col = 0)
messy_index = [x!=x for x in school_final["Guardian First"]]
n = sum(messy_index)
res = records_gen(race_weights, n)
school_final.loc[messy_index, "Street"] = list(res["Street"])
school_final.loc[messy_index, "Guardian First"] = list(res["Guardian First"])
school_final.to_csv("school2.csv")
snap_final.to_csv("snap2.csv")
