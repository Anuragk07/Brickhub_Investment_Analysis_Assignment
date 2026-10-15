import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

# 12 Target Pune micro-markets
LOCALITIES = [
    'Baner', 'Wakad', 'Kharadi', 'Hadapsar', 'Hinjewadi', 'Balewadi',
    'Bavdhan', 'Aundh', 'Wagholi', 'Pimple Saudagar', 'Kothrud', 'Undri'
]

# Real-world project names per locality for authentic dummy data
PROJECT_NAMES = {
    'Baner': ['Kasturi The Balmoral', 'Pride Platinum', 'Rohan Leher', 'Kalpataru Jade Residences', 'VTP Verve'],
    'Wakad': ['Kolte Patil Western Avenue', 'Rohan Tarang', 'Paranjape Blue Ridge Annex', 'Sukhwani Palms', 'Akshay Park'],
    'Kharadi': ['Gera World of Joy', 'Panchshil Towers', 'Kolte Patil Downtown', 'VTP Beaumonde', 'EON Waterfront'],
    'Hadapsar': ['Amanora Park Town', 'Magarpatta City Trillium', 'Shapoorji Joyville Hadapsar', 'Marvel Bounty', 'Kumar Prospera'],
    'Hinjewadi': ['Megapolis Sparklet', 'TCG The Crown Greens', 'Kolte Patil Life Republic', 'Godrej 24', 'Rohan Prathama'],
    'Balewadi': ['F Residences', 'Majestique Signature Towers', 'Kunal Aspiree', 'Naiknavare Avon Vista', 'Mantra Monarch'],
    'Bavdhan': ['Nyati Equator', 'Shapoorji Pallonji Vanaha', 'Puraniks Abitante', 'Goel Ganga Legend', 'Pebbles Urban Living'],
    'Aundh': ['Pride Regalia', 'Rohan Nilay', 'Kalpataru Harmony', 'Chateaux De Aundh', 'Sneh Residency'],
    'Wagholi': ['Kolte Patil Ivy Estate', 'Majestique City', 'Rohan Abhilasha', 'Varia Valley View', 'Nyati Elan'],
    'Pimple Saudagar': ['Roseland Residency', 'Kunal Icon', 'Rose Icon', 'G K Rose Valley', 'Daffodils Society'],
    'Kothrud': ['Kulkarni Sobha Carnation', 'Rohan Madhuban', 'Dahanukar Colony Enclave', 'Rambaug Housing', 'Bhairav Residency'],
    'Undri': ['Godrej Greens', 'Dynamic Grandeur', 'Amit Colori', 'Nyati Esteban', 'Atur Hermitage']
}

# Baseline price per sqft (Current 12M: 2025-04-01 to 2026-03-31) and prior 12M (2024-04-01 to 2025-03-31)
PRICING_BENCHMARKS = {
    'Baner': (9450, 8600),
    'Wakad': (8100, 7350),
    'Kharadi': (8900, 8050),
    'Hadapsar': (7450, 6850),
    'Hinjewadi': (7650, 6800),
    'Balewadi': (9200, 8400),
    'Bavdhan': (8400, 7750),
    'Aundh': (11500, 10650),
    'Wagholi': (5850, 5350),
    'Pimple Saudagar': (7950, 7300),
    'Kothrud': (13200, 11900),
    'Undri': (5400, 5000),
}

# ----------------------------------------------------------------------------------
# 1. igr_transactions.csv
# Columns: transaction_id, transaction_date, locality, project_name, property_type, agreement_value_inr, carpet_area_sqft, bhk
# ----------------------------------------------------------------------------------
rng = np.random.default_rng(42)
igr_rows = []
txn_counter = 10001

