from pathlib import Path
import re
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
COVID_CUTOFF = pd.Timestamp("2020-03-01")


def normalize_name(name):
    """Normalize dataset headers to lowercase underscore names."""
    name = str(name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def find_dataset():
    """Find a non-sample CSV in data/; fail with a helpful message if absent."""
    files = sorted(p for p in DATA_DIR.glob("*.csv") if p.name.lower() != "sample_unemployment.csv")
    if not files:
        raise FileNotFoundError(
            "No real dataset found. Download the Kaggle 'Unemployment in India' CSV "
            "and place it inside the data/ folder."
        )
    return files[0]


def load_and_clean_data(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = [normalize_name(c) for c in df.columns]

    aliases = {
        "region": ["region", "state", "states"],
        "date": ["date", "month"],
        "unemployment_rate": [
            "estimated_unemployment_rate", "estimated_unemployment_rate_",
            "estimated_unemployment_rate_percent", "unemployment_rate",
            "unemployment_rate_percent"
        ],
        "estimated_employed": ["estimated_employed", "employed", "employment"],
        "labour_participation_rate": [
            "estimated_labour_participation_rate",
            "estimated_labour_participation_rate_",
            "estimated_labour_participation_rate_percent",
            "labour_participation_rate", "labor_participation_rate"
        ],
    }

    rename = {}
    for target, candidates in aliases.items():
        for candidate in candidates:
            if candidate in df.columns:
                rename[candidate] = target
                break
    df = df.rename(columns=rename)

    required = ["region", "date", "unemployment_rate", "estimated_employed", "labour_participation_rate"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns after header normalization: {missing}\n"
            f"Columns found: {list(df.columns)}\n"
            "Check that you downloaded the correct 'Unemployment in India' dataset."
        )

    df["region"] = df["region"].astype("string").str.strip()
    df["date"] = pd.to_datetime(df["date"].astype(str).str.strip(), dayfirst=True, errors="coerce")
    numeric_cols = ["unemployment_rate", "estimated_employed", "labour_participation_rate"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False).str.strip(),
            errors="coerce"
        )

    before = len(df)
    df = df.dropna(subset=required).copy()
    df = df[df["region"].ne("") & df["unemployment_rate"].between(0, 100)
            & df["labour_participation_rate"].between(0, 100)
            & df["estimated_employed"].ge(0)]
    df = df.drop_duplicates().sort_values("date").reset_index(drop=True)
    print(f"Rows before cleaning: {before:,}")
    print(f"Rows after cleaning:  {len(df):,}")
    if df.empty:
        raise ValueError("No valid rows remain after cleaning. Check the CSV format and values.")

    # The source provides employed counts and labour participation %, not a direct employment-rate column.
    # This derives an implied employment-to-population ratio and labels it explicitly.
    df["implied_employment_rate"] = (
        df["labour_participation_rate"] * (1 - df["unemployment_rate"] / 100)
    )
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


def main():
    sns.set_theme(style="whitegrid")
    csv_path = find_dataset()
    print(f"Using dataset: {csv_path.name}")
    df = load_and_clean_data(csv_path)

    print("\n--- Dataset inspection ---")
    print("Shape:", df.shape)
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isna().sum())
    print("\nPreview:\n", df.head())

    # 1. Region-wise average unemployment rate
    region_avg = df.groupby("region", as_index=False)["unemployment_rate"].mean()
    region_avg = region_avg.sort_values("unemployment_rate", ascending=False)
    plt.figure(figsize=(12, 7))
    sns.barplot(data=region_avg, x="unemployment_rate", y="region", color="steelblue")
    plt.title("Average Unemployment Rate by Region")
    plt.xlabel("Average unemployment rate (%)")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "region_average_unemployment.png", dpi=150)
    plt.show()
    print("Observation: The regions at the top of this chart have the highest average unemployment rates over the available observation period. Check sample coverage before interpreting rankings.")

    # 2. Month-wise overall trend
    monthly = df.groupby("month", as_index=False)["unemployment_rate"].mean()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="month", y="unemployment_rate", marker="o")
    plt.title("Monthly Average Unemployment Rate in India")
    plt.xlabel("Month")
    plt.ylabel("Average unemployment rate (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_unemployment_trend.png", dpi=150)
    plt.show()
    peak = monthly.loc[monthly["unemployment_rate"].idxmax()]
    print(f"Observation: The highest monthly average in this dataset is {peak['unemployment_rate']:.2f}% in {peak['month']:%B %Y}. This describes the supplied dataset, not necessarily every person or region in India.")

    # 3. Time-series for at least three regions with the most observations
    counts = df.groupby("region")["date"].nunique().sort_values(ascending=False)
    selected_regions = counts.head(3).index.tolist()
    trend3 = df[df["region"].isin(selected_regions)].groupby(
        ["month", "region"], as_index=False
    )["unemployment_rate"].mean()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=trend3, x="month", y="unemployment_rate", hue="region", marker="o")
    plt.title("Unemployment Rate Over Time – Three Regions")
    plt.xlabel("Month")
    plt.ylabel("Unemployment rate (%)")
    plt.xticks(rotation=45)
    plt.legend(title="Region")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "three_region_time_series.png", dpi=150)
    plt.show()
    print("Observation: This chart compares the direction and timing of changes across the three regions with the broadest date coverage:", ", ".join(selected_regions) + ". A rise or fall should be interpreted in the context of each region's data coverage.")

    # 4. Top 10 regions
    top10 = region_avg.head(10)
    plt.figure(figsize=(11, 6))
    sns.barplot(data=top10, x="unemployment_rate", y="region", color="coral")
    plt.title("Top 10 Regions by Average Unemployment Rate")
    plt.xlabel("Average unemployment rate (%)")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_10_regions.png", dpi=150)
    plt.show()
    print("Observation: The bars rank the ten regions with the highest mean unemployment rate across the available dates. Averages can hide short-term spikes, so compare this chart with the time-series plots.")

    # 5. Correlation heatmap
    corr_cols = ["unemployment_rate", "implied_employment_rate", "labour_participation_rate"]
    corr = df[corr_cols].corr(numeric_only=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", square=True)
    plt.title("Correlation: Unemployment, Implied Employment and Labour Participation")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150)
    plt.show()
    print("Observation: Correlation indicates association, not causation. The employment-rate measure is derived from labour participation and unemployment rates because the source dataset does not supply a direct employment-rate percentage.")

    # 6. Pre-COVID vs post-COVID
    df["period"] = np.where(df["date"] < COVID_CUTOFF, "Pre-COVID (before Mar 2020)", "Post-COVID (Mar 2020 onward)")
    comparison = df.groupby("period", as_index=False).agg(
        mean_unemployment_rate=("unemployment_rate", "mean"),
        mean_implied_employment_rate=("implied_employment_rate", "mean"),
        mean_labour_participation_rate=("labour_participation_rate", "mean"),
        observations=("unemployment_rate", "size")
    )
    print("\n--- Pre-COVID vs Post-COVID comparison ---")
    print(comparison.to_string(index=False))
    comparison.to_csv(OUTPUT_DIR / "pre_post_covid_summary.csv", index=False)

    plt.figure(figsize=(10, 5))
    plot_data = comparison.melt(
        id_vars="period",
        value_vars=["mean_unemployment_rate", "mean_implied_employment_rate", "mean_labour_participation_rate"],
        var_name="metric", value_name="mean_percent"
    )
    sns.barplot(data=plot_data, x="metric", y="mean_percent", hue="period")
    plt.title("Average Labour Market Indicators: Pre-COVID vs Post-COVID")
    plt.xlabel("Indicator")
    plt.ylabel("Mean (%)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "pre_post_covid_comparison.png", dpi=150)
    plt.show()

    lookup = comparison.set_index("period")
    pre_label, post_label = "Pre-COVID (before Mar 2020)", "Post-COVID (Mar 2020 onward)"
    if pre_label in lookup.index and post_label in lookup.index:
        delta = lookup.loc[post_label, "mean_unemployment_rate"] - lookup.loc[pre_label, "mean_unemployment_rate"]
        direction = "higher" if delta > 0 else "lower"
        print(f"Observation: The post-COVID mean unemployment rate is {abs(delta):.2f} percentage points {direction} than the pre-COVID mean in this dataset. This is a descriptive comparison, not proof that COVID alone caused the difference.")
    else:
        print("Observation: Both periods are not represented in the supplied data, so a valid pre-/post-COVID comparison cannot be made.")

    print("\nAnalysis complete. Charts and summary saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
