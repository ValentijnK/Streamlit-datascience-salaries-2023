import pandas as pd
import plotly.express as px

df = pd.read_csv('ds_salaries.csv')

cross_tab = pd.crosstab(df['job_title'], df['salary'])

correlation_matrix = cross_tab.corr()

fig = px.imshow(
    correlation_matrix,
    x=cross_tab.columns,
    y=cross_tab.columns,
    labels=dict(x="Salary Range", y="Job Title"),
    color_continuous_scale='coolwarm'
)

fig.update_layout(
    title='Correlation Heatmap between Job Titles and Salaries',
    xaxis_title='Salary Range',
    yaxis_title='Job Title',
)

fig.show()
