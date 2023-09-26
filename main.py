# Imports
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Home'
)


# Load CSV file into DataFrame
df = pd.read_csv('@/../ds_salaries.csv')

# Filter job titles based on top 5 entries
column = df['job_title']
functie_per_group = df['job_title'].value_counts()
functie_100 = functie_per_group[functie_per_group > 100]
df_salary = df[df['job_title'].isin(functie_100.index)]


# Setup Streamlit app
st.title('Salaris van datascientists in 2023')

st.write(
'Welkom bij onze Streamlit-app! Stap in de toekomst van gegevensanalyse terwijl we je meenemen op een boeiende reis door de wereld van datawetenschapssalarissen in 2023.'
'Met behulp van een uitgebreide dataset hebben we een intuïtieve en interactieve ervaring gecreëerd waarmee je diep in de gegevens kunt duiken en inzicht kunt krijgen in de trends, '
'gemiddelden en variabelen die de wereld van data science in dit spannende jaar kenmerken. Of je nu een data scientist bent die op zoek is naar benchmarkinformatie of gewoon nieuwsgierig bent '
'naar de evolutie van salarissen in deze branche, onze Streamlit-app staat klaar om je te informeren en te inspireren. Laten we beginnen met het verkennen van de gegevens en ontdekken wat 2023 te bieden heeft voor data scientists!'
)
st.header('Over de dataset')
st.divider()
st.dataframe(df)
st.write('@Michael: Text over de analyse van de data mag hier..')



