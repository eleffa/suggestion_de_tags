import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np


# Configuration de la page principale
st.set_page_config(
    page_title="Système de suggestion de tags",
    page_icon="",
    layout="wide"
)

# Ajout de la barre de navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Accueil", "Dashboard", "Système de suggestion de tags"]
)


@st.cache
def load_data_from_github(url: str):
    """
    Load data from a CSV file hosted on GitHub.

    Parameters:
    - url (str): The raw URL of the CSV file in the GitHub repository.

    Returns:
    - pd.DataFrame: Loaded DataFrame.
    """
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if an error occurs



df = load_data_from_github("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/queryResult02.csv")

# Accueil
if page == "Accueil":
    st.title("Welcome to MuchMore Project! 👋")
    st.sidebar.success("Vous êtes sur la page d'accueil.")

    st.markdown(
        """
        ### Système de suggestion de tags 
        Stack Overflow is a question-and-answer website for computer programmers. It was created in 2008. 
        It features questions and answers on certain computer programming topics. As of March 2024 Stack 
        Overflow has over 23 million registered users and has received over 24 million questions and 
        35 million answers.
        
        **👈 Select a page from the sidebar** to see the dashboard
        or to play with the interactive exploration of data!
        """
    )

# Dashboard
elif page == "Dashboard":
    st.title("Système de suggestion de tags 📊")
    st.sidebar.success("Vous êtes sur la page Dashboard.")

    # Section 1 : Vue d'ensemble
    st.header("Vue d'ensemble")
    st.write("Résumé des données")
    # Exemple : ajouter des statistiques clés
    st.metric("Total Abstracts", 7823)
    st.metric("Nombre de Classes", 39)

    # Ajouter un diagramme de distribution des classes (importer une image générée)
    #st.image("https://raw.githubusercontent.com/eleffa/MuchMore-project/main/dashboard/distribution_categories.png",
    #caption="Distribution des Classes", use_column_width=True)

    # Section 2 : Analyse exploratoire
    #st.header("Analyse exploratoire")
    #st.subheader("Histogramme des longueurs")
    #st.image("https://raw.githubusercontent.com/eleffa/MuchMore-project/main/dashboard/distribution_longueur.png", 
    #         caption="Distribution des longueurs des abstracts")
    

    #st.subheader("Nuage de mots")
    #st.image("https://raw.githubusercontent.com/eleffa/MuchMore-project/main/dashboard/nuage_de_mots.png", caption="Nuage de mots")

    #st.subheader("Heatmap de similarité")
    #st.image("https://raw.githubusercontent.com/eleffa/MuchMore-project/main/dashboard/heatmap_similarite.png", caption="Similarité entre catégories")

    
        

# Exploration Interactive
elif page == "système de suggestion de tags":
  st.title("système de suggestion de tags 👋")
    

   
