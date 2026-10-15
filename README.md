# 🏘️ Brickhub Intelligence — Pune Residential Micro-Market Investment Analysis
### Strategic Decision-Support Framework for a 5–7 Year Buy-and-Hold Investor

This repository contains the complete quantitative solution and submission deliverables for the **Brickhub Intelligence Assignment**. It screens and ranks 12 Pune residential micro-markets across 7 core investment indicators to identify the optimal **Top 3 micro-markets** for a 5–7 year residential apartment buy-and-hold investor.

---

## 🏆 Key Investment Recommendations

Under baseline balanced multi-criteria weighting, the screening engine identifies:

| Rank | Micro-Market | Composite Score | YoY Price Growth | Gross Rental Yield | Key Catalyst |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **🥇 #1** | **Hinjewadi** | **80.2 / 100** | +10.8% | 4.4% | Origin terminus of PMRDA Metro Line 3 (>85% viaduct complete). Huge IT employment pool. |
| **🥈 #2** | **Kharadi** | **78.6 / 100** | +11.2% | 4.1% | Dominant Eastern IT corridor anchor (EON Free Zone, WTC). Rapid commercial absorption. |
| **🥉 #3** | **Baner** | **76.4 / 100** | +9.8% | 3.4% | Established Western corridor anchor with premium social infrastructure and 2 Metro Line 3 stations. |

*Statistical Stability: In 500 Monte Carlo Dirichlet random weight variations, all three markets achieve **>84% Top-3 retention**.*

---

## 📓 Primary Deliverable: The Jupyter Notebook

The entire quantitative pipeline is implemented, documented, and pre-executed in:
👉 **[`Brickhub_Investment_Analysis.ipynb`](Brickhub_Investment_Analysis.ipynb)**

The notebook can be viewed directly on GitHub (all charts, markdown formulas, tables, and sensitivity outputs are pre-rendered). It walks step-by-step through:
1. **Raw Data Ingestion & Audit:** Inspecting registered deeds, RERA project disclosures, rental listings, and 100% verified transit projects.
2. **Pipeline Aggregation:** Modular aggregation of raw data into the standardized 12-market master matrix (`src/pipeline.py`).
3. **Feature Engineering:** Mathematical derivation of 7 indicators (growth, yield, absorption, overhang, infra, liquidity, risk).
4. **Missing-Data Strategy:** Transparent handling and side-by-side comparison of `median`, `conservative`, and `complete-case` modes.
5. **MCDA Scoring Engine:** Min-Max relative normalization and composite score calculation (`src/engine.py`).
6. **Visual Analytics:** Stacked factor attribution and composite score comparisons.
7. **Stress Testing & Robustness Lab:** 500-trial Monte Carlo Dirichlet simulation, 200 data noise trials, and Leave-One-Out checks.
8. **Executive Recommendations & Risks:** Detailed commercial rationale for each top pick.

---

## 📂 Repository Structure

```text
.
├── Brickhub_Investment_Analysis.ipynb   # Complete pre-executed Jupyter Notebook (Primary Deliverable)
├── INTERVIEW_GUIDE.md                  # Comprehensive interview preparation guide & technical Q&A
├── requirements.txt                    # Minimal Python dependencies
│
├── src/                                # Core Modular Python Package
│   ├── __init__.py
│   ├── engine.py                       # Mathematical formulas, MCDA scoring, stress tests, validation
│   └── pipeline.py                     # Raw dataset aggregation & master matrix builder
│
├── data/                               # Grounded Raw & Matrix Datasets
│   ├── igr_transactions.csv            # 682 raw IGR registered sales deeds across 2 annual windows
│   ├── rera_projects.csv               # Raw MahaRERA project quarterly inventory disclosures
│   ├── rental_listings.csv             # Raw rental listings and leave-and-license signed lease data
│   ├── infrastructure.csv              # 13 verified public transit projects (PMRDA, Maha Metro, NHAI)
│   ├── synthetic_observed.csv          # 12-market input matrix with simulated real-world reporting gaps
│   ├── synthetic_truth.csv             # 12-market complete baseline matrix
│   └── public_evidence_template.csv    # Per-cell data provenance audit template
│
├── docs/                               # Formal Submission Deliverables
│   ├── design_note.pdf / .docx         # Pre-build design blueprint & decision context
│   ├── method_note.pdf / .docx         # Quantitative methodology & algorithmic specification
│   ├── analysis_recommendation.pdf     # Executive report with embedded charts and sensitivity tables
│   └── walkthrough.pdf / .docx         # 15-minute presentation & interview walkthrough script
│
└── tests/
    └── test_engine.py                  # 13 automated unit tests verifying math, schemas, and stability
```

---

## ⚡ Quickstart & Reproducibility

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Anuragk07/Brickhub_Investment_Analysis_Assignment.git
cd Brickhub_Investment_Analysis_Assignment

# Create and activate virtual environment
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Automated Verification Tests
```bash
python -m pytest tests/ -v
# Output: 13 passed in ~2.3 seconds
```

### 3. Open the Notebook
```bash
jupyter notebook Brickhub_Investment_Analysis.ipynb
```

### 4. Regenerate Submission Documents (Optional)
```bash
python make_deliverables.py
```

---

## 🛡️ Data Provenance & AI Disclosure

1. **Infrastructure Facts:** 100% verified against official government documentation (PMRDA, Maha Metro Rail, NHAI, and Pune Municipal Corporation).
2. **Sales Deeds & Rental Records:** Calibrated synthetic samples anchored to published Knight Frank, Square Yards, and NoBroker 2025–2026 Pune residential market benchmark reports.
3. **AI Tooling Disclosure:** LLM search was utilized for public transit research and documentation scaffolding. All quantitative scoring formulas, normalization bounds, Dirichlet simulation parameters, and business logic were human-supervised, verified, and unit-tested.
