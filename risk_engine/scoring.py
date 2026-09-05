from risk_engine.preprocesing import(
    check_large_transaction,
    check_new_payee, 
    check_odd_hours, 
    check_pattern_deviation, 
    check_transaction_burst
)

#create a analyze function  to find the risk score of each transaction based on the rules defined in the preprocessing module.

def analyze_transaction(transaction_data,profile):

    findings=[]

    for index,row in transaction_data.iterrows():

        transaction_findings=[]

        result=check_large_transaction(row,profile)
        if result:
            transaction_findings.append(result)

        result=check_new_payee(row,profile)
        if result:
            transaction_findings.append(result)

        result=check_odd_hours(row,profile)

        if result:
            transaction_findings.append(result) 

        result=check_pattern_deviation(row,profile)
        if result:
            transaction_findings.append(result)

        result=check_transaction_burst(transaction_data,index)
        if result:
            transaction_findings.append(result)

        if transaction_findings:

            total_score=sum(
                item["score"]
                for item in transaction_findings)
            
            findings.append({
                "transaction_id": row["transaction_id"],
                "date": row["date"],
                "payee": row["payee"],
                "amount": row["amount"],
                "channel": row["channel"],
                "risk_score": total_score,
                "rules": transaction_findings
            })
    return findings

#create a calculation function to calculate the overall risk score for the customer based on the individual transaction risk scores.    

def calculate_overall_risk(findings):

    if not findings:
        return {
            "status": "NO ATTENTION REQUIRED",
            "risk_level": "LOW",
            "score": 0
        }

    maximum_score = max(
        finding["risk_score"]
        for finding in findings
    )

    if maximum_score >= 80:
        level = "CRITICAL"

    elif maximum_score >= 60:
        level = "HIGH"

    elif maximum_score >= 30:
        level = "MEDIUM"

    else:
        level = "LOW"

    return {
        "status": "ATTENTION REQUIRED",
        "risk_level": level,
        "score": maximum_score
    }

