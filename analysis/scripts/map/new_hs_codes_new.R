library(dplyr)
library(tidyverse)
library(readxl)
library(openxlsx)
library(stringr)

existing <- read.csv("../raw/tariff-hscodes_noderiv.csv", stringsAsFactors = FALSE)
new_path <- "../raw/july_20_effec_august_19.xlsx"

if ("HS.Code" %in% colnames(existing)) {
  colnames(existing)[colnames(existing) == "HS.Code"] <- "HS Code"
}
existing <- existing %>%
  mutate(`HS Code` = as.character(`HS Code`))

# remove internal duplicate
existing_clean <- existing %>%
  distinct(`HS Code`, Category, .keep_all = TRUE)

cat("Rows after dedup:", nrow(existing_clean), "\n")
cat("Duplicates removed:", nrow(existing) - nrow(existing_clean), "\n")

# ---- Find all rows that have duplicates (same HS Code + same Category) ----
duplicate_groups <- existing %>%
  group_by(`HS Code`, Category) %>%
  filter(n() > 1) %>%
  arrange(`HS Code`, Category) %>%
  ungroup()

# ---- Show all rows in duplicate groups ----
cat("\n===== ALL rows that have duplicates (including the one kept) =====\n")
print(duplicate_groups)

# ---- Show ONLY the extra copies that were removed (9 rows) ----
duplicates_removed <- existing %>%
  group_by(`HS Code`, Category) %>%
  filter(n() > 1) %>%
  slice(-1) %>%   # Keeps rows 2, 3, 4... (drops the first occurrence)
  ungroup()

cat("\n===== The 9 rows that were REMOVED =====\n")
print(duplicates_removed)

## OK NOW WE CONTINUE

sheet_names <- excel_sheets(new_path)

combined_list <- list()

for (sheet_name in sheet_names){
  df <- read_excel(new_path, sheet = sheet_name)
  hs_codes <- df[[1]]
  
  temp_df <- data.frame(
    `HS Code` = hs_codes,
    Category = str_to_title(sheet_name),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )
  
  combined_list[[sheet_name]] <- temp_df
}

new_data <- bind_rows(combined_list)

combined_df <- bind_rows(existing_clean, new_data)

combined_df <- combined_df %>% filter(!is.na(`HS Code`))

print(head(combined_df))
print(unique(combined_df$Category))

colnames(combined_df)[1] <- "HS Code"

write.csv(combined_df, "../raw/tariff_hs_codes_8_24_2026.csv", row.names = FALSE)

print(head(combined_df, 10))
print(paste("Total rows in master file:", nrow(combined_df)))
print("Unique categories:")
print(unique(combined_df$Category))

duplicates <- combined_df %>%
  filter(!is.na(`HS Code`) & `HS Code` != "") %>%
  group_by(`HS Code`) %>%
  filter(n() > 1) %>%
  arrange(`HS Code`)

print(duplicates)

unique(duplicates$Category)

cat("\nTotal unique HS codes:", n_distinct(combined_df$`HS Code`))
cat("\nTotal rows:", nrow(combined_df))
cat("\nTotal duplicate rows (including originals):", nrow(duplicates))


## ----------- THREE CATEGORIES ----------------

### This one does a new csv file for the 3 new categories of before august 22, after august 22, section 338

# 1. "before August 22": all HS codes from the original noderiv file
before_aug22 <- existing_clean %>%
  select(`HS Code`) %>%
  mutate(Category = "before August 22")

#before_aug22

# 2. "after August 22": all HS codes from the combined set (original + new)
after_aug22 <- combined_df %>%
  select(`HS Code`) %>%
  distinct() %>%
  mutate(Category = "after August 22")

# 3. "Section 338": only HS codes that appear in the new data but NOT in the original
section338 <- new_data %>%
  anti_join(existing_clean, by = "HS Code") %>%
  select(`HS Code`) %>%
  mutate(Category = "Section 338")

section338 %>%
  filter(str_starts(`HS Code`, "87"))

# Combine the original rows with the new category rows
final_df <- bind_rows(
  combined_df,      # original rows (with their own Category values)
  before_aug22,
  after_aug22,
  section338
)

# Remove any potential NA HS codes (should already be clean)
final_df <- final_df %>%
  filter(!is.na(`HS Code`) & `HS Code` != "")

# Write to a new CSV
write.csv(final_df, "../raw/tariff_hs_codes_8_27_2026.csv", row.names = FALSE)

# Optional: Print summary
cat("\n=== New categories added ===\n")
cat("Rows added for 'before August 22':", nrow(before_aug22), "\n")
cat("Rows added for 'after August 22':", nrow(after_aug22), "\n")
cat("Rows added for 'Section 338':", nrow(section338), "\n")
cat("Total rows in final file:", nrow(final_df), "\n")
cat("Unique categories in final file:\n")
print(unique(final_df$Category))
