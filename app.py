import streamlit as st
import pandas as pd

from risk_engine.preprocessing import load_transactions
from risk_engine.preprocessing import create_customer_profile
from risk_engine.scoring import (
    analyze_transaction,
    calculate_overall_risk
)
from reports.report_generator import generate_report


st.set_page_config(
    page_title="Banking Risk Investigation",
    layout="wide"
)

st.title("🏦 Banking Transaction Risk Investigation Assistant")

st.write(
    "Analyze a customer's transaction history and identify "
    "activity requiring investigation."
)

uploaded_file = st.file_uploader(
    "Upload Transaction CSV",
    type=["csv"]
)


if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Save temporary data
    df.to_csv(
        "data/uploaded_transactions.csv",
        index=False
    )

    try:

        # Preprocess
        df = load_transactions(
            "data/uploaded_transactions.csv"
        )

        # Profile
        profile = create_customer_profile(df)

        # Analyze
        findings = analyze_transaction(
            df,
            profile
        )

        # Overall risk
        overall_risk = calculate_overall_risk(
            findings
        )

        # Dashboard
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Transactions",
            len(df)
        )

        col2.metric(
            "Transactions Flagged",
            len(findings)
        )

        col3.metric(
            "Risk Level",
            overall_risk["risk_level"]
        )

        st.divider()

        if overall_risk["status"] == "ATTENTION REQUIRED":

            st.warning(
                "⚠️ ATTENTION REQUIRED"
            )

        else:

            st.success(
                "✅ NO ATTENTION REQUIRED"
            )

        st.subheader("Transaction History")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("Investigation Findings")

        if findings:

            for finding in findings:

                with st.expander(
                    f"{finding['transaction_id']} - "
                    f"₹{finding['amount']:,.2f}"
                ):

                    st.write(
                        f"**Payee:** {finding['payee']}"
                    )

                    st.write(
                        f"**Channel:** {finding['channel']}"
                    )

                    st.write(
                        f"**Risk Score:** "
                        f"{finding['risk_score']}"
                    )

                    st.write("### Triggered Rules")

                    for rule in finding["rules"]:

                        st.write(
                            f"**{rule['rule']}**"
                        )

                        st.write(
                            rule["reason"]
                        )

        else:

            st.success(
                "No configured risk rules were triggered."
            )

        # Generate report
        report = generate_report(
            df,
            findings,
            overall_risk,
            profile
        )

        st.subheader("Investigation Report")

        st.text(report)

        st.download_button(
            label="Download Report",
            data=report,
            file_name="investigation_report.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error(
            f"Error processing file: {e}"
        )