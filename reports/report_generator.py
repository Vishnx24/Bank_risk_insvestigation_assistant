from datetime import datetime


def generate_report(transaction_data, findings, overall_risk, profile):

    report = []

    report.append("=" * 60)
    report.append("BANKING TRANSACTION RISK INVESTIGATION REPORT")
    report.append("=" * 60)

    report.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report.append("")

    # Overall finding
    report.append("OVERALL FINDING")
    report.append("-" * 30)

    report.append(
        f"Status: {overall_risk['status']}"
    )

    report.append(
        f"Risk Level: {overall_risk['risk_level']}"
    )

    report.append(
        f"Maximum Risk Score: {overall_risk['score']}"
    )

    report.append("")

    # Customer profile
    report.append("CUSTOMER NORMAL PROFILE")
    report.append("-" * 30)

    report.append(
        f"Median Transaction: "
        f"₹{profile['median_amount']:,.2f}"
    )

    report.append(
        f"Average Transaction: "
        f"₹{profile['average_amount']:,.2f}"
    )

    report.append(
        "Normal Activity Hours: 08:00 - 22:00"
    )

    report.append("")

    # No findings
    if not findings:

        report.append(
            "No configured risk rules were triggered."
        )

        report.append(
            "The reviewed activity is broadly consistent "
            "with the customer's established behaviour."
        )

        report.append("")

        report.append(
            "No immediate investigation is recommended."
        )

        report.append("")

        report.append(
            "IMPORTANT: This system does not determine "
            "whether fraud has occurred."
        )

        return "\n".join(report)

    # Findings
    report.append("TRANSACTIONS REQUIRING ATTENTION")
    report.append("-" * 40)

    for finding in findings:

        report.append(
            f"\nTransaction ID: {finding['transaction_id']}"
        )

        report.append(
            f"Date: {finding['date']}"
        )

        report.append(
            f"Payee: {finding['payee']}"
        )

        report.append(
            f"Amount: ₹{finding['amount']:,.2f}"
        )

        report.append(
            f"Channel: {finding['channel']}"
        )

        report.append(
            f"Risk Score: {finding['risk_score']}"
        )

        report.append("Triggered Rules:")

        for rule in finding["rules"]:

            report.append(
                f"  - {rule['rule']}: "
                f"{rule['reason']}"
            )

    report.append("")
    report.append("INVESTIGATION PRIORITY")
    report.append("-" * 30)

    report.append(
        "1. Verify whether the customer authorized "
        "the highlighted transactions."
    )

    report.append(
        "2. Review the relationship with the highlighted payee."
    )

    report.append(
        "3. Review account activity immediately before "
        "and after the flagged transactions."
    )

    report.append(
        "4. Check whether the transaction pattern has "
        "a legitimate explanation."
    )

    report.append("")

    report.append(
        "IMPORTANT: Risk indicators do not establish fraud. "
        "Final judgement must be made by a qualified investigator."
    )

    return "\n".join(report)