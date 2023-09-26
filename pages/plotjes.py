import streamlit as st

# Setup Streamlit app
st.title('Salary of datascientist')

import pandas as pd 

df = pd.read_csv("ds_salaries.csv")

column = df['job_title']
functie_per_group = df['job_title'].value_counts()
functie_100 = functie_per_group[functie_per_group>100]
clean_data = df[df['job_title'].isin(functie_100.index)]
clean_data['work_year'] = clean_data['work_year'].astype('str')


x = 'experience_level'
y = 'salary_in_usd'

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

a = clean_data.groupby('experience_level')['salary_in_usd'].mean()

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



