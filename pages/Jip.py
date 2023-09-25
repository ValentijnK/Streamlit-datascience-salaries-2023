import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Setting page configuration
st.set_page_config(
    page_title='Jip',
    page_icon=':chart_with_upwards_trend:'
)

df = pd.read_csv(os.getcwd() + '/ds_salaries.csv')

# Filter job titles based on top 5 entries
column = df['job_title']
functie_per_group = df['job_title'].value_counts()
functie_100 = functie_per_group[functie_per_group > 100]
df_salary = df[df['job_title'].isin(functie_100.index)]

company_size_salary = df_salary.groupby('company_size')['salary_in_usd'].mean().round(0).sort_values(ascending=False).reset_index()
# barplot = sns.barplot(data=company_size_salary, x='company_size', y='salary_in_usd', errorbar='sd')
st.bar_chart(data=company_size_salary, x='company_size', y='salary_in_usd')