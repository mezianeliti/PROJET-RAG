"""Étape 3 du RAG : découper le texte propre en chunks, sans couper les lignes."""

from clean_text import CHEMIN_PDF, extraire_texte, nettoyer

TAILLE_CHUNK = 150        # taille visée, en caractères
LIGNES_REPRISES = 2       # lignes du chunk précédent recopiées au début du suivant


def decouper(texte, taille=TAILLE_CHUNK, lignes_reprises=LIGNES_REPRISES):
    """Découpe le texte en chunks en respectant les fins de ligne.

    Une ligne entre en entier dans un chunk ou pas du tout : elle n'est
    jamais coupée en deux. Chaque chunk reprend les dernières lignes du
    précédent (chevauchement) pour ne pas perdre l'info à la jonction.
    """
    chunks = []
    en_cours = []        # les lignes de la pile en construction
    longueur = 0         # taille actuelle de la pile, en caractères

    for ligne in texte.split("\n"):
        # La ligne ferait-elle déborder la pile ?
        if en_cours and longueur + len(ligne) + 1 > taille:
            chunks.append("\n".join(en_cours))

            # La nouvelle pile démarre avec les dernières lignes de l'ancienne.
            en_cours = en_cours[-lignes_reprises:] if lignes_reprises else []
            longueur = sum(len(l) + 1 for l in en_cours)

        en_cours.append(ligne)
        longueur += len(ligne) + 1

    # Ne pas oublier la dernière pile.
    if en_cours:
        chunks.append("\n".join(en_cours))

    return chunks


if __name__ == "__main__":
    texte = nettoyer(extraire_texte(CHEMIN_PDF))
    chunks = decouper(texte)

    print("=== RÉSUMÉ ===")
    print(f"Texte nettoyé : {len(texte)} caractères")
    print(f"Réglages      : {TAILLE_CHUNK} caractères max, {LIGNES_REPRISES} lignes reprises")
    print(f"Chunks créés  : {len(chunks)}")

    for numero, chunk in enumerate(chunks, start=1):
        lignes = len(chunk.splitlines())
        print(f"\n----- CHUNK {numero}/{len(chunks)} ({len(chunk)} car., {lignes} lignes) -----")
        print(chunk)
