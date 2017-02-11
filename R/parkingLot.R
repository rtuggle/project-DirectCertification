cbPalette <- c("#999999", "#56B4E9",  "#E69F00", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
fn.plotHeritage <- function(df, title) {
    total <- length(df$First.Name)
    ggplot(aes(x = Selected.Race, fill = Gender), data = df) +
        geom_bar(stat = "count", position = "dodge") + 
        coord_flip() + 
        ggtitle(paste(title, "by Heritage")) +
        annotate("text", x= 4.5, y= 100, label = paste("Total Records =", total)) +
        scale_fill_manual(values=cbPalette) +
        facet_wrap(~as.factor(dataset))
}

dataset <- c('School', 'SNAP')
val <- c(nrow(school), nrow(snap))
total <- data.frame(dataset, val)

ggplot(aes(x = age.years), data = subset(df.cleantown, !is.na(df.cleantown$age.years))) +
    geom_histogram(binwidth = 1, colour = "#56B4E9", fill = "#999999") +
    ggtitle("Cleantown \n Age Distribution, Students Enrolled")

ggplot(aes(x = as.factor(birth.month)), 
       data =subset(df.cleantown, !is.na(df.cleantown$birth.month))) + 
    geom_bar(colour = "#56B4E9", fill = "white") +
    ggtitle("Cleantown \n Birth Month Distribution, Students Enrolled")

school <- df.cleantown %>%
    select(Selected.Race, Gender, full.char, full.vowel.pct, age.years, birth.month, hyphen) %>%
    mutate(dataset = 'School')

snap <- df.cleantown_SNAP %>%
    select(Selected.Race, Gender, full.char, full.vowel.pct, age.years, birth.month, hyphen) %>%
    mutate(dataset = 'SNAP')

combined <- bind_rows(school, snap)

ggplot(aes(x = as.factor(dataset), y = full.char), data = combined) +
    geom_boxplot()

ggplot(aes(x = as.factor(Selected.Race), y = full.char), data = school) +
    geom_boxplot() +
    geom_jitter(aes(colour = hyphen))

ggplot(aes(x = full.char, y = full.vowel.pct), data = combined) +
    geom_point(aes(colour = dataset), position = "jitter")

ggplot(aes(x = full.char, y = full.vowel.pct), data = school) +
    geom_point(aes(colour = Selected.Race), position = "jitter")

dist <- stringdist("Jones", df.cleantown_SNAP$Last.Name)
minDist <- min(dist)
lenDist <- length(dist[dist == minDist])

test <- stringdist(df.cleantown$Last.Name, df.cleantown_SNAP$Last.Name)
df.cleantown$test <- by(df.cleantown$Last.Name, seq_len(nrow(df.cleantown)), 
                        function(row) min(stringdist(row, df.cleantown_SNAP$Last.Name)))