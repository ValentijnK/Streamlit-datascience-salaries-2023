# Imports
import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
st.set_page_config(
    page_title='Home'
)


# Load CSV file into DataFrame
df = pd.read_csv('ds_salaries.csv')

# Filter job titles based on top 5 entries
column = df['job_title']
functie_per_group = df['job_title'].value_counts()
functie_100 = functie_per_group[functie_per_group > 100]
df_salary = df[df['job_title'].isin(functie_100.index)]

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = True

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

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
st.dataframe(filter_dataframe(df))


#data type aanpassen
df["work_year"] = df["work_year"].astype("category").cat.codes
df["experience_level"] = df["experience_level"].astype("category").cat.codes
df["employment_type"] = df["employment_type"].astype("category").cat.codes
df["job_title"] = df["job_title"].astype("category").cat.codes
df["employee_residence"] =df["employee_residence"].astype("category").cat.codes
df["remote_ratio"] =df["remote_ratio"].astype("category").cat.codes
df["company_location"] = df["company_location"].astype("category").cat.codes
df["company_size"] = df["company_size"].astype("category").cat.codes

import plotly.express as px
#correlatie bepalen
corr_matrix = df.corr()

fig = px.imshow(corr_matrix, x=corr_matrix.columns, y=corr_matrix.columns, 
                text_auto = True, title = 'Correlatiematrix')
fig.update_layout(width=900, height=900)
st.plotly_chart(fig)

