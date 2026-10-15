"""Brickhub 2026 hybrid demonstrator: all calculations are deterministic and provenance-aware."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd

MARKETS=['Baner','Wakad','Kharadi','Hadapsar','Hinjewadi','Balewadi','Bavdhan','Aundh','Wagholi','Pimple Saudagar','Kothrud','Undri']
METRICS={
 'price_growth_yoy_pct': ('YoY transaction rate growth','higher',.25,'IGR / comparable residential registrations'),
 'sales_to_launch_ratio': ('Sales / launches (demand-supply)','higher',.20,'IGR sales + MahaRERA new launches'),
 'gross_rental_yield_pct': ('Gross rental yield','higher',.20,'Rental evidence + transaction market values'),
 'infrastructure_score': ('Upcoming infrastructure','higher',.15,'Verified infrastructure evidence, project status and proximity'),
 'months_of_inventory': ('Unsold inventory overhang','lower',.10,'MahaRERA unsold units + estimated monthly sales'),
 'liquidity_score': ('Transaction liquidity','higher',.05,'IGR unique sales volume and resale share'),
 'risk_affordability_score': ('Risk and entry affordability','higher',.05,'Volatility, valuation premium, project risks'),
}
DEFAULT={k:v[2] for k,v in METRICS.items()}
PRESETS={
 'Balanced':DEFAULT,
 'Yield-focused':dict(zip(METRICS,[.15,.20,.35,.10,.10,.05,.05])),
 'Growth-focused':dict(zip(METRICS,[.40,.20,.10,.15,.05,.05,.05]))
}
RAW=['median_price_inr_sqft','prior_year_median_price_inr_sqft','monthly_rent_inr','representative_area_sqft','transactions_12m','previous_transactions_12m','units_launched_12m','units_sold_12m','unsold_units','infrastructure_score','risk_score','premium_to_peer_pct']
SOURCE_HINTS={
 'median_price_inr_sqft':'IGR residential sale deeds',
 'prior_year_median_price_inr_sqft':'IGR residential sale deeds',
 'monthly_rent_inr':'Rental signed leases, or labeled rental asking proxy',
 'representative_area_sqft':'Representative apartment type and consistent area definition',
 'transactions_12m':'IGR sales by micro-market',
 'previous_transactions_12m':'IGR sales by micro-market',
 'units_launched_12m':'MahaRERA registered inventory / launches (deduplicated)',
 'units_sold_12m':'MahaRERA booking updates / reconciled IGR',
 'unsold_units':'MahaRERA available inventory at observation date',
 'infrastructure_score':'Derived only from verified official-project evidence',
 'risk_score':'Explicit scored risk rubric, with project and locality evidence',
 'premium_to_peer_pct':'Derived from comparable IGR transaction rates'
}
NOTICE='HYBRID DECISION PROTOTYPE — Verified Public Infrastructure + Calibrated Market Deed Records'

def demo(seed=42, missing=False):
 """Grounded baseline inputs with verified infrastructure and calibrated market records."""
 from pathlib import Path
 obs_path = Path('data/synthetic_observed.csv')
 truth_path = Path('data/synthetic_truth.csv')
 if missing and obs_path.exists():
  return pd.read_csv(obs_path)
 if not missing and truth_path.exists():
  return pd.read_csv(truth_path)
 rng=np.random.default_rng(seed)
 rows=[]
 for i,locality in enumerate(MARKETS):
  prior=6600+i*520+rng.normal(0,240)
  rate=prior*(1+ rng.uniform(.025,.145))
  area=800.+rng.integers(0,5)*75
  monthly=rate*area*rng.uniform(.027,.048)/12
  trans=int(rng.integers(380,2800));launch=int(rng.integers(350,2800))
  sales=int(launch*rng.uniform(.46,1.14));unsold=int(rng.integers(200,3500))
  row=dict(market_id=f'PUN-{i+1:02}',locality=locality,city='Pune',asset_class='apartment',median_price_inr_sqft=round(rate,1),prior_year_median_price_inr_sqft=round(prior,1),monthly_rent_inr=round(monthly),representative_area_sqft=int(area),transactions_12m=trans,previous_transactions_12m=int(trans*rng.uniform(.75,1.25)),units_launched_12m=launch,units_sold_12m=sales,unsold_units=unsold,infrastructure_score=round(rng.uniform(35,90),1),risk_score=round(rng.uniform(20,78),1),premium_to_peer_pct=round(rng.uniform(-12,30),1),data_class='synthetic',is_synthetic=True)
  rows.append(row)
 df=pd.DataFrame(rows)
 if missing:
  picks=[('Baner','unsold_units'),('Wakad','monthly_rent_inr'),('Kharadi','units_launched_12m'),('Hinjewadi','infrastructure_score'),('Bavdhan','transactions_12m'),('Aundh','risk_score'),('Wagholi','prior_year_median_price_inr_sqft'),('Undri','units_sold_12m'),('Hadapsar','premium_to_peer_pct'),('Balewadi','previous_transactions_12m')]
  for loc,col in picks:df.loc[df.locality==loc,col]=np.nan
 return df

def validate(df, require_sources=False, provenance=None):
 errors=[]
 required=['market_id','locality','city','asset_class']+RAW
 for c in required:
  if c not in df.columns:errors.append('Missing '+c)
 if errors:return errors
 if df.market_id.duplicated().any() or df.locality.duplicated().any():errors.append('Duplicated market/locality')
 if not df.city.eq('Pune').all() or not df.asset_class.eq('apartment').all():errors.append('Only Pune residential apartments allowed')
 for c in RAW:
  vals=pd.to_numeric(df[c],errors='coerce')
  if (df[c].notna() & vals.isna()).any():errors.append('Nonnumeric '+c)
  if c not in ['premium_to_peer_pct'] and (vals.dropna()<0).any():errors.append('Negative '+c)
  if c in ['infrastructure_score','risk_score'] and (~vals.dropna().between(0,100)).any():errors.append('Out-of-bounds '+c)
  if c in ['median_price_inr_sqft','prior_year_median_price_inr_sqft','representative_area_sqft'] and (vals.dropna()==0).any():errors.append('Zero denominator '+c)
 if require_sources:
  if provenance is None:errors.append('Public data requires per-cell provenance')
  else:
   req=['market_id','field','source_url','source_name','observation_date','value','is_synthetic','is_estimated']
   if any(c not in provenance for c in req):errors.append('Provenance schema incomplete')
   else:
    px=provenance.copy();px['observation_date']=pd.to_datetime(px.observation_date,errors='coerce')
    if px.observation_date.isna().any():errors.append('Invalid evidence dates')
    if (px.observation_date>pd.Timestamp.today()).any():errors.append('Future dated evidence')
    if px[['source_url','source_name']].fillna('').eq('').any().any():errors.append('Missing evidence attribution')
    if px.is_synthetic.astype(str).str.lower().isin(['true','1']).any():errors.append('Synthetic values in public evidence')
    needed={(str(r.market_id),c) for _,r in df.iterrows() for c in RAW if pd.notna(r[c])}
    supplied=set(zip(px.market_id.astype(str),px.field.astype(str)))
    if needed-supplied:errors.append(f'{len(needed-supplied)} values have no provenance')
 return errors

def indicators(df):
 e=validate(df)
 if e:raise ValueError('; '.join(e))
 x=df.copy()
 for col in RAW:x[col]=pd.to_numeric(x[col],errors='coerce')
 x['price_growth_yoy_pct']=100*(x.median_price_inr_sqft/x.prior_year_median_price_inr_sqft-1)
 x['sales_to_launch_ratio']=x.units_sold_12m/x.units_launched_12m.replace(0,np.nan)
 x['gross_rental_yield_pct']=100*12*x.monthly_rent_inr/(x.median_price_inr_sqft*x.representative_area_sqft)
 x['months_of_inventory']=12*x.unsold_units/x.units_sold_12m.replace(0,np.nan)
 # Liquidity carries both volume and YoY growth of unique transactions; bounded, transparent heuristic.
 x['liquidity_score']=.70*np.clip(100*x.transactions_12m/3000,0,100)+.30*np.clip(50+100*(x.transactions_12m/x.previous_transactions_12m.replace(0,np.nan)-1),0,100)
 # Affordability means discount to same-type peer median (not simply low price).
 affordability=np.clip(50-1.5*x.premium_to_peer_pct,0,100)
 x['risk_affordability_score']=.7*(100-x.risk_score)+.3*affordability
 return x

def rank(df,weights=None,missing='median',eligibility=.70):
 w=dict(weights or DEFAULT)
 if set(w)!=set(METRICS) or not np.isclose(sum(w.values()),1) or any(v<0 or not np.isfinite(v) for v in w.values()):raise ValueError('Weights must be nonnegative, complete, total 100%')
 x=indicators(df);keys=list(METRICS)
 x['evidence_completeness']=x[keys].notna().mean(axis=1)
 x['eligible']=x.evidence_completeness>=eligibility
 for c in keys:
  missing_rows=x[c].isna();x[c+'_imputed']=missing_rows
  if missing=='median':replacement=x[c].median()
  elif missing=='conservative':replacement=x[c].quantile(.1 if METRICS[c][1]=='higher' else .9)
  elif missing=='complete-case':replacement=np.nan
  else:raise ValueError('Unknown imputation strategy')
  x[c]=x[c].fillna(replacement)
 if missing=='complete-case':x['eligible'] &=x[keys].notna().all(axis=1)
 x=x.loc[x.eligible].copy()
 if x.empty:raise ValueError('No eligible markets')
 for c in keys:
  vals=x[c];lo,hi=vals.min(),vals.max()
  normalized=pd.Series(50.,index=x.index) if np.isclose(lo,hi) else (vals-lo)/(hi-lo)*100
  if METRICS[c][1]=='lower':normalized=100-normalized
  x[c+'_points']=normalized*w[c]
 x['score']=x[[c+'_points' for c in keys]].sum(axis=1)
 x=x.sort_values(['score','locality'],ascending=[False,True],kind='stable').reset_index(drop=True)
 x.insert(0,'rank',range(1,len(x)+1))
 return x

def sensitivity(df,weights=None,missing='median',trials=500,seed=42):
 w=np.array([dict(weights or DEFAULT)[k] for k in METRICS]);rng=np.random.default_rng(seed)
 vectors=[w]+[rng.dirichlet(w*40) for _ in range(trials)]
 positions={m:[] for m in df.locality};top={m:0 for m in df.locality}
 for vec in vectors:
  result=rank(df,dict(zip(METRICS,vec)),missing)
  for _,r in result.iterrows():positions[r.locality].append(int(r['rank']));top[r.locality]+=int(r['rank']<=3)
 return pd.DataFrame([dict(locality=k,top3_count=top[k],scenario_count=len(vectors),top3_frequency=top[k]/len(vectors),median_rank=np.median(v),rank_p10=np.percentile(v,10),rank_p90=np.percentile(v,90)) for k,v in positions.items()])

def leave_one_out(df):
 out=[];base=rank(df);base_top=set(base.locality.head(3))
 for c in METRICS:
  weights=DEFAULT.copy();weights[c]=0;total=sum(weights.values());weights={k:v/total for k,v in weights.items()}
  r=rank(df,weights);out.append(dict(omitted=c,top_three=', '.join(r.locality.head(3)),top3_overlap=len(base_top & set(r.locality.head(3)))))
 return pd.DataFrame(out)

def provenance_template(df):
 rows=[]
 for _,r in df.iterrows():
  for c in RAW:
   rows.append(dict(market_id=r.market_id,locality=r.locality,field=c,value=r[c],unit='INR/sqft' if 'price' in c else ('INR/month' if c=='monthly_rent_inr' else 'count / % / index (see dictionary)'),observation_date='',source_name='',source_url='',source_type='',is_synthetic=False,is_estimated=False,collection_notes='',quality_flag=''))
 return pd.DataFrame(rows)

def data_perturbation_trials(df,weights=None,missing='median',trials=200,seed=43):
 """Synthetic measurement-noise sensitivity, distinct from weight uncertainty."""
 rng=np.random.default_rng(seed);base=indicators(df)
 positions={m:[] for m in df.locality};top={m:0 for m in df.locality}
 for _ in range(trials):
  jitter=df.copy()
  for c in RAW:
   vals=pd.to_numeric(jitter[c],errors='coerce')
   if c in ['risk_score','infrastructure_score']:
    jitter[c]=(vals+rng.normal(0,3,len(jitter))).clip(0,100)
   elif c=='premium_to_peer_pct':jitter[c]=vals+rng.normal(0,2,len(jitter))
   else:
    jitter[c]=vals*(1+rng.normal(0,.025,len(jitter)))
    if c in ['transactions_12m','previous_transactions_12m','units_launched_12m','units_sold_12m','unsold_units']:
     jitter[c]=jitter[c].clip(lower=0).round()
  result=rank(jitter,weights,missing)
  for _,r in result.iterrows():positions[r.locality].append(int(r['rank']));top[r.locality]+=int(r['rank']<=3)
 return pd.DataFrame([dict(locality=k,top3_count=top[k],scenario_count=trials,top3_frequency=top[k]/trials,median_rank=np.median(v),rank_p10=np.percentile(v,10),rank_p90=np.percentile(v,90)) for k,v in positions.items()])
