import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Smart Expense Analyzer", layout="centered")

st.title("💸 AI-Powered Financial Behavior Analyzer")
st.write("Upload your expense data and get intelligent insights!")

# File upload
uploaded_file = st.file_uploader("Upload your expense CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Basic cleaning
    if "Amount" not in df.columns or "Category" not in df.columns:
        st.error("CSV must contain 'Amount' and 'Category' columns")
    else:
        st.success("File uploaded successfully!")

        # Show raw data
        with st.expander("📄 View Raw Data"):
            st.write(df)

        # Total spending
        total_spent = df["Amount"].sum()
        st.subheader(f"💰 Total Spending: ₹{total_spent}")

        # Category-wise spending
        category_spending = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        st.subheader("📂 Spending by Category")
        st.write(category_spending)

        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(category_spending, labels=category_spending.index, autopct="%1.1f%%")
        ax.set_title("Spending Distribution")
        st.pyplot(fig)

        # Budget input
        st.subheader("🎯 Budget Check")
        budget = st.number_input("Enter your total budget (₹)", value=5000)

        if total_spent > budget:
            st.error("🚨 You have exceeded your budget!")
        else:
            st.success("✅ You are within your budget!")

        # Monthly analysis (if Date exists)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
            monthly = df.groupby(df["Date"].dt.month)["Amount"].sum()

            st.subheader("📅 Monthly Spending")
            st.bar_chart(monthly)

        # 🔥 SMART INSIGHTS
        st.subheader("🧠 Smart Insights")

        highest_category = category_spending.idxmax()
        highest_amount = category_spending.max()

        st.write(f"⚠️ Highest spending category: **{highest_category} (₹{highest_amount})**")

        avg_spending = df["Amount"].mean()
        st.write(f"📊 Average expense per transaction: ₹{avg_spending:.2f}")

        # Insight conditions
        if highest_amount > total_spent * 0.4:
            st.warning("🚨 One category dominates your spending. Consider balancing expenses.")

        if "Food" in category_spending and category_spending["Food"] > total_spent * 0.3:
            st.warning("🍔 High food spending detected. Try reducing eating out.")

        # Savings suggestion
        recommended_savings = total_spent * 0.2
        st.info(f"💡 Suggested Savings Target (20% rule): ₹{recommended_savings:.0f}")

        st.success("✅ Analysis Complete!")

        # 🧍 SPENDING PERSONALITY
        st.subheader("🧍 Spending Personality")

        if "Food" in category_spending and category_spending["Food"] > total_spent * 0.4:
            st.warning("🍔 Impulse Spender: You spend heavily on food and instant gratification.")
        elif "Shopping" in category_spending and category_spending["Shopping"] > total_spent * 0.4:
            st.warning("🛍️ Lifestyle Spender: High spending on lifestyle and non-essentials.")
        elif highest_amount < total_spent * 0.25:
            st.success("💼 Balanced Spender: Your expenses are well distributed.")
        else:
            st.info("📊 Moderate Spender: You have some imbalance but manageable.")

        # ⚠️ RISK SCORE
        st.subheader("⚠️ Financial Risk Score")

        risk_score = (highest_amount / total_spent) * 100

        if risk_score > 50:
            st.error(f"🔴 High Risk ({risk_score:.1f}%) - Spending is too concentrated in one category")
        elif risk_score > 30:
            st.warning(f"🟠 Moderate Risk ({risk_score:.1f}%) - Needs attention")
        else:
            st.success(f"🟢 Low Risk ({risk_score:.1f}%) - Good financial balance")

        # 💡 PERSONALIZED ADVICE
        st.subheader("💡 Personalized Advice")

        if total_spent > budget:
            st.write("👉 Reduce unnecessary expenses immediately to stay within budget.")

        if "Food" in category_spending and category_spending["Food"] > total_spent * 0.3:
            st.write("👉 Try cooking at home more often to cut food costs.")

        if "Shopping" in category_spending:
            st.write("👉 Avoid impulse purchases. Set a monthly shopping limit.")

        if "Transport" in category_spending:
            st.write("👉 Consider carpooling or public transport to save money.")

        if highest_amount > total_spent * 0.5:
            st.write("👉 Diversify your spending to reduce financial risk.")

        st.info("💡 Follow the 50-30-20 rule: Needs (50%), Wants (30%), Savings (20%)")