#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
})

# This script converts area-level tariff-affected employee totals
# (ADA-based for work, CSD-based for home) into CT totals via DA bridges.

script_dir <- dirname(normalizePath(commandArgs(trailingOnly = FALSE)[grep("--file=", commandArgs(trailingOnly = FALSE))]))

path_rel <- file.path(script_dir, "..", "..", "data", "dissemination geographies relationship file", "2021_98260004.csv")
path_work_ada <- file.path(script_dir, "trail7.csv")
path_home_csd <- file.path(script_dir, "trail7_csd.csv")

out_work_ct <- file.path(script_dir, "tariff_affected_work_ct.csv")
out_home_ct <- file.path(script_dir, "tariff_affected_home_ct.csv")
out_joined_ct <- file.path(script_dir, "tariff_affected_home_work_ct.csv")

required_paths <- c(path_rel, path_work_ada, path_home_csd)
missing_paths <- required_paths[!file.exists(required_paths)]

if (length(missing_paths) > 0) {
  stop(
    "Missing required input file(s):\n",
    paste0(" - ", missing_paths, collapse = "\n"),
    call. = FALSE
  )
}

crosswalk <- suppressMessages(read_csv(path_rel, show_col_types = FALSE)) %>%
  transmute(
    DADGUID = as.character(DADGUID_ADIDUGD),
    ADADGUID = as.character(ADADGUID_ADAIDUGD),
    CSDDGUID = as.character(CSDDGUID_SDRIDUGD),
    CTDGUID = as.character(CTDGUID_SRIDUGD)
  ) %>%
  filter(!is.na(DADGUID), !is.na(CTDGUID))

work_ada <- suppressMessages(read_csv(path_work_ada, show_col_types = FALSE)) %>%
  transmute(
    ADADGUID = as.character(ADADGUID),
    affected_work = suppressWarnings(as.numeric(Sum))
  ) %>%
  mutate(affected_work = coalesce(affected_work, 0))

home_csd <- suppressMessages(read_csv(path_home_csd, show_col_types = FALSE)) %>%
  transmute(
    CSDDGUID = as.character(CSDDGUID),
    affected_home = suppressWarnings(as.numeric(Sum))
  ) %>%
  mutate(affected_home = coalesce(affected_home, 0))

# Build unique DA->ADA->CT relationships and allocate ADA totals across DAs.
da_ada_ct <- crosswalk %>%
  filter(!is.na(ADADGUID)) %>%
  distinct(DADGUID, ADADGUID, CTDGUID)

ada_da_counts <- da_ada_ct %>%
  group_by(ADADGUID) %>%
  summarise(n_da = n_distinct(DADGUID), .groups = "drop")

work_ct <- da_ada_ct %>%
  left_join(work_ada, by = "ADADGUID") %>%
  left_join(ada_da_counts, by = "ADADGUID") %>%
  mutate(
    affected_work = coalesce(affected_work, 0),
    n_da = if_else(is.na(n_da) | n_da == 0, 1, n_da),
    affected_work_da = affected_work / n_da
  ) %>%
  group_by(CTDGUID) %>%
  summarise(affected_work = sum(affected_work_da, na.rm = TRUE), .groups = "drop")

# Build unique DA->CSD->CT relationships and allocate CSD totals across DAs.
da_csd_ct <- crosswalk %>%
  filter(!is.na(CSDDGUID)) %>%
  distinct(DADGUID, CSDDGUID, CTDGUID)

csd_da_counts <- da_csd_ct %>%
  group_by(CSDDGUID) %>%
  summarise(n_da = n_distinct(DADGUID), .groups = "drop")

home_ct <- da_csd_ct %>%
  left_join(home_csd, by = "CSDDGUID") %>%
  left_join(csd_da_counts, by = "CSDDGUID") %>%
  mutate(
    affected_home = coalesce(affected_home, 0),
    n_da = if_else(is.na(n_da) | n_da == 0, 1, n_da),
    affected_home_da = affected_home / n_da
  ) %>%
  group_by(CTDGUID) %>%
  summarise(affected_home = sum(affected_home_da, na.rm = TRUE), .groups = "drop")

home_work_ct <- full_join(work_ct, home_ct, by = "CTDGUID") %>%
  mutate(
    affected_work = coalesce(affected_work, 0),
    affected_home = coalesce(affected_home, 0),
    affected_total = affected_work + affected_home
  ) %>%
  arrange(CTDGUID)

write_csv(work_ct, out_work_ct)
write_csv(home_ct, out_home_ct)
write_csv(home_work_ct, out_joined_ct)

message("Wrote: ", out_work_ct)
message("Wrote: ", out_home_ct)
message("Wrote: ", out_joined_ct)