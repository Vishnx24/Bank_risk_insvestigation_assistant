import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_investigation_report(
    findings,
    overall_risk,
    profile
):

    # ------------------------------------------------
    # No Risk Findings
    # ------------------------------------------------
    if not findings:

        return """
## 1. Overall Finding

NO ATTENTION REQUIRED

No configured risk rules were triggered in the
reviewed transaction history.

The activity appears broadly consistent with the
customer's established transaction behaviour.

No conclusion of fraud has been made.
"""


    # ------------------------------------------------
    # Prepare Evidence
    # ------------------------------------------------

    evidence = []

    for finding in findings:

        evidence.append({

            "transaction_id":
                finding["transaction_id"],

            "date":
                str(finding["date"]),

            "payee":
                finding["payee"],

            "amount":
                float(finding["amount"]),

            "channel":
                finding["channel"],

            "risk_score":
                finding["risk_score"],

            "rules": [

                {
                    "rule":
                        rule["rule"],

                    "reason":
                        rule["reason"]
                }

                for rule in finding["rules"]
            ]
        })


    evidence_json = json.dumps(
        evidence,
        indent=2
    )


    # ------------------------------------------------
    # Gemini Prompt
    # ------------------------------------------------

    prompt = f"""

You are a Banking Transaction Risk Investigation
Assistant.

Analyze ONLY the evidence provided below.

Your role is to help a human bank investigator
understand unusual transaction activity.

IMPORTANT RULES:

1. Never state that fraud occurred.
2. Never accuse the customer.
3. Never accuse the payee.
4. Never invent transaction information.
5. Every transaction mentioned must use its exact
   transaction_id.
6. Use only the supplied transaction evidence.
7. Clearly separate observed facts from recommendations.
8. Explain how unusual activity differs from the
   customer's normal behaviour.
9. Explain connections between suspicious transactions
   using only supplied information.
10. If evidence is insufficient, clearly say so.
11. The final decision must always be made by a
    human investigator.

CUSTOMER BASELINE

Median transaction amount:
₹{profile["median_amount"]:,.2f}

Average transaction amount:
₹{profile["average_amount"]:,.2f}

Typical activity hours:
08:00 - 22:00


RULE ENGINE RESULT

Status:
{overall_risk["status"]}

Risk Level:
{overall_risk["risk_level"]}

Risk Score:
{overall_risk["score"]}


TRANSACTION EVIDENCE

{evidence_json}


Generate the investigation report using exactly
these sections:

## 1. Overall Finding

State clearly whether attention is required.

## 2. Executive Summary

Briefly summarize the important activity.

## 3. Transactions Requiring Attention

List the exact transaction IDs and explain why
they were flagged.

## 4. Triggered Risk Rules

Explain which risk rules were triggered.

## 5. Difference From Normal Behaviour

Compare the flagged activity against the customer's
baseline.

## 6. Connection Between Transactions

Explain relationships based on:
- time
- payee
- amount
- channel
- transaction pattern

Only mention relationships supported by the evidence.

## 7. Investigation Priority

Give the first 3 things a human investigator
should review.

## 8. Important Disclaimer

Clearly state that the system identifies risk
indicators and does not establish fraud.

Keep the report factual, concise and professional.
"""


    # ------------------------------------------------
    # Gemini API Call
    # ------------------------------------------------

    response = client.models.generate_content(

        model="gemini-3.8-flash",

        contents=prompt
    )


    return response.text