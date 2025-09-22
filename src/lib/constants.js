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

export const TARIFF_BREAKS_PCT = {
    "Total_1": [0.05, 0.1, 0.2, 0.3],
    "Auto_1": [0.01, 0.02, 0.03, 0.06],
    "Alum_1": [0.01, 0.02, 0.03, 0.05],
    "Steel_1": [0.01, 0.02, 0.03, 0.07],
    "Cop_1": [0.01, 0.02, 0.03, 0.04],
    "Lum_1": [0.01, 0.02, 0.07, 0.15],
    "Ene_1": [0.01, 0.02, 0.03, 0.08],
    "CUSMA_1": [0.05, 0.1, 0.2, 0.3],
    "Total_2": [0.04, 0.1, 0.2, 0.4],
    "Auto_2": [0.01, 0.04, 0.08, 0.2],
    "Alum_2": [0.01, 0.05, 0.1, 0.2],
    "Steel_2": [0.01, 0.05, 0.1, 0.3],
    "Cop_2": [0.01, 0.02, 0.04, 0.08],
    "Lum_2": [0.01, 0.05, 0.1, 0.2],
    "Ene_2": [0.01, 0.05, 0.1, 0.2],
    "CUSMA_2": [0.05, 0.1, 0.2, 0.4],
    "Total_3": [0.05, 0.1, 0.2, 0.5],
    "Auto_3": [0.01, 0.02, 0.05, 0.2],
    "Alum_3": [0.01, 0.03, 0.07, 0.2],
    "Steel_3": [0.01, 0.05, 0.1, 0.25],
    "Cop_3": [0.01, 0.02, 0.03, 0.04],
    "Lum_3": [0.01, 0.03, 0.08, 0.2],
    "Ene_3": [0.01, 0.03, 0.08, 0.2],
    "CUSMA_3": [0.05, 0.1, 0.2, 0.5],
};

export const TARIFF_BREAKS_COUNT = {
    "Total_B": [10, 50, 100, 200],
    "Auto_B": [5, 10, 20, 50],
    "Alum_B": [5, 10, 20, 50],
    "Steel_B": [5, 10, 20, 50],
    "Cop_B": [2, 5, 10, 20],
    "Lum_B": [2, 5, 10, 20],
    "Ene_B": [5, 10, 20, 50],
    "CUSMA_B": [10, 50, 100, 200],
    "Total_E": [500, 1000, 2500, 5000],
    "Auto_E": [200, 500, 1000, 2000],
    "Alum_E": [200, 500, 1000, 2000],
    "Steel_E": [200, 500, 1000, 2000],
    "Cop_E": [200, 500, 1000, 2000],
    "Lum_E": [25, 100, 250, 500],
    "Ene_E": [50, 100, 250, 1000],
    "CUSMA_E": [500, 1000, 2500, 5000],
    "Total_C": [400, 700, 1000, 1500],
    "Auto_C": [50, 100, 250, 500],
    "Alum_C": [50, 100, 250, 500],
    "Steel_C": [50, 100, 250, 500],
    "Cop_C": [10, 25, 50, 100],
    "Lum_C": [25, 100, 200, 500],
    "Ene_C": [25, 100, 200, 500],
    "CUSMA_C": [400, 700, 1000, 1500],
};
