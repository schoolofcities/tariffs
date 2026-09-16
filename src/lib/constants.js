export const GRADUATED_COLORS = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];

export const TARIFF_LIST = ["All goods subject to tariffs (after Sep 29, 2026)", "All goods subject to tariffs (prior to Sep 29, 2026)", "Section 338 – Total", "Section 338 – Tariffed", "Section 338 – Excluded", "Section 338 – Dairy", "Section 338 – Alcohol", "Section 338 – Motor vehicles", "Automobiles", "Aluminum", "Steel", "Copper", "Lumber (before Oct 14)", "Lumber (after Oct 14)", "Trucks (Medium & Heavy Duty Vehicles)", "Energy and natural resources", "Non-CUSMA-Compliant"];
// ScenAfter  = 'after September 29'  ∪ nonCUSMA
// ScenBefore = 'before September 29' ∪ nonCUSMA
// The bare 'after September 29' / 'before September 29' columns are still emitted by
// the notebooks but are NOT scenario totals — they exclude non-CUSMA exposure
// entirely. Do not point the dropdown at them.
//
// Section 338 is now three columns instead of one:
//   S338_Tar = codes actually subject to the Section 338 tariff
//   S338_Exc = codes carved out / exempted from it
//   S338_Tot = Tariffed + Excluded (the full Section 338 universe)
// S338_Tot equals the union of Dairy ∪ Alcohol ∪ Motor exactly, so those three
// sub-categories are subsets of it — the selections are not additive.
// S338_Exc is defined here but deliberately left out of TARIFF_LIST: mapping
// "exposure" to goods that are exempt from the tariff reads as misleading. Add the
// "Section 338 – Excluded" label to TARIFF_LIST if you do want it selectable.
export const TARIFF_NAME_CODES = {
    "All goods subject to tariffs (after Sep 29, 2026)": 'ScenAfter',
    "All goods subject to tariffs (prior to Sep 29, 2026)": 'ScenBefore',
    "Section 338 – Total": 'S338_Tot',
    "Section 338 – Tariffed": 'S338_Tar',
    "Section 338 – Excluded": 'S338_Exc',
    "Section 338 – Dairy": "Dairy",
    "Section 338 – Alcohol": "Alcohol",
    "Section 338 – Motor vehicles": 'Motor',
    "Automobiles": 'Auto',
    "Aluminum": 'Alum',
    "Steel": 'Steel',
    "Copper": 'Cop',
    "Lumber (before Oct 14)": 'LumOld',
    "Lumber (after Oct 14)": 'LumNew',
    "Trucks (Medium & Heavy Duty Vehicles)": 'MHDV',
    "Energy and natural resources": 'Ene',
    "Non-CUSMA-Compliant": 'CUSMA',
};

export const TARIFF_IMPACT_CODES_PCT = {
    'Business': "_1",
    'EmployeeWork': "_2",
    'EmployeeHome': "_3",
};

export const TARIFF_IMPACT_CODES_COUNT = {
    'Business': "_B",
    'EmployeeWork': "_E",
    'EmployeeHome': "_C",
};

