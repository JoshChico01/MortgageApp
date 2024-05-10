import streamlit as st
import pandas as pd
 

def run(interest, loan_amount, repayment_fortnightly):
    interest_rate = interest / 100

    interest_rate_daily = interest_rate / 365

    days = 0 
    year = 1 

    start_loan = loan_amount

    track = {"Years" : [0],
            "Amount" : [loan_amount]}

    interest_add = 0
    increasing = False

    total_repayments = 0

    while loan_amount > 0 and not increasing:
        if days % 14 == 0:
            loan_amount -= repayment_fortnightly

            total_repayments += repayment_fortnightly

        loan_amount += interest_rate_daily * loan_amount

            
        days += 1

        if days % 365 == 0:
            
            if days != 365:
                if track["Amount"][-1] < loan_amount:
                    increasing = True

            track["Years"].append(year)
            track["Amount"].append(loan_amount)

            year += 1

    total_repayments += loan_amount

    df = pd.DataFrame(track)


    if increasing:
        st.write("WARNING: Minimum Repayment Not Reached")
    else:
        st.write("""# Mortgage Projection
                 Mortgage amount at the end of each year""")
        st.bar_chart(df, x = "Years")
        st.write(f"""
                 Loan Amount: {start_loan:,}\n
                 Total Repayments: {round(total_repayments):,}\n
                 Interest Paid: {round(total_repayments - start_loan):,}
""")


st.write("Open sidebar and click run")

with st.sidebar:
    st.write("# Settings")

    interest = st.number_input("Interest Rate", value = 6.00, step = 0.05)

    loan_amount = st.number_input("Loan Amount", step = 500, value = 500000)

    repayment_fortnightly = st.number_input("Fortnightly Repayments", step = 50, value = 1500)

    st.button("Run", on_click=run, args = (interest, loan_amount, repayment_fortnightly) )


