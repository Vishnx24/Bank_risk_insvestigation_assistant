import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_id",
    "date",
    "description",
    "payee",
    "amount",
    "channel"
]


def load_transactions(file_path):
    df = pd.read_csv(file_path)

    # Check required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Convert date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove invalid rows
    df = df.dropna(
        subset=[
            "transaction_id",
            "date",
            "payee",
            "amount",
            "channel"
        ]
    )

    # Remove negative amounts
    df = df[df["amount"] >= 0]

    # Sort chronologically
    df = df.sort_values("date").reset_index(drop=True)

    # Add useful features
    df["hour"] = df["date"].dt.hour

    return df