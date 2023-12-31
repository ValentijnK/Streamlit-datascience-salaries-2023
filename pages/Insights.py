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
st.header('Gemiddelde salaris per baan')
st.write("""

Om de gemiddelde salarissen per banen te berekenen, moeten we eerst de verschillende categorieën van datascience-banen identificeren, dit is gedaan op basis van  "job_title" in het gegevensbestand, omdat wij natuurlijk ook salarissen nodig hebben gebruiken wij ook "salary_in_usd" uit het gegevensbestand. Vervolgens kunnen we voor elke categorie het gemiddelde salaris berekenen per functie. Wij hebben onze bevindingen uitgebeeld in een Histogram, zie de plot(‘ Avererage job per category’).
""")

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
st.header('Gemiddelde salaris per bedrijfsgrootte')
st.write("""

Wij gaan in het onderstaande stukje kijken naar de gemiddelde salarissen per bedrijfsgrootte, dit doen wij met de data uit het bestand "ds_salaries.csv". De twee belangrijkste variabelen die we in dit hier zullen gebruiken zijn "salary_in_usd" en "company_size". 
Uit onze analyse blijkt dat middelgrote bedrijven de hoogste salarissen betalen. Zij betalen gemiddeld wel $32000 meer dan grote bedrijven, wij hebben deze data gevisualiseerd in een histogram. Zie de  plot (‘Average Salary per company size’). De middelgrote bedrijven betalen over het algemeen het meest, daarna de grote bedrijven en als laatste de kleine bedrijven

""")

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
st.header('Salaris vs. bedrijfsgrootte')
st.write(""" 

Het gemiddelde salaris  varieert sterk afhankelijk van de omvang van het bedrijf waarin iemand werkt. Over het algemeen geldt dat grotere bedrijven vaak hogere salarissen aanbieden dan kleinere ondernemingen. Dit kan komen doordat grotere bedrijven meestal meer financiële middelen hebben en een bredere reeks bieden. 
Wij hebben voor deze bevinding 'salary_in_usd' en 'company_size' gebruikt en hebben deze gevisualiseerd in een boxplot, zie de plot(‘ Salary vs Company size’). Iets wat gelijk op te merken is aan de boxplot is dat de medium bedrijven de grootste uitschieters hebben van de salarissen.
""")

st.subheader('Salary vs. Company Size')
fig = px.box(df_salary, x='company_size', y='salary_in_usd',
             labels={'salary_in_usd': 'Salary in USD', 'company_size': 'Company Size'})
fig.update_xaxes(categoryorder='array', categoryarray=['L', 'M', 'S'], tickvals=[0, 1, 2], ticktext=['Large', 'Medium', 'Small'])
st.plotly_chart(fig)


# Avarage salary by Company Location
st.header('Gemiddelde Salaris per bedrijfslocatie')
st.write(""" 

Het gemiddelde salaris varieert aanzienlijk afhankelijk van de locatie van het bedrijf waarin iemand werkzaam is. Dit wordt inzichtelijk wanneer we kijken naar de gemiddelde salarissen per bedrijfslocatie.
Bedrijven hebben de neiging om hun salarissen aan te passen aan de kosten van levensonderhoud, concurrentie op de arbeidsmarkt en andere lokale factoren. Wij hebben dit inzichtelijk gemaakt door middel van een map,  zie de plot(‘Average Salary by Company Location’)
""")

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
st.header('Salaris vs. ervaringsniveau')
st.write("""

Het verband tussen salaris en ervaringsniveau is een belangrijk aspect van de arbeidsmarkt dat de loopbaanontwikkeling van individuen beïnvloedt. Het is algemeen bekend dat ervaring een aanzienlijke impact heeft op het salaris dat een persoon kan verwachten te verdienen gedurende zijn of haar carrière. Dit verband kan worden verklaard door verschillende factoren die samenkomen om het salaris te beïnvloeden.
Naarmate iemand meer jaren in een bepaalde branche of functie werkt, vergaart hij of zij doorgaans diepgaandere kennis en expertise. 

Hierdoor zijn zij vaak in een positie om hogere salarissen te onderhandelen.
Ten tweede speelt senioriteit een belangrijke rol. Werknemers met meer ervaring kunnen doorgaans rekenen op promoties en leiderschapsposities, die vaak gepaard gaan met aanzienlijke salarisverhogingen. Wij hebben dit inzichtelijk gemaakt doormiddel van een  slider voor het salaris, deze slider interacteert met de plot die eronder staat aan de hand van het  'experience_level'.
Zie de plot (‘Salary Histogram’) 
""")

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
st.header('Salaris per ervaringsniveau')
st.write(""" 

In het dynamische veld van data-analyse en -wetenschap is het salaris sterk afhankelijk van het ervaringsniveau van professionals. Verschillende ervaringsniveaus weerspiegelen niet alleen een groeiende vaardigheid, maar ook een  begrip van complexe gegevensprocessen en -technologieën. Hieronder volgt een overzicht van het salaris per ervaringsniveau in het data-gebied. 
Om de salarissen tegenover de werkervaring in beeld te brengen hebben wij de variablen "salary_in_usd" en experience_level gebruikt, daarnaast hebben wij een boxplot gemaakt zie plot (‘Salary by experience level’). 

Uit deze plot is uit te lezen wat het mediaan, eerste en derde kwartiel, de boven en ondergrens, en de uitschieters zijn van de salarissen. Deze zijn gerangschikt per ervaringsniveau. Dit hebben wij ook uitgewerkt per werkjaar met als extra variabel 'work_year'.
Zie de boxplot (‘Salary by experience level by work year’)
""")

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

st.header('Conclusie')
st.write("""

In dit onderzoek naar het bestand "ds_salaries.csv" hebben we verschillende verbanden en inzichten ontdekt met betrekking tot salarissen in het vakgebied van Data Science. We hebben gekeken naar gemiddelde salarissen per baan, bedrijfsgrootte, bedrijfslocatie en ervaringsniveau. Hier zijn enkele belangrijke conclusies:

1. Gemiddelde salaris per baan: We hebben vastgesteld dat er aanzienlijke variatie is in de salarissen binnen verschillende datascience-banen. De gemiddelde salarissen per functie zijn in kaart gebracht, wat ons in staat heeft gesteld om te begrijpen hoe salarissen zich verhouden tot specifieke rollen binnen het vakgebied.

2. Gemiddelde salaris per bedrijfsgrootte: Onze analyse heeft aangetoond dat middelgrote bedrijven over het algemeen de hoogste salarissen bieden, gevolgd door grote bedrijven en kleine bedrijven. Dit kan duiden op de financiële middelen en het aanbod van verschillende bedrijfsgroottes.

3. Salaris vs. Bedrijfsgrootte: We hebben visueel weergegeven hoe het gemiddelde salaris varieert afhankelijk van de bedrijfsgrootte. Grotere bedrijven bieden doorgaans hogere salarissen, en opvallend was dat middelgrote bedrijven de grootste uitschieters hadden in salarissen.

4. Gemiddelde salaris per bedrijfslocatie: Salarissen blijken sterk afhankelijk te zijn van de locatie van het bedrijf. Dit kan worden verklaard door de kosten van levensonderhoud en lokale arbeidsmarktcondities. We hebben deze gegevens inzichtelijk gemaakt met behulp van een kaartweergave.

5. Salaris vs. ervaringsniveau: Er is een duidelijk verband tussen salaris en ervaringsniveau. Naarmate professionals meer ervaring opdoen, hebben ze de neiging hogere salarissen te verdienen. Dit kan worden toegeschreven aan diepgaandere kennis, expertise en mogelijkheid tot promoties in de loop van de carrière.

6. Salaris per ervaringsniveau: We hebben de salarissen op basis van ervaringsniveau gevisualiseerd met behulp van boxplots. Dit biedt inzicht in de spreiding van salarissen binnen verschillende ervaringsniveaus en jaarlijkse werkervaring.

Dit onderzoek heeft waardevolle inzichten opgeleverd over de factoren die van invloed zijn op salarissen in het Data Science-veld, waaronder de functie, bedrijfsgrootte, locatie en ervaring van professionals. Deze informatie kan nuttig zijn voor zowel werkzoekenden als werkgevers om weloverwogen beslissingen te nemen met betrekking tot beloning en carrièreontwikkeling in de data gestuurde industrie.

""")



# st.button('Thank you for reading ', on_click=st.balloons)
