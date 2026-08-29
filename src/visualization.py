import pandas as pd
import matplotlib.pyplot as plt


def load_data():

    # Charge les données nettoyées.
    df = pd.read_csv(
        "data/processed/dvf_cote_emerald.csv"
    )

    return df


# =========================================================
# Prix moyen au m² par commune
# =========================================================

def prix_moyen_par_commune(df):

    # Crée une nouvelle figure.
    plt.figure()

    # Donne un titre à la fenêtre.
    manager = plt.get_current_fig_manager()
    manager.set_window_title(
        "Prix moyen au m² par commune"
    )

    # Calcule le prix moyen au m² par commune.
    prix_communes = (
        df.groupby("nom_commune")["prix_m2"]
        .mean()
        .sort_values(ascending=False)
    )

    # Crée le diagramme.
    ax = prix_communes.plot(kind="bar")

    # Ajoute la valeur au-dessus de chaque barre.
    for barre in ax.patches:

        valeur = barre.get_height()

        ax.annotate(
            f"{valeur:,.0f}",
            (barre.get_x() + barre.get_width() / 2, valeur),
            ha="center",
            va="bottom"
        )

    # Nomme les axes.
    ax.set_ylabel("Prix moyen (€/m²)")
    ax.set_xlabel("Commune")

    # Garde les noms des communes horizontaux.
    plt.xticks(rotation=0)

    # Ajuste automatiquement les espaces.
    plt.tight_layout()


# =========================================================
# Nombre de ventes par commune
# =========================================================

def nombre_ventes_par_commune(df):

    # Crée une nouvelle figure.
    plt.figure()

    # Donne un titre à la fenêtre.
    manager = plt.get_current_fig_manager()
    manager.set_window_title(
        "Nombre de ventes par commune"
    )

    # Compte les ventes par commune.
    ventes_communes = (
        df["nom_commune"]
        .value_counts()
        .sort_values(ascending=False)
    )

    # Crée le diagramme.
    ax = ventes_communes.plot(kind="bar")

    # Ajoute la valeur au-dessus de chaque barre.
    for barre in ax.patches:

        valeur = barre.get_height()

        ax.annotate(
            f"{valeur:,.0f}",
            (barre.get_x() + barre.get_width() / 2, valeur),
            ha="center",
            va="bottom"
        )

    # Nomme les axes.
    ax.set_ylabel("Nombre de ventes")
    ax.set_xlabel("Commune")

    # Garde les noms des communes horizontaux.
    plt.xticks(rotation=0)

    # Ajuste automatiquement les espaces.
    plt.tight_layout()


# =========================================================
# Prix moyen au m² par type de bien
# =========================================================

def prix_moyen_par_type(df):

    # Crée une nouvelle figure.
    plt.figure()

    # Donne un titre à la fenêtre.
    manager = plt.get_current_fig_manager()
    manager.set_window_title(
        "Prix moyen au m² par type de bien"
    )

    # Calcule le prix moyen au m² par type de bien.
    prix_types = (
        df.groupby("type_local")["prix_m2"]
        .mean()
        .sort_values(ascending=False)
    )

    # Crée le diagramme.
    ax = prix_types.plot(kind="bar")

    # Ajoute la valeur au-dessus de chaque barre.
    for barre in ax.patches:

        valeur = barre.get_height()

        ax.annotate(
            f"{valeur:,.0f}",
            (barre.get_x() + barre.get_width() / 2, valeur),
            ha="center",
            va="bottom"
        )

    # Nomme les axes.
    ax.set_ylabel("Prix moyen (€/m²)")
    ax.set_xlabel("Type de bien")

    # Garde les noms horizontaux.
    plt.xticks(rotation=0)

    # Ajuste automatiquement les espaces.
    plt.tight_layout()


# =========================================================
# Nombre de ventes par type de bien
# =========================================================

def nombre_ventes_par_type(df):

    # Crée une nouvelle figure.
    plt.figure()

    # Donne un titre à la fenêtre.
    manager = plt.get_current_fig_manager()
    manager.set_window_title(
        "Nombre de ventes par type de bien"
    )

    # Compte les ventes par type de bien.
    ventes_types = (
        df["type_local"]
        .value_counts()
        .sort_values(ascending=False)
    )

    # Crée le diagramme.
    ax = ventes_types.plot(kind="bar")

    # Ajoute la valeur au-dessus de chaque barre.
    for barre in ax.patches:

        valeur = barre.get_height()

        ax.annotate(
            f"{valeur:,.0f}",
            (barre.get_x() + barre.get_width() / 2, valeur),
            ha="center",
            va="bottom"
        )

    # Nomme les axes.
    ax.set_ylabel("Nombre de ventes")
    ax.set_xlabel("Type de bien")

    # Garde les noms horizontaux.
    plt.xticks(rotation=0)

    # Ajuste automatiquement les espaces.
    plt.tight_layout()


# =========================================================
# Prix moyen au m² par commune et type de bien
# =========================================================

def prix_commune_type(df):

    # Crée une figure et son axe.    
    # plt.subplots() retourne 2 objets :
    # fig
    #  ↓
    # La figure complète
    #        │
    #        └── ax
    #             ↓
    #             Zone du graphique
    #             │
    #             ├── Axe X (abscisses)
    #             └── Axe Y (ordonnées)
    # Sans déballage (unpacking) :
    # resultat = plt.subplots()
    # fig = resultat[0]
    # ax = resultat[1]
    # Python permet de faire directement :
    fig, ax = plt.subplots()

    # Donne un titre à la fenêtre.
    fig.canvas.manager.set_window_title(
        "Prix moyen au m² par commune et type de bien"
    )

    # Calcule le prix moyen par commune et type.
    prix = (
        df.groupby(
            ["nom_commune", "type_local"]
        )["prix_m2"]
        .mean()
        .unstack()
        .sort_index()
    )

    # Crée le diagramme dans l'axe ax.
    # La légende est créée automatiquement.
    prix.plot(kind="bar", ax=ax)

    # Ajoute la valeur au-dessus de chaque barre.
    for barre in ax.patches:

        valeur = barre.get_height()

        ax.annotate(
            f"{valeur:,.0f}",
            (barre.get_x() + barre.get_width() / 2, valeur),
            ha="center",
            va="bottom"
        )

    # Nomme les axes.
    ax.set_ylabel("Prix moyen (€/m²)")
    ax.set_xlabel("Commune")

    # Garde les noms des communes horizontaux.
    plt.xticks(rotation=0)

    # Ajuste automatiquement les espaces.
    plt.tight_layout()

# =========================================================
# Lancement des visualisations
# =========================================================

def run_visualization():

    print("==============================")
    print("VISUALISATION DVF - Côte d'Émeraude")
    print("==============================")

    df = load_data()

    # Crée une figure pour chaque analyse.
    prix_moyen_par_commune(df)

    nombre_ventes_par_commune(df)

    prix_moyen_par_type(df)

    nombre_ventes_par_type(df)

    prix_commune_type(df)

    # Affiche toutes les figures.
    plt.show()


if __name__ == "__main__":
    run_visualization()