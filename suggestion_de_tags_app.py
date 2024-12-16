import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline
from sklearn.metrics import classification_report

# Configuration de la page principale
st.set_page_config(
    page_title="Système de suggestion de tags",
    page_icon="",
    layout="wide"
)

# Ajout de la barre de navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Accueil", "Dashboard", "Tags"]
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
elif page == "Tags":
    st.title("Système de Suggestion de Tags")
    st.sidebar.success("Vous êtes sur la page système de suggestion de tags.")    

    random_questions = df.sample(10, random_state=42)  # Sélection de 10 questions aléatoires
    question_selected = st.selectbox("Sélectionnez une question :", random_questions['Title'].tolist())
    

    # 2. Obtenir les vrais tags pour la question sélectionnée
    if question_selected:
        st.write(question_selected)
        true_tags = random_questions.loc[random_questions['Title'] == question_selected, 'Tags'].values[0]
        st.write("Tags réels pour la question sélectionnée :", true_tags)
        # Interface pour prédire les tags
        if st.button("Prédire les tags"):
            # Utiliser facebook/bart-large-mnli
            bart_model = pipeline("text-classification", model="facebook/bart-large-mnli", multi_label=True)
    	    prompt = f"Suggest relevant tags for the following programming question: {question_selected}"
            bart_pred = bart_model(prompt)
            bart_tags = [label['label'] for label in bart_pred if label['score'] > 0.5]
            st.write("Tags prédits avec BART :", bart_tags)
    
            # Utiliser google/flan-t5-base
            flan_model = pipeline("text2text-generation", model="google/flan-t5-base")
            flan_prompt = f"Suggest relevant tags for the following question: {question_selected}. Provide tags separated by commas."
            flan_response = flan_model(flan_prompt, max_length=50)
            flan_tags = flan_response[0]['generated_text'].split(',')
            flan_tags = [tag.strip() for tag in flan_tags]
            st.write("Tags prédits avec FLAN-T5 :", flan_tags)
    
            # Évaluation des résultats
            # Préparer les vrais tags sous forme de liste
            #true_tags_list = [tag.strip() for tag in true_tags.strip('<>').split('><')]
            true_tags_list = true_tags
    	    # Évaluation pour BART
            bart_evaluation = classification_report([true_tags_list], [bart_tags], output_dict=True)
            st.write("Évaluation pour BART :")
            st.json(bart_evaluation)
    
            # Évaluation pour FLAN-T5
            flan_evaluation = classification_report([true_tags_list], [flan_tags], output_dict=True)
            st.write("Évaluation pour FLAN-T5 :")
            st.json(flan_evaluation)
    else:
          st.write("Veuillez sélectionner une question pour continuer.")    
        
        


   
