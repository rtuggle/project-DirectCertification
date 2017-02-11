###Plots
##heritage
#calculate total counts to include in graphic
counts <- data.frame(dataset = c('School', 'SNAP'), 
                     val = c(nrow(filter(df.graphics, dataset == "School")),
                             nrow(filter(df.graphics, dataset == "SNAP"))))
#plot
pl.heritage <- ggplot(aes(x = Selected.Race, fill = Gender), data = df.graphics) +
    geom_bar(stat = "count", position = "dodge") + 
    coord_flip() + 
    ggtitle(paste(town, "\n", type, "Records by Heritage")) +
    geom_text(data = counts, aes(x= 4.5, y= 100, 
                                 label = paste("Total =", val),
                                 fill = NULL)) +
    facet_wrap(~dataset)

##birthdays
#age
pl.age <- ggplot(aes(x = age.years, y = ..density.., colour = dataset), data = df.graphics) +
    geom_freqpoly(binwidth = 1) +
    ggtitle(paste(town,"\n", type, "Age Distributions"))

#month
pl.month <- ggplot(aes(x = birth.month, y = ..density.., colour = dataset), data = df.graphics) + 
    geom_freqpoly(binwidth = 1) +
    ggtitle(paste(town,"\n", type, "Birth Month Distributions"))

##names
#length
pl.length <- ggplot(aes(x = as.factor(dataset), y = full.char), data = df.graphics) +
    geom_boxplot() + 
    #geom_jitter(aes(colour = hyphen)) +
    ggtitle(paste(town,"\n", type, "Name Length Distributions")) 

#length + hyphen
pl.length.hyphen <- ggplot(aes(x = as.factor(dataset), y = full.char), data = df.graphics) +
    geom_boxplot() + 
    geom_jitter(aes(colour = hyphen)) +
    ggtitle(paste(town,"\n", type, "Name Length Distributions")) 

#vowels
pl.vowel <- ggplot(aes(x = full.char, y = full.vowel.pct), data = df.graphics) +
    geom_point(aes(colour = dataset), position = "jitter") +
    ggtitle(paste(town, "\n", type, "Name Characteristics \n Length by Vowel Density"))

##distance 
pl.distance <- ggplot(aes(x = as.factor(dist.min.between), 
                          fill = as.factor(dist.count.between)), 
       data = df.graphics) +
    geom_bar() +
    coord_flip() +
    facet_wrap(~dataset) + 
    ggtitle(paste(town, "\n", type, "String Distances"))


#backup : histogram of length
pl.length.hist <- ggplot(data = df.graphics, aes(x = full.char, y = ..density..)) +
    geom_histogram() +
    facet_wrap(~dataset) + 
    ggtitle(paste(town, "\n", type, "Name Length Distributions"))