for loc in LOCALITIES:
    current_base, prior_base = PRICING_BENCHMARKS[loc]
    projects = PROJECT_NAMES[loc]
    
    # 25 to 35 transactions in current year, 20 to 30 in prior year
    # Current window: 2025-04-01 to 2026-03-31
    for _ in range(rng.integers(26, 36)):
        p_name = rng.choice(projects)
        bhk_choice = rng.choice([1, 2, 3], p=[0.15, 0.65, 0.20])
        if bhk_choice == 1:
            carpet = int(rng.integers(480, 620))
        elif bhk_choice == 2:
            carpet = int(rng.integers(720, 1050))
        else:
            carpet = int(rng.integers(1150, 1550))
            
        rate = current_base * rng.uniform(0.95, 1.05)
        agreement_value = int(round((rate * carpet) / 10000) * 10000)
        
        days_offset = int(rng.integers(0, 365))
        txn_date = (datetime(2025, 4, 1) + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        igr_rows.append({
            'transaction_id': f"TXN-MH-PUN-{txn_counter}",
            'transaction_date': txn_date,
            'locality': loc,
            'project_name': p_name,
            'property_type': 'Apartment',
            'agreement_value_inr': agreement_value,
            'carpet_area_sqft': carpet,
            'bhk': bhk_choice
        })
        txn_counter += 1
        
    # Prior window: 2024-04-01 to 2025-03-31
    for _ in range(rng.integers(22, 32)):
        p_name = rng.choice(projects)
        bhk_choice = rng.choice([1, 2, 3], p=[0.15, 0.65, 0.20])
        if bhk_choice == 1:
            carpet = int(rng.integers(480, 620))
        elif bhk_choice == 2:
            carpet = int(rng.integers(720, 1050))
        else:
            carpet = int(rng.integers(1150, 1550))
            
        rate = prior_base * rng.uniform(0.95, 1.05)
        agreement_value = int(round((rate * carpet) / 10000) * 10000)
        
        days_offset = int(rng.integers(0, 365))
        txn_date = (datetime(2024, 4, 1) + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        igr_rows.append({
            'transaction_id': f"TXN-MH-PUN-{txn_counter}",
            'transaction_date': txn_date,
            'locality': loc,
            'project_name': p_name,
            'property_type': 'Apartment',
            'agreement_value_inr': agreement_value,
            'carpet_area_sqft': carpet,
            'bhk': bhk_choice
        })
        txn_counter += 1

df_igr = pd.DataFrame(igr_rows)
df_igr.to_csv(DATA_DIR / 'igr_transactions.csv', index=False)
print(f"Saved igr_transactions.csv ({len(df_igr)} rows)")

# ----------------------------------------------------------------------------------
# 2. rera_projects.csv
# Columns: rera_number, project_name, locality, report_date, total_units, sold_booked_units, project_status
# ----------------------------------------------------------------------------------
rera_rows = []
rera_base_num = 52100021000

for loc in LOCALITIES:
    projects = PROJECT_NAMES[loc]
    for p_name in projects:
        total_u = int(rng.integers(180, 650))
        # Absorption rate between 65% and 92%
        sold_u = int(round(total_u * rng.uniform(0.68, 0.92)))
        status = rng.choice(['Under Construction', 'Near Completion', 'Ongoing Phase II', 'Partially Handed Over'])
        
        rera_rows.append({
            'rera_number': f"P{rera_base_num}",
            'project_name': p_name,
            'locality': loc,
            'report_date': '2026-03-31',
            'total_units': total_u,
            'sold_booked_units': sold_u,
            'project_status': status
        })
        rera_base_num += rng.integers(15, 85)

df_rera = pd.DataFrame(rera_rows)
df_rera.to_csv(DATA_DIR / 'rera_projects.csv', index=False)
print(f"Saved rera_projects.csv ({len(df_rera)} rows)")

# ----------------------------------------------------------------------------------
# 3. rental_listings.csv
# Columns: listing_id, locality, project_name, bhk, carpet_area_sqft, monthly_rent_inr, listing_date, source_url
# ----------------------------------------------------------------------------------
RENTAL_BASE = {
    'Baner': 31000,
    'Wakad': 26500,
    'Kharadi': 29000,
    'Hadapsar': 24000,
    'Hinjewadi': 25500,
    'Balewadi': 29500,
    'Bavdhan': 26000,
    'Aundh': 35000,
    'Wagholi': 18500,
    'Pimple Saudagar': 25000,
    'Kothrud': 42000,
    'Undri': 17000,
}

rental_rows = []
listing_counter = 80001

for loc in LOCALITIES:
    base_rent = RENTAL_BASE[loc]
    projects = PROJECT_NAMES[loc]
    
    # 8 to 12 active listings per locality
    for _ in range(rng.integers(8, 13)):
        p_name = rng.choice(projects)
        bhk_choice = rng.choice([1, 2, 3], p=[0.20, 0.65, 0.15])
        
        if bhk_choice == 1:
            carpet = int(rng.integers(500, 620))
            rent = int(round((base_rent * 0.68 * rng.uniform(0.95, 1.05)) / 500) * 500)
        elif bhk_choice == 2:
            carpet = int(rng.integers(800, 1050))
            rent = int(round((base_rent * rng.uniform(0.94, 1.06)) / 500) * 500)
        else:
            carpet = int(rng.integers(1200, 1550))
            rent = int(round((base_rent * 1.45 * rng.uniform(0.95, 1.08)) / 500) * 500)
            
        days_offset = int(rng.integers(0, 90))
        listing_date = (datetime(2026, 1, 1) + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        rental_rows.append({
            'listing_id': f"LST-PUN-{listing_counter}",
            'locality': loc,
            'project_name': p_name,
            'bhk': bhk_choice,
            'carpet_area_sqft': carpet,
            'monthly_rent_inr': rent,
            'listing_date': listing_date,
            'source_url': f"https://www.magicbricks.com/propertyDetails/rent-flats-{loc.lower()}-pune-id-{listing_counter}"
        })
        listing_counter += 1

df_rental = pd.DataFrame(rental_rows)
df_rental.to_csv(DATA_DIR / 'rental_listings.csv', index=False)
print(f"Saved rental_listings.csv ({len(df_rental)} rows)")

# ----------------------------------------------------------------------------------
# 4. infrastructure.csv
# Columns: project_name, project_type, status, expected_completion, affected_locality, source_url, source_date
# ----------------------------------------------------------------------------------
infra_records = [
    {
        'project_name': 'Pune Metro Line 3 (Hinjewadi to Civil Court)',
        'project_type': 'Metro Rail',
        'status': 'Under Construction (>85% viaduct complete)',
        'expected_completion': '2025-2026',
        'affected_locality': 'Hinjewadi',
        'source_url': 'https://www.pmrda.gov.in/en/pune-metro-line-3/maan-hinjawadi-shivajinagar-metro-line/',
        'source_date': '2026-03-15'
    },
    {
        'project_name': 'Pune Metro Line 3 (Wakad Chowk Station)',
        'project_type': 'Metro Rail',
        'status': 'Under Construction',
        'expected_completion': '2025-2026',
        'affected_locality': 'Wakad',
        'source_url': 'https://punerimetro.in',
        'source_date': '2026-03-15'
    },
    {
        'project_name': 'Pune Metro Line 3 (Balewadi High Street & Sports Complex Stations)',
        'project_type': 'Metro Rail',
        'status': 'Under Construction',
        'expected_completion': '2025-2026',
        'affected_locality': 'Balewadi',
        'source_url': 'https://punerimetro.in',
        'source_date': '2026-03-15'
    },
    {
        'project_name': 'Pune Metro Line 3 (Baner Gaon & Link Road Stations)',
        'project_type': 'Metro Rail',
        'status': 'Under Construction',
        'expected_completion': '2025-2026',
        'affected_locality': 'Baner',
        'source_url': 'https://www.pmrda.gov.in/en/pune-metro-line-3/maan-hinjawadi-shivajinagar-metro-line/',
        'source_date': '2026-03-15'
    },
    {
        'project_name': 'Pune Metro Line 3 & University Chowk Multi-Tier Flyover',
        'project_type': 'Integrated Metro & Flyover',
        'status': 'Under Construction',
        'expected_completion': '2025-2026',
        'affected_locality': 'Aundh',
        'source_url': 'https://punemetrorail.org',
        'source_date': '2026-02-10'
    },
    {
        'project_name': 'Pune Metro Line 2 (Aqua Line) Vanaz Terminal',
        'project_type': 'Metro Rail',
        'status': 'Operational',
        'expected_completion': 'Completed (Operational)',
        'affected_locality': 'Kothrud',
        'source_url': 'https://punemetrorail.org',
        'source_date': '2026-03-01'
    },
    {
        'project_name': 'Pune Metro Line 2B Extension (Ramwadi-Wagholi Double Decker)',
        'project_type': 'Double-Decker Metro & Flyover',
        'status': 'Soil Investigation & Geotechnical Survey',
        'expected_completion': '2027-2028',
        'affected_locality': 'Kharadi',
        'source_url': 'https://punemetrorail.org/project-update',
        'source_date': '2026-02-28'
    },
    {
        'project_name': 'Pune Metro Line 4 (Kharadi-Hadapsar-Swargate)',
        'project_type': 'Metro Rail',
        'status': 'Union Cabinet Approved Phase 2 DPR',
        'expected_completion': '2028',
        'affected_locality': 'Hadapsar',
        'source_url': 'https://pmindia.gov.in',
        'source_date': '2026-02-15'
    },
    {
        'project_name': 'Pune Metro Line 2B Vitthalwadi/Wagholi Corridor',
        'project_type': 'Double-Decker Metro & Flyover',
        'status': 'Site Barricading & Soil Testing',
        'expected_completion': '2027-2028',
        'affected_locality': 'Wagholi',
        'source_url': 'https://punemetrorail.org/project-update',
        'source_date': '2026-03-01'
    },
    {
        'project_name': 'Nashik Phata Metro Line 1 Interchange & BRTS Grid',
        'project_type': 'BRTS & Metro Feeder',
        'status': 'Operational',
        'expected_completion': 'Completed (Operational)',
        'affected_locality': 'Pimple Saudagar',
        'source_url': 'https://pcmcindia.gov.in',
        'source_date': '2026-01-15'
    },
    {
        'project_name': 'Chandani Chowk Multi-Level Grade Separator',
        'project_type': 'Highway Multi-Tier Interchange',
        'status': 'Operational (Main Flyover Open)',
        'expected_completion': 'Completed',
        'affected_locality': 'Bavdhan',
        'source_url': 'https://pmc.gov.in',
        'source_date': '2026-01-20'
    },
    {
        'project_name': 'Katraj-Kondhwa-Undri 84m Arterial Road Widening',
        'project_type': 'Major Arterial Road Widening',
        'status': 'Civil Road Widening In Progress',
        'expected_completion': '2026-2027',
        'affected_locality': 'Undri',
        'source_url': 'https://pmc.gov.in',
        'source_date': '2026-02-12'
    }
]

df_infra = pd.DataFrame(infra_records)
df_infra.to_csv(DATA_DIR / 'infrastructure.csv', index=False)
print(f"Saved infrastructure.csv ({len(df_infra)} rows)")

print("\nALL 4 USER-SPECIFIED RAW DATASETS SUCCESSFULLY GENERATED IN e:\\Anurags Assignment\\data!")
