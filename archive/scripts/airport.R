library(dplyr)
library(ggplot2)
library(scales)

library(readxl)
library(openxlsx)

planes <- read_xlsx("../raw/commercialenplanements.xlsx")
cities_raw <- read.csv("../../static/canada-us-visits/us_normalized_trips_daily.csv")

head(planes)
head(cities)

msa_list <- unique(cities_raw$METRO)

msa_list


# left join with the city name from (planes) being in the msa vector list we have (cities)

planes <- planes %>%
  mutate(
    in_msa = sapply(City, function(city) {
      any(grepl(city, msa_list, ignore.case = TRUE))
    }),
    MSA = sapply(City, function(city) {
      match <- msa_list[grepl(city, msa_list, ignore.case = TRUE)]
      if (length(match) > 0) match[1] else NA_character_
    })
  )

planes %>%
  select(City, ST, `Airport Name`, MSA, in_msa)

