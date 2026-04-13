# Coaching App — Maxliftt

Application Flask qui génère automatiquement des PDFs de coaching personnalisés.

## Déploiement sur Railway

1. Va sur https://railway.app et crée un compte (gratuit)
2. Clique sur "New Project" → "Deploy from GitHub"
3. Upload ce dossier sur GitHub d'abord (voir ci-dessous)
4. Dans Railway, va dans "Variables" et ajoute :
   - ANTHROPIC_API_KEY = ta clé API Anthropic (sur https://console.anthropic.com)
5. Railway démarre automatiquement l'app et te donne une URL publique

## Mettre le dossier sur GitHub

1. Va sur https://github.com et crée un compte
2. Crée un nouveau repository (bouton vert "New")
3. Installe GitHub Desktop sur ton PC : https://desktop.github.com
4. Glisse le dossier coaching_app dans GitHub Desktop et publie

## URL de l'app

Une fois déployée, ton app sera accessible à une URL du type :
https://coaching-app-xxxx.railway.app

## Endpoint principal

POST /generate
Corps JSON avec les paramètres client → renvoie le PDF

## Test rapide

curl -X POST https://ton-url.railway.app/generate \
  -H "Content-Type: application/json" \
  -d '{"nom":"Thomas","age":22,"taille":"1m82","poids":80,"bf":12,"niveau":"intermédiaire","jours_dispo":5,"objectif":"pdm","points_faibles":["épaules"],"points_forts":["dos"],"objectif_force":null,"passe_morpho":"mince"}' \
  --output Thomas.pdf
