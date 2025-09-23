export const GRADUATED_COLORS = ["#f1c500", "#fb921f", "#f3603e", "#d73256", "#ab1368"];

export const TARIFF_LIST = ["All goods subject to tariffs", "Automobiles", "Aluminum", "Steel", "Copper", "Lumber", "Energy and natural resources", "Non-CUSMA-Compliant"];

export const TARIFF_NAME_CODES = {
    "All goods subject to tariffs": 'Total', 
    "Automobiles": 'Auto', 
    "Aluminum": 'Alum', 
    "Steel": 'Steel', 
    "Copper": 'Cop', 
    "Lumber": 'Lum', 
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

export const TARIFF_CMA_BREAKS_PCT = {
    "Total_1": [1.25, 2.5, 5, 10],
    "Auto_1": [0.25, 0.5, 1, 2],
    "Alum_1": [0.25, 0.5, 1, 2],
    "Steel_1": [0.25, 0.5, 1, 2],
    "Cop_1": [0.25, 0.5, 1, 2],
    "Lum_1": [0.25, 0.5, 1, 2],
    "Ene_1": [0.25, 0.5, 1, 2],
    "CUSMA_1": [1.25, 2.5, 5, 10],
    "Total_2": [1.25, 2.5, 5, 10],
    "Auto_2": [0.625, 1.25, 2.5, 5],
    "Alum_2": [0.625, 1.25, 2.5, 5],
    "Steel_2": [0.625, 1.25, 2.5, 5],
    "Cop_2": [0.25, 0.5, 1, 2],
    "Lum_2": [0.25, 0.5, 1, 2],
    "Ene_2": [0.625, 1.25, 2.5, 5],
    "CUSMA_2": [1.25, 2.5, 5, 10],
    "Total_3": [1.25, 2.5, 5, 10],
    "Auto_3": [0.25, 0.5, 1, 2],
    "Alum_3": [0.625, 1.25, 2.5, 5],
    "Steel_3": [0.25, 0.5, 1, 2],
    "Cop_3": [0.25, 0.5, 1, 2],
    "Lum_3": [0.25, 0.5, 1, 2],
    "Ene_3": [0.25, 0.5, 1, 2],
    "CUSMA_3": [1.25, 2.5, 5, 10],
};

export const TARIFF_CMA_BREAKS_COUNT_LINEAR = {
    "Total_B": [2500, 5000, 7500, 10000],
    "Auto_B": [250, 500, 750, 1000],
    "Alum_B": [1250, 2500, 3750, 5000],
    "Steel_B": [500, 1000, 1500, 2000],
    "Cop_B": [125, 250, 375, 500],
    "Lum_B": [125, 250, 375, 500],
    "Ene_B": [250, 500, 750, 1000],
    "CUSMA_B": [2500, 5000, 7500, 10000],
    "Total_E": [50000, 100000, 150000, 200000],
    "Auto_E": [12500, 25000, 37500, 50000],
    "Alum_E": [25000, 50000, 75000, 100000],
    "Steel_E": [25000, 50000, 75000, 100000],
    "Cop_E": [25000, 50000, 75000, 100000],
    "Lum_E": [1250, 2500, 3750, 5000],
    "Ene_E": [12500, 25000, 37500, 50000],
    "CUSMA_E": [50000, 100000, 150000, 200000],
    "Total_C": [125000, 250000, 375000, 500000],
    "Auto_C": [25000, 50000, 75000, 100000],
    "Alum_C": [25000, 50000, 75000, 100000],
    "Steel_C": [25000, 50000, 75000, 100000],
    "Cop_C": [2500, 5000, 7500, 10000],
    "Lum_C": [2500, 5000, 7500, 10000],
    "Ene_C": [12500, 25000, 37500, 50000],
    "CUSMA_C": [125000, 250000, 375000, 500000],
};

export const TARIFF_CMA_BREAKS_COUNT_POW = {
    "Total_B": [100, 1000, 5000, 10000],
    "Auto_B": [10, 100, 500, 1000],
    "Alum_B": [50, 500, 2000, 5000],
    "Steel_B": [20, 200, 1000, 2000],
    "Cop_B": [5, 50, 200, 500],
    "Lum_B": [5, 50, 200, 500],
    "Ene_B": [10, 100, 500, 1000],
    "CUSMA_B": [100, 1000, 5000, 10000],
    "Total_E": [2000, 20000, 100000, 200000],
    "Auto_E": [500, 5000, 20000, 50000],
    "Alum_E": [1000, 10000, 50000, 100000],
    "Steel_E": [1000, 10000, 50000, 100000],
    "Cop_E": [1000, 10000, 50000, 100000],
    "Lum_E": [50, 500, 2000, 5000],
    "Ene_E": [500, 5000, 20000, 50000],
    "CUSMA_E": [2000, 20000, 100000, 200000],
    "Total_C": [5000, 50000, 200000, 500000],
    "Auto_C": [1000, 10000, 50000, 100000],
    "Alum_C": [1000, 10000, 50000, 100000],
    "Steel_C": [1000, 10000, 50000, 100000],
    "Cop_C": [100, 1000, 5000, 10000],
    "Lum_C": [100, 1000, 5000, 10000],
    "Ene_C": [500, 5000, 20000, 50000],
    "CUSMA_C": [5000, 50000, 200000, 500000],
};