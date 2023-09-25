import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('ds_salaries.csv')

cross_tab = pd.crosstab(df['job_title'], df['salary'])

correlation_matrix = cross_tab.corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap between Job Titles and Salaries')
plt.xlabel('Salary Range')
plt.ylabel('Job Title')

plt.show()
