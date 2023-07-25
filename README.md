  <h2 align="center">Exploitation des données de la plateforme PRIM d'Île-de-France Mobilités</h2>

<br />

### **À propos**

Île-de-France Mobilités met à disposition de nombreuses données statiques et dynamiques relatives à la mobilité en Île-de-France sur la Plateforme Régionale d'Information pour la Mobilité (<a href="https://prim.iledefrance-mobilites.fr/fr">PRIM</a>).

L'accès aux API (qui possèdent toutes une version gratuite) est possible sur simple création de compte.

Avec les données collectées, on peut par exemple imaginer un suivi (journalier/hebdomadaire/mensuel) sur sa ligne de transport en commun préférée (bus/métro/tramway/RER) avec tout un tas d'indicateurs potentiels : fréquence de passage, retard moyen, statuts des trains, ...

Voici dans ce repo un exemple d'exploitation de ces données avec la mise en place d'un pipeline ETL qui permet :

- d'extraire les données exposées par l'API Prochains passages - Requête globale
- de transformer les données brutes extraites depuis l'API (focus sur les données de la ligne de tramway T4)
- de les charger dans une base dédiée PostgreSQL

Vous trouverez également un exemple d'automatisation du lancement du pipeline de données (avec Airflow), ainsi qu'un exemple de visualisation (avec la librairie Plotly) qui pourrait faire l'objet d'un reporting régulier et automatisé (par exemple la mise en place de publications quotidiennes/hebdomadaires sur Twitter en utilisant des credentials de l'API Twitter depuis un DAG Airflow).

<br />

### **Étapes**

Voici les étapes d'implémentation qui sont proposées dans ce repo :

&#10004; Créer une base de données SQL (PostgreSQL)

&#10004; Créer dans la base de données les tables correspondant au modèle de données souhaité (modèle en étoile)

&#10004; Développer un script Python permettant d'extraire les données brutes de l'API et de les transformer

&#10004; Développer un script Python permettant d'insérer les données transformées dans la base de données

&#10004; Développer un script Python permettant de visualiser une partie des données en utilisation un outil de data visualisation (Plotly)

&#10004; Automatiser le pipeline ETL et la production du reporting avec un outil de planification (Apache Airflow)

<br />

### **Structure du repo**

Le repo contient les éléments suivants :

- `airflow/` contient des exemples de DAG 
- `data/` contient un fichier d'exemple de données traitées obtenues en sortie de pipeline avant ingestion dans Postgres + un exemple de data visualisation sauvegardée sous format HTML
- `setup/` contient des procédures d'installation d'outils utilisés ici
- `sql/` contient les requêtes SQL pour la création des tables dans PostgreSql
- `src/` contient les principaux codes sources Python utilisés pour la création du pipeline ETL et la data visualisation
- `MIT-LICENSE.txt` : une des licences applicables ici
- `README.md` : fichier d'accueil
- `requirements.txt` : la liste des dépendances Python nécessaires

<br />

### Pré-requis

- <a href="https://www.python.org/downloads/">Python 3</a>

- le fichier `requirements.txt` contenant la liste des blibliothèques Python utilisées

<br />

### Installation

1. Si vous souhaitez cloner le repo :

	```
	git clone https://github.com/MohamedKheroua/prim_data_etl
	```

2. Installation du client PostgreSQL

	Voici les procédures que l'on pourra suivre pour l'installation en local de postgreSQL :

    - Les packages d'installation sont disponibles à cette <a href="https://www.postgresql.org/download/">adresse</a>.
	- On pourra également installer <a href="https://www.pgadmin.org/">pgAdmin</a> qui est un outil opensource d'administration des bases de données PostgreSQL.

	<br/>

	*Remarque :*

	*Vous pouvez également faire le choix d'utiliser les services cloud pour la création de la base de données SQL (par exemple sur le data warehouse BigQuery de GCP)*

<br />

3. Utilisation d'un environnement virtuel
	
	Si vous souhaitez utiliser un environnement virtuel, vous pouvez installer les dépendances du fichier `requirements.txt` comme ceci :

	*Linux / MacOS / WSL2*
	```
	python3 -m venv venv/
	source venv/bin/activate
	pip install -r requirements.txt
	```
	
	<br/>

	*Windows*
	```
	python3 -m venv venv/
	C:\<chemin_dossir>\venv\Scripts\activate.bat
	pip install -r requirements.txt
	```
	
	*Remarque :*

	*Pour les machines sous Windows, on pourra utiliser :*
	
	- *<a href="https://code.visualstudio.com/download">Visual Studio Code</a> en tant qu'IDE*

	- *couplé à <a href="https://learn.microsoft.com/fr-fr/windows/wsl/install">WSL2</a> (qui permet d'installer facilement une distribution Linux et d'utiliser les outils en ligne de commande Bash directement sous Windows, sans passer par une machine virtuelle)*

<br />

4. Installer VcXsrv

	VcXsrv est un outil permettant de gérer l'accès souris/écran/clavier.
	
	Ici, il est utilisé pour simuler une sortie écran sur une distribution Linux depuis Windows, ce qui permet l'ouverture d'un navigateur Web pour la connexion à l'API depuis WSL2.

	Une procédure d'installation détaillée est décrite dans le fichier `setup/setup_chrome_vcxsrv.md` .

<br />

5. Paramétrage d'Apache Airflow

	Apache Airflow est utilisé dans ce projet pour automatiser les pipelines de données. La version utilisée est la version 2.5.2 .

	Avant de pouvoir l'utiliser pour exécuter des workflows, un minimum de paramétrage sera nécessaire.

	Une procédure d'installation détaillée est décrite dans le fichier `setup/setup_airflow.md` . 

<br />

### **Démarrage**

- #### Documentation

	Un article concernant les API Île-de-France Mobilités et leurs données temps réels est disponible :
	
	- <a href="https://prim.iledefrance-mobilites.fr/fr/actualites/article/temps-reel">Le temps réel et les API Île-de-France Mobilités</a>

	<br/>

	Une documentation générale est également disponible pour mieux appréhender les API et les données exposées :

	- <a href="https://prim.iledefrance-mobilites.fr/content/files/2023/03/Documentation-fonctionnelle-PRIM----Syst-me-d-authentification--5.pdf">Documentation fonctionnelle PRIM - Système d'authentification</a>
	- <a href="https://learn.microsoft.com/fr-fr/windows/wsl/install">Documentation fonctionnelle PRIM - Prise en main des API temps réel IDFM</a>

- #### Création d'un compte utilisateur

	Un compte utilisateur sera nécessaire pour pouvoir utiliser l'API Prochains passages (plateforme Île-de-France Mobilités) - Requête globale. Il peut être créé <a href="https://connect.navigo.fr/auth/realms/connect-b2b/protocol/openid-connect/auth?client_id=prim&redirect_uri=https://prim.iledefrance-mobilites.fr/fr/&response_type=code&scope=openid%20email">ici</a>.

- #### Création de la base de données dans PostgreSQL
 
	Des scripts SQL sont disponibles dans le dossier `sql/` pour la création des différentes tables utilisées, notamment les tables de dimension.

    Un schéma basique du modèle de données utilisé est donné par l'image `sql/star_schema.png` .

	*Remarque : pgAdmin pourra être utilisé pour créer la base de données.*

- #### Extraction et transformation des données brutes

	Le script `src/extract_and_transform_job.py` permet d'extraire les données temps réel de l'API "Prochains passages", de les transformer puis de les sauvegarder sous format de fichiers .csv .

	Le choix a été fait de ne conserver qu'une partie des données extraites (données de la ligne de tramway T4), par souci de volumétrie des données.

- #### Ingestion des données dans PostgreSQL

	Le script `src/load_job.py` permet de charger les fichiers .csv sauvegardés précédemment dans la table `prochains_passages_T4` de la base Postgres.

    Les variables d'environnement spécifiées dans le fichier de configuration `src/custom/postgresql/database.ini` correspondent aux logins pour se connecter à PostgreSQL. Il faudra donc :
	- soit créer ces variables d'environnement
	- soit modifier la connexion à PostgreSQL pour s'affranchir de variables d'environnement.

- #### Data visualisation

	Le script `src/my_data_viz.py` présente un exemple de visualisation (histogramme empilé) des données agrégées (pourcentage de tramways par station et par statut, à destination de la station 'Aulnay-sous-Bois', pour la journée du 18 juillet 2023).

	Le fichier de sortie est sauvegardé sous format HTML, pour conserver l'interactivité du graphique.

	Le graphique pour les données du 18 juillet 2023 est disponible dans le fichier `data/20230718_my_bar_graph.html` .

- #### **Automatisation avec Airflow**

	Des exemples de DAG Airflow sont disponibles pour la planification et l'automatisation du lancement des différents workflows :

	- `dag_example_ET_job.py` : pour la collecte continue des données et de leur transformation, avec une fréquence de 15 minutes tous les jours de la semaine

	- `dag_example_LOAD_job.py` : pour le chargement des données dans la base Postgres, une fois par jour (tous les jours à 6h00)

	- `dag_example_DATA_VIZ_job.py` : pour la création et la sauvegarde du graphique représentant une agrégation des données quotidiennes, chaque jour à 6h00 sur les données de la veille

<br/>

### **Licence**

- *MIT License pour la réutilisation des scripts partagés ici*

- *L'utilisation de l'API Île-de-France Mobilités est soumise à des <a href="https://prim.iledefrance-mobilites.fr/fr/conditions-utilisation">Conditions Générales d'Utilisation</a>. Les données issues de l'API Île-de-France Mobilités sont soumises à la <a href="https://cloud.fabmob.io/s/eYWWJBdM3fQiFNm?ref=ile-de-france-mobilites">Licence Mobilité</a>.*

<br/>

### **Contact**

Pour toute question, voici l'adresse mail de contact : [mohamedrkheroua@gmail.com](mailto:mohamedrkheroua@gmail.com)