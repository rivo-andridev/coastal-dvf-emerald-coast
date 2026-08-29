import pandas as pd


def load_data():

    print("Chargement des données nettoyées...")

    df = pd.read_csv(
        "data/processed/dvf_cote_emerald.csv"
    )

    print("Données chargées !")
    print(f"Nombre de lignes : {len(df)}")

    return df


# ===========================
# KPI principaux
# ===========================

def kpi_principaux(df):

    print("\n===== KPI PRINCIPAUX =====")

    # Nombre total de ventes
    nombre_ventes = len(df)

    print(f"Nombre total de ventes : {nombre_ventes}")

    # Prix moyen au m²
    prix_moyen = df["prix_m2"].mean()

    print(f"Prix moyen : {prix_moyen:,.0f} €/m²")

    # Prix médian au m²
    prix_median = df["prix_m2"].median()

    print(f"Prix médian : {prix_median:,.0f} €/m²")


    # ===========================
    # Commune la plus chère
    # ===========================

    prix_communes = (
        df.groupby("nom_commune")["prix_m2"]
        .mean()
        .sort_values(ascending=False)
    )

    # index[0] récupère le nom de la première commune du classement.
    commune_plus_chere = prix_communes.index[0]
    # iloc[0] récupère le prix correspondant à cette première commune.
    prix_commune_plus_chere = prix_communes.iloc[0]

    print(
        f"Commune la plus chère : "
        f"{commune_plus_chere} "
        f"({prix_commune_plus_chere:,.0f} €/m²)"
    )


    # ===========================
    # Commune avec le plus de ventes
    # ===========================

    ventes_communes = df["nom_commune"].value_counts()

    # Première commune = celle qui possède le plus de ventes.
    commune_plus_vendue = ventes_communes.index[0]
    # Nombre de ventes correspondant à cette commune.
    nombre_ventes_commune = ventes_communes.iloc[0]

    print(
        f"Commune avec le plus de ventes : "
        f"{commune_plus_vendue} "
        f"({nombre_ventes_commune} ventes)"
    )


    # ===========================
    # Type de bien le plus cher
    # ===========================

    prix_types = (
        df.groupby("type_local")["prix_m2"]
        .mean()
        .sort_values(ascending=False)
    )

    # Premier type = celui dont le prix moyen au m² est le plus élevé.
    type_plus_cher = prix_types.index[0]
    # Prix correspondant à ce type de bien.
    prix_type_plus_cher = prix_types.iloc[0]

    print(
        f"Type de bien le plus cher : "
        f"{type_plus_cher} "
        f"({prix_type_plus_cher:,.0f} €/m²)"
    )


    # ===========================
    # Type de bien le plus vendu
    # ===========================

    ventes_types = df["type_local"].value_counts()

    # Premier type = celui qui possède le plus de ventes.
    type_plus_vendu = ventes_types.index[0]

    # Nombre de ventes correspondant à ce type.
    nombre_ventes_type = ventes_types.iloc[0]

    print(
        f"Type de bien le plus vendu : "
        f"{type_plus_vendu} "
        f"({nombre_ventes_type} ventes)"
    )


# ===========================
# Analyse des prix par commune
# ===========================
def analyse_communes(df):

    print("\n===== Prix moyen au m² par commune =====")

    prix_communes = (
    df.groupby("nom_commune")["prix_m2"]
    .mean()
    .sort_values(ascending=False) # Des communes les plus chères vers les moins chères.
    )

    for commune, prix in prix_communes.items():# Un Tuple (clé= "nom_commune" , valeur = "prix_m2")
        print(f"{commune} : {prix:,.0f} €/m²")


# ===========================
# Nombre de ventes par commune
# ===========================
def nombre_ventes_communes(df):

    print("\n===== Nombre de ventes par commune =====")

    ventes_communes = (
        df["nom_commune"]
        .value_counts()
    )

    for commune, nombre in ventes_communes.items():
        print(f"{commune} : {nombre} ventes")


# ===================================
# Part des ventes par commune
# ===================================

def part_ventes_communes(df):

    print("\n===== Part des ventes par commune =====")

    # Compte le nombre de ventes pour chaque commune.
    ventes_communes = df["nom_commune"].value_counts()

    # Calcule le pourcentage des ventes de chaque commune
    # par rapport au nombre total de ventes.
    part_ventes = (
        ventes_communes / len(df) * 100
    )

    # Affiche les communes de la plus représentée à la moins représentée.
    for commune, part in part_ventes.items():
        print(f"{commune} : {part:.1f} % des ventes")


# ===========================
# Analyse des prix par type de bien
# ===========================
def analyse_types_biens(df):

    print("\n===== Prix moyen au m² par type de bien =====")

    prix_types = (
    df.groupby("type_local")["prix_m2"]
    .mean()
    .sort_values(ascending=False)
    )

    for type_bien, prix in prix_types.items():
        print(f"{type_bien} : {prix:,.0f} €/m²")

# ===================================
# Nombre de ventes par Types de Biens
# ===================================

