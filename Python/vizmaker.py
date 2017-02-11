import pandas as pd
from matching_engine import matchmaker
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def vizmaker(snap,school, school_name, fname_func, lname_func, dob_func, add_data, threshold, threshold_label, filename_prefix):
    filename_prefix = filename_prefix+"_"+school_name+"_"
    print(filename_prefix)    
    predicted = matchmaker(snap, school, fname_func, lname_func, 
                           dob_func, add_data, threshold)
    snap_final = snap
    school_final = school
    
    #Create an indexer for the accurately identified
    comparer = snap_final["SCHOOL_ID"][predicted["SNAP Row"]].reset_index(drop = True)
    indexer = (comparer == predicted["SNAP Row"])

    #Calculate Confusion Matrix Indexers
    true_positive_indexer = school_final["ELIGIBLE"] & indexer
    false_positive_indexer = (school_final["ELIGIBLE"] != True) & (predicted["SNAP Row"] >= 0)
    true_negative_indexer = (school_final["ELIGIBLE"] != True) & (predicted["SNAP Row"] < 0)
    false_negative_indexer = school_final["ELIGIBLE"] & (predicted["SNAP Row"] < 0)
    #Calculate Metrics
    precision = float(sum(true_positive_indexer))/(sum(true_positive_indexer)+sum(false_positive_indexer))
    match_rate = float(sum(true_positive_indexer))/len(snap_final)
    
    #Subset School Data
    true_positive_df = school_final.ix[true_positive_indexer]
    false_positive_df = school_final.ix[false_positive_indexer]
    true_negative_df = school_final.ix[true_negative_indexer]
    false_negative_df = school_final.ix[false_negative_indexer]
    
    #Results Page:

    match_techniques_dict = {"exact":"Exact Match",
                             "jaro_winkler":"Jaro Winkler Similarity",
                             "leven":"Levenshtein distance",
                             "nysiis":"NYSIIS System",
                             "metaphone":"Metaphone",
                             "soundex":"Soundex",
                             "dob_magic":"Approximation"}
    fig = plt.figure(1)
    line = school_name+" Match Results: Precision %.2f%%      Match Rate: %.2f%%" 
    fig.suptitle(line%(round(precision*100,2), round(match_rate*100,2)), fontsize=20, fontweight='bold')
    
    #Summary of school 
    ax = plt.subplot(221)
    ax.set_title("School Summary", fontsize=16, fontweight='bold')
    ax.text(0, 8, 'School District: '+school_name, fontsize=15, fontweight='bold')
    line = "Number of Enrolled Students: %d"
    ax.text(0, 7, line%(len(school_final)), fontsize=12)
    line = "Number of Eligible Students:  %d"
    ax.text(0, 6, line%(len(snap_final)), fontsize=12)
    ax.text(0, 5, "Match Techniques:", fontsize=15, fontweight='bold')
    line = "First Name: %s"
    ax.text(1, 4, line%(match_techniques_dict.get(fname_func)), fontsize=12)
    line = "Last Name: %s"
    ax.text(1, 3, line%(match_techniques_dict.get(lname_func)), fontsize=12)
    line = "DOB: %s"
    ax.text(1, 2, line%(match_techniques_dict.get(dob_func)), fontsize=12)
    line = "Additional Data Included: %s" 
    ax.text(1, 1, line%(add_data), fontsize=12)
    line = "Sensitivity Threshold: %s" 
    ax.text(1, 0, line%(threshold_label), fontsize=12)
    ax.axis([0, 10, 0, 10])
    ax.axis("off")
    
    #Create the Gender Barplot
    df_viz = pd.concat([true_positive_df["Gender"].value_counts(),true_negative_df["Gender"].value_counts(), false_positive_df["Gender"].value_counts(),false_negative_df["Gender"].value_counts()],axis = 1) 
    df_viz.columns = ["True Positives", "True Negatives","False Positives","False Negatives" ]
    df_viz =  df_viz.div(df_viz.sum(axis=1), axis=0)
    
    ax = plt.subplot(223)
    df_viz.plot.barh(stacked = True, ax = ax)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    ax.set_title("Gender Breakdown", fontsize=16, fontweight='bold')
    
    #Create the Race Barplot
    df_viz = pd.concat([true_positive_df["Selected Race"].value_counts(),true_negative_df["Selected Race"].value_counts(), false_positive_df["Selected Race"].value_counts(),false_negative_df["Selected Race"].value_counts()],axis = 1) 
    df_viz.columns = ["True Positives", "True Negatives","False Positives","False Negatives" ]
    df_viz =  df_viz.div(df_viz.sum(axis=1), axis=0)
    
    ax = plt.subplot(224)
    df_viz.plot.barh(stacked = True, ax = ax)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    ax.set_title("Ethnicity Breakdown", fontsize=16, fontweight='bold')
        
    #Create the Confusion Matrix
    ax = plt.subplot(222)
    data = [[sum(true_positive_indexer), (sum(false_negative_indexer)+sum(snap["SCHOOL_ID"] < 0))], [sum(false_positive_indexer),sum(true_negative_indexer)]]
    collabel = ("Outcome: Records Matched","Outcome: Records Not Matched")
    rowlabel = ("Actual: SNAP Records","Actual: Not SNAP Records")
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=data,colLabels=collabel,rowLabels = rowlabel, loc='center')
    the_table.set_fontsize(14)
    ax.set_title("Confusion Matrix", fontsize=16, fontweight='bold')
    fig.set_size_inches(15,11.25)
    filename = filename_prefix+"results.png"
    fig.savefig(filename, dpi=96)
    plt.clf()
    
    #Output the False Positives
    selected_samples = predicted[false_positive_indexer]
    schoollabels = ["First Name", 'Last Name', 'DOB', 'Gender', "ELIGIBLE","ERROR TYPE"]
    snaplabels = schoollabels[0:3]
    school = school_final.loc[selected_samples["School Row"],schoollabels].reset_index(drop = True)
    snap = snap_final.loc[selected_samples["SNAP Row"],snaplabels].reset_index(drop = True)
    res = pd.concat([school,pd.Series(["Incorrectly Matched With -->"]*len(selected_samples),name = "Divider"),snap], axis = 1)
    filename = filename_prefix+"false_positive_data.csv"    
    res.to_csv(filename, index = False)
    fp = res.copy(deep = True)
    
    #Output the False Negatives
    selected_samples = predicted[false_negative_indexer]
    schoollabels = ["First Name", 'Last Name', 'DOB', 'Gender', "ELIGIBLE","ERROR TYPE"]
    snaplabels = schoollabels[0:3]
    school = school_final.loc[selected_samples["School Row"],schoollabels].reset_index(drop = True)
    snap = snap_final.loc[selected_samples["School Row"],snaplabels].reset_index(drop = True)
    res = pd.concat([school,pd.Series(["Should have matched-->"]*len(selected_samples),name = "Divider"),snap], axis = 1)
    filename = filename_prefix+"false_negative_data.csv"    
    res.to_csv(filename, index = False)
    fn  = res.copy(deep = True)
    return(fp,fn)