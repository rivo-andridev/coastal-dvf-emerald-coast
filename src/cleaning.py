import pandas as pd
import requests
import os

DVF_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2024/full.csv.gz"

USE_COLS = [            # Les Champs dont on aura besoins
    "date_mutation",
    "nom_commune",
    "code_commune",
    "type_local",
    "surface_reelle_bati",
    "valeur_fonciere",
    "longitude",
    "latitude",
]

COMMUNES_INTERET = [    # Les Communes dont on aura besoins
    "Saint-Malo",
    "Cancale",
    "Dinard",
    "Saint-Coulomb",
]

TYPES_BIENS = [
    "Maison",
    "Appartement",
]

def download_data():
    print("Téléchargement des données DVF...")

    url = DVF_URL

    print(f"URL utilisée : {url}")

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        print("Téléchargement réussi !")
        os.makedirs("data/raw", exist_ok=True)

        print("Enregistrement sur le disque par blocs de 8192 octets...")
        # Ouvre (ou crée) le fichier en mode écriture binaire (.gz).
        nombre_blocs = 0
        taille_totale = 0
        with open("data/raw/dvf_2024.csv.gz", "wb") as file:
            # Lit la réponse HTTP par petits blocs de 8 Ko
            # afin de ne pas charger tout le fichier en mémoire RAM.
            for bloc in response.iter_content(chunk_size=8192):
                # Écrit chaque bloc dans le fichier au fur et à mesure du téléchargement.
                file.write(bloc)
                nombre_blocs += 1
                taille_totale += len(bloc)
                
        # Affiche le nombre de blocs écrits et la taille totale convertie en Mo avec 2 décimales.
        print(
                f"Écriture terminée : {nombre_blocs} blocs enregistrés "
                f"({taille_totale / 1024 / 1024:.2f} Mo)"
            )

        # Confirme que le téléchargement et l'enregistrement sont terminés.
        # Bien à l'exterieur de la boucle For du dessus pour eviter la répétion du message.
        print("Fichier enregistré dans data/raw/") 

    else:
        print(f"Erreur de téléchargement : {response.status_code}")
        print("Impossible de récupérer les données.")


def inspect_data():
    print("Inspection des données DVF par morceaux (Blocs)")

    # Correction : lecture du gros fichier DVF par blocs
    # pour éviter de charger tout le fichier en mémoire.
    chunks = pd.read_csv(
        "data/raw/dvf_2024.csv.gz",
        compression="gzip",        # fichier compressé .gz
        usecols=USE_COLS,          # garde uniquement les colonnes utiles
        chunksize=50000,           # lecture par blocs de 50 000 lignes
        on_bad_lines="warn",       # ignore les lignes mal formées
        engine="python"            # lecture plus tolérante après erreur pandas
    )

    # Stocke les blocs contenant les communes recherchées
    resultats = []

    # Traitement bloc par bloc
    print(f"Lecture du fichier DVF par blocs de {chunks.chunksize} lignes...")# chunksize=50000
    nombre_blocs = 0
    for chunk in chunks:
        nombre_blocs += 1        
        #print("Traitement d'un bloc :", chunk.shape), c'est une autre forme d'affichage
        # Filtre uniquement les communes de Côte d'Émeraude
        # Et les types de biens qui nous intéressent
        chunk_filtre = chunk[
           (chunk["nom_commune"].isin(COMMUNES_INTERET))
            &
           (chunk["type_local"].isin(TYPES_BIENS))
        ]

        # Ajoute uniquement les blocs non vides
        if len(chunk_filtre) > 0:
            resultats.append(chunk_filtre)

    print(f"{nombre_blocs} blocs DVF traités.")
    
    # Regroupe tous les blocs filtrés dans un seul DataFrame
    if resultats:        
        df = pd.concat(resultats)

        # Supprime les lignes où la valeur de la colonne 'surface_reelle_bati' est manquante (NaN).
        df = df.dropna(subset=["surface_reelle_bati"]) 

        # On garde uniquement les surfaces strictement positives
        df = df[df["surface_reelle_bati"] > 0]

        # Ajoute une nouvelle NOUVELLE colonne "prix_m2" au DataFrame en calculant le prix au m² de chaque bien.
        df["prix_m2"] = (
            df["valeur_fonciere"] / df["surface_reelle_bati"]
        )
        # ===========================
        # Statistiques générales
        # ===========================

        print("\n===== Statistiques générales =====")

        print("Nombre de ventes :", len(df))

        # Moyenne
        print("Prix moyen au m² :")
        print(f"{df['prix_m2'].mean():,.0f} €/m²")

        # Prix médian au m² : valeur qui sépare les ventes en deux moitiés (50 % en dessous, 50 % au-dessus).
        print("\nPrix médian au m² :")
        print(f"{df['prix_m2'].median():,.0f} €/m²")

        # ===========================
        # Affichage du résultat
        # ===========================

        # Sauvegarde du résultat nettoyé pour les prochaines étapes du projet:

        # Création du dossier de sauvegarde des données traitées s'il n'existe pas.
        os.makedirs("data/processed", exist_ok=True)
        # Sauvegarde du DataFrame nettoyé au format CSV sans l'index Pandas.
        df.to_csv(
            "data/processed/dvf_cote_emerald.csv",
            index=False
        )

        print("\nFichier nettoyé enregistré dans data/processed/")

        print("\n=== Résultat final ===")
        print(df.head())

        print("\n=== Aperçu du prix au m² ===")
        print(
            df[
                [
                    "nom_commune",
                    "type_local",
                    "valeur_fonciere",
                    "surface_reelle_bati",
                    "prix_m2",
                ]
            ].head()
        )

        # Vérification des communes trouvées
        print("\nCommunes trouvées :")
        print(df["nom_commune"].unique())

        # Nombre total de transactions sélectionnées
        print("\nNombre de transactions retenues :")
        print(len(df))

    else:
        print("Aucune transaction trouvée.")


def run_pipeline():
    print("=================================")
    print("PIPELINE DVF - Côte d'Émeraude")
    print("Étape 1 : Initialisation")
    print("=================================")

    download_data()
    inspect_data()


if __name__ == "__main__":
    run_pipeline()

   # Ordre des processus:
#     1. importe pandas
#     2. importe requests
#     3. importe os
#     4. crée DVF_URL
#     5. crée download_data()
#     6. crée inspect_data()
#     7. crée run_pipeline()
#     8. arrive à : run_pipeline() et il lance le pipeline.
#
# Ici nous sommes dans le fichier cleaning.py :

#  Valeur de __name__ :
#
# Si on lance :
#     python cleaning.py
#
# Alors :
#     cleaning.__name__ == "__main__"
#
# Les modules importés conservent leur propre __name__ :
#
# cleaning.py
#
# ├── __name__ = "__main__"     (si lancé directement)
# ├── import pandas
# │       └── pandas.__name__ = "pandas"
# ├── import requests
# │       └── requests.__name__ = "requests"
# └── import os
#         └── os.__name__ = "os"