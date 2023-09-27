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
st.write('
Het Ontdekken van verbanden  in het bestand ds_salaries.csv
Data Science is een vakgebied dat draait om het verzamelen, analyseren en interpreteren van gegevens om waardevolle inzichten te verkrijgen. Een van de meest krachtige technieken binnen datagestuurde besluitvorming is het onderzoeken van correlaties tussen variabelen. In deze blogpost zullen we een analyse uitvoeren van het bestand "ds_salaries.csv" om te ontdekken welke verbanden er bestaan tussen de variabelen in dit dataset.
Belangrijke informatie uit de dataset
We beginnen met een korte beschrijving van de dataset. Het bestand ds_salaries.csv bevat gegevens over salarissen in het veld van Data en de bijhorende functies Het bevat verschillende kolommen, waaronder:
1. Experience_level: Het aantal jaren ervaring van de respondenten in 
2. Residence: Waar de respondenten wonen 
3. Job_title: De functie of positie van de respondent.
4. Salary: Het salaris van de respondent.
5. Company_size: De grootte van het bedrijf uitgedrukt in klein(S), medium(M) en groot (L)
6. Experience_level: Het ervaringsniveau van de respondent 
7. Company_location: Locatie van he bedrijf

Gemiddelde salaris per baan
Om de gemiddelde salarissen per banen te berekenen, moeten we eerst de verschillende categorieën van datascience-banen identificeren op basis van de "job_title" in het gegevensbestand. Vervolgens kunnen we voor elke categorie het gemiddelde salaris berekenen. Wij hebben onze bevindingen uitgebeeld in de Historgram, zie de plot(‘ Avererage job per category’).
Gemiddelde salaris per bedrijfsgrootte 
Wij gaan in het onderstaande stukje kijken naar de gemiddelde salarissen per bedrijfsgrootte, dit doen wij door de data uit het bestand "ds_salaries.csv". De twee belangrijkste variabelen die we in dit onderzoek zullen gebruiken zijn "salary_in_usd" en "company_size". 
Uit onze analyse blijkt dat middelgrote bedrijven de hoogste salarissen betalen. Zij betalen gemiddeld wel $32000 meer dan grote bedrijven, wij hebben deze data gevisualiseerd in een histogram. Zie de  plot (‘Average Salary per company size’). De middelgrote bedrijven betalen over het algemeen het meest, daarna de grote bedrijven en als laatste de kleine bedrijven
 

Salaris vs. bedrijfsgrootte 
Het gemiddelde salaris  varieert sterk afhankelijk van de omvang van het bedrijf waarin iemand werkt. Over het algemeen geldt dat grotere bedrijven vaak hogere salarissen aanbieden dan kleinere ondernemingen. Dit kan komen doordat grotere bedrijven meestal meer financiële middelen hebben en een bredere reeks bieden. 
Wij hebben deze bevinding gevisualiseerd in een boxplot, zie de plot(‘ Salary vs Company size’). Iets wat gelijk op te merken is aan de boxplot is dat de medium bedrijven de grootste uitschieters hebben van salarissen.

Gemiddelde Salaris per bedrijfslocatie 
Het gemiddelde salaris varieert aanzienlijk afhankelijk van de locatie van het bedrijf waarin iemand werkzaam is. Dit wordt inzichtelijk wanneer we kijken naar de gemiddelde salarissen per bedrijfslocatie.
 Bedrijven hebben de neiging om hun salarissen aan te passen aan de kosten van levensonderhoud, concurrentie op de arbeidsmarkt en andere lokale factoren. Wij hebben dit inzichtelijk gemaakt door middel van een map,  zie de plot(‘Average Salary by Company Location’)

Salaris vs. ervaringsniveau
Het verband tussen salaris en ervaringsniveau is een belangrijk aspect van de arbeidsmarkt dat de loopbaanontwikkeling van individuen beïnvloedt. Het is algemeen bekend dat ervaring een aanzienlijke impact heeft op het salaris dat een persoon kan verwachten te verdienen gedurende zijn of haar carrière. Dit verband kan worden verklaard door verschillende factoren die samenkomen om het salaris te beïnvloeden.
Naarmate iemand meer jaren in een bepaalde branche of functie werkt, vergaart hij of zij doorgaans diepgaandere kennis en expertise. Hierdoor zijn zij vaak in een positie om hogere salarissen te onderhandelen.
Ten tweede speelt senioriteit een belangrijke rol. Werknemers met meer ervaring kunnen doorgaans rekenen op promoties en leiderschapsposities, die vaak gepaard gaan met aanzienlijke salarisverhogingen. Wij hebben dit inzichtelijk gemaakt doormiddel slider van voor het salaris, deze slider interacteert met de plot die eronder staat aan de hand het experience_level.
Zie de plot (‘Salary Histogram’) 

 
Salaris per ervaringsniveau 
In het dynamische veld van data-analyse en -wetenschap is het salaris sterk afhankelijk van het ervaringsniveau van professionals. Verschillende ervaringsniveaus weerspiegelen niet alleen een groeiende vaardigheid, maar ook een  begrip van complexe gegevensprocessen en -technologieën. Hieronder volgt een overzicht van het salaris per ervaringsniveau in het data-gebied. 
Om de salarissen tegenover de werkervaring in beeld te brengen hebben wij een boxplot gemaakt, zie plot (‘Salary by experience level’). Uit deze plot is uit te lezen wat het mediaan, eerste en derde kwartiel, de boven en ondergrens, en de uitschieters zijn van de salarissen. Deze zijn gerangschikt per ervaringsniveau. Dit hebben wij ook uitgewerkt per werkjaar.
Zie de boxplot (‘Salary by experience level by work year’)

Conclusie
In dit onderzoek naar het bestand "ds_salaries.csv" hebben we verschillende verbanden en inzichten ontdekt met betrekking tot salarissen in het vakgebied van Data Science. We hebben gekeken naar gemiddelde salarissen per baan, bedrijfsgrootte, bedrijfslocatie en ervaringsniveau. Hier zijn enkele belangrijke conclusies:

1. Gemiddelde salaris per baan: We hebben vastgesteld dat er aanzienlijke variatie is in de salarissen binnen verschillende datascience-banen. De gemiddelde salarissen per functie zijn in kaart gebracht, wat ons in staat heeft gesteld om te begrijpen hoe salarissen zich verhouden tot specifieke rollen binnen het vakgebied.

2. Gemiddelde salaris per bedrijfsgrootte: Onze analyse heeft aangetoond dat middelgrote bedrijven over het algemeen de hoogste salarissen bieden, gevolgd door grote bedrijven en kleine bedrijven. Dit kan duiden op de financiële middelen en het aanbod van verschillende bedrijfsgroottes.

3. Salaris vs. Bedrijfsgrootte: We hebben visueel weergegeven hoe het gemiddelde salaris varieert afhankelijk van de bedrijfsgrootte. Grotere bedrijven bieden doorgaans hogere salarissen, en opvallend was dat middelgrote bedrijven de grootste uitschieters hadden in salarissen.

4. Gemiddelde salaris per bedrijfslocatie: Salarissen blijken sterk afhankelijk te zijn van de locatie van het bedrijf. Dit kan worden verklaard door de kosten van levensonderhoud en lokale arbeidsmarktcondities. We hebben deze gegevens inzichtelijk gemaakt met behulp van een kaartweergave.

5. Salaris vs. ervaringsniveau: Er is een duidelijk verband tussen salaris en ervaringsniveau. Naarmate professionals meer ervaring opdoen, hebben ze de neiging hogere salarissen te verdienen. Dit kan worden toegeschreven aan diepgaandere kennis, expertise en mogelijkheid tot promoties in de loop van de carrière.

6. Salaris per ervaringsniveau: We hebben de salarissen op basis van ervaringsniveau gevisualiseerd met behulp van boxplots. Dit biedt inzicht in de spreiding van salarissen binnen verschillende ervaringsniveaus en jaarlijkse werkervaring.

Dit onderzoek heeft waardevolle inzichten opgeleverd over de factoren die van invloed zijn op salarissen in het Data Science-veld, waaronder de functie, bedrijfsgrootte, locatie en ervaring van professionals. Deze informatie kan nuttig zijn voor zowel werkzoekenden als werkgevers om weloverwogen beslissingen te nemen met betrekking tot beloning en carrièreontwikkeling in de data gestuurde industrie.

')

