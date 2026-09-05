from risk_engine.preprocessing import load_transactions
from risk_engine.preprocessing import create_customer_profile
from risk_engine.scoring import (
    analyze_transaction,
    calculate_overall_risk
)

from llm.llm_report import generate_llm_report


DATA_FILE = "data/transactions.csv"


def main():

    print("Loading transactions...")

    df = load_transactions(DATA_FILE)

    print(
        f"Loaded {len(df)} transactions."
    )


    # Create customer baseline
    profile = create_customer_profile(df)

    print("Customer profile created.")


    # Rule-based analysis
    findings = analyze_transaction(
        df,
        profile
    )

    print(
        f"{len(findings)} transaction(s) "
        "require review."
    )


    # Risk score
    overall_risk = calculate_overall_risk(
        findings
    )


    print("Generating LLM investigation report...")


    # LLM
    report = generate_llm_report(
        findings,
        overall_risk,
        profile
    )


    print("\n")
    print("=" * 70)
    print(report)
    print("=" * 70)


    # Save report
    with open(
        "reports/llm_investigation_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)


    print(
        "\nReport saved successfully."
    )


if __name__ == "__main__":
    main()