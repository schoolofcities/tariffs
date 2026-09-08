import { GRADUATED_COLORS, TARIFF_NAME_CODES } from './constantsv2.js';

export const GRADUATED_SIZES = [5, 9, 15, 24, 34];

// ---------------------------------------------------------------------------
// Layer specs — one entry per tariff CODE (must match TARIFF_NAME_CODES values)
//
// `subject` completes the sentence "Estimated % of <who> directly exposed to ___"
// `breaks`  are the choropleth/centroid class breaks. Percent suffixes (_1/_2/_3)
//           are FRACTIONS (0.05 = 5%); count suffixes (_B/_E/_C) are raw counts.
//
// ScenAfter  = 'after August 22'  ∪ nonCUSMA
// ScenBefore = 'before August 22' ∪ nonCUSMA
// The bare 'after August 22' / 'before August 22' columns still exist in the
// pmtiles but are NOT scenario totals — they exclude non-CUSMA exposure. They are
// deliberately absent from this file so they can't be selected.
// ---------------------------------------------------------------------------

const LAYER_SPECS = [
    {
        code: 'Total',
        subject: "all types of U.S. Administration's Tariffs on Canada",
        breaks: {
            _1: [0.05, 0.1, 0.2, 0.3],
            _2: [0.04, 0.1, 0.2, 0.4],
            _3: [0.05, 0.1, 0.2, 0.5],
            _B: [10, 50, 100, 200],
            _E: [500, 1000, 2500, 5000],
            _C: [400, 700, 1000, 1500],
        },
    },
    {
        code: 'ScenAfter',
        subject: 'all tariffs in effect after August 22, 2026',
        breaks: {
            _1: [0.05, 0.1, 0.2, 0.3],
            _2: [0.04, 0.1, 0.2, 0.4],
            _3: [0.05, 0.1, 0.2, 0.5],
            _B: [10, 50, 100, 200],
            _E: [500, 1000, 2500, 5000],
            _C: [400, 700, 1000, 1500],
        },
    },
    {
        code: 'ScenBefore',
        subject: 'all tariffs in effect prior to August 22, 2026',
        breaks: {
            _1: [0.05, 0.1, 0.2, 0.3],
            _2: [0.05, 0.1, 0.2, 0.4],
            _3: [0.05, 0.1, 0.2, 0.5],
            _B: [10, 50, 100, 200],
            _E: [500, 1000, 2500, 5000],
            _C: [400, 700, 1000, 1500],
        },
    },
    {
        code: 'CUSMA',
        subject: "U.S. Administration's non-CUSMA Compliant Tariffs on Canada",
        breaks: {
            _1: [0.05, 0.1, 0.2, 0.3],
            _2: [0.05, 0.1, 0.2, 0.4],
            _3: [0.05, 0.1, 0.2, 0.5],
            _B: [10, 50, 100, 200],
            _E: [500, 1000, 2500, 5000],
            _C: [400, 700, 1000, 1500],
        },
    },
    {
        code: 'Section 338',
        subject: 'Section 338 tariffs',
        breaks: {
            _1: [0.05, 0.1, 0.2, 0.3],
            _2: [0.05, 0.1, 0.2, 0.4],
            _3: [0.05, 0.1, 0.2, 0.5],
            _B: [10, 50, 100, 200],
            _E: [500, 1000, 2500, 5000],
            _C: [400, 700, 1000, 1500],
        },
    },
    {
        code: 'Motor',
        subject: "U.S. Administration's Motor Vehicle Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.04, 0.08, 0.2],
            _2: [0.01, 0.04, 0.08, 0.2],
            _3: [0.01, 0.04, 0.08, 0.2],
            _B: [10, 50, 100, 200],
            _E: [200, 500, 1000, 2000],
            _C: [200, 500, 1000, 2000],
        },
    },
    {
        code: 'Dairy',
        subject: "U.S. Administration's Dairy Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.04],
            _2: [0.01, 0.02, 0.03, 0.04],
            _3: [0.01, 0.02, 0.03, 0.04],
            _B: [2, 5, 10, 20],
            _E: [25, 100, 250, 500],
            _C: [25, 100, 200, 500],
        },
    },
    {
        code: 'Alcohol',
        subject: "U.S. Administration's Alcohol Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.04],
            _2: [0.01, 0.02, 0.03, 0.04],
            _3: [0.01, 0.02, 0.03, 0.04],
            _B: [2, 5, 10, 20],
            _E: [25, 100, 250, 500],
            _C: [25, 100, 200, 500],
        },
    },
    {
        code: 'Auto',
        subject: "U.S. Administration's Automobile Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.06],
            _2: [0.01, 0.04, 0.08, 0.2],
            _3: [0.01, 0.02, 0.05, 0.2],
            _B: [5, 10, 20, 50],
            _E: [200, 500, 1000, 2000],
            _C: [50, 100, 250, 500],
        },
    },
    {
        code: 'Alum',
        subject: "U.S. Administration's Aluminum Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.05],
            _2: [0.01, 0.05, 0.1, 0.2],
            _3: [0.01, 0.03, 0.07, 0.2],
            _B: [5, 10, 20, 50],
            _E: [200, 500, 1000, 2000],
            _C: [50, 100, 250, 500],
        },
    },
    {
        code: 'Steel',
        subject: "U.S. Administration's Steel Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.07],
            _2: [0.01, 0.05, 0.1, 0.3],
            _3: [0.01, 0.05, 0.1, 0.25],
            _B: [5, 10, 20, 50],
            _E: [200, 500, 1000, 2000],
            _C: [50, 100, 250, 500],
        },
    },
    {
        code: 'Cop',
        subject: "U.S. Administration's Copper Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.04],
            _2: [0.01, 0.02, 0.04, 0.08],
            _3: [0.01, 0.02, 0.03, 0.04],
            _B: [2, 5, 10, 20],
            _E: [200, 500, 1000, 2000],
            _C: [10, 25, 50, 100],
        },
    },
    {
        code: 'LumOld',
        subject: "U.S. Administration's Lumber Tariffs on Canada (before Oct 14, 2025)",
        breaks: {
            _1: [0.01, 0.02, 0.07, 0.15],
            _2: [0.01, 0.05, 0.1, 0.2],
            _3: [0.01, 0.03, 0.08, 0.2],
            _B: [2, 5, 10, 20],
            _E: [25, 100, 250, 500],
            _C: [25, 100, 200, 500],
        },
    },
    {
        code: 'LumNew',
        subject: "U.S. Administration's Lumber Tariffs on Canada (after Oct 14, 2025)",
        breaks: {
            _1: [0.01, 0.02, 0.07, 0.15],
            _2: [0.01, 0.05, 0.1, 0.2],
            _3: [0.01, 0.03, 0.08, 0.2],
            _B: [2, 5, 10, 20],
            _E: [25, 100, 250, 500],
            _C: [25, 100, 200, 500],
        },
    },
    {
        code: 'MHDV',
        subject: "U.S. Administration's Medium Heavy Duty Vehicles Tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.04],
            _2: [0.01, 0.02, 0.03, 0.04],
            _3: [0.01, 0.02, 0.03, 0.04],
            _B: [2, 5, 10, 20],
            _E: [50, 100, 250, 500],
            _C: [25, 100, 200, 500],
        },
    },
    {
        code: 'Ene',
        subject: "U.S. Administration's Energy and natural resources tariffs on Canada",
        breaks: {
            _1: [0.01, 0.02, 0.03, 0.08],
            _2: [0.01, 0.05, 0.1, 0.2],
            _3: [0.01, 0.03, 0.08, 0.2],
            _B: [5, 10, 20, 50],
            _E: [50, 100, 250, 1000],
            _C: [25, 100, 200, 500],
        },
    },
];

