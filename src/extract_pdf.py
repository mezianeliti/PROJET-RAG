# Étape 1 du RAG : extraire le texte d'un PDF et l'afficher page par page.

from pypdf import PdfReader

# Chemin du PDF, relatif à la racine du projet.
chemin_pdf = "documents/situation-holding-azazga-2026-08-v1.pdf"

# Ouvre le PDF et prépare sa lecture.
lecteur = PdfReader(chemin_pdf)

print(f"Fichier lu : {chemin_pdf}")
print(f"Nombre de pages : {len(lecteur.pages)}")

# Parcourt chaque page en gardant son numéro (en commençant à 1).
for numero, page in enumerate(lecteur.pages, start=1):
    texte = page.extract_text()
    print(f"\n===== PAGE {numero} =====")
    print(texte)
