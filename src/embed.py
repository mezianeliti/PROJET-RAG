"""Étape 4 du RAG : transformer chaque chunk en vecteur de nombres."""

from sentence_transformers import SentenceTransformer

from chunk_text import decouper
from clean_text import CHEMIN_PDF, extraire_texte, nettoyer

# Modèle multilingue : il comprend le français. 384 nombres par vecteur.
MODELE = "paraphrase-multilingual-MiniLM-L12-v2"


def charger_modele(nom=MODELE):
    """Charge le modèle. Le télécharge automatiquement au premier appel."""
    return SentenceTransformer(nom)


def vectoriser(modele, textes):
    """Transforme une liste de textes en liste de vecteurs."""
    return modele.encode(textes)


if __name__ == "__main__":
    print("Chargement du modèle (téléchargement au premier lancement)…")
    modele = charger_modele()

    texte = nettoyer(extraire_texte(CHEMIN_PDF))
    chunks = decouper(texte)
    vecteurs = vectoriser(modele, chunks)

    print(f"\n=== {len(chunks)} CHUNKS VECTORISÉS ===")
    for numero, (chunk, vecteur) in enumerate(zip(chunks, vecteurs), start=1):
        apercu = chunk.replace("\n", " ")[:45]
        premiers = ", ".join(f"{v:+.3f}" for v in vecteur[:4])
        print(f"  Chunk {numero} : {len(vecteur)} nombres  [{premiers}, …]  « {apercu}… »")

    # Reprise de la démo qui échouait, cette fois avec un vrai modèle.
    print("\n=== LE TEST QUI ÉCHOUAIT AVEC LE COMPTAGE DE MOTS ===")

    phrases = [
        "le loyer du local A est payé",
        "le loyer du local B est en retard",
        "les charges de copropriété sont réglées",
        "le contrat de bail arrive à échéance",
    ]
    question = "qui n'a pas payé son bail"

    v_phrases = vectoriser(modele, phrases)
    v_question = vectoriser(modele, [question])[0]

    scores = []
    for phrase, v in zip(phrases, v_phrases):
        # Similarité cosinus, la même formule que dans demo_embeddings.py
        produit = sum(a * b for a, b in zip(v_question, v))
        norme1 = sum(a * a for a in v_question) ** 0.5
        norme2 = sum(b * b for b in v) ** 0.5
        scores.append((produit / (norme1 * norme2), phrase))

    print(f"Question : {question}\n")
    for score, phrase in sorted(scores, reverse=True):
        barre = "#" * max(0, int(score * 40))
        print(f"  {score:+.3f} {barre:<40} {phrase}")
