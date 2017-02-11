from numpy import random
def dob_guess(dobs, n):
    dobs = dobs.copy()
    index = random.choice(range(len(dobs)),n, replace = False)
    for i in index:
        s = dobs.loc[i]
        s = s.replace(s[-2:],"01")        
        dobs.loc[i] = s
    return dobs
    
    