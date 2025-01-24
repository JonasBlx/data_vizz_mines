# Présentation du Projet de Suivi des Tendances de Recherche du CGI

Ce projet a pour objectif d’analyser et de visualiser les tendances de recherche du Centre Génie Industriel (CGI) à travers ses publications scientifiques. Pour cela, deux scripts principaux ont été développés :

1. **scrap.ipynb**  
2. **laste_updated.py**  

**scrap.ipynb** sert à créer des csv alimentant un site web interactif (développé avec Streamlit) sur lequel nous avons des visu qui permet d’explorer les mots-clés et thématiques des publications de manière visuelle et dynamique.

---

## 1. **scrap.ipynb** : Scraping, Nettoyage et Préparation des Données

### 1.1 Objectifs
- **Récupérer les publications** depuis la plateforme [IMT Mines Albi - HAL](https://imt-mines-albi.hal.science/).
- **Nettoyer et normaliser les données** (auteurs, mots-clés, résumés, dates, etc.).
- **Identifier et filtrer** les auteurs rattachés au Centre Génie Industriel.
- **Réaliser un clustering** avancé des mots-clés et associer ensuite chaque publication à l’un de ces clusters.

### 1.2 Étapes Clés

1. **Scraping**
   - Utilisation des bibliothèques `requests` et `BeautifulSoup` pour extraire le contenu HTML.
   - Extraction des informations pertinentes : titre, résumé, mots-clés, auteurs, date de publication, etc.

2. **Nettoyage et Normalisation**
   - Conversion en minuscules et suppression des accents pour homogénéiser le texte.
   - Filtrage des auteurs pour ne conserver que ceux affiliés au CGI.

3. **Clustering des Mots-Clés**
   - Génération d’**embeddings** (représentations vectorielles) de chaque mot-clé grâce au modèle `sentence-transformers/all-MiniLM-L6-v2`.
   - Application de l’algorithme **K-Means** pour regrouper les mots-clés.
   - Détermination du **nombre optimal de clusters** via les scores de silhouette et la méthode du coude (Elbow method).
   - **Nomination des clusters** en se basant sur la fréquence des termes les plus représentatifs.

4. **Clustering des Publications**
   - Association de chaque publication au cluster dominant de ses mots-clés.
   - Création d’une **matrice auteur-cluster** (pivot table) pour analyser la distribution des publications par auteur et par cluster.

5. **Visualisation et Export**
   - Génération de graphiques (par ex. courbes Elbow et silhouette pour le choix du k de K-Means).
   - Réalisation d’un **graphe de relations** entre mots-clés, avec détection de communautés via la modularité.
   - Export des données (fichiers CSV) et des résultats de clustering (pour un usage ultérieur dans la web app).

---

## 2. **laste_updated.py** : Application Streamlit pour Visualiser et Explorer les Données

### 2.1 Objectifs
- **Charger et afficher** les données (issues de `scrap.ipynb`).
- **Permettre une exploration interactive** des tendances de recherche.
- **Fournir des visualisations** conviviales (bar charts, pie charts, word cloud, etc.).

### 2.2 Fonctionnalités Principales

1. **Chargement et Prétraitement des Données**
   - Lecture du fichier `data.csv` (exporté depuis `scrap.ipynb`).
   - Nettoyage et unification des mots-clés (traitement des variations).

2. **Analyse des Mots-Clés**
   - **Calcul de la fréquence** des mots-clés et affichage des 20 plus utilisés.
   - **Word Cloud** pour visualiser l’importance relative des mots-clés.

3. **Analyse par Cluster**
   - Utilisation des clusters nommés (ex. *Stability and Random Disturbance*, *Healthcare and Patient Pathways*, etc.).
   - **Diagramme en secteurs (Pie Chart)** pour la répartition globale des publications par cluster.
   - **Diagramme en barres** pour afficher le nombre de publications par cluster.

4. **Évolution Temporelle des Mots-Clés**
   - Sélection des 35 mots-clés les plus représentés sur la durée.
   - **Graphique interactif (Plotly)** permettant de filtrer les mots-clés et d’en suivre la tendance au fil des années.

5. **Relations entre Clusters**
   - Affichage d’un **graphe pré-calculé** (image `links.png`) illustrant les relations entre les différents clusters.

6. **Personnalisation et Interactivité**
   - Interface Streamlit permettant une **navigation fluide**, une sélection de mots-clés et un zoom sur les tendances spécifiques.

---

## 3. **Comment ces Deux Scripts Interagissent**

- **`scrap.ipynb`** se charge de toute la partie **extraction, normalisation et segmentation** des données. Les résultats (CSV et images) servent ensuite de source de référence.
- **`laste_updated.py`** exploite directement ces résultats pour offrir une **interface visuelle** permettant de **parcourir**, de **comparer** et de **filtrer** les données de recherche.

En d’autres termes, **`scrap.ipynb`** produit les données prêtes à l’emploi et **`laste_updated.py`** transforme ces données en **visualisations interactives** à destination des utilisateurs finaux (chercheurs, décideurs, etc.).

---

## 4. **Applications et Bénéfices**

1. **Analyse de la Recherche**  
   - Aperçu rapide des domaines les plus explorés au CGI.
   - Identification des auteurs clés et de leurs axes de publication.

2. **Suivi des Tendances**  
   - Visualisation de l’évolution des mots-clés sur plusieurs années.
   - Mise en évidence des sujets émergents et des domaines en déclin.

3. **Collaboration et Orientation Stratégique**  
   - Le **graphe de relations** et les **clusters** aident à repérer les ponts entre différentes thématiques.
   - Soutien à la prise de décision pour orienter les axes futurs de recherche.

4. **Export et Réutilisation des Données**  
   - Les fichiers CSV permettent une **analyse complémentaire** dans d’autres outils (Excel, Python, R, etc.).
   - Partage facile avec d’autres équipes ou partenaires.

---

## 5. **Conclusion**

Ce projet offre une **vue d’ensemble** des travaux de recherche du CGI et **facilite l’exploration** des thématiques clés via des visualisations adaptées.  
- La **phase de collecte et de traitement** (fichier `scrap.ipynb`) garantit une **base de données fiable** et structurée.  
- L’**application Streamlit** (`laste_updated.py`) fournit, quant à elle, une **expérience utilisateur** optimale pour analyser la recherche et **encourager la collaboration**.

La combinaison de ces deux approches **technique** (scraping et clustering) et **visuelle** (interface interactive) constitue un outil puissant pour **comprendre** et **piloter** l’évolution des recherches au Centre Génie Industriel.

---

st.markdown("[Lien du repo GitHub](https://github.com/JonasBlx/data_vizz_mines/)", unsafe_allow_html=True)
