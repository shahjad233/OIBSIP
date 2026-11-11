# OIBSIP Data Science – Task 2: Unemployment Analysis with Python

## Objective
Explore unemployment trends in India, compare regions, study monthly patterns, inspect correlations, and compare pre-COVID and post-COVID periods.

## Dataset
Download the **Unemployment in India** CSV from Kaggle:
https://www.kaggle.com/datasets/gokulrajkmv/unemployment-in-india

Place the downloaded CSV in this project's `data/` folder. The notebook searches that folder automatically and ignores `sample_unemployment.csv`.

Expected common columns:
- `Region`
- `Date`
- `Estimated Unemployment Rate (%)`
- `Estimated Employed`
- `Estimated Labour Participation Rate (%)`

Column names are normalized by the notebook. A CSV with equivalent column names is also accepted.

## Important methodology note
The commonly used Kaggle dataset contains **Estimated Employed** (a count), not a directly measured employment-rate percentage. To satisfy the requested correlation analysis without mislabelling a count as a rate, this project calculates an **implied employment-to-population ratio**:

`Estimated Labour Participation Rate × (1 − Unemployment Rate / 100)`

This is a derived estimate based on the dataset's labour-force definitions, not an independently supplied official employment-rate column. The notebook labels it clearly.

## Windows setup (PowerShell)
```powershell
cd DataScience-Task2-UnemploymentAnalysis
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m notebook
```

## Run
```powershell
jupyter notebook
```
Open `Unemployment_Analysis.ipynb` and run **Kernel → Restart Kernel and Run All Cells**.

You can also run the script:
```powershell
python unemployment_analysis.py
```

## Outputs
Charts and a CSV summary are saved to `outputs/`. The notebook also displays each chart inline.

## Before submitting
1. Use the real Kaggle CSV, not the synthetic sample.
2. Run all notebook cells successfully.
3. Review the printed observations and write your own short interpretations based on your results.
4. Save the notebook with outputs.
5. Add screenshots to `screenshots/`.
6. Do not claim sample-data results as real findings.
