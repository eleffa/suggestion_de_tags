import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline
#from sklearn.metrics import classification_report

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


@st.cache_data
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



df = load_data_from_github("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/queryResult02_clean.csv")

# Accueil
if page == "Accueil":
    st.title("Welcome! 👋")
    st.sidebar.success("Vous êtes sur la page d'accueil.")

    st.markdown(
        """
        ### Tag Suggestion System
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
    st.title("Système de suggestion de tags")
    st.sidebar.success("Vous êtes sur la page Dashboard.")

    # Section 1 : Vue d'ensemble
    st.header("Vue d'ensemble")
    st.write("Résumé des données")
    # Exemple : ajouter des statistiques clés
    st.metric("Nombre Total de Questions", 46500)
    st.metric("Nombre de colonnes", 11)
    st.metric("Longueurs de la question la plus longue", 763)
    st.metric("Longueurs de la question la plus courte", 0)
    
    # Ajouter un diagramme de distribution des classes (importer une image générée)
    #st.image("https://raw.githubusercontent.com/eleffa/MuchMore-project/main/dashboard/distribution_categories.png",
    #caption="Distribution des Classes", use_column_width=True)

    # Section 2 : Analyse exploratoire
    st.header("Analyse exploratoire")
    st.subheader("Statistiques générales")
    st.dataframe(df[['Score','ViewCount','AnswerCount','CommentCount','FavoriteCount']].describe())
        
    st.subheader("Distribution des tags")
    st.image("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/dashboard/distribution_des_tags.jpg", caption="distribution des tags")
    
    st.subheader("Questions avec les scores les plus élevés")
    popular_questions = df.sort_values(by='Score', ascending=False).head(5)
    st.dataframe(popular_questions[['Title', 'Score', 'ViewCount']])
    
    st.subheader("Tags les plus fréquents")
    st.image("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/dashboard/tags_les_plus_frequents.jpg", caption="Tags les plus fréquents")
    
    st.subheader("Corrélations Entre les Variables Numériques")
    st.image("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/dashboard/correlation_matrix.png", caption="correlation matrix")
    
    st.subheader("Évolution du Nombre de Questions Dans le Temps")
    st.image("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/dashboard/evolution_data.png", caption="évolution dans le temps")
    
    st.subheader("Nuage de mots")
    st.image("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/dashboard/nuage_de_mots.png", caption="Nuage de mots")

    st.subheader("Histogramme des longueurs")
    st.image("https://raw.githubusercontent.com/eleffa/suggestion_de_tags/main/dashboard/histogramme.png", caption="Distribution des longueurs des questions")
    
        

# Exploration Interactive
elif page == "système de suggestion de tags":
  st.title("Système de Suggestion de Tags")

  # 1. Charger un sous-ensemble de questions du dataframe
  random_questions = df.sample(10, random_state=42)  # Sélection de 10 questions aléatoires
  question_selected = st.selectbox("Sélectionnez une question :", random_questions['Title'].tolist()) 

   
