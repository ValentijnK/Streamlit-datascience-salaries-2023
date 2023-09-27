import streamlit as st
import pandas as pd
from plotly import express as px

# Setting page configuration
st.set_page_config(
    page_title='Insights',
    page_icon=':chart_with_upwards_trend:'
)
df = pd.read_csv('ds_salaries.csv')

# Filter job titles based on top 5 entries
column = df['job_title']
functie_per_group = df['job_title'].value_counts()
functie_100 = functie_per_group[functie_per_group > 100]
df_salary = df[df['job_title'].isin(functie_100.index)]

# Salary per job role

df_salary_per_role = df_salary.groupby('job_title')['salary_in_usd'].mean().reset_index()
print(df_salary_per_role)
fig = px.bar(df_salary_per_role, color='job_title')
fig.update_layout(xaxis_title='Job Category', yaxis_title='Salary in USD', title='Average Salary per job category')
job_cat = ['Analytics Engineer', 'Data Analyst', 'Data Architect', 'Data Engineer', 'Data Scientist', 'Machine Learning Engineer']
fig.update_xaxes(
    tickvals=[0, 1, 2, 3, 4, 5],
    ticktext=job_cat
)

st.plotly_chart(fig)
# JIP
# Salary vs company size bar chart
company_size_salary = df_salary.groupby('company_size')['salary_in_usd'].mean().round(0).reset_index()
sorting_order = ['Large', 'Medium', 'Small']
fig = px.bar(company_size_salary, x='company_size', y='salary_in_usd')
fig.update_layout(xaxis_title='Company size', yaxis_title='Salary in USD', title='Average salary per company size')
fig.update_xaxes(
    tickvals=[0, 1, 2],
    ticktext=['Large', 'Medium', 'Small']
)
st.plotly_chart(fig)


# Salary vs company size box plot
fig = px.box(df_salary, x='company_size', y='salary_in_usd',
             labels={'salary_in_usd': 'Salary in USD', 'company_size': 'Company Size'},
             title='Salary vs. Company Size')
fig.update_xaxes(categoryorder='array', categoryarray=['L', 'M', 'S'], tickvals=[0, 1, 2], ticktext=['Large', 'Medium', 'Small'])
st.plotly_chart(fig)

# Chong
clean_data = df[df['job_title'].isin(functie_100.index)]
clean_data['work_year'] = clean_data['work_year'].astype('str')


# Salary historgram by experience level
fig = px.histogram(clean_data, x="salary_in_usd", nbins = 10, color = 'experience_level',
                   category_orders={'experience_level': ['SE', 'MI', 'EX', 'EN']},
                   text_auto = True)
# Overlay both histograms
fig.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.5)
fig.update_layout(
    title_text='Salary Histogram',
    xaxis_title_text='Salary (USD)',
    yaxis_title_text='Count'
)
st.plotly_chart(fig)


# Salary vs experience_level box plot
fig = px.box(clean_data, x='experience_level', y='salary_in_usd',
             labels={'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'},
             title='Salary vs Experience Level',
             color = 'experience_level',
             category_orders={'experience_level': ['EN', 'EX', 'MI', 'SE']},
             )
st.plotly_chart(fig)


# Salary vs experience_level box plot by year
fig = px.box(clean_data, x='work_year', y='salary_in_usd', color='experience_level',
             category_orders={'work_year': ['2020', '2021', '2022', '2023'],
                              'experience_level': ['EN', 'EX', 'MI', 'SE']},
             labels={'work_year': 'Work year', 'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'},
             title='Salary vs Experience level by work year')
st.plotly_chart(fig)
#Bij 2020 was heeft maar 1 medewerker expeience level as Ex, en bij 2021 is 0


#barplot gemiddeld salary per experience level per jaar
b = clean_data.groupby(['work_year', 'experience_level'])['salary_in_usd'].mean()

fig = px.bar(b.reset_index(), x='work_year', y='salary_in_usd', color='experience_level',
             category_orders={'work_year': ['2020', '2021', '2022', '2023'],
                              'experience_level': ['EN', 'EX', 'MI', 'SE']},
             labels={'work_year': 'Work year', 'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'},
             title='Salary by Experience Level by year')
st.plotly_chart(fig)


#line plot
fig = px.line(b.reset_index(), x='work_year', y='salary_in_usd', color='experience_level',
              category_orders={'work_year': ['2020', '2021', '2022', '2023'],
                               'experience_level': ['EN', 'EX', 'MI', 'SE']},
              labels={'work_year': 'Work year', 'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'},
              title='Salary by Experience Level by year')
fig.update_xaxes(type='category')
st.plotly_chart(fig)






