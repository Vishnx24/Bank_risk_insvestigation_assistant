import streamlit as st

from reports.report_generator import generate_report
from risk_engine.preprocessing import (
    create_customer_profile,
    load_transactions,
)
from risk_engine.scoring import (
    analyze_transaction,
    calculate_overall_risk,
)


st.set_page_config(
    page_title="Bank Risk Investigation Assistant",
    page_icon="🏦",
    layout="wide",
)

st.title("Bank Risk Investigation Assistant")
st.write("Upload a transaction CSV to review rule-based risk indicators.")

uploaded_file = st.file_uploader(
    "Choose a transaction CSV",
    type="csv",
)

if uploaded_file is not None:
    try:
        df = load_transactions(uploaded_file)
        profile = create_customer_profile(df)
        findings = analyze_transaction(df, profile)
        overall_risk = calculate_overall_risk(findings)

        st.subheader("Risk Summary")
        st.write(
            f"**Status:** {overall_risk['status']}  "
            f"**Risk level:** {overall_risk['risk_level']}  "
            f"**Score:** {overall_risk['score']}"
        )
        st.dataframe(df, use_container_width=True)

        report = generate_report(df, findings, overall_risk, profile)
        st.subheader("Investigation Report")
        st.text(report)
        st.download_button(
            label="Download Report",
            data=report,
            file_name="investigation_report.txt",
            mime="text/plain",
        )

        st.subheader("AI Investigation Report")
        if st.button("Generate AI Report"):
            with st.spinner("AI is analyzing the rule-based findings..."):
                try:
                    from llm.llm_report import generate_investigation_report

                    ai_report = generate_investigation_report(
                        findings,
                        overall_risk,
                        profile,
                    )
                    st.markdown(ai_report)
                    st.download_button(
                        label="Download AI Report",
                        data=ai_report,
                        file_name="ai_investigation_report.txt",
                        mime="text/plain",
                    )
                except (ImportError, ValueError) as error:
                    st.error(str(error))
    except Exception as error:
        st.error(f"Error processing file: {error}")
