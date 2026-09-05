import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_id",
    "date",
    "description",
    "payee",
    "amount",
    "channel"
]

#load all transaction in .csv file

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

###create a customer profile based on the transaction data, which includes median and 
# average transaction amounts, known payees, 
# common channels, and normal transaction hours.

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

#========================================
# create a rule to check
#=================================

#create a function to check for large transactions 

def check_large_transaction(row, profile):

    median_amount = profile["median_amount"]

    # Avoid division problems
    if median_amount <= 0:
        return None

    if row["amount"] >= median_amount * 5:

        ratio = row["amount"] / median_amount

        return {
            "rule": "UNUSUALLY_LARGE_TRANSFER",
            "score": 30,
            "reason": (
                f"Transaction amount ₹{row['amount']:,.2f} "
                f"is approximately {ratio:.1f}x the customer's "
                f"median transaction amount."
            )
        }

    return None

# create a function to check for new payees

def check_new_payee(row,profile):

    if row["payee"] not in profile["known_payees"]:

        return{
            "rule":"NEW_PAYEE_DETECTED",
            "score":20,
            "reason":
                f"Transaction payee '{row['payee']}' is not in the customer's known payees."
                
                f"median transaction amount."
        }

    return None

#create a function to check for transactions outside normal hours

def check_odd_hours(row, profile):

    hour = row["hour"]

    if hour < profile["normal_start_hour"] or \
       hour >= profile["normal_end_hour"]:

        return {
            "rule": "ODD_HOURS_ACTIVITY",
            "score": 15,
            "reason": (
                f"Transaction occurred at {row['date'].strftime('%H:%M')}, "
                f"outside the customer's typical activity period."
            )
        }

    return None

#create a function to check for transactions that deviate significantly from the customer's established transaction pattern

def check_pattern_deviation(row, profile):

    median_amount = profile["median_amount"]

    if median_amount <= 0:
        return None

    if row["amount"] >= median_amount * 3:

        return {
            "rule": "BEHAVIOUR_PATTERN_DEVIATION",
            "score": 20,
            "reason": (
                "Transaction amount is significantly different "
                "from the customer's established transaction pattern."
            )
        }

    return None
#create a function to check for multiple transactions in a short time frame

def check_transaction_burst(transaction_data, index):

    current_time = transaction_data.loc[index, "date"]

    window_start = current_time - pd.Timedelta(minutes=30)

    nearby = transaction_data[
        (transaction_data["date"] >= window_start) &
        (transaction_data["date"] <= current_time)
    ]

    if len(nearby) >= 3:

        total_amount = nearby["amount"].sum()

        return {
            "rule": "TRANSACTION_BURST",
            "score": 25,
            "reason": (
                f"{len(nearby)} transactions totaling "
                f"₹{total_amount:,.2f} occurred within "
                f"approximately 30 minutes."
            )
        }

    return None
