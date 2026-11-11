# OIBSIP Data Science – Task 3: Car Price Prediction

## Includes

- Data cleaning, duplicate removal and category normalization
- Car age feature engineering and brand extraction when possible
- Selling-price distribution, fuel-type box plot, price-vs-age scatter plot
- Numeric correlation heatmap
- One-hot encoding, train/test split
- Linear Regression, Random Forest and Gradient Boosting
- MAE, RMSE, R² evaluation and feature importance
- Saved model and metrics

## Dataset

`data/sample_car_data.csv` is synthetic demo data to verify that the notebook runs. For the actual internship submission, downloaded a real **Vehicle dataset from cardekho** CSV from Kaggle and place it in `data/`. The notebook automatically selects the first CSV other than `cardekho_dataset.csv`.

Supported schemas include CarDekho columns (`Car_Name`, `Year`, `Selling_Price`, `Present_Price`, `Kms_Driven`, `Fuel_Type`, `Seller_Type`, `Transmission`, `Owner`) and alternate columns (`brand`, `model`, `year`, `fuel_type`, `transmission_type`, `distance_driven`, `selling_price`).

## Windows PowerShell setup

Run these commands from this project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python setup.py install
python setup.py check
python setup.py notebook
```

If activation is blocked:

```powershell
.\.venv\Scripts\python.exe setup.py install
.\.venv\Scripts\python.exe setup.py check
.\.venv\Scripts\python.exe setup.py notebook
```

Run all notebook cells from top to bottom. Charts and model outputs are saved in `outputs/`.

## Submission reminder

Use the real dataset, rerun the notebook, save screenshots in `screenshots/`, and complete the conclusion using actual model metrics. Do not submit synthetic-data metrics as real results.
