cat > README.md << 'EOF'
# Manhwa Project – Backend API

## Description

API REST (Flask + Flask-RESTx) pour la gestion d'une bibliothèque de manhwas :
utilisateurs, manhwas, genres et avis (reviews).

## Stack technique

- Python / Flask, Flask-RESTx (documentation Swagger)
- Flask-SQLAlchemy / SQLAlchemy (persistance)
- Flask-JWT-Extended (authentification JWT)
- Flask-Bcrypt (hachage des mots de passe)

## Architecture

Client → Services (routes) → Facade → Repository → Models

- **Models** : User, Manhwa, Genre, Review
- **Services** : endpoints REST et validation des entrées
- **Facade** : point d'accès unique à la logique métier
- **Repository** : couche de persistance
- **auth** : authentification et gestion des rôles (admin / utilisateur)

## Lancement

Depuis le dossier `hbnb` :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
