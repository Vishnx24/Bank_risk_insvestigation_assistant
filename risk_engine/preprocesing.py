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
    transaction_data = pd.read_csv(file_path)

    # Check required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in transaction_data.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Convert date
    transaction_data["date"] = pd.to_datetime(transaction_data["date"], errors="coerce")

    # Convert amount
    transaction_data["amount"] = pd.to_numeric(transaction_data["amount"], errors="coerce")

    # Remove invalid rows
    transaction_data = transaction_data.dropna(
        subset=[
            "transaction_id",
            "date",
            "payee",
            "amount",
            "channel"
        ]
    )

    # Remove negative amounts
    transaction_data = transaction_data[transaction_data["amount"] >= 0]

    # Sort chronologically
    transaction_data = transaction_data.sort_values("date").reset_index(drop=True)

    # Add useful features
    transaction_data["hour"] = transaction_data["date"].dt.hour

    return transaction_data

def create_customer_profile(transaction_data):

    profile = {}

    # Typical transaction amount
    profile["median_amount"] = transaction_data["amount"].median()
    profile["average_amount"] = transaction_data["amount"].mean()

    # Known payees
    profile["known_payees"] = set(
        transaction_data["payee"].dropna().unique()
    )

    # Common channels
    profile["common_channels"] = set(
        transaction_data["channel"].dropna().unique()
    )

    # Normal transaction hours
    profile["normal_start_hour"] = 8
    profile["normal_end_hour"] = 22

    return profile