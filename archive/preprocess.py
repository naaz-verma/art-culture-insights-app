import pandas as pd
import os

RAW_PATH = "data/raw"
PROC_PATH = "data/processed"

# Ensure processed directory exists
os.makedirs(PROC_PATH, exist_ok=True)

# 1. Process Tourism Fee Data (normalize + fix 2021 scale)
def preprocess_tourism_fee():
    raw_file = os.path.join(RAW_PATH, "fee-from-tourism2019-21.csv")
    df = pd.read_csv(raw_file, encoding='ISO-8859-1')

    print("🔍 Raw Columns:", df.columns.tolist())
    
    # Clean column names: remove non-breaking space, extra spaces, upper case
    df.columns = (
        df.columns
        .str.upper()
        .str.replace('\xa0', ' ', regex=False)
        .str.replace(' +', ' ', regex=True)
        .str.strip()
    )
    
    print("🧼 Cleaned Columns:", df.columns.tolist())

    # Map the cleaned columns to years
    year_map = {
        'FEE FROM TOURISM (IN ? CRORE) - 2019': 2019,
        'FEE FROM TOURISM (IN ? CRORE) - 2020': 2020,
        'FEE FROM TOURISM (IN ? CRORE) - 2021': 2021,
        'FEE FROM TOURISM (IN ? CRORE) - 2023': 2023,
        'FEE FROM TOURISM (IN ? CRORE) - 2024': 2024,
    }

    # Find matching columns by substring to avoid hardcoding mismatch
    col_map = {}
    for col in df.columns:
        for target, year in year_map.items():
            if target in col:
                col_map[col] = year

    print(f"📅 Matched Columns for Years: {col_map}")

    records = []
    for col, year in col_map.items():
        for idx, row in df.iterrows():
            fee = row[col]
            if pd.notnull(fee):
                if year == 2021:
                    fee = round(fee / 100, 2)  # Convert Lakhs to Cr
                records.append([row['MONTH'], year, fee])

    clean_df = pd.DataFrame(records, columns=['month', 'year', 'total_fee_cr'])
    clean_df.to_csv(os.path.join(PROC_PATH, "tourism_fee_final.csv"), index=False)
    print("✅ tourism_fee_final.csv saved")




# 2. Process Foreign Exchange Earnings
def preprocess_forex():
    raw_file = os.path.join(RAW_PATH, "Foreign-exchange-earning2014-20.csv")
    df = pd.read_csv(raw_file)
    df.columns = ['year', 'forex_earnings_cr']
    df.to_csv(os.path.join(PROC_PATH, "foreign_exchange_earnings.csv"), index=False)
    print("✅ foreign_exchange_earnings.csv saved")


# 3. Process International Tourism Stats
def preprocess_international_tourism():
    raw_file = os.path.join(RAW_PATH, "internation-tourism2001-21.csv")
    df = pd.read_csv(raw_file, encoding='ISO-8859-1')
    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]
    # Rename weird quote character in rank column
    df.columns = [col.replace("’", "").replace("‘", "").replace("\x92", "") for col in df.columns]
    # Create calculated columns
    df['WORLD_RECEIPTS_BN'] = (df['WORLD_TOURISM_RECEIPTS'] / 1000).round(2)
    df['INDIA_RECEIPTS_BN'] = (df['WORLD_TOURISM_RECEIPTS_-_FEE_IN_INDIA'] / 1000).round(2)
    df.to_csv(os.path.join(PROC_PATH, "international_tourism_stats.csv"), index=False)
    print("✅ international_tourism_stats.csv saved")

# 4. Process Cultural Funding Data
def preprocess_cultural_funding():
    raw_file = os.path.join(RAW_PATH, "state-wise-finance-artcluture-2019-24.csv")
    df = pd.read_csv(raw_file, encoding='ISO-8859-1')

    print("🔍 Raw Columns:", df.columns.tolist())
    df.columns = [col.strip().upper().replace(" ", "_") for col in df.columns]
    print("🧼 Cleaned Columns:", df.columns.tolist())

    # Use actual column name after cleaning
    fund_col = 'AMOUNT_SANCTIONED(RS._L)'
    if fund_col not in df.columns:
        raise ValueError(f"❌ Column '{fund_col}' not found even after cleaning!")

    df = df[df[fund_col].notnull()].copy()
    df.rename(columns={
        'STATE': 'STATE_NAME',
        'NAME_OF_PROJECT': 'PROJECT_NAME',
        fund_col: 'FUND_ALLOCATED_LAKH'
    }, inplace=True)

    df['STATE_NAME'] = df['STATE_NAME'].str.strip()
    df['PROJECT_NAME'] = df['PROJECT_NAME'].str.strip()
    df['AGENCY'] = df['AGENCY'].str.strip()
    df['FUND_ALLOCATED_CR'] = (df['FUND_ALLOCATED_LAKH'] * 1e5 / 1e7).round(2)  # Convert Lakh Rs to Cr ₹

    df.to_csv(os.path.join(PROC_PATH, "state_cultural_funding.csv"), index=False)
    print("✅ state_cultural_funding.csv saved")




# # Run all processors
# if __name__ == "__main__":
#     preprocess_tourism_fee()
#     preprocess_forex()
#     preprocess_international_tourism()
#     preprocess_cultural_funding()
#     print("✅ All 4 datasets processed and saved to data/processed/")
