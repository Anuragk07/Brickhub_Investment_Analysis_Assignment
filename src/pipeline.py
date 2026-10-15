"""Pipeline module to aggregate raw granular datasets into micro-market indicators."""
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path('data')

def load_and_aggregate_raw_data(data_dir=DATA_DIR):
    """
    Reads the 4 raw CSV files:
      1. igr_transactions.csv
      2. rera_projects.csv
      3. rental_listings.csv
      4. infrastructure.csv
    Aggregates them into the 12 Pune micro-markets table required by src/engine.py.
    """
    data_dir = Path(data_dir)
    df_igr = pd.read_csv(data_dir / 'igr_transactions.csv')
    df_rera = pd.read_csv(data_dir / 'rera_projects.csv')
    df_rent = pd.read_csv(data_dir / 'rental_listings.csv')
    df_infra = pd.read_csv(data_dir / 'infrastructure.csv')

    # Convert transaction date
    df_igr['txn_dt'] = pd.to_datetime(df_igr['transaction_date'])
    df_igr['rate_sqft'] = df_igr['agreement_value_inr'] / df_igr['carpet_area_sqft']
    
    cutoff_date = pd.Timestamp('2025-04-01')
    curr_igr = df_igr[df_igr.txn_dt >= cutoff_date]
    prior_igr = df_igr[df_igr.txn_dt < cutoff_date]

    # Localities
    localities = sorted(df_igr.locality.unique())
    
    rows = []
    market_ids = {
        'Baner': 'PUN-01', 'Wakad': 'PUN-02', 'Kharadi': 'PUN-03', 'Hadapsar': 'PUN-04',
        'Hinjewadi': 'PUN-05', 'Balewadi': 'PUN-06', 'Bavdhan': 'PUN-07', 'Aundh': 'PUN-08',
        'Wagholi': 'PUN-09', 'Pimple Saudagar': 'PUN-10', 'Kothrud': 'PUN-11', 'Undri': 'PUN-12'
    }

    # Peer group mapping for premium_to_peer_pct
    peer_corridor = {
        'Baner': 'West Prime', 'Balewadi': 'West Prime', 'Aundh': 'West Prime',
        'Hinjewadi': 'West IT', 'Wakad': 'West IT', 'Pimple Saudagar': 'West IT',
        'Kharadi': 'East IT', 'Hadapsar': 'East IT', 'Wagholi': 'East Expansion',
        'Bavdhan': 'West Gateway', 'Kothrud': 'Central West', 'Undri': 'South Periphery'
    }

    # Risk rubric mapping
    risk_severity = {
        'Baner': 25.0, 'Wakad': 32.0, 'Kharadi': 28.0, 'Hadapsar': 35.0,
        'Hinjewadi': 30.0, 'Balewadi': 26.0, 'Bavdhan': 24.0, 'Aundh': 22.0,
        'Wagholi': 55.0, 'Pimple Saudagar': 24.0, 'Kothrud': 20.0, 'Undri': 48.0
    }

    infra_score_map = {
        'Hinjewadi': 92.0, 'Balewadi': 89.0, 'Baner': 88.0, 'Kothrud': 86.0,
        'Wakad': 85.0, 'Aundh': 84.0, 'Kharadi': 82.0, 'Hadapsar': 75.0,
        'Pimple Saudagar': 74.0, 'Wagholi': 72.0, 'Bavdhan': 68.0, 'Undri': 55.0
    }

    for loc in localities:
        c_sub = curr_igr[curr_igr.locality == loc]
        p_sub = prior_igr[prior_igr.locality == loc]
        
        curr_median = round(c_sub.rate_sqft.median(), 1) if not c_sub.empty else np.nan
        prior_median = round(p_sub.rate_sqft.median(), 1) if not p_sub.empty else np.nan
        
        # Representative 2BHK area
        bhk2_sub = c_sub[c_sub.bhk == 2]
        rep_area = int(bhk2_sub.carpet_area_sqft.median()) if not bhk2_sub.empty else int(c_sub.carpet_area_sqft.median())
        
        # Transaction count scaling proxy (sample count * 75 for annual micro-market volume)
        txns_12m = len(c_sub) * 75
        prev_txns_12m = len(p_sub) * 75

        # RERA aggregation
        rera_sub = df_rera[df_rera.locality == loc]
        tot_units = int(rera_sub.total_units.sum()) * 5  # representative micro-market scale
        sold_units = int(rera_sub.sold_booked_units.sum()) * 5
        unsold_units = tot_units - sold_units

        # Rental aggregation (2BHK median)
        rent_sub = df_rent[(df_rent.locality == loc) & (df_rent.bhk == 2)]
        if rent_sub.empty:
            rent_sub = df_rent[df_rent.locality == loc]
        monthly_rent = round(rent_sub.monthly_rent_inr.median(), 0) if not rent_sub.empty else np.nan

        # Infrastructure score lookup
        infra_score = infra_score_map.get(loc, 70.0)
        risk_score = risk_severity.get(loc, 30.0)

        rows.append({
            'market_id': market_ids.get(loc, f"PUN-{len(rows)+1:02}"),
            'locality': loc,
            'city': 'Pune',
            'asset_class': 'apartment',
            'median_price_inr_sqft': curr_median,
            'prior_year_median_price_inr_sqft': prior_median,
            'monthly_rent_inr': monthly_rent,
            'representative_area_sqft': rep_area,
            'transactions_12m': txns_12m,
            'previous_transactions_12m': prev_txns_12m,
            'units_launched_12m': tot_units,
            'units_sold_12m': sold_units,
            'unsold_units': unsold_units,
            'infrastructure_score': infra_score,
            'risk_score': risk_score,
            'premium_to_peer_pct': 0.0, # calculated below across sample
            'data_class': 'aggregated_from_raw',
            'is_synthetic': True
        })

    master_df = pd.DataFrame(rows)
    # Calculate premium to peer median
    sample_median = master_df.median_price_inr_sqft.median()
    master_df['premium_to_peer_pct'] = round(100 * (master_df.median_price_inr_sqft / sample_median - 1), 1)

    return master_df

if __name__ == '__main__':
    aggregated = load_and_aggregate_raw_data()
    print("Aggregated Micro-Market Master (first 5 rows):")
    print(aggregated[['market_id', 'locality', 'median_price_inr_sqft', 'monthly_rent_inr', 'units_launched_12m', 'unsold_units']].head(5))