export const TARIFF_IMPACT_TEXT = {
    'Total_1': "Estimated % and number of businesses directly exposed to all types of US Administration's Tariffs on Canada",
    'Auto_1': "Estimated % and number of businesses directly exposed to US Administration's Automobile Tariffs on Canada",
    'Alum_1': "Estimated % and number of businesses directly exposed to US Administration's Aluminum Tariffs on Canada",
    'Steel_1': "Estimated % and number of businesses directly exposed to US Administration's Steel Tariffs on Canada",
    'Cop_1': "Estimated % and number of businesses directly exposed to US Administration's Copper Tariffs on Canada",
    'LumOld_1': "Estimated % and number of businesses directly exposed to US Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
    'LumNew_1': "Estimated % and number of businesses directly exposed to US Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
    'MHDV_1': "Estimated % and number of businesses directly exposed to US Administration's MHDV Tariffs on Canada",
    'ScenBefore_1': "Estimated % and number of businesses directly exposed to all tariffs in effect prior to September 29, 2026",
    'ScenAfter_1': "Estimated % and number of businesses directly exposed to all tariffs in effect after September 29, 2026",
    'S338_Tot_1': "Estimated % and number of businesses directly exposed to Section 338 tariffs (tariffed and excluded goods combined)",
    'S338_Tar_1': "Estimated % and number of businesses directly exposed to goods subject to Section 338 tariffs",
    'S338_Exc_1': "Estimated % and number of businesses producing goods excluded from Section 338 tariffs",
    'Dairy_1': "Estimated % and number of businesses directly exposed to US Administration's Dairy Tariffs on Canada",
    'Alcohol_1': "Estimated % and number of businesses directly exposed to US Administration's Alcohol Tariffs on Canada",
    'Motor_1': "Estimated % and number of businesses directly exposed to US Administration's Motor Vehicle Tariffs on Canada",
    'Ene_1': "Estimated % and number of businesses directly exposed to US Administration's Energy and natural resources tariffs on Canada",
    'CUSMA_1': "Estimated % and number of businesses directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",

    'Total_2': "Estimated % and number of employees (by work location) directly exposed to all types of US Administration's Tariffs on Canada",
    'Auto_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Automobile Tariffs on Canada",
    'Alum_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Aluminum Tariffs on Canada",
    'Steel_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Steel Tariffs on Canada",
    'Cop_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Copper Tariffs on Canada",
    'LumOld_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
    'LumNew_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
    'MHDV_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's MHDV Tariffs on Canada",
    'ScenBefore_2': "Estimated % and number of employees (by work location) directly exposed to all tariffs in effect prior to September 29, 2026",
    'ScenAfter_2': "Estimated % and number of employees (by work location) directly exposed to all tariffs in effect after September 29, 2026",
    'S338_Tot_2': "Estimated % and number of employees (by work location) directly exposed to Section 338 tariffs (tariffed and excluded goods combined)",
    'S338_Tar_2': "Estimated % and number of employees (by work location) directly exposed to goods subject to Section 338 tariffs",
    'S338_Exc_2': "Estimated % and number of employees (by work location) producing goods excluded from Section 338 tariffs",
    'Dairy_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Dairy Tariffs on Canada",
    'Alcohol_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Alcohol Tariffs on Canada",
    'Motor_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Motor Vehicle Tariffs on Canada",
    'Ene_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's Energy and natural resources tariffs on Canada",
    'CUSMA_2': "Estimated % and number of employees (by work location) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",

    'Total_3': "Estimated % and number of employees (by primary residence) directly exposed to all types of US Administration's Tariffs on Canada",
    'Auto_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Automobile Tariffs on Canada",
    'Alum_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Aluminum Tariffs on Canada",
    'Steel_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Steel Tariffs on Canada",
    'Cop_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Copper Tariffs on Canada",
    'LumOld_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
    'LumNew_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
    'MHDV_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's MHDV Tariffs on Canada",
    'ScenBefore_3': "Estimated % and number of employees (by primary residence) directly exposed to all tariffs in effect prior to September 29, 2026",
    'ScenAfter_3': "Estimated % and number of employees (by primary residence) directly exposed to all tariffs in effect after September 29, 2026",
    'S338_Tot_3': "Estimated % and number of employees (by primary residence) directly exposed to Section 338 tariffs (tariffed and excluded goods combined)",
    'S338_Tar_3': "Estimated % and number of employees (by primary residence) directly exposed to goods subject to Section 338 tariffs",
    'S338_Exc_3': "Estimated % and number of employees (by primary residence) producing goods excluded from Section 338 tariffs",
    'Dairy_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Dairy Tariffs on Canada",
    'Alcohol_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Alcohol Tariffs on Canada",
    'Motor_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Motor Vehicle Tariffs on Canada",
    'Ene_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's Energy and natural resources tariffs on Canada",
    'CUSMA_3': "Estimated % and number of employees (by primary residence) directly exposed to US Administration's non-CUSMA Compliant Tariffs on Canada",
};