def nombre_ventes_types(df):

    print("\n===== Nombre de ventes par Types de Biens =====")

    ventes_types = (
        df["type_local"]
        .value_counts()
    )

    for type_bien, nombre in ventes_types.items():
        print(f"{type_bien} : {nombre} ventes")


# ===================================
# Part des ventes par type de bien
# ===================================

def part_ventes_types(df):

    print("\n===== Part des ventes par type de bien =====")

    # Compte le nombre de ventes pour chaque type de bien.
    ventes_types = df["type_local"].value_counts()

    # Calcule la part de chaque type de bien
    # par rapport au nombre total de ventes.
    part_ventes = (
        ventes_types / len(df) * 100
    )

    # Affiche les types de biens du plus représenté au moins représenté.
    for type_bien, part in part_ventes.items():
        print(f"{type_bien} : {part:.1f} % des ventes")


# ================================================
# Nombre de ventes par commune et par type de bien
# ================================================       

def nombre_ventes_types_par_commune(df):

    # Affiche le titre de l'analyse
    print("\n===== Nombre de ventes par commune et par type de bien =====")

    ventes = (
        # Regroupe les ventes par commune et par type de bien
        df.groupby(["nom_commune", "type_local"])

        # Compte le nombre de ventes dans chaque groupe
        .size()

        # Transforme les types de biens en colonnes
        # et remplace les valeurs manquantes par 0
        .unstack(fill_value=0)
        # Trie les communes par nombre d'appartements décroissant
        .sort_values("Appartement", ascending=False)
    )

    # Affiche le tableau final
    print(ventes)

# =========================================================
# Prix moyen au m² par commune et type de bien
# =========================================================

def prix_commune_type(df):

    print("\n===== Prix moyen au m² par commune et type de bien =====")

    # Calcule le prix moyen par commune et type de bien.
    prix = (
        df.groupby(["nom_commune", "type_local"])["prix_m2"]
        .mean()
        .unstack()       # Transforme les types de biens en colonnes.
        .sort_index()    # Trie les communes par ordre alphabétique.
    )

    # Affiche les prix arrondis à l'euro.
    print(prix.round(0))

# =========================================================
# Prix moyen et nombre de ventes par commune et type
# =========================================================

def prix_et_ventes_commune_type(df):

    print("\n===== Prix moyen et nombre de ventes par commune et type =====")

    # Regroupe les ventes par commune et type de bien.
    analyse = (
        df.groupby(["nom_commune", "type_local"])
        .agg(
            prix_moyen=("prix_m2", "mean"),       # Prix moyen au m²
            nombre_ventes=("prix_m2", "count")    # Nombre de ventes
        )
        .sort_index()                             # Trie par commune
    )

    # Arrondit les prix à l'euro.
    analyse["prix_moyen"] = analyse["prix_moyen"].round(0)

    print(analyse)

# =========================================================
# Vérification de la qualité des données
# =========================================================

def qualite_donnees(df):

    print("\n===== Qualité des données =====")

    # Compte les valeurs manquantes par colonne.
    valeurs_manquantes = df.isna().sum()

    print("Valeurs manquantes :")

    # Affiche uniquement les colonnes avec des valeurs manquantes.
    print(valeurs_manquantes[valeurs_manquantes > 0])

# =========================================================
# Taux de complétude des données
# =========================================================

def completude_donnees(df):

    print("\n===== Complétude des données =====")

    # Calcule le taux de données présentes pour chaque colonne.
    completude = df.notna().mean() * 100

    # .items() fournit (colonne, taux) ; Python fait le déballage (unpacking).
    for colonne, taux in completude.items():
        print(f"{colonne} : {taux:.1f} %")

# =========================================================
# Prix fiables selon le nombre de ventes
# =========================================================

def analyse_fiabilite(df, seuil=10):

    print("\n===== Fiabilité des prix par commune et type =====")

    analyse = (
        df.groupby(["nom_commune", "type_local"])
        .agg(
            prix_moyen=("prix_m2", "mean"),
            nombre_ventes=("prix_m2", "count")
        )
    )

    # Garde uniquement les groupes ayant au moins le seuil de ventes.
    # analyse[condition] = filtre les lignes qui respectent la condition.
    analyse = analyse[analyse["nombre_ventes"] >= seuil]

    # Trie du prix moyen le plus élevé au plus faible.
    analyse = analyse.sort_values("prix_moyen", ascending=False)

    # Arrondit les prix pour faciliter la lecture.
    analyse["prix_moyen"] = analyse["prix_moyen"].round(0)

    print(analyse)


def run_analysis():

    print("==============================")
    print("ANALYSE DVF - Côte d'Émeraude")
    print("==============================")

    df = load_data()   

    kpi_principaux(df)

    analyse_communes(df)

    nombre_ventes_communes(df)

    part_ventes_communes(df)

    analyse_types_biens(df)

    nombre_ventes_types(df)

    part_ventes_types(df)

    nombre_ventes_types_par_commune(df)

    prix_commune_type(df)

    prix_et_ventes_commune_type(df)

    qualite_donnees(df)

    completude_donnees(df)

    analyse_fiabilite(df)


if __name__ == "__main__":
    run_analysis()