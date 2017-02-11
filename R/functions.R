require(dplyr) 
require(stringdist) 
require(lubridate)

#function: ingest data
fn.dataIngest <- function(source) {
    name <- read.csv(paste(dir, source, sep = ''), stringsAsFactors = FALSE)
}

#function: prep base data 
fn.prepBase <- function(town) {
    if (town == "Careful") {
        source.school <- df.carefultown
        source.snap <- df.carefultown.snap
    } else if (town == "Oops") {
        source.school <- df.oopstown
        source.snap <- df.oopstown.snap
    }
    
    x <- bind_rows(
        select(source.school, -ELIGIBLE, -ERRORS, -ERROR.TYPE) %>%
            mutate(dataset = "School"),
        select(source.snap, -SCHOOL_ID) %>%
            mutate(dataset = "SNAP")
    )
}

#function: prep data to explore unmatched data
fn.prepUnmatched <- function(town) {
    if (town == "Careful") {
        source.school <- df.carefultown
        source.snap <- df.carefultown.snap
        source.falseNegative <- df.falseNegative.carefultown
        source.falsePositive <- df.falsePositive.carefultown
    } else if (town == "Oops") {
        source.school <- df.oopstown
        source.snap <- df.oopstown.snap
        source.falseNegative <- df.falseNegative.oopstown
        source.falsePositive <- df.falsePositive.oopstown
    }
    #query the school records of not eligible, remove the false positives
    school.notEligible <- source.school %>%
        mutate(SCHOOL_ID = X, id = paste(First.Name, Last.Name, DOB)) %>%
        anti_join(source.snap, by = "SCHOOL_ID") %>%
        anti_join(
            mutate(source.falsePositive, id = paste(First.Name, Last.Name, DOB)),
            by = "id"
        ) %>%
        select(-SCHOOL_ID)
    
    #query the school records for not Matched, union with not eligible
    school.unMatched <- source.school %>%
        mutate(id = paste(First.Name, Last.Name, DOB)) %>%
        semi_join(
            mutate(source.falseNegative, id = paste(First.Name, Last.Name, DOB)),
            by = "id") %>%
        bind_rows(school.notEligible) %>%
        select(-id, -ELIGIBLE, -ERRORS, -ERROR.TYPE) %>%
        mutate(dataset = "School")
    
    #query the SNAP records of not enrolled, union with the not matched 
    snap.unMatched <- source.snap %>%
        mutate(id= paste(First.Name, Last.Name, DOB)) %>%
        semi_join(
            mutate(source.falseNegative, id = paste(First.Name.1, Last.Name.1, DOB.1)),
            by = "id") %>%
        bind_rows(
            filter(source.snap, SCHOOL_ID < 0)
            ) %>%
        select(-id, -SCHOOL_ID) %>%
        mutate(dataset = "SNAP")
    
    #combine the records into one data frame
    combined.unMatched <- bind_rows(school.unMatched, snap.unMatched)
    return(combined.unMatched)
} 

#function: count vowels
fn.vowelCount <- function(string){
    x <- length(gregexpr("a|e|i|o|u|y", string, ignore.case = TRUE)[[1]])
    return(x)
}

#function: prep data for graphics
fn.prepGraphics <- function(x) {
    y <- x %>%
        mutate(full.name = paste(First.Name, Last.Name, sep = ''),
               full.string = paste(First.Name, Last.Name, DOB, sep = ''),
               first.char = nchar(First.Name), last.char = nchar(Last.Name),
               full.char = nchar(paste(First.Name, Last.Name, sep = '')),
               hyphen = grepl('-', Last.Name),
               age.years = difftime(Sys.Date(), as.Date(DOB), units = "days") / 365,
               birth.month = month(as.Date(DOB)),
               birth.day = day(as.Date(DOB)),
               id = paste(X, dataset))
    
    #calculate the vowels in the names
    y$full.vowel = sapply(y$full.name, fn.vowelCount)
    y$full.vowel.pct = y$full.vowel / y$full.char
    
    ##calculate string distances
    #split by dataset
    school <- y %>%
        filter(dataset == "School") %>%
        select(id, full.string)

    snap <- y %>%
        filter(dataset == "SNAP") %>%
        select(id, full.string)
    
    #calculate min distances between
    school$dist.min.between <- by(school$full.string, seq_len(nrow(school)), 
                             function(row) min(stringdist(row, snap$full.string, method = 'osa')))
    
    snap$dist.min.between <- by(snap$full.string, seq_len(nrow(snap)), 
                                  function(row) min(stringdist(row, school$full.string, method = 'osa')))
    
    #count matches at min distance
    school$dist.count.between <- by(school, seq_len(nrow(school)), 
                                    function(row) sum(
                                        stringdist(row[["full.string"]], snap$full.string, method = 'osa') == 
                                            row[["dist.min.between"]]))
    
    snap$dist.count.between <- by(snap, seq_len(nrow(snap)), 
                                    function(row) sum(
                                        stringdist(row[["full.string"]], school$full.string, method = 'osa') == 
                                            row[["dist.min.between"]]))
    
    #combine datasets, join back to rest of data
    z <- bind_rows(school, snap) %>%
        select(-full.string) %>%
        right_join(y, by = 'id')
    
    return(z)
}