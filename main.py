from risk_engine.preprocessing import load_transactions
from risk_engine.preprocessing import create_customer_profile
from risk_engine.scoring import (
    analyze_transaction,
    calculate_overall_risk
)
from reports.report_generator import generate_report


DATA_FILE = "data/transactions.csv"


def main():

    print("\nLoading transaction history...")

    # Step 1: Load data
    df = load_transactions(DATA_FILE)

    print(f"Loaded {len(transaction_data)} transactions.")

    # Step 2: Create customer profile
    profile = create_customer_profile(df)

    print("Customer behavioural profile created.")

    # Step 3: Analyze transactions
    findings = analyze_transaction(
        transaction_data,
        profile
    )

    print(
        f"Found {len(findings)} transaction(s) "
        "requiring review."
    )

    # Step 4: Calculate risk
    overall_risk = calculate_overall_risk(
        findings
    )

    # Step 5: Generate report
    report = generate_report(
        transaction_data,
        findings,
        overall_risk,
        profile
    )

    # Display report
    print("\n")
    print(report)

    # Save report
    with open(
        "reports/investigation_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print(
        "\nReport saved to "
        "reports/investigation_report.txt"
    )


if __name__ == "__main__":
    main()