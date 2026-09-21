# PROJET RAG LITI

Prototype de **recherche documentaire augmentée (RAG)**, construit étape par étape en Python simple.

Objectif final : ajouter une brique RAG à un SaaS immobilier Django — poser une question sur ses
documents (contrats, paiements, informations locataires) et obtenir une réponse fondée sur ces
documents.

## La feuille de route

| Étape | Ce qu'elle fait | Fichier | État |
|:---|:---|:---|:---|
| 1 | Extraire le texte d'un PDF | `src/extract_pdf.py` | ✅ Fait |
| 2 | Nettoyer le texte | `src/clean_text.py` | ✅ Fait |
| 3 | Découper en chunks | `src/chunk_text.py` | ✅ Fait |
| 4 | Transformer les chunks en vecteurs | `src/embed.py` | ✅ Fait |
| 5 | Rechercher par similarité | `src/search.py` | ✅ Fait |
| 6 | Générer la réponse | `src/answer.py` | 🚧 Écrit, en attente d'une clé d'API |
| 7 | Stocker en base (PostgreSQL + pgvector) | — | ⬜ À faire |
| 8 | Tâches en arrière-plan (Celery) | — | ⬜ À faire |
| 9 | Intégration Django | — | ⬜ À faire |

Les étapes 1 à 6 tournent en local, sans base de données ni framework. Chaque script se lance seul
et affiche son résultat : si ça casse, on sait où.

## Structure

```
PROJET RAG LITI/
├── src/                 le code Python, une étape par fichier
├── docs/                documentation du projet
├── documents/           les PDF de test — jamais versionnés
├── requirements.txt     les bibliothèques nécessaires
└── .gitignore           ce que Git doit ignorer
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
.venv/bin/python src/extract_pdf.py    # étape 1 : le texte du PDF
.venv/bin/python src/search.py         # étape 5 : chercher un passage
.venv/bin/python src/answer.py "..."   # étape 6 : poser une question
```

L'étape 6 a besoin d'une clé d'API, à placer dans un fichier `.env` à la racine :

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Protection des données

Les documents de test contiennent des données réelles (noms, loyers, impayés). Ils ne sont **jamais**
versionnés : `documents/`, `.env` et les documents de travail dérivés sont exclus par le `.gitignore`.
Aucune donnée réelle n'apparaît dans ce dépôt.
