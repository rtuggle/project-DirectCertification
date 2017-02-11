import pandas as pd 
from numpy import random,percentile
from datetime import datetime, timedelta
import pickle 

def records_gen(race_weights,n):
    #Unpickle the data 
    with open("boys_names.pkl","rb") as filename:
        boys_names = pickle.load(filename)
    with open("girls_names.pkl","rb") as filename:
        girls_names = pickle.load(filename)    
    with open("male_names.pkl","rb") as filename:
        male_names = pickle.load(filename)    
    with open("female_names.pkl","rb") as filename:
        female_names = pickle.load(filename)    
    with open("hispanic_surnames.pkl","rb") as filename:
        hispanic_surnames = pickle.load(filename)    
    with open("black_surnames.pkl","rb") as filename:
        black_surnames = pickle.load(filename)    
    with open("native_surnames.pkl","rb") as filename:
        native_surnames = pickle.load(filename)    
    with open("other_surnames.pkl","rb") as filename:
        other_surnames = pickle.load(filename)     
    with open("white_surnames.pkl","rb") as filename:
        white_surnames = pickle.load(filename)  
    with open("aapi_surnames.pkl","rb") as filename:
        aapi_surnames = pickle.load(filename)  
    with open("address_master.pkl","rb") as filename:
        address_master = pickle.load(filename)  


    race_choices = ["White", "Hispanic", "Black", "AAPI", "Native", "Other"]
    race_selections = random.choice(race_choices, n, p = race_weights)
    results = pd.DataFrame()
    counter = 0
    
    stime = datetime(1998,01,01)
    etime = datetime(2010,12,21)
    
    for selected in race_selections: 
        #Give Birth 
        gender = random.choice(["Boy","Girl"],1, p = [0.5,0.5])[0]
        
        if(gender == "Girl"):
            sampler = girls_names
        else:
            sampler = boys_names
          
        sampler["Population"] = sampler["Population"].apply(int)
        
        #Create guardian sampler 
        guardian_gender = random.choice(["Male","Female"],1, p = [0.25,0.75])[0]
        if(guardian_gender == "Male"):
            guardian_sampler = male_names
        else:
            guardian_sampler = female_names
        
        guardian_sampler["Population"] = guardian_sampler["Population"].apply(int)
         
        
        #Ascribe Subset for first name and surname
        if(selected == "Other"):
            fname_bounds = percentile(sampler["Population"],[0,1])
            gfname_bounds = percentile(guardian_sampler["Population"],[0,1])
            surname_sampler = other_surnames
        elif(selected == "Native"):
            fname_bounds = percentile(sampler["Population"],[1,2])
            gfname_bounds = percentile(guardian_sampler["Population"],[1,2])
            surname_sampler = native_surnames
        elif(selected == "AAPI"):
            fname_bounds = percentile(sampler["Population"],[2,9])
            gfname_bounds = percentile(guardian_sampler["Population"],[2,9])
            surname_sampler = aapi_surnames
        elif(selected == "Black"):
            fname_bounds = percentile(sampler["Population"],[9,25])
            gfname_bounds = percentile(guardian_sampler["Population"],[9,25])            
            surname_sampler = black_surnames
        elif(selected == "Hispanic"):
            fname_bounds = percentile(sampler["Population"],[25,42])
            gfname_bounds = percentile(guardian_sampler["Population"],[25,42])
            surname_sampler = hispanic_surnames
        elif(selected == "White"):
            fname_bounds = percentile(sampler["Population"],[42,100])
            gfname_bounds = percentile(guardian_sampler["Population"],[25,42])
            surname_sampler = white_surnames

        #First Name Creator        
        subset = sampler.ix[(sampler["Population"] <= fname_bounds[1]) & (sampler["Population"] >=fname_bounds[0])]
        first_name = random.choice(list(subset["Name"]),1,p = list(subset["Population"]/sum(subset["Population"])))[0]
        
        #Guardians FIrst Name Creator
        guardian_subset = guardian_sampler.ix[(guardian_sampler["Population"] <= gfname_bounds[1]) & (guardian_sampler["Population"] >= gfname_bounds[0])] 
        guardian_first = random.choice(list(guardian_subset["Name"]),1,p = list(guardian_subset["Population"]/sum(guardian_subset["Population"])))[0]
        
        
        #Last Name Creator        
        surname_sampler["Percent_Sub"] = surname_sampler["Percent_Sub"].apply(str).apply(str.strip, args = "%").apply(float)
        bounds = percentile(surname_sampler["Percent_Sub"],[80,100])
        surname_subset = surname_sampler.ix[(surname_sampler["Percent_Sub"] <= bounds[1]) & (surname_sampler["Percent_Sub"] >=bounds[0])].reset_index(drop = True)
        surname_subset["Pop_Sub"] = surname_subset["Pop_Sub"].apply(int)        
        last_name = random.choice(list(surname_subset["Surname"]),1,p = list(surname_subset["Pop_Sub"]/sum(surname_subset["Pop_Sub"])))[0]
        
        hyphen_choice = random.choice(["Y","N"],1, p = [0.06,0.94])[0]
        if(hyphen_choice == "Y"):
            second_last = random.choice(list(surname_subset["Surname"]),1,p = list(surname_subset["Pop_Sub"]/sum(surname_subset["Pop_Sub"])))[0]
            last_name = last_name+"-"+second_last
            
        
        #Guardians Last Name
        guardian_l = random.choice(["Same","Different"],1, p = [0.70,0.3])[0]
        if(guardian_l == "Same"):
            guardian_last = last_name
        else:
            guardian_last = random.choice(list(surname_subset["Surname"]),1,p = list(surname_subset["Pop_Sub"]/sum(surname_subset["Pop_Sub"])))[0]
        
        dob = (stime + timedelta(days = int(((etime-stime).days)*random.random()))).strftime("%Y-%m-%d")
        address = address_master.sample(1)       
        street = address["StreetAddress"].item()
        city = address["City"].item()
        state = address["State"].item()
        zipcode = address["ZipCode"].item()
        
        results.loc[counter,"First Name"] = first_name
        results.loc[counter,"Last Name"] = last_name
        results.loc[counter,"DOB"] = dob
        results.loc[counter,"Gender"] = gender
        results.loc[counter,"Selected Race"] = selected
        results.loc[counter,"Guardian First"] = guardian_first
        results.loc[counter,"Guardian Last"] = guardian_last
        results.loc[counter,"Street"] = street
        results.loc[counter,"City"] = city
        results.loc[counter,"State"] = state
        results.loc[counter,"Zip"] = zipcode
        counter = counter+1

    return(results)
