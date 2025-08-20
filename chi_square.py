import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

st.set_page_config(
    page_title="Chi-Square Test Online | Free Statistics Tool - WebxWorks",
    page_icon="/assets/favicon.ico",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("Chi-Square Test")

st.markdown("""
### 🧮 Chi-Square Test Online - provided by WebxWorks

Easily perform a **Chi-Square Test of Independence** online using your own dataset.  
Simply upload a CSV file, pick two categorical variables, and get the **contingency table**,  
the **Chi-Square statistic**, and the **p-value** instantly.

This free tool is perfect for **students, researchers, and data analysts** who want to check  
whether two variables are statistically independent without installing any software.
""")



uploaded_file = st.file_uploader("Upload a CSV", type=["csv"])

def create_contingency_table(data, col1, col2):
    return pd.crosstab(data[col1], data[col2])

def perform_chi_square(data, col1, col2):
    contingency_table = create_contingency_table(data, col1, col2)
    chi2, p_value, df, expected = chi2_contingency(contingency_table)
    result_table = pd.DataFrame({
        "Particulars": ["Pearson Chi-Square", "No. of Valid Cases"],
        "Value": [round(chi2, 3), contingency_table.to_numpy().sum()],
        "df": [df, ""],
        "Asymptotic Significance (2-sided)": [round(p_value, 3), ""]
    })
    significance = "✅ Significant (Reject Null Hypothesis)" if p_value < 0.05 else "❌ Not Significant (Fail to Reject Null Hypothesis)"
  
    return (contingency_table, result_table, expected, significance)

if uploaded_file is not None:
  
  data = pd.read_csv(uploaded_file)

  if len(data.columns) < 2:
        st.error("❗ The dataset must have at least 2 columns.")

  column_remaining = list(data.columns)
  column1 = st.selectbox("Select Column 1", column_remaining)
  column_remaining.remove(column1)
  column2 = st.selectbox("Select Column 2", column_remaining)
    
  st.write(f"Selected Variables: **{column1}** vs **{column2}**")

  is_clicked = st.button("Run Chi-Square Test")

  if is_clicked:
    contingency_table, result, expected, significance = perform_chi_square(data, column1, column2)
    tab1, tab2, tab3 = st.tabs(["📋 Contingency Table", "📊 Chi-Square Results", "ℹ️ Interpretation"])
    
    with tab1:
      st.subheader("Contingency Table")
      st.dataframe(contingency_table)

    with tab2:
      st.subheader("Chi-Square Results")
      st.dataframe(result)

    with tab3:
      st.subheader("Interpretation")
      st.success(significance)

    if (expected < 5).sum() > 0:
                    st.warning("⚠️ Some expected frequencies are less than 5. Chi-Square test may not be valid.")

    csv_result = result.to_csv(index=False).encode("utf-8")
    st.download_button(
                label="📥 Download Results as CSV",
                data=csv_result,
                file_name="chi_square_results.csv",
                mime="text/csv"
            )
