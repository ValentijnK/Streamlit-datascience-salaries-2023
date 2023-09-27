import streamlit as st
import pandas as pd
from plotly import express as px
import plotly.graph_objects as go
import country_converter as coco

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
country = coco.convert(names=df['company_location'], to="ISO3")
df['company_location'] = country

# Salary per job role
st.subheader('Average Salary per job category')
df_salary_per_role = df_salary.groupby('job_title')['salary_in_usd'].mean().reset_index()
print(df_salary_per_role)
fig = px.bar(df_salary_per_role, color='job_title')
fig.update_layout(xaxis_title='Job Category', yaxis_title='Salary in USD')
job_cat = ['Analytics Engineer', 'Data Analyst', 'Data Architect', 'Data Engineer', 'Data Scientist', 'Machine Learning Engineer']
fig.update_xaxes(
    tickvals=[0, 1, 2, 3, 4, 5],
    ticktext=job_cat
)
st.plotly_chart(fig)


# JIP
# Salary vs company size bar chart
st.subheader('Average salary per company size')
company_size_salary = df_salary.groupby('company_size')['salary_in_usd'].mean().round(0).reset_index()
sorting_order = ['Large', 'Medium', 'Small']
fig = px.bar(company_size_salary, x='company_size', y='salary_in_usd')
fig.update_layout(xaxis_title='Company size', yaxis_title='Salary in USD')
fig.update_xaxes(
    tickvals=[0, 1, 2],
    ticktext=['Large', 'Medium', 'Small']
)
st.plotly_chart(fig)


# Salary vs company size box plot
st.subheader('Salary vs. Company Size')
fig = px.box(df_salary, x='company_size', y='salary_in_usd',
             labels={'salary_in_usd': 'Salary in USD', 'company_size': 'Company Size'})
fig.update_xaxes(categoryorder='array', categoryarray=['L', 'M', 'S'], tickvals=[0, 1, 2], ticktext=['Large', 'Medium', 'Small'])
st.plotly_chart(fig)

# Avarage salary by Company Location
st.subheader('Average Salary by Company Location')
Large = st.checkbox('Large', value=True)
Medium = st.checkbox('Medium', value=True)
Small = st.checkbox('Small', value=True)
selected_sizes = []
if Large:
    selected_sizes.append('L')
if Medium:
    selected_sizes.append('M')
if Small:
    selected_sizes.append('S')
filtered_df = df[df['company_size'].isin(selected_sizes)]
salary_location = filtered_df.groupby(['salary_in_usd', 'company_location']).size().reset_index()
means = salary_location.groupby('company_location').mean().reset_index()

fig = px.choropleth(locations = means['company_location'], color = means['salary_in_usd'])
st.plotly_chart(fig)

# Chong
clean_data = df[df['job_title'].isin(functie_100.index)]
clean_data['work_year'] = clean_data['work_year'].astype('str')


# Salary historgram by experience level
st.subheader('Salary Histogram')
salary_range = st.slider("Select Salary Range (USD)", 
                         min_value=clean_data['salary_in_usd'].min(), 
                         max_value=clean_data['salary_in_usd'].max(), 
                         value=(clean_data['salary_in_usd'].min(), clean_data['salary_in_usd'].max()),
                         step=1000)

filtered_data = clean_data[(clean_data['salary_in_usd'] >= salary_range[0]) & (clean_data['salary_in_usd'] <= salary_range[1])]
fig = px.histogram(filtered_data, x="salary_in_usd", nbins = 10, color = 'experience_level',
                   category_orders={'experience_level': ['SE', 'MI', 'EX', 'EN']},
                   text_auto = True)
# Overlay both histograms
fig.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.5)
fig.update_layout(
    xaxis_title_text='Salary (USD)',
    yaxis_title_text='Count'
)
st.plotly_chart(fig)


# Salary vs experience_level box plot
st.subheader('Salary vs Experience Level')
fig = px.box(clean_data, x='experience_level', y='salary_in_usd',
             labels={'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'},
             color = 'experience_level',
             category_orders={'experience_level': ['EN', 'EX', 'MI', 'SE']},
             )
st.plotly_chart(fig)


# Salary vs experience_level box plot by year
st.subheader('Salary vs Experience level by work year')
fig = px.box(clean_data, x='work_year', y='salary_in_usd', color='experience_level',
             category_orders={'work_year': ['2020', '2021', '2022', '2023'],
                              'experience_level': ['EN', 'EX', 'MI', 'SE']},
             labels={'work_year': 'Work year', 'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'})
st.plotly_chart(fig)
#Bij 2020 was heeft maar 1 medewerker expeience level as Ex, en bij 2021 is 0


#barplot gemiddeld salary per experience level per jaar
b = clean_data.groupby(['work_year', 'experience_level'])['salary_in_usd'].mean()
st.subheader('Salary by Experience Level by year')
fig = px.bar(b.reset_index(), x='work_year', y='salary_in_usd', color='experience_level',
             category_orders={'work_year': ['2020', '2021', '2022', '2023'],
                              'experience_level': ['EN', 'EX', 'MI', 'SE']},
             labels={'work_year': 'Work year', 'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'})
st.plotly_chart(fig)


#line plot
st.subheader('Salary by Experience Level by year')
fig = px.line(b.reset_index(), x='work_year', y='salary_in_usd', color='experience_level',
              category_orders={'work_year': ['2020', '2021', '2022', '2023'],
                               'experience_level': ['EN', 'EX', 'MI', 'SE']},
              labels={'work_year': 'Work year', 'salary_in_usd': 'Salary in USD', 'experience_level': 'Experience level'})
fig.update_xaxes(type='category')
st.plotly_chart(fig)

st.button('Thank you for reading ', on_click=st.balloons)
