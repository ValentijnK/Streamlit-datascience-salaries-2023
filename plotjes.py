# Bezem door de data
# Salary vs. experience lvl
# Salary over the years
# Slider

import streamlit as st

# Setup Streamlit app
st.title('Salary of datascientist in 2023')

import pandas as pd 
import numpy as np
df = pd.read_csv("ds_salaries.csv")

column = df['job_title']
functie_per_group = df['job_title'].value_counts()
functie_100 = functie_per_group[functie_per_group>100]
clean_data = df[df['job_title'].isin(functie_100.index)]
clean_data['work_year'] = clean_data['work_year'].astype('str')
# print(clean_data.head())

# print(clean_data.info())

x = 'experience_level'
y = 'salary_in_usd'

import seaborn as sns
import matplotlib.pyplot as plt

a = clean_data.groupby('experience_level')['salary_in_usd'].mean()



st.title("Salary Data Histogram")
plt.figure(figsize=(8, 6))
sns.histplot(data=clean_data, x='salary_in_usd', hue='experience_level', element='step', bins=10)
plt.xlabel("Salary (USD)")
plt.ylabel("Count")
plt.title("Salary Data Histogram")
st.pyplot()



st.title("Salary Data Boxplot by Experience Level")
plt.figure(figsize=(8, 6))
sns.boxplot(data=clean_data, x='experience_level', y='salary_in_usd', palette="Set2")
plt.xlabel("Experience Level")
plt.ylabel("Salary (USD)")
st.pyplot()




st.title("Salary Data Boxplot by Work year")
plt.figure(figsize=(12, 12))
sns.boxplot(data = clean_data, x = 'work_year', y = 'salary_in_usd', hue = 'experience_level',
            order = ['2020','2021','2022','2023'],
            hue_order=['EN','EX','MI','SE'])
plt.xlabel("Work year")
plt.ylabel("Salary (USD)")
st.pyplot()



#data groeperen
b = clean_data.groupby(['work_year', 'experience_level'])['salary_in_usd'].mean()
st.title("Salary Data Barplot by Work year")
plt.figure(figsize=(8, 6))
sns.barplot(data = b.reset_index(), x = 'work_year', y = 'salary_in_usd', 
            hue = 'experience_level', ci = None, 
            order = ['2020','2021','2022','2023'],
            hue_order=['EN','EX','MI','SE']
            )
plt.xlabel("Work year")
plt.ylabel("Salary (USD)")
st.pyplot()

st.bar_chart(data = b.reset_index(),  x = 'work_year', y = 'salary_in_usd', 
             color = 'experience_level',
             use_container_width  = False)

# print(b.reset_index())

