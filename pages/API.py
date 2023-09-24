import streamlit as st

# Setting page configuration
st.set_page_config(
    page_title='API',
    page_icon=':old_key:'
)
'''
# Kaggle API
De makkelijkste manier om met de publieke Kaggle API te communiceren is via hun eigen Command-line tool (CLI).
Alleen het downloaden van datasets wordt behandeld in deze beschrijving.

De Python package is eenvoundig te downloaden met het volgende commando:
'''
st.code('''pip install kaggle''')
'''
## Authenticatie
Om met de API te kunnen communiceren moet de gebruiker een publieke API sleutel (ook wel token genoemd) aanvragen.
Het token kan gevonden worden in de *Account* tab van jouw persoonlijke Kaggle account. Selecteer 'Create New Token'.
Er zal nu een bestand worden gedownload genaamd 'kaggle.json'. Hierin zit de informatie van de publieke sleutel.

Dit bestand moet op de volgende locatie worden opgeslagen om direct toegang te krijgen tot de API:

*C:/Users/<windows-username>/.kaggle/kaggle.json*

Het bestand bevat de volgende informatie:
'''
st.code(''' {"username":"YOUR_USERNAME","key":"YOUR_KEY"} ''')
'''
### Interactie met datasets
Via de CLI kan de gebruiker eenvoudig datasets bekijken en downloaden.
Zie hieronder het commando voor het ophalen van een lijst met datasets op basis van een keyword:
'''
st.code('''kaggle datasets list -s [KEYWORD]''')
'''
De gewenste dataset kan gedownload worden met het volgende commando:
'''
st.code('''kaggle datasets download -d [DATASET]''')
'''
Voor de complete lijst met commando's [klik hier](https://github.com/Kaggle/kaggle-api#datasets)
'''