import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter

# Chargement des données (à remplacer par le chemin de votre fichier si nécessaire)
data = pd.read_csv("data.csv")  # Remplacez "data.csv" par le nom de votre fichier

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



# Affichage des premières lignes des données
st.header("Aperçu des Données")
st.dataframe(data.head())

# Analyse des mots-clés
st.header("Analyse des Mots-Clés")
all_keywords = []
for keywords in data['Keywords']:
    cleaned_keywords = keywords.replace("['", "").replace("]'", "").replace("'", "")
    all_keywords.extend(cleaned_keywords.split(", "))

# Regroupement des mots-clés similaires
keyword_mapping = {
    'decision support': 'decision support system',
    'decision support systems': 'decision support system'
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
st.subheader("Répartition des Mots-Clés (Diagramme Circulaire)")
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
st.subheader("Répartition des Clusters (Diagramme Circulaire)")
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
st.subheader("Répartition des Clusters (Barres)")
cluster_counts.rename(index=cluster_title_mapping, inplace=True)
st.bar_chart(cluster_counts)

# Analyse des mots-clés par cluster
st.subheader("Mots-Clés par Cluster")
selected_cluster = st.selectbox("Sélectionnez un Cluster", [cluster_title_mapping.get(i, i) for i in cluster_counts.index])
cluster_keywords = []

for i, cluster in enumerate(data['Paper Cluster']):
    if cluster == selected_cluster:
        cleaned_keywords = data.iloc[i]['Keywords'].replace("['", "").replace("]'", "").replace("'", "")
        cluster_keywords.extend(cleaned_keywords.split(", "))

cluster_keywords = [keyword_mapping.get(keyword, keyword) for keyword in cluster_keywords]
cluster_keywords_count = Counter(cluster_keywords)
cluster_keywords_df = pd.DataFrame(cluster_keywords_count.most_common(20), columns=['Keyword', 'Count'])

st.write(f"Mots-Clés les Plus Fréquents dans le Cluster {selected_cluster}")
st.bar_chart(cluster_keywords_df.set_index('Keyword'))

# Nuage de mots pour le cluster sélectionné
st.write(f"Nuage de Mots pour le Cluster {selected_cluster}")
cluster_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(cluster_keywords_count)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(cluster_wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Heatmap des relations mots-clés et clusters
st.subheader("Heatmap des Relations entre Mots-Clés et Clusters")
keyword_cluster_matrix = pd.DataFrame(0, index=set(all_keywords), columns=data['Paper Cluster'].unique())
for i, row in data.iterrows():
    cleaned_keywords = row['Keywords'].replace("['", "").replace("]'", "").replace("'", "")
    for keyword in cleaned_keywords.split(", "):
        keyword_cluster_matrix.at[keyword_mapping.get(keyword, keyword), row['Paper Cluster']] += 1

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(keyword_cluster_matrix, cmap="YlGnBu", annot=False, ax=ax)
st.pyplot(fig)

# Scatter plot des clusters et des dates de publication
st.subheader("Clusters en Fonction de la Date de Publication")
data['Publication Date'] = pd.to_datetime(data['Publication Date'], errors='coerce')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=data, x='Publication Date', y='Paper Cluster', hue='Paper Cluster', palette='tab10', ax=ax)
ax.set_title("Distribution des Clusters par Date de Publication")
st.pyplot(fig)

# Résumé et insights
st.header("Résumé et Insights")
st.write(
    """Cette analyse permet d'explorer les relations entre les mots-clés et les clusters. Voici quelques points clés :
    - Les mots-clés les plus fréquents donnent un aperçu des thèmes principaux abordés dans les publications.
    - Les clusters regroupent des publications similaires, permettant d'identifier des tendances ou des domaines de recherche spécifiques.
    - La visualisation par nuage de mots aide à comprendre rapidement les sujets dominants dans un cluster particulier.
    - Les diagrammes circulaires et les scatter plots fournissent une perspective supplémentaire sur la répartition des données."""
)
