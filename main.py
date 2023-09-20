# Imports
import pandas as pd
import streamlit as st

# Setup Streamlit app
st.title('Salary of datascientist in 2023')




# Load CSV file into DataFrame
df = pd.read_csv('ds_salaries.csv')

print(df.head())
