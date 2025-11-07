🚀 Mise à Jour Automatisée de Page Confluence
Ce projet fournit une solution d'automatisation pour maintenir à jour une table de topologie ou d'inventaire sur une page Confluence. 
L'objectif principal est de permettre la mise à jour en masse d'informations dans Confluence dans le cadre d'un processus de déploiement ou d'un workflow CI/CD.
✨ Fonctionnalités
Ciblage par ID : Met à jour une table sur une page Confluence spécifique via son ID, ce qui est rapide et fiable.
Création ou Modification : Recherche une ligne basée sur une colonne de référence unique (Ref).
Si la référence existe, les colonnes Login et Password sont mises à jour.
Si la référence n'est pas trouvée, une nouvelle ligne est créée avec les informations fournies.
Sécurité : Gestion sécurisée des identifiants de l'API Confluence via un fichier .env qui n'est pas versionné dans Git.

🔧 Prérequis
Avant de commencer, assurez-vous d'avoir installé les éléments suivants :
Python (version 3.8+ recommandée)
pip (le gestionnaire de paquets pour Python)
Un accès à une instance Confluence Cloud ou Server.
Un token API Atlassian avec les permissions nécessaires pour lire et écrire sur la page cible.
⚙️ Installation
Clonez le dépôt :
code
Bash
git clone [URL_DE_VOTRE_DEPOT]
cd [NOM_DE_VOTRE_DEPOT]
Créez un environnement virtuel (recommandé) :
code
Bash
python -m venv .venv
source .venv/bin/activate
# Sur Windows, utilisez : .\.venv\Scripts\activate
Installez les dépendances Python :
Le fichier requirements.txt contient toutes les bibliothèques Python nécessaires.
code
Bash
pip install -r requirements.txt
```    *(Si vous n'avez pas de fichier `requirements.txt`, créez-le avec le contenu suivant :)*
requirements.txt
requests
beautifulsoup4
python-dotenv
code
Code
🔑 Configuration
La configuration des accès à l'API Confluence se fait via un fichier .env.
Créez le fichier .env :
Créez un fichier nommé .env à la racine du projet. Ce fichier est ignoré par Git (via .gitignore) pour ne jamais exposer vos identifiants.
Remplissez le fichier .env avec vos informations :
code
Ini
# .env
CONFLUENCE_EMAIL="votre_email@exemple.com"
CONFLUENCE_API_TOKEN="VOTRE_TOKEN_API_SECRET_ATLASSIAN"
