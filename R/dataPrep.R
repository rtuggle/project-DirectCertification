
dir <- 'Make Results/'
df.carefultown <- fn.dataIngest('school1_small.csv')
df.carefultown.snap <- fn.dataIngest('snap1_small.csv')
df.oopstown <- fn.dataIngest('school2_small.csv')
df.oopstown.snap<- fn.dataIngest('snap2_small.csv')

#ingest false negatives
df.falseNegative.carefultown <- fn.dataIngest('Results\\run2_Cleantown_false_negative_data.csv')
df.falseNegative.oopstown <- fn.dataIngest('Results\\run2_Oopstown_false_negative_data.csv')
