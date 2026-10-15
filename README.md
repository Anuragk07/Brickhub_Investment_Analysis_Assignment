# Brickhub Intelligence – Pune residential investment ranking (v2)

## Data integrity
**DEFAULT DATA ARE SYNTHETIC DEMONSTRATIONS, NOT VALID ASSIGNMENT EVIDENCE.** No locality investment recommendation is made from the supplied example figures. The original Brickhub assignment calls for independently sourced public observations and a citation/date per data point; do not submit the demo as though it meets that requirement.

## Setup & Execution
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# Run automated tests
python -m pytest tests/ -v

# Option A: Interactive Streamlit Screener UI
python -m streamlit run app.py

# Option B: End-to-End Jupyter Notebook Walkthrough
jupyter notebook Brickhub_Investment_Analysis.ipynb
```
*Note: `Brickhub_Investment_Analysis.ipynb` comes fully pre-executed with all plots, tables, and narrative markdown rendered.*

## Method
Pune, 12 apartment micro-markets, 5–7-year hold. Seven score families: YoY comparable IGR rates 25%, demand-to-new-launch supply 20%, gross rental yield 20%, verified upcoming infrastructure 15%, unsold inventory months 10%, IGR liquidity 5%, risk and relative affordability 5%. Price level is not mechanically treated as an opportunity. Normalize relative to eligible sample; weighted sum and alphabetical tie-break. Methods: median/conservative/complete-case missingness, seed-42 scenario testing, leave-one-factor-out. Synthetic data are illustrative only.

## Real-data collection
1. Obtain apartment-only IGR sale transaction records for TWO matching 12-month windows, including registration date, area basis, consideration, subtype, micro-market location, floor/BHK/age where available. Deduplicate and compute trimmed comparable median per sqft. Preserve both window sizes and source references.
2. Obtain MahaRERA registered residential units/launches, booking progression and latest quarterly updates at project level. Harmonize project boundaries, age and unit definitions; avoid treating missing quarterly updates as zero inventory.
3. Obtain rental evidence from public current listings or signed-lease evidence where available, record gross advertised-vs-transacted status. Normalize to comparable area/BHK type, mark asking rent estimates explicitly.
4. Obtain official infrastructure project sources (PMRDA, Maha Metro, municipal/road authorities), record project ID, route/affected micro-markets, current verified status, date, distance and execution risk. Review and justify any infrastructure score manually; do not let an AI model hallucinate scores.
5. Document the risk rubric and peer-group price comparisons. Fill `data/public_evidence_template.csv` with a *distinct record for each locality-field* and evidence date/url; attach underlying raw files. Separate derived fields from observed values.
6. Run the app with collected data, compare all sensitivity methods and reissue the recommendation and reports. Claims about market data should cite the exact input records.

## Limitations
The real-data stage is NOT complete. IGR and RERA counts may represent different units/timings and must be reconciled before using sales/launch comparisons. Apartment price indices are not a causal forecast. Gross yield excludes vacancy, taxes, maintenance and transaction costs. Inventory counts are often as-of dates; incomplete reporting creates bias. Infrastructure benefit is uncertain. The 12 micro-markets are judgmentally selected, not a statistical sample.

## Reproducibility
Use Python 3.11+. `src/engine.py` owns formulas and validation; UI is `app.py`, tests are `tests/`. Source evidence template and seeded output CSVs are in `data/`. See `docs/` for submission documentation. Do not state a data provenance validation pass as proof that published sources are authentic.
