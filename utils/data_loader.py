import pandas as pd
import os

PROC_PATH = "data/processed"

# ---------- 1. Tourism Trends ----------
def get_tourism_annual_summary():
    df = pd.read_csv(os.path.join(PROC_PATH, "tourism_fee_final.csv"))
    return df.groupby("year")["total_fee_cr"].sum().reset_index()

def get_tourism_monthly_avg():
    df = pd.read_csv(os.path.join(PROC_PATH, "tourism_fee_final.csv"))
    return df.groupby("month")["total_fee_cr"].mean().reset_index()

def get_recovery_speed_by_year():
    df = pd.read_csv(os.path.join(PROC_PATH, "tourism_fee_final.csv"))
    annual = df.groupby("year")["total_fee_cr"].sum().reset_index()
    annual["yoy_growth_pct"] = annual["total_fee_cr"].pct_change().round(2) * 100
    return annual

def get_peak_tourism_months():
    df = pd.read_csv(os.path.join(PROC_PATH, "tourism_fee_final.csv"))
    return df.groupby("month")["total_fee_cr"].sum().reset_index().sort_values(by="total_fee_cr", ascending=False)


# ---------- 2. Economic Impact ----------
def get_forex_earnings_summary():
    return pd.read_csv(os.path.join(PROC_PATH, "foreign_exchange_earnings.csv"))

def get_funding_vs_tourism_by_year():
    tourism = pd.read_csv(os.path.join(PROC_PATH, "tourism_fee_final.csv"))
    funding = pd.read_csv(os.path.join(PROC_PATH, "state_cultural_funding.csv"))
    t = tourism.groupby("year")["total_fee_cr"].sum()
    f = funding.groupby("YEAR")["FUND_ALLOCATED_CR"].sum()
    return pd.DataFrame({
        "year": t.index,
        "total_tourism_fee_cr": t.values,
        "total_funding_cr": f.reindex(t.index, fill_value=0).values
    })



# ---------- 3. Global Standing ----------
def get_india_vs_world_growth():
    df = pd.read_csv(os.path.join(PROC_PATH, "international_tourism_stats.csv"))
    return df[["YEAR", "WORLD_RECEIPTS_GROWTH_RATE", "INDIA_SHARE_GROWTH_RATE", "INDIA_RANK"]]

def get_india_global_share_trend():
    df = pd.read_csv(os.path.join(PROC_PATH, "international_tourism_stats.csv"))
    return df[["YEAR", "INDIA_SHARE_PCT", "INDIA_SHARE_USD_MILLION", "INDIA_RANK"]]


# ---------- 4. Government Funding Overview ----------
def get_funding_by_state():
    df = pd.read_csv(os.path.join(PROC_PATH, "state_cultural_funding.csv"))
    return df.groupby("STATE")["FUND_ALLOCATED_CR"].sum().reset_index().sort_values(by="FUND_ALLOCATED_CR", ascending=False)

def get_funding_by_year():
    df = pd.read_csv(os.path.join(PROC_PATH, "state_cultural_funding.csv"))
    return df.groupby("YEAR")["FUND_ALLOCATED_CR"].sum().reset_index()

def get_funding_by_agency():
    df = pd.read_csv(os.path.join(PROC_PATH, "state_cultural_funding.csv"))
    return df.groupby("AGENCY")["FUND_ALLOCATED_CR"].sum().reset_index().sort_values(by="FUND_ALLOCATED_CR", ascending=False)

def get_top_funded_states(n=10):
    return get_funding_by_state().head(n)

def get_state_funding_trends():
    df = pd.read_csv(os.path.join(PROC_PATH, "state_cultural_funding.csv"))
    top_states = get_top_funded_states()["STATE"].tolist()
    return df[df["STATE"].isin(top_states)].groupby(["STATE", "YEAR"])["FUND_ALLOCATED_CR"].sum().reset_index()


# ---------- 5. ROI & Correlation (Placeholders) ----------
def get_funding_vs_tourism_states():
    # Only funding available by state, placeholder until tourism-by-state added
    return get_funding_by_state()

def get_low_funding_high_impact_states():
    df = get_funding_by_state()
    return df[df["FUND_ALLOCATED_CR"] < 200]

def get_high_funding_low_impact_states():
    df = get_funding_by_state()
    return df[df["FUND_ALLOCATED_CR"] > 2000]


# ---------- 6. Outliers & Rankings ----------
def get_highest_growth_year():
    df = get_recovery_speed_by_year()
    return df.sort_values(by="yoy_growth_pct", ascending=False).head(1)

def get_lowest_growth_year():
    df = get_recovery_speed_by_year()
    return df.sort_values(by="yoy_growth_pct").head(1)