// NOTE: Dairy_*, Alcohol_*, and Motor_* break values below are ESTIMATES based on
// ADA-level percentiles from tariff-impacts-ada-data_8_27_2026.xlsx (not real CMA
// aggregates, unlike the other rows in this file). Dairy/Alcohol are sized similarly
// to Cop/MHDV; Motor is sized closer to Auto/Steel. Re-check these once Motor/Dairy/
// Alcohol are running through the CMA-level pipeline and swap in real values.
//
// NOTE: ScenBefore_* and ScenAfter_* breaks are PROVISIONAL. They are copied from
// Total_*/CUSMA_* because those are the only columns on a comparable scale — the
// scenarios now include non-CUSMA exposure, so the old 'before/after' breaks
// (calibrated on ~26.6k businesses nationally vs ~70k+ now) would saturate at the
// top colour almost everywhere. Recompute from CMA percentiles after the pipeline
// re-run and replace these.
//
// NOTE: S338_Tot_* / S338_Tar_* breaks are carried over from the old single
// 'Section 338' column, which was itself calibrated against the much broader
// before/after distribution — wrong for Section 338 even then. S338_Tot now equals
// Dairy ∪ Alcohol ∪ Motor, and Motor dominates it (521 of 676 codes), so these
// should really be recalibrated closer to the Motor scale. S338_Exc_* is sized down
// hard since it's only 24 HS codes. All of these need recomputing from real
// percentiles — treat them as placeholders.

export const TARIFF_CMA_BREAKS_PCT = {
    "Total_1": [5.5, 7, 8.5, 11],
    "Auto_1": [0.75, 1, 1.25, 1.5],
    "Alum_1": [1.25, 1.75, 2.25, 3],
    "Steel_1": [1.25, 1.75, 2.25, 2.75],
    "Cop_1": [0.4, 0.5, 0.65, 0.85],
    "LumOld_1": [0.5, 0.65, 0.7, 0.9],
    "LumNew_1": [0.5, 0.65, 0.7, 0.9],
    "MHDV_1": [0.4, 0.5, 0.65, 0.85],
    "ScenBefore_1": [5, 6.5, 8, 10.5],
    "ScenAfter_1": [5.5, 7, 8.5, 11],
    "S338_Tot_1": [1.75, 3.75, 6.75, 9.25],
    "S338_Tar_1": [1.5, 3.5, 6.5, 9],
    "S338_Exc_1": [0.1, 0.25, 0.5, 1],
    "Dairy_1": [0.4, 0.7, 0.95, 1.5],
    "Alcohol_1": [0.4, 0.75, 1, 1.75],
    "Motor_1": [1.5, 3.5, 6.5, 9],
    "Ene_1": [0.9, 1.1, 1.3, 1.75],
    "CUSMA_1": [5.5, 6.5, 8, 11],

    "Total_2": [7.5, 9.5, 12.5, 15],
    "Auto_2": [1, 2.25, 3.5, 6],
    "Alum_2": [2, 3, 5, 8],
    "Steel_2": [2.5, 4, 5.5, 8],
    "Cop_2": [0.25, 0.5, 0.85, 1.75],
    "LumOld_2": [0.65, 1.25, 1.75, 2.25],
    "LumNew_2": [0.65, 1.25, 1.75, 2.25],
    "MHDV_2": [0.25, 0.5, 0.85, 1.75],
    "ScenBefore_2": [6, 8, 10.5, 13.5],
    "ScenAfter_2": [7.5, 9.5, 12.5, 15],
    "S338_Tot_2": [0.9, 3.25, 8.25, 11.75],
    "S338_Tar_2": [0.7, 3, 8, 11.5],
    "S338_Exc_2": [0.05, 0.2, 0.5, 1.25],
    "Dairy_2": [0.1, 0.5, 0.9, 2.75],
    "Alcohol_2": [0.15, 0.6, 1.3, 5],
    "Motor_2": [0.7, 3, 8, 11.5],
    "Ene_2": [1.75, 2.5, 3, 4.75],
    "CUSMA_2": [6, 8, 10.5, 13.5],

    "Total_3": [6, 7.5, 9, 13],
    "Auto_3": [0.5, 0.9, 1.4, 2],
    "Alum_3": [1.25, 1.5, 2.5, 4],
    "Steel_3": [1, 1.75, 2.25, 3.25],
    "Cop_3": [0.1, 0.175, 0.225, 0.4],
    "LumOld_3": [0.25, 0.35, 0.45, 0.75],
    "LumNew_3": [0.25, 0.35, 0.45, 0.75],
    "MHDV_3": [0.1, 0.175, 0.225, 0.4],
    "ScenBefore_3": [5.5, 6.75, 8, 11],
    "ScenAfter_3": [6, 7.5, 9, 13],
    "S338_Tot_3": [4.5, 6.25, 8.25, 10.75],
    "S338_Tar_3": [4.25, 6, 8, 10.5],
    "S338_Exc_3": [0.1, 0.25, 0.5, 1],
    "Dairy_3": [0.35, 0.5, 0.7, 1],
    "Alcohol_3": [0.4, 0.6, 1, 1.5],
    "Motor_3": [4.25, 6, 8, 10.5],
    "Ene_3": [0.75, 1, 1.25, 1.75],
    "CUSMA_3": [5.5, 6.75, 8, 11],
};

