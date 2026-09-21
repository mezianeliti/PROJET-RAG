"""Étape 6 du RAG : générer une réponse à partir des chunks trouvés.

Usage :
    .venv/bin/python src/answer.py                     # questions d'exemple
    .venv/bin/python src/answer.py "ta question ici"   # ta propre question
"""

import os
import sys
from pathlib import Path

import anthropic

from embed import charger_modele
from search import chercher, preparer

MODELE_IA = "claude-opus-5"

# La consigne donnée à l'IA. C'est elle qui l'empêche d'inventer.
CONSIGNE = """Tu réponds à des questions sur des documents de gestion immobilière.

Règles impératives :
- Réponds UNIQUEMENT à partir des extraits fournis.
- Si l'information ne s'y trouve pas, dis-le clairement. N'invente jamais.
- Reproduis les montants et les dates exactement tels qu'ils apparaissent.
- Réponds en français, de façon courte et directe."""

QUESTIONS_EXEMPLE = [
    "Qui n'a pas payé son loyer ?",
    "Quel est le montant total encaissé ?",
    "Quelle est la capitale du Japon ?",  # hors-sujet volontaire : l'IA doit refuser
]


def charger_env(chemin=".env"):
    """Lit un fichier .env (des lignes CLE=valeur) et charge ses variables.

    Un .env n'a rien de magique : c'est un simple fichier texte, gardé
    hors de Git, où l'on range les secrets au lieu de les écrire dans le code.
    """
    fichier = Path(chemin)
    if not fichier.exists():
        return False

    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, valeur = ligne.split("=", 1)
        os.environ.setdefault(cle.strip(), valeur.strip().strip('"').strip("'"))

    return True


def construire_prompt(question, resultats):
    """Assemble les extraits trouvés et la question en un seul message."""
    extraits = [
        f"[Extrait {numero} — pertinence {score:.2f}]\n{chunk}"
        for score, numero, chunk in resultats
    ]
    contexte = "\n\n".join(extraits)
    return f"Extraits du document :\n\n{contexte}\n\n---\n\nQuestion : {question}"


def repondre(client, question, resultats):
    """Envoie les extraits + la question à l'IA et renvoie sa réponse."""
    reponse = client.messages.create(
        model=MODELE_IA,
        max_tokens=1000,
        system=CONSIGNE,
        messages=[{"role": "user", "content": construire_prompt(question, resultats)}],
    )
    return "".join(bloc.text for bloc in reponse.content if bloc.type == "text")


if __name__ == "__main__":
    charger_env()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Aucune clé d'API trouvée.")
        print("   Crée un fichier .env à la racine du projet, contenant :")
        print("   ANTHROPIC_API_KEY=sk-ant-ta-cle-ici")
        sys.exit(1)

    client = anthropic.Anthropic()

    print("Chargement du modèle d'embeddings…")
    modele = charger_modele()

    print("Lecture et vectorisation du document…")
    chunks, vecteurs = preparer(modele)
    print(f"{len(chunks)} chunks prêts.\n")

    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else QUESTIONS_EXEMPLE

    for question in questions:
        resultats = chercher(question, chunks, vecteurs, modele)

        print("=" * 70)
        print(f"QUESTION : {question}")
        print("=" * 70)

        numeros = ", ".join(f"chunk {n} ({s:.2f})" for s, n, _ in resultats)
        print(f"Extraits envoyés à l'IA : {numeros}")

        print(f"\nRÉPONSE :\n{repondre(client, question, resultats)}\n")
