# Architecture du Backend

```
backend/
│
├── .env                    # Variables d'environnement (DB, JWT, etc.)
├── requirements.txt        # Dépendances Python
├── server.py              # Point d'entrée de l'application
│
└── app/
    ├── __init__.py        # Initialisation de l'application Flask
    ├── config.py          # Configuration de l'application
    ├── extensions.py      # Extensions Flask (SQLAlchemy)
    ├── decorators.py      # Décorateurs (token_required)
    │
    ├── models/            # Modèles de données
    │   ├── __init__.py
    │   └── user_model.py  # Modèle utilisateur
    │
    ├── routes/            # Routes de l'API
    │   ├── __init__.py
    │   ├── auth_routes.py # Routes d'authentification
    │   └── hello_routes.py# Routes de test
    │
    └── services/          # Services métier
        ├── __init__.py
        ├── auth_service.py# Service d'authentification
        └── token_service.py# Service de gestion des tokens

```

## Description des composants

### 1. Configuration et initialisation

- `.env`: Configuration des variables d'environnement
- `server.py`: Point d'entrée, initialisation du serveur
- `config.py`: Configuration de Flask et des extensions

### 2. Authentification et Sécurité

- `decorators.py`: Protection des routes avec JWT
- `services/token_service.py`: Gestion des tokens JWT
- `services/auth_service.py`: Logique d'authentification

### 3. Base de données

- `extensions.py`: Configuration SQLAlchemy
- `models/user_model.py`: Modèle de données utilisateur

### 4. API Routes

- `routes/auth_routes.py`: Endpoints d'authentification (/register, /login)
- `routes/hello_routes.py`: Routes de test

## Flux de données typique

1. Client → Routes
2. Routes → Services
3. Services → Modèles
4. Modèles → Base de données

## Sécurité

- Hashage des mots de passe avec bcrypt
- Authentification par JWT
- Protection CORS
- Validation des données d'entrée