export const TARIFF_CMA_BREAKS_COUNT_LINEAR = {
    "Total_B": [2500, 5000, 7500, 10000],
    "Auto_B": [250, 500, 750, 1000],
    "Alum_B": [1250, 2500, 3750, 5000],
    "Steel_B": [500, 1000, 1500, 2000],
    "Cop_B": [125, 250, 375, 500],
    "LumOld_B": [125, 250, 375, 500],
    "LumNew_B": [125, 250, 375, 500],
    "MHDV_B": [125, 250, 375, 500],
    "ScenBefore_B": [2500, 5000, 7500, 10000],
    "ScenAfter_B": [2500, 5000, 7500, 10000],
    "S338_Tot_B": [800, 1600, 2600, 4200],
    "S338_Tar_B": [750, 1500, 2500, 4000],
    "S338_Exc_B": [50, 100, 200, 400],
    "Dairy_B": [125, 250, 375, 500],
    "Alcohol_B": [125, 250, 375, 500],
    "Motor_B": [750, 1500, 2500, 4000],
    "Ene_B": [250, 500, 750, 1000],
    "CUSMA_B": [2500, 5000, 7500, 10000],

    "Total_E": [50000, 100000, 150000, 200000],
    "Auto_E": [12500, 25000, 37500, 50000],
    "Alum_E": [25000, 50000, 75000, 100000],
    "Steel_E": [20000, 40000, 60000, 80000],
    "Cop_E": [2500, 5000, 7500, 10000],
    "LumOld_E": [1250, 2500, 3750, 5000],
    "LumNew_E": [5000, 10000, 15000, 20000],
    "MHDV_E": [2500, 5000, 7500, 10000],
    "ScenBefore_E": [50000, 100000, 150000, 200000],
    "ScenAfter_E": [50000, 100000, 150000, 200000],
    "S338_Tot_E": [16000, 32000, 52000, 72000],
    "S338_Tar_E": [15000, 30000, 50000, 70000],
    "S338_Exc_E": [1000, 2500, 5000, 10000],
    "Dairy_E": [2500, 5000, 7500, 10000],
    "Alcohol_E": [2500, 5000, 10000, 15000],
    "Motor_E": [15000, 30000, 50000, 70000],
    "Ene_E": [10000, 20000, 30000, 40000],
    "CUSMA_E": [50000, 100000, 150000, 200000],

    "Total_C": [125000, 250000, 375000, 500000],
    "Auto_C": [25000, 50000, 75000, 100000],
    "Alum_C": [25000, 50000, 75000, 100000],
    "Steel_C": [25000, 50000, 75000, 100000],
    "Cop_C": [2500, 5000, 7500, 10000],
    "LumOld_C": [2500, 5000, 7500, 10000],
    "LumNew_C": [7500, 15000, 22500, 30000],
    "MHDV_C": [2500, 5000, 7500, 10000],
    "ScenBefore_C": [125000, 250000, 375000, 500000],
    "ScenAfter_C": [125000, 250000, 375000, 500000],
    "S338_Tot_C": [42000, 78000, 115000, 155000],
    "S338_Tar_C": [40000, 75000, 110000, 150000],
    "S338_Exc_C": [2500, 5000, 10000, 20000],
    "Dairy_C": [2500, 5000, 7500, 10000],
    "Alcohol_C": [2500, 5000, 10000, 15000],
    "Motor_C": [40000, 75000, 110000, 150000],
    "Ene_C": [12500, 25000, 37500, 50000],
    "CUSMA_C": [125000, 250000, 375000, 500000],
};

