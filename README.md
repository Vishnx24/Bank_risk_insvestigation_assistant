# 🏦 Banking Transaction Risk Investigation Assistant

### Hackathon Project — TRACK_ID: PS06

An AI-powered **Banking Transaction Risk Investigation Assistant** that analyzes a customer's transaction history, identifies unusual activity using explainable risk rules, and uses **Google Gemini** to generate a concise investigation report for human investigators.

> **Important:** The system identifies risk indicators. It does **not** determine or claim that fraud has occurred. Final judgment remains with a human investigator.

---

## 🚨 Problem Statement

Banks process thousands of customer transactions every day. Most transactions are routine, but a small number may contain unusual patterns that require investigation.

Manually reviewing months of transaction history is:

* Time-consuming
* Difficult to scale
* Prone to human oversight
* Difficult to explain consistently

The goal of this project is to build an intelligent assistant that automatically reviews transaction histories and highlights activity that deserves closer investigation.

---

## 💡 Solution

The **Banking Transaction Risk Investigation Assistant** combines:

1. Transaction preprocessing
2. Customer behaviour profiling
3. Explainable risk rules
4. Risk scoring
5. Transaction relationship analysis
6. Google Gemini-powered explanation
7. Human-readable investigation reports

The system compares transactions against the customer's own historical behaviour rather than simply treating every unusual transaction as fraud.

---

## 🎯 Objectives

* Analyze several months of customer transaction history.
* Detect unusually large transactions.
* Detect transactions involving newly observed payees.
* Detect unusual transaction times.
* Detect bursts of transactions within a short period.
* Detect transactions that differ significantly from the customer's normal behaviour.
* Assign explainable risk scores.
* Show the exact transactions that triggered rules.
* Generate an AI-assisted investigation report using Gemini.
* Maintain transaction traceability.
* Keep the final decision with a human investigator.

---

## 🔍 Risk Indicators

The project currently uses five major risk indicators.

### 1. Large Transaction

Identifies transactions significantly larger than the customer's normal transaction amount.

Example:

```text
Normal transaction: ₹1,500
Observed transaction: ₹75,000

→ Large Transaction Indicator
```

---

### 2. New Payee

Identifies transactions involving a payee that has not previously appeared in the customer's transaction history.

Example:

```text
Existing payees:
Amazon
SuperMart
Uber

New payee:
Unknown Payee

→ New Payee Indicator
```

---

### 3. Odd-Hours Activity

Identifies transactions outside the customer's configured normal activity period.

Example:

```text
Normal hours:
08:00 – 22:00

Transaction:
02:35 AM

→ Odd-Hours Indicator
```

---

### 4. Transaction Burst

Identifies multiple transactions occurring within a short period.

Example:

```text
02:35 → ₹75,000
02:42 → ₹70,000
02:50 → ₹65,000

Three transactions within minutes

→ Transaction Burst Indicator
```

---

### 5. Behavioural Deviation

Compares a transaction with the customer's established transaction behaviour.

Example:

```text
Typical transaction:
₹500 – ₹5,000

Observed transaction:
₹75,000

→ Significant Behavioural Deviation
```

---

# 🧠 System Architecture

```text
                  Customer Transaction History
                              │
                              ▼
                    ┌─────────────────┐
                    │  Preprocessing  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │Customer Profiling│
                    └────────┬────────┘
                             │
                             ▼
                     ┌───────────────┐
                     │   Risk Engine │
                     └───────┬───────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        Large Amount     New Payee      Odd Hours
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │ Burst Detection │
                    │ & Deviation     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Risk Scoring   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Google Gemini  │
                    │  AI Explanation │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Investigation   │
                    │     Report      │
                    └────────┬────────┘
                             │
                             ▼
                    Human Investigator
```

---

# 🤖 Gemini AI Integration

Google Gemini is used as the **explanation and report-generation layer**.

The Python risk engine first produces structured evidence.

Gemini then converts that evidence into a professional investigation report.

### Design principle

```text
Python Risk Engine
       ↓
Evidence + Risk Signals
       ↓
Google Gemini
       ↓
Explanation
       ↓
Investigator
```

The Gemini model is instructed to:

* Use only supplied evidence.
* Never invent transactions.
* Use exact transaction IDs.
* Never declare fraud.
* Explain triggered rules.
* Compare activity with the customer's baseline.
* Explain relationships between transactions.
* Recommend investigation priorities.

This provides an important separation between **risk detection** and **AI explanation**.

---

# 🛠️ Technology Stack

| Technology        | Purpose                  |
| ----------------- | ------------------------ |
| Python            | Core development         |
| Pandas            | Transaction processing   |
| FastAPI           | Backend API              |
| Uvicorn           | API server               |
| Google Gemini API | AI investigation report  |
| python-dotenv     | API key management       |
| CSV               | Transaction data storage |
| Streamlit         | Optional interactive UI  |

---

# 📁 Project Structure

```text
banking-risk-assistant/
│
├── data/
│   └── transactions.csv
│
├── risk_engine/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── profiling.py
│   ├── rules.py
│   └── scoring.py
│
├── llm/
│   ├── __init__.py
│   └── llm_report.py
│
├── reports/
│   ├── __init__.py
│   └── investigation_report.txt
│
├── server.py
├── main.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 📊 Dataset

The project uses a transaction CSV containing:

```text
transaction_id
date
description
payee
amount
channel
```

Example:

```csv
transaction_id,date,description,payee,amount,channel
TXN0001,2026-01-05 10:30,Grocery,SuperMart,850,UPI
TXN0002,2026-01-08 19:20,Food,Restaurant A,650,UPI
TXN0003,2026-01-15 11:10,Salary,ABC Ltd,45000,Bank Transfer
TXN0004,2026-02-02 10:15,Grocery,SuperMart,920,UPI
```

The hackathon demonstration dataset contains **1,000 transaction samples** covering multiple months.

---

# ⚙️ Installation

## Step 1 — Clone the project

```bash
git clone <your-github-repository-url>
cd banking-risk-assistant
```

---

## Step 2 — Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Gemini API Configuration

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

The application reads the API key from the environment.

### Never commit the API key to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# ▶️ Running the Project

## Option 1 — Run the Python application

```bash
python main.py
```

The system will:

```text
Load transactions
      ↓
Create customer profile
      ↓
Run risk rules
      ↓
Calculate risk score
      ↓
Send structured evidence to Gemini
      ↓
Generate investigation report
```

The report is saved in:

```text
reports/ai_investigation_report.txt
```

---

# 🌐 Running the FastAPI Server

The project is configured to run on **port 8000**.

Start the server:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at:

```text
http://localhost:8000
```

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

Use:

```text
POST /analyze
```

Upload:

```text
transactions.csv
```

The API returns:

* Number of transactions analyzed
* Overall risk level
* Risk score
* Customer profile
* Triggered findings
* AI-generated investigation report

---

# 🖥️ Streamlit Interface

If the Streamlit interface is included, run:

```bash
streamlit run app.py
```

The interface allows the investigator to:

1. Upload transaction CSV.
2. Analyze transactions.
3. View risk indicators.
4. View risk scores.
5. Generate the Gemini investigation report.
6. Download the report.

---

# 📄 Example Investigation Output

```text
==================================================
AI INVESTIGATION REPORT
==================================================

## 1. Overall Finding

ATTENTION REQUIRED

Several transactions triggered configured
risk indicators and should be reviewed by
a human investigator.

## 2. Executive Summary

Transactions TXN1001, TXN1002 and TXN1003
occurred within a short period and involved
large amounts.

## 3. Transactions Requiring Attention

TXN1001
Amount: ₹75,000
Channel: IMPS
Payee: Unknown Payee

TXN1002
Amount: ₹70,000
Channel: IMPS
Payee: Unknown Payee

TXN1003
Amount: ₹68,000
Channel: IMPS
Payee: Unknown Payee

## 4. Triggered Risk Rules

- Large Transaction
- New Payee
- Odd-Hours Activity
- Transaction Burst
- Behavioural Deviation

## 5. Difference From Normal Behaviour

The flagged transactions are substantially
larger than the customer's typical transaction
amount.

## 6. Connection Between Transactions

The transactions occurred within minutes of
each other and used the same payee and channel.

## 7. Investigation Priority

1. Verify the beneficiary/payee details.
2. Review the authentication and transaction
   authorization records.
3. Check whether the customer recognizes the
   transactions.

## 8. Important Disclaimer

The system identifies risk indicators only.
It does not establish that fraud has occurred.
Final judgment must be made by a human investigator.
```

---

# 🔐 Explainability & Traceability

A major feature of the project is **explainable risk detection**.

For every flagged transaction, the system maintains:

```text
Transaction ID
      ↓
Triggered Rule
      ↓
Reason
      ↓
Risk Score
      ↓
Evidence
```

For example:

```text
TXN1001
   │
   ├── Large Transaction
   │
   ├── New Payee
   │
   ├── Odd Hours
   │
   └── Behavioural Deviation
```

This makes the result easier for a human investigator to verify.

---

# 🛡️ Responsible AI

The system follows a human-in-the-loop approach.

### The AI does:

* Identify risk indicators.
* Explain unusual activity.
* Summarize evidence.
* Suggest investigation priorities.

### The AI does NOT:

* Declare fraud.
* Accuse customers.
* Make final banking decisions.
* Invent transaction information.
* Replace human investigators.

```text
AI Assistant
     ↓
Risk Evidence
     ↓
Human Review
     ↓
Final Decision
```

---

# 🚀 Future Enhancements

Future versions could include:

### 1. Machine Learning

Add anomaly detection models such as:

* Isolation Forest
* Autoencoders
* One-Class SVM

### 2. Advanced Customer Profiling

Build separate behavioural profiles for:

* UPI
* NEFT
* IMPS
* Card transactions
* Income
* Spending
* Transfers

### 3. Transaction Relationship Graph

Represent relationships between:

```text
Customer
   ↓
Payee
   ↓
Transaction
   ↓
Channel
   ↓
Time
```

This can help investigators identify connected activity.

### 4. Database Integration

Replace CSV storage with:

* SQLite
* PostgreSQL
* MySQL

### 5. Real-Time Monitoring

Process transactions as they occur instead of analyzing historical CSV files.

### 6. Investigator Dashboard

Add:

* Risk charts
* Transaction timelines
* Payee networks
* Risk heatmaps
* Investigation workflow

### 7. PDF Investigation Reports

Generate downloadable professional PDF reports.

---

# 🏆 Hackathon Innovation

The key innovation is the combination of:

```text
Rule-Based Detection
        +
Customer-Specific Behaviour
        +
Explainable Risk Scoring
        +
Gemini AI Explanation
        +
Human Investigation
```

Instead of simply saying:

> "This transaction is suspicious."

the system explains:

```text
WHAT happened
      ↓
WHY it was flagged
      ↓
HOW it differs from normal behaviour
      ↓
WHICH transactions are connected
      ↓
WHAT the investigator should check first
```

This makes the system more useful for real-world banking investigation workflows.

---

# 📌 Key Benefits

* ⚡ Faster transaction review
* 🔍 Explainable risk detection
* 📊 Customer-specific behavioural analysis
* 🤖 Gemini-powered investigation summaries
* 🔗 Transaction relationship analysis
* 🧾 Traceable evidence
* 🛡️ Human-in-the-loop decision making
* 📈 Scalable architecture
* 🔐 API key protection

---

# 👥 Team

**Hackathon Project**

### Project Title

**Banking Transaction Risk Investigation Assistant**

### Track ID

**PS06**

---

# 📜 Disclaimer

This project is a prototype developed for educational and hackathon purposes.

It identifies transaction patterns that may require additional investigation. It does not determine whether a transaction is fraudulent and should not be used as the sole basis for financial, legal, or customer-account decisions.

All final decisions should be made by qualified human investigators following applicable banking policies and regulations.

---

## ⭐ Project Flow

```text
             TRANSACTION HISTORY
                     │
                     ▼
              DATA PROCESSING
                     │
                     ▼
             CUSTOMER PROFILE
                     │
                     ▼
              RISK DETECTION
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Amount       Payee        Time
        │            │            │
        └────────────┼────────────┘
                     ▼
               RISK SCORING
                     │
                     ▼
              GEMINI AI
                     │
                     ▼
          INVESTIGATION REPORT
                     │
                     ▼
           HUMAN INVESTIGATOR
```

**Built for Hackathon — Banking Risk Intelligence & Explainable AI**
