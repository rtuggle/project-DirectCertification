require(dplyr)
require(ggplot2)
#source the user defined functions
source('~/Repositories/CNAAT/functions.R')
#source the datasets
source('~/Repositories/CNAAT/dataLoad.R')

##combine data for use in graphics
#base
df.combined.base.carefultown <- fn.prepBase("Careful")
df.combined.base.oopstown <- fn.prepBase("Oops")

#unMatched
df.combined.unMatched.carefultown <- fn.prepUnmatched("Careful")
df.combined.unMatched.oopstown <- fn.prepUnmatched("Oops")

##prep selected data for graphics
town <- "Cleantown"
type <- "Base"
df.graphics <- fn.prepGraphics(df.combined.base.carefultown)

##Plots
#source plots, wait until df.graphics correctly assigned
source('~/Repositories/CNAAT/plots.R')
pl.heritage
pl.age
pl.month
pl.length
pl.length.hyphen
pl.vowel
pl.distance