export const TARIFF_CMA_BREAKS_COUNT_POW = {
    "Total_B": [100, 1000, 5000, 10000],
    "Auto_B": [10, 100, 500, 1000],
    "Alum_B": [50, 500, 2000, 5000],
    "Steel_B": [20, 200, 1000, 2000],
    "Cop_B": [5, 50, 200, 500],
    "LumOld_B": [5, 50, 200, 500],
    "LumNew_B": [5, 50, 200, 500],
    "MHDV_B": [5, 50, 200, 500],
    "ScenBefore_B": [100, 1000, 5000, 10000],
    "ScenAfter_B": [100, 1000, 5000, 10000],
    "S338_Tot_B": [25, 250, 1000, 3000],
    "S338_Tar_B": [25, 250, 1000, 3000],
    "S338_Exc_B": [5, 25, 100, 300],
    "Dairy_B": [5, 50, 200, 500],
    "Alcohol_B": [5, 50, 200, 500],
    "Motor_B": [25, 250, 1000, 3000],
    "Ene_B": [10, 100, 500, 1000],
    "CUSMA_B": [100, 1000, 5000, 10000],

    "Total_E": [2000, 20000, 100000, 200000],
    "Auto_E": [500, 5000, 20000, 50000],
    "Alum_E": [1000, 10000, 50000, 100000],
    "Steel_E": [1000, 10000, 50000, 100000],
    "Cop_E": [1000, 10000, 50000, 100000],
    "LumOld_E": [50, 500, 2000, 5000],
    "LumNew_E": [50, 500, 2000, 5000],
    "MHDV_E": [1000, 10000, 50000, 100000],
    "ScenBefore_E": [2000, 20000, 100000, 200000],
    "ScenAfter_E": [2000, 20000, 100000, 200000],
    "S338_Tot_E": [500, 5000, 30000, 60000],
    "S338_Tar_E": [500, 5000, 30000, 60000],
    "S338_Exc_E": [50, 500, 2000, 5000],
    "Dairy_E": [50, 500, 2000, 5000],
    "Alcohol_E": [100, 1000, 5000, 10000],
    "Motor_E": [500, 5000, 30000, 60000],
    "Ene_E": [500, 5000, 20000, 50000],
    "CUSMA_E": [2000, 20000, 100000, 200000],

    "Total_C": [5000, 50000, 200000, 500000],
    "Auto_C": [1000, 10000, 50000, 100000],
    "Alum_C": [1000, 10000, 50000, 100000],
    "Steel_C": [1000, 10000, 50000, 100000],
    "Cop_C": [100, 1000, 5000, 10000],
    "LumOld_C": [100, 1000, 5000, 10000],
    "LumNew_C": [100, 1000, 5000, 10000],
    "MHDV_C": [100, 1000, 5000, 10000],
    "ScenBefore_C": [5000, 50000, 200000, 500000],
    "ScenAfter_C": [5000, 50000, 200000, 500000],
    "S338_Tot_C": [500, 5000, 30000, 60000],
    "S338_Tar_C": [500, 5000, 30000, 60000],
    "S338_Exc_C": [100, 1000, 5000, 10000],
    "Dairy_C": [100, 1000, 5000, 10000],
    "Alcohol_C": [200, 2000, 8000, 15000],
    "Motor_C": [500, 5000, 30000, 60000],
    "Ene_C": [500, 5000, 20000, 50000],
    "CUSMA_C": [5000, 50000, 200000, 500000],
};