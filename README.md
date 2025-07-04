# Docker Velib Project 🚲

## À propos du projet

Le projet Docker Velib est un système de gestion de vélos en libre-service, conçu avec une architecture moderne utilisant Docker pour faciliter le déploiement et le développement. Ce projet s'appuie sur une API Flask pour le backend, une base de données MySQL pour stocker les données, et comprend un script d'insertion de données pour alimenter la base avec des informations sur les stations Velib.

> **Important** : Ce projet Docker est le backend qui fonctionne avec l'application mobile Velib disponible sur [https://github.com/aariisto/Velib_MobileApp](https://github.com/aariisto/Velib_MobileApp). Pour une expérience complète, vous devez configurer les deux projets.

## 🛠 &nbsp;Tech Stack

- 🐍 &nbsp;
  ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)
  ![Flask](https://img.shields.io/badge/-Flask-333333?style=flat&logo=flask)
  ![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-333333?style=flat&logo=sqlalchemy)
  ![JWT](https://img.shields.io/badge/-JWT-333333?style=flat&logo=json-web-tokens)
- 🛢 &nbsp;
  ![MySQL](https://img.shields.io/badge/-MySQL-333333?style=flat&logo=mysql)
- 🐳 &nbsp;
  ![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
  ![Docker Compose](https://img.shields.io/badge/-Docker%20Compose-333333?style=flat&logo=docker)
- 🔧 &nbsp;
  ![RESTful API](https://img.shields.io/badge/-RESTful%20API-333333?style=flat&logo=api)
  ![CORS](https://img.shields.io/badge/-CORS-333333?style=flat&logo=cors)

## 📂 Structure du projet

```
Docker_Velib/
│
├── docker-compose.yml     # Configuration Docker Compose
│
├── flask-app/             # Application Flask (Backend)
│   ├── ARCHITECTURE.md    # Documentation de l'architecture
│   ├── Dockerfile         # Configuration Docker pour Flask
│   ├── requirements.txt   # Dépendances Python
│   ├── server.py          # Point d'entrée de l'application
│   └── app/               # Structure modulaire de l'application
│       ├── __init__.py
│       ├── config.py      # Configuration de l'application
│       ├── decorators.py  # Décorateurs personnalisés (authentication)
│       ├── extensions.py  # Extensions Flask (SQLAlchemy)
│       ├── models/        # Modèles de données
│       ├── routes/        # Routes de l'API
│       └── services/      # Services métier
│
└── mysql/                 # Configuration MySQL et scripts d'insertion
    ├── database.sql       # Structure initiale de la base de données
    ├── Dockerfile         # Configuration Docker pour MySQL
    ├── insersion.py       # Script d'insertion de données
    └── requirements.txt   # Dépendances Python pour le script
```

## 🚀 &nbsp;Services

Le projet est divisé en trois services Docker:

### 1. flask-app

- API RESTful développée avec Flask
- Endpoints pour la gestion des stations, vélos, utilisateurs et réservations
- Authentification sécurisée avec JWT
- Structure modulaire avec separation des responsabilités (routes, models, services)

### 2. mysql

- Stockage persistant des données avec MySQL 8.0
- Base de données initialisée avec un script SQL
- Volume Docker pour préserver les données

### 3. python-script

- Script automatisé pour l'insertion de données
- Synchronisation des données entre l'API et la base de données
- Utilise wait-for-it pour assurer le bon ordre de démarrage des services

## 🌟 &nbsp;Fonctionnalités

- 🔐 &nbsp; Authentification sécurisée des utilisateurs
- 🔍 &nbsp; Recherche de stations et vélos disponibles
- 📝 &nbsp; Réservation de vélos
- 📊 &nbsp; Gestion des stations et vélos
- 🔄 &nbsp; Architecture modulaire et extensible

## 🚀 &nbsp;Démarrage rapide

```bash
# Cloner le repository
git clone https://github.com/aariisto/Docker_Velib_Mobile

# Accéder au dossier du projet
cd Docker_Velib

# Construire et démarrer les conteneurs
docker-compose up -d

# L'API est disponible à l'adresse
http://localhost:5001
```

## 📚 &nbsp;API Routes

### Voici le lien vers la [documentation complète de l'API](https://documenter.getpostman.com/view/39128991/2sB2x9hqEY)

- **Authentication**

  - `/api/auth/register` - Inscription utilisateur
  - `/api/auth/login` - Connexion utilisateur
  - `/api/auth/verify-token` - Vérifier la validité d'un token JWT

- **Stations**

  - `/api/station/stations` - Liste de toutes les stations Velib
  - `/api/station/stations/<station_id>` - Récupérer le statut d'une station spécifique

- **Search**

  - `/api/search/` (POST) - Rechercher des stations et sauvegarder la recherche (requiert authentification)
  - `/api/search/` (GET) - Récupérer l'historique des recherches d'un utilisateur (requiert authentification)
  - `/api/search/delete` (POST) - Supprimer une recherche par son ID (requiert authentification)

- **Reservations**

  - `/api/reservation/` (POST) - Créer une réservation (requiert authentification)
  - `/api/reservation/` (GET) - Obtenir les réservations d'un utilisateur (requiert authentification)

- **Hello World**
  - `/api/hello/` - Route de test pour vérifier que l'API fonctionne
 
### 🧪 Tests (Pytest)

Une base de tests automatisés a été mise en place avec **Pytest** pour valider certaines fonctionnalités critiques du backend. Cependant, les tests **ne sont pas encore complets** et plusieurs **configurations importantes restent à finaliser**.

> 🔧 Vous pouvez consulter l'état actuel des tests dans la branche [`tests` du projet](https://github.com/aariisto/Velib_MobileApp/tree/tests).

## 🔄 &nbsp;Relation avec l'application mobile

Ce projet Docker Velib est le **backend** qui fournit les API nécessaires au fonctionnement de l'application mobile [MobileApp Vélib](https://github.com/aariisto/Velib_MobileApp).

L'architecture complète du système comprend:

- **Ce repository (backend)**: Services Docker avec API Flask et base de données MySQL
- **[MobileApp Vélib](https://github.com/aariisto/Velib_MobileApp) (frontend)**: Application mobile React Native pour la géolocalisation des stations

Pour déployer le système complet:

1. Configurez ce backend Docker selon les instructions de démarrage rapide
2. Configurez ensuite l'application mobile en suivant les instructions de son [README](https://github.com/aariisto/Velib_MobileApp)
