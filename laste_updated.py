import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import plotly.express as px  # Importer Plotly Express

# Chargement des données (à remplacer par le chemin de votre fichier si nécessaire)
data = pd.read_csv("data.csv")  # Remplacez "data.csv" par le nom de votre fichier

st.subheader("Comment l'analyse des mots-clés, leur répartition et leur évolution permettent-elles de visualiser les dynamiques de recherche du CGI et d'orienter ses priorités stratégiques ?")

# Titre de l'application
st.title("Analyse des Mots-Clés et Clusters des Publications")

cluster_title_mapping = {
    'Cluster 0': 'Stability and Random Disturbance',
    'Cluster 1': 'IT Solutions and Operations',
    'Cluster 2': 'Supply Chain and Risk Management',
    'Cluster 3': 'Project Success and Process Design',
    'Cluster 4': 'Resilience Evaluation',
    'Cluster 5': 'Performance Analysis and Traceability',
    'Cluster 6': 'Risk Management and Modelling',
    'Cluster 7': 'Smart Cities and Virtual Worlds',
    'Cluster 8': 'AI and Decision Support Systems',
    'Cluster 9': 'Knowledge Management',
    'Cluster 10': 'Healthcare and Patient Pathways',
    'Cluster 11': 'Service and Maintenance Scheduling',
    'Cluster 12': 'Social Networks and Collaboration',
    'Cluster 13': 'Logistics and Last-Mile Delivery',
    'Cluster 14': 'Strategic Planning and Decentralized Management',
    'Cluster 15': 'Emergency and Disaster Technologies',
    'Cluster 16': 'Nonlinear Systems and Experimental Design',
    'Cluster 17': 'Business Modeling and Simulation',
    'Cluster 18': 'Uncertainty and Robustness Optimization',
    'Cluster 19': 'Constraint Modeling and Optimization',
    'Cluster 20': 'Optimization and Evolutionary Algorithms'
}





# Analyse des mots-clés
st.header("Analyse des Mots-Clés")
all_keywords = []
for keywords in data['Keywords']:
    cleaned_keywords = keywords.replace("['", "").replace("]'", "").replace("'", "")
    all_keywords.extend(cleaned_keywords.split(", "))

# Regroupement des mots-clés similaires
keyword_mapping = {
    'decision support': 'decision support system',
    'decision support systems': 'decision support system',
    'decision support system]': 'decision support system',
    'simulation]': 'simulation',
    'simulations': 'simulation',
    'risk management]': 'risk management system',
    'industrial case]': 'industrial case',
    'cambodia]': 'cambodia',
    'supply chain]': 'supply chain',
    'safety]': 'safety',
    'performance management]': 'performance management'
    
}
all_keywords = [keyword_mapping.get(keyword, keyword) for keyword in all_keywords]

# Calcul des fréquences des mots-clés
keywords_count = Counter(all_keywords)

# Affichage des mots-clés les plus fréquents
st.subheader("Mots-Clés les Plus Fréquents")
most_common_keywords = pd.DataFrame(keywords_count.most_common(20), columns=['Keyword', 'Count'])
st.bar_chart(most_common_keywords.set_index('Keyword'))

# Nuage de mots pour les mots-clés
st.subheader("Nuage de Mots des Mots-Clés")
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(keywords_count)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Diagramme circulaire pour les mots-clés
st.subheader("Répartition des Mots-Clés (Top 10)")
filtered_keywords = Counter({k: v for k, v in keywords_count.items() if k in dict(keywords_count.most_common(10))})
fig, ax = plt.subplots()
ax.pie([count for _, count in filtered_keywords.most_common()], labels=[keyword for keyword, _ in filtered_keywords.most_common()], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Assure un cercle parfait
st.pyplot(fig)

# Analyse des Clusters
st.header("Analyse des Clusters")
cluster_counts = data['Paper Cluster'].value_counts()
cluster_counts.rename(index=cluster_title_mapping, inplace=True)

# Répartition des clusters (avec regroupement des petits clusters)
st.subheader("Répartition des Clusters")
threshold = 0.04  # Seuil de 4 %
total_count = cluster_counts.sum()
cluster_counts_filtered = cluster_counts[cluster_counts / total_count >= threshold]
others_count = cluster_counts[cluster_counts / total_count < threshold].sum()

# Ajout de la catégorie "Autres" si nécessaire
if others_count > 0:
    cluster_counts_filtered['Autres'] = others_count

# Palette de couleurs distinctes pour le diagramme circulaire
colors = plt.cm.tab20.colors  # Une palette avec 20 couleurs distinctes

# Création du diagramme circulaire avec les clusters filtrés
fig, ax = plt.subplots()
ax.pie(cluster_counts_filtered, 
       labels=cluster_counts_filtered.index, 
       autopct='%1.1f%%', 
       startangle=90, 
       colors=colors[:len(cluster_counts_filtered)])  # Application des couleurs distinctes
ax.axis('equal')  # Assure un cercle parfait
st.pyplot(fig)


# Répartition des clusters (Barres)
st.subheader("Répartition des Clusters")
cluster_counts.rename(index=cluster_title_mapping, inplace=True)
st.bar_chart(cluster_counts)


st.header("Liens entre Clusters")
st.image("links.png", caption="Liens entre Clusters", use_column_width=True)

# Charger les données pour l'évolution des mots-clés
keywords_evolution_data = pd.read_csv("top_35_keywords_evolution_by_year.csv")

# Afficher les données
st.subheader("Évolution des Mots-Clés au Fil des Années")

# Créer un sélecteur pour choisir plusieurs mots-clés
keywords_list = keywords_evolution_data['Keyword'].tolist()  # Récupérer la liste des mots-clés
selected_keywords = st.multiselect("Sélectionnez des Mots-Clés", keywords_list)

# Préparer les données pour le graphique
if selected_keywords:
    # Filtrer les données pour les mots-clés sélectionnés
    filtered_data = keywords_evolution_data[keywords_evolution_data['Keyword'].isin(selected_keywords)]

    # Transformer les données pour le graphique
    filtered_data_melted = filtered_data.melt(id_vars='Keyword', var_name='Year', value_name='Frequency')

    # Créer un graphique interactif avec Plotly
    fig = px.line(filtered_data_melted, 
                  x='Year', 
                  y='Frequency', 
                  color='Keyword', 
                  title='Évolution des Mots-Clés au Fil des Années',
                  labels={'Frequency': 'Occurence', 'Year': 'Années'})

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)
else:
    st.write("Veuillez sélectionner au moins un mot-clé.")

