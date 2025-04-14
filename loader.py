import os
import requests
from pathlib import Path

GITHUB_USER = "SREIGNIER"
GITHUB_REPO = "chatbot-sre-ai"
DOCS_FOLDER = "docs"
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{DOCS_FOLDER}"
LOCAL_DOCS_PATH = Path("docs")

def download_docs_from_github():
    print("📥 Téléchargement des documents depuis GitHub...")

    if not LOCAL_DOCS_PATH.exists():
        LOCAL_DOCS_PATH.mkdir()

    filenames = [
        "Ajout Mail collaborateur VEOS (outlook)-VF.docx",
        "Ajout de Type ou modification GED sur VEOS - VF.docx",
        "Analyses et suivi des envois de mails - VF.docx",
        "CREATION COMPAGNIE METHODO SRE-VF.docx",
        "Codes situation de modèles de courriers et mails EUROSUD - VF.docx",
        "Création ou Modifications des produits VEOS - VF.docx",
        "Import Global des personnes VEOS - VF.docx",
        "METHODO ANNULATION REGLEMENT-VF.docx",
        "Modification des mails - VF.docx",
        "Modification documents VEOS - VF.docx",
        "Modifier et Ajouter de nouveaux barèmes de frais sur VEOS - VF.docx",
        "Modifier le produit d'un contrat VEOS - VF.docx",
        "Passer les collaborateurs à Manager sur VEOS - VF.docx",
        "PROCEDURE DE TRAITEMENT DES TERMES VEOS.docx",
        "Transférer un contrat à un autre assuré - VF.docx",
        "Utilisation d'EDI SIGNATURE - VF.docx"
    ]

    for filename in filenames:
        url = f"{RAW_URL}/{filename.replace(' ', '%20')}"
        local_file = LOCAL_DOCS_PATH / filename

        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(local_file, "wb") as f:
                f.write(response.content)
            print(f"✅ {filename} téléchargé.")
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement de {filename}: {e}")