// ---------------------------------------------------------------------------
// Expansion — builds the flat { "Auto_1": {...}, ... } object the map consumes.
// `tariffType` is always set to the CODE, which is what mapSelected matches on.
// ---------------------------------------------------------------------------

const SUFFIXES = {
    _1: { metricType: 'Percent', impactType: 'Business',      who: 'businesses' },
    _2: { metricType: 'Percent', impactType: 'EmployeeWork',  who: 'employees (by work location)' },
    _3: { metricType: 'Percent', impactType: 'EmployeeHome',  who: 'employees (by primary residence)' },
    _B: { metricType: 'Count',   impactType: 'Business',      who: 'businesses' },
    _E: { metricType: 'Count',   impactType: 'EmployeeWork',  who: 'employees (by work location)' },
    _C: { metricType: 'Count',   impactType: 'EmployeeHome',  who: 'employees (by primary residence)' },
};

function buildDataLayers() {
    const layers = {};

    for (const spec of LAYER_SPECS) {
        for (const [suffix, meta] of Object.entries(SUFFIXES)) {
            const breaks = spec.breaks[suffix];
            if (!breaks) continue;

            const key = `${spec.code}${suffix}`;
            const lead = meta.metricType === 'Percent'
                ? `Estimated % of ${meta.who}`
                : `Estimated count of ${meta.who}`;

            layers[key] = {
                dataSource: key,
                metricType: meta.metricType,
                impactType: meta.impactType,
                tariffType: spec.code,
                breaks,
                colours: GRADUATED_COLORS,
                text: `${lead} directly exposed to ${spec.subject}`,
                ...(meta.metricType === 'Count' ? { size: GRADUATED_SIZES } : {}),
            };
        }
    }

    return layers;
}

export const DATA_LAYERS = buildDataLayers();

// ---------------------------------------------------------------------------
// Dev-only consistency check. Catches the class of bug where a dropdown option
// maps to a code that has no layer (silently logs "no matching data layer").
// ---------------------------------------------------------------------------

if (import.meta.env?.DEV) {
    const specCodes = new Set(LAYER_SPECS.map((s) => s.code));
    const dropdownCodes = new Set(Object.values(TARIFF_NAME_CODES));

    const missing = [...dropdownCodes].filter((c) => !specCodes.has(c));
    if (missing.length) {
        console.warn('[dataLayers] dropdown codes with no layer spec:', missing);
    }

    const unreachable = [...specCodes].filter((c) => !dropdownCodes.has(c));
    if (unreachable.length) {
        console.warn('[dataLayers] layer specs not reachable from the dropdown:', unreachable);
    }
}
