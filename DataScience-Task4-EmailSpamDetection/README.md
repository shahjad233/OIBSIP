# OIBSIP Data Science Task 4 – Email Spam Detection

Includes class distribution, text preprocessing, TF-IDF explanation, stratified train/test split, Multinomial Naive Bayes and Logistic Regression, accuracy/precision/recall/F1, confusion matrices, recall discussion, optional word clouds, and saved model.

## Dataset
`data/sample_spam.csv` is synthetic demo data for smoke testing only. For internship submission download the SMS Spam Collection from UCI/Kaggle and place its CSV in `data/`. The notebook automatically selects a CSV other than `sample_spam.csv`. Supported schemas: UCI `v1`,`v2`; `label`,`message`; `category`,`text`. If the UCI download is tab-separated text, export it to CSV with headers `label,message`.

## Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python setup.py install
python setup.py check
python setup.py notebook
```
If activation is blocked, use `.\.venv\Scripts\python.exe setup.py install` and similarly for `check`/`notebook`.

Run all cells top to bottom. Charts, metrics CSV and saved classifier are written to `outputs/`. Use the real dataset and actual metrics for submission; never present synthetic sample results as real. Add screenshots to `screenshots/`.
