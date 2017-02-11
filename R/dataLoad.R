#set directory
dir <- 'Make Results/'

#ingest sources
df.carefultown <- fn.dataIngest('school1_small.csv')
df.carefultown.snap <- fn.dataIngest('snap1_small.csv')
df.oopstown <- fn.dataIngest('school2_small.csv')
df.oopstown.snap<- fn.dataIngest('snap2_small.csv')

#ingest false negatives
df.falseNegative.carefultown <- fn.dataIngest('Results\\run2_Carefultown_false_negative_data.csv')
df.falsePositive.carefultown <- fn.dataIngest('Results\\run2_Carefultown_false_positive_data.csv')
df.falseNegative.oopstown <- fn.dataIngest('Results\\run2_Oopstown_false_negative_data.csv')
df.falsePositive.oopstown <- fn.dataIngest('Results\\run2_Oopstown_false_positive_data.csv')
