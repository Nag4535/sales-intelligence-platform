import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

# ── CONFIG ────────────────────────────────
DB_PATH = "database/sales.db"
DATA_PATH = "data/train.csv"

def create_database():
    """Create database folder if not exists"""
    os.makedirs("database", exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    print("✅ Database created!")
    return engine

def extract_data():
    """Extract data from CSV"""
    df = pd.read_csv(DATA_PATH, encoding='utf-8')
    print(f"✅ Extracted {len(df)} rows, {df.shape[1]} columns")
    return df

def transform_data(df):
    """Clean and transform data"""
    # Parse dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)

    # Extract date features
    df['Year']         = df['Order Date'].dt.year
    df['Month']        = df['Order Date'].dt.month
    df['Quarter']      = df['Order Date'].dt.quarter
    df['MonthName']    = df['Order Date'].dt.strftime('%B')
    df['YearMonth']    = df['Order Date'].dt.to_period('M').astype(str)

    # Shipping days
    df['ShippingDays'] = (df['Ship Date'] - df['Order Date']).dt.days

    # Sales bands
    df['SalesBand'] = pd.cut(
        df['Sales'],
        bins=[0, 100, 500, 1000, 10000],
        labels=['Low', 'Medium', 'High', 'Very High']
    )

    # Remove duplicates and nulls
    df = df.drop_duplicates()
    df = df.dropna(subset=['Sales'])

    print(f"✅ Transformed data — {len(df)} clean rows")
    return df

def load_data(df, engine):
    """Load data into SQLite database"""
    df.to_sql('sales', engine, if_exists='replace', index=False)
    print(f"✅ Loaded {len(df)} rows into database!")

def run_pipeline():
    """Run full ETL pipeline"""
    print("\n🚀 Starting ETL Pipeline...")
    print("=" * 40)
    engine = create_database()
    df     = extract_data()
    df     = transform_data(df)
    load_data(df, engine)
    print("=" * 40)
    print("✅ ETL Pipeline completed successfully!")
    return df

if __name__ == "__main__":
    run_pipeline()