"""DÉMO pédagogique — comprendre les embeddings sans rien installer.

Ce fichier ne fait PAS partie du pipeline RAG. Il sert uniquement à
comprendre le mécanisme : texte -> nombres -> comparaison.
"""

import math

# Nos "documents" fictifs : ce dans quoi on va chercher.
DOCUMENTS = [
    "le loyer du local A est payé",
    "le loyer du local B est en retard",
    "les charges de copropriété sont réglées",
    "le contrat de bail arrive à échéance",
]


def en_mots(texte):
    """Découpe un texte en mots simples, en minuscules."""
    return texte.lower().split()


def construire_vocabulaire(textes):
    """Liste tous les mots distincts, dans un ordre fixe."""
    mots = set()
    for texte in textes:
        mots.update(en_mots(texte))
    return sorted(mots)


def vectoriser(texte, vocabulaire):
    """Transforme un texte en liste de nombres : un compteur par mot du vocabulaire."""
    mots = en_mots(texte)
    return [mots.count(mot) for mot in vocabulaire]


def similarite_cosinus(v1, v2):
    """Mesure si deux vecteurs pointent dans la même direction. Entre 0 et 1."""
    produit = sum(a * b for a, b in zip(v1, v2))
    norme1 = math.sqrt(sum(a * a for a in v1))
    norme2 = math.sqrt(sum(b * b for b in v2))

    if norme1 == 0 or norme2 == 0:
        return 0.0

    return produit / (norme1 * norme2)


def chercher(question, documents, vocabulaire):
    """Classe les documents du plus proche au plus éloigné de la question."""
    v_question = vectoriser(question, vocabulaire)

    scores = []
    for doc in documents:
        score = similarite_cosinus(v_question, vectoriser(doc, vocabulaire))
        scores.append((score, doc))

    return sorted(scores, reverse=True)


if __name__ == "__main__":
    vocabulaire = construire_vocabulaire(DOCUMENTS)

    print("=== 1. LE VOCABULAIRE ===")
    print(f"{len(vocabulaire)} mots distincts :")
    print(vocabulaire)

    print("\n=== 2. UN DOCUMENT DEVENU VECTEUR ===")
    exemple = DOCUMENTS[1]
    print(f"Texte  : {exemple}")
    print(f"Vecteur: {vectoriser(exemple, vocabulaire)}")
    print("(un nombre par mot du vocabulaire : 1 = présent, 0 = absent)")

    print("\n=== 3. RECHERCHE QUI MARCHE ===")
    question = "quel loyer est en retard"
    print(f"Question : {question}\n")
    for score, doc in chercher(question, DOCUMENTS, vocabulaire):
        barre = "#" * int(score * 40)
        print(f"  {score:.3f} {barre:<40} {doc}")

    print("\n=== 4. LA MÊME QUESTION, AUTREMENT FORMULÉE ===")
    question = "qui n'a pas payé son bail"
    print(f"Question : {question}\n")
    for score, doc in chercher(question, DOCUMENTS, vocabulaire):
        barre = "#" * int(score * 40)
        print(f"  {score:.3f} {barre:<40} {doc}")
