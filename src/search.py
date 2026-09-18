"""Étape 5 du RAG : poser une question et retrouver les chunks les plus proches.

Usage :
    .venv/bin/python src/search.py                     # questions d'exemple
    .venv/bin/python src/search.py "ta question ici"   # ta propre question
"""

import sys

from chunk_text import decouper
from clean_text import CHEMIN_PDF, extraire_texte, nettoyer
from embed import charger_modele, vectoriser

TOP = 3  # combien de chunks on garde

QUESTIONS_EXEMPLE = [
    "qui n'a pas payé son loyer",
    "quel est le montant total encaissé",
    "combien y a-t-il de locataires",
    "y a-t-il des dépenses enregistrées",
]


def similarite_cosinus(v1, v2):
    """Mesure si deux vecteurs pointent dans la même direction. Entre -1 et 1."""
    produit = sum(a * b for a, b in zip(v1, v2))
    norme1 = sum(a * a for a in v1) ** 0.5
    norme2 = sum(b * b for b in v2) ** 0.5

    if norme1 == 0 or norme2 == 0:
        return 0.0

    return produit / (norme1 * norme2)


def preparer(modele, chemin=CHEMIN_PDF):
    """Lit le PDF, le nettoie, le découpe et vectorise les chunks.

    À faire une seule fois : c'est l'étape lente.
    """
    chunks = decouper(nettoyer(extraire_texte(chemin)))
    vecteurs = vectoriser(modele, chunks)
    return chunks, vecteurs


def chercher(question, chunks, vecteurs, modele, top=TOP):
    """Renvoie les `top` chunks les plus proches de la question.

    Résultat : une liste de (score, numero_du_chunk, texte_du_chunk),
    du plus pertinent au moins pertinent.
    """
    v_question = vectoriser(modele, [question])[0]

    resultats = []
    for numero, (chunk, vecteur) in enumerate(zip(chunks, vecteurs), start=1):
        score = similarite_cosinus(v_question, vecteur)
        resultats.append((score, numero, chunk))

    resultats.sort(key=lambda r: r[0], reverse=True)
    return resultats[:top]


def afficher(question, resultats):
    """Affiche proprement le résultat d'une recherche."""
    print(f"\n{'=' * 70}")
    print(f"QUESTION : {question}")
    print("=" * 70)

    for rang, (score, numero, chunk) in enumerate(resultats, start=1):
        barre = "#" * max(0, int(score * 40))
        apercu = chunk.replace("\n", " · ")[:150]
        print(f"\n  #{rang} — chunk {numero} — score {score:+.3f}  {barre}")
        print(f"     {apercu}…")


if __name__ == "__main__":
    print("Chargement du modèle…")
    modele = charger_modele()

    print("Lecture et vectorisation du document…")
    chunks, vecteurs = preparer(modele)
    print(f"{len(chunks)} chunks prêts.")

    # Une question passée en argument, sinon les questions d'exemple.
    if len(sys.argv) > 1:
        questions = [" ".join(sys.argv[1:])]
    else:
        questions = QUESTIONS_EXEMPLE

    for question in questions:
        afficher(question, chercher(question, chunks, vecteurs, modele))
