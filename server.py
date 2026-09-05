from fastapi import FastAPI, UploadFile, File
import pandas as pd
import tempfile
import os

from risk_engine.preprocessing import load_transactions
from risk_engine.preprocessing import create_customer_profile
from risk_engine.scoring import (
    analyze_transaction,
    calculate_overall_risk
)
from llm.llm_report import generate_investigation_report


app = FastAPI(
    title="Banking Transaction Risk Investigation Assistant",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Banking Risk Investigation Assistant is running",
        "status": "OK"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # Save uploaded CSV temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    ) as temp:

        content = await file.read()
        temp.write(content)
        temp_path = temp.name


    try:
        # Load transactions
        df = load_transactions(temp_path)

        # Customer profile
        profile = create_customer_profile(df)

        # Risk analysis
        findings = analyze_transactions(
            df,
            profile
        )

        # Overall risk
        overall_risk = calculate_overall_risk(
            findings
        )

        # Gemini AI report
        report = generate_investigation_report(
            findings,
            overall_risk,
            profile
        )


        return {
            "status": "success",
            "transactions_analyzed": len(df),

            "risk": overall_risk,

            "customer_profile": {
                "median_amount":
                    profile["median_amount"],

                "average_amount":
                    profile["average_amount"]
            },

            "findings": findings,

            "ai_investigation_report":
                report
        }


    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)