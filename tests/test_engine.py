import numpy as np
from src.engine import *
def test_deterministic(): assert demo().equals(demo())
def test_twelve(): assert len(demo())==12
def test_one_hundred(): assert abs(sum(DEFAULT.values())-1)<1e-10
def test_rank():
 r=rank(demo()); assert list(r['rank'])==list(range(1,13));assert r.score.between(0,100).all()
def test_missing_modes():
 df=demo(missing=True)
 assert len(rank(df,missing='median'))==12
 assert len(rank(df,missing='conservative'))==12
 assert len(rank(df,missing='complete-case'))<12
def test_reverse_risk():
 d=demo();a=rank(d);assert 'risk_affordability_score' in a.columns
 idx=0;d.loc[idx,'risk_score']=95;new=indicators(d)
 assert new.loc[idx,'risk_affordability_score']<indicators(demo()).loc[idx,'risk_affordability_score']
def test_wrong_weights():
 import pytest
 with pytest.raises(ValueError):rank(demo(),dict.fromkeys(METRICS,.2))
def test_sensitivity():
 s=sensitivity(demo(),trials=10);assert (s.scenario_count==11).all()
def test_source_validation():
 d=demo();assert validate(d,require_sources=True)
 p=provenance_template(d);assert len(p)==12*len(RAW)
def test_invalid_data():
 d=demo();d.loc[0,'median_price_inr_sqft']=-100;assert validate(d)
def test_loo():assert len(leave_one_out(demo()))==len(METRICS)
def test_derived_math():
 d=demo();i=indicators(d);assert np.allclose(i.price_growth_yoy_pct,100*(d.median_price_inr_sqft/d.prior_year_median_price_inr_sqft-1))
def test_data_perturbation():
 s=data_perturbation_trials(demo(missing=True),trials=5)
 assert len(s)==12 and (s.scenario_count==5).all()
