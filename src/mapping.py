import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium


# =========================================================
# Chargement des données
# =========================================================

def load_data():

    # Charge le fichier CSV nettoyé.
    df = pd.read_csv(
        "data/processed/dvf_cote_emerald.csv"
    )

    return df


# =========================================================
# Création du GeoDataFrame
# =========================================================

def create_geodataframe(df):

    # Transforme longitude + latitude en points géographiques.
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(
            df["longitude"],
            df["latitude"]
        ),
        # Système de coordonnées géographiques.
        crs="EPSG:4326"
    )

    return gdf


# =========================================================
# Première carte des transactions
# =========================================================

def afficher_carte(gdf):

    # Crée une nouvelle figure.
    fig, ax = plt.subplots()

    # Donne un titre à la fenêtre.
    fig.canvas.manager.set_window_title(
        "Transactions DVF - Côte d'Émeraude"
    )

    # Affiche les transactions sous forme de points.
    gdf.plot(
        ax=ax,
        markersize=5
    )

    # Nomme les axes.
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Ajuste automatiquement les espaces.
    plt.tight_layout()

    # Affiche la carte.
    plt.show()


# =========================================================
# Création de la carte interactive
# =========================================================

def creer_carte_interactive(gdf):

    # Calcule la latitude moyenne.
    centre_lat = gdf["latitude"].mean()

    # Calcule la longitude moyenne.
    centre_lon = gdf["longitude"].mean()

    # Crée la carte interactive.
    #
    # OpenStreetMap est utilisé automatiquement
    # comme fond de carte par défaut par Folium.
    carte = folium.Map(
        location=[
            centre_lat,
            centre_lon
        ],
        zoom_start=11,

        # Autorise la carte à aller jusqu'au zoom 20.
        max_zoom=20
    )

    # =====================================================
    # FONDS DE CARTE
    # =====================================================

    # OpenStreetMap est déjà le fond de carte
    # créé automatiquement par folium.Map().
    #
    # Il ne faut donc PAS ajouter ici un deuxième
    # TileLayer("OpenStreetMap"), sinon nous aurions
    # deux couches OpenStreetMap dans le sélecteur.


    # =====================================================
    # COUCHE SATELLITE
    # =====================================================

    # Ajoute la couche satellite.
    #
    # IMPORTANT :
    # Satellite est une couche superposable.
    #
    # Cela permet de garder OpenStreetMap dessous
    # et de rendre le satellite transparent.
    satellite = folium.TileLayer(

        # Adresse du service satellite ArcGIS.
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),

        # Crédit obligatoire du fournisseur.
        attr="Esri",

        # Nom affiché dans le sélecteur de couches.
        name="Satellite",

        # Satellite est une couche superposable.
        overlay=True,

        # Affiche Satellite dans le contrôle des couches.
        control=True,

        # 100 % d'opacité au départ.
        opacity=1.0,

        # Satellite n'est PAS sélectionné au démarrage.
        show=False,

        # =================================================
        # Gestion du zoom satellite
        # =================================================

        # Dernier niveau de zoom avec une image
        # satellite réellement disponible.
        max_native_zoom=18,

        # Autorise Leaflet à continuer jusqu'au zoom 20.
        #
        # Au-delà de 18, Leaflet agrandit la dernière
        # image satellite disponible.
        max_zoom=20
    )

    # Ajoute la couche satellite à la carte.
    satellite.add_to(carte)

    return carte, satellite


# =========================================================
# Contrôle de l'opacité du satellite
# =========================================================

def ajouter_controle_opacite(carte, satellite):

    # Crée le panneau HTML du contrôle.
    #
    # Le panneau est caché au démarrage.
    #
    # Il apparaîtra uniquement lorsque l'utilisateur
    # activera la couche Satellite.
    html = """
    <div
        id="controle_opacite"
        style="
            display: none;
            position: absolute;
            top: 10px;
            right: 250px;
            z-index: 9999;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
            font-size: 13px;
        "
    >

        <label for="opacite_satellite">
            <b>Opacité satellite</b>
        </label>

        <br>

        <input
            id="opacite_satellite"
            type="range"
            min="0"
            max="100"
            value="100"
        >

        <span id="valeur_opacite">
            100 %
        </span>

    </div>
    """

    # Ajoute le panneau HTML dans la carte.
    carte.get_root().html.add_child(
        folium.Element(html)
    )


    # =====================================================
    # JavaScript
    # =====================================================

    script = f"""
    <script>

        document.addEventListener(
            "DOMContentLoaded",
            function() {{

                // Récupère le curseur.
                var curseur = document.getElementById(
                    "opacite_satellite"
                );

                // Récupère le texte qui affiche la valeur.
                var valeur = document.getElementById(
                    "valeur_opacite"
                );

                // Récupère le panneau complet.
                var controle = document.getElementById(
                    "controle_opacite"
                );


                // =========================================
                // Modification de l'opacité
                // =========================================

                // Surveille les mouvements du curseur.
                curseur.addEventListener(
                    "input",
                    function() {{

                        // Récupère la valeur du curseur.
                        var opacite = this.value;

                        // Affiche la valeur en pourcentage.
                        valeur.innerHTML = opacite + " %";

                        // Convertit le pourcentage
                        // en valeur comprise entre 0 et 1.
                        var opaciteLeaflet = opacite / 100;

                        // Applique l'opacité à la couche satellite.
                        {satellite.get_name()}.setOpacity(
                            opaciteLeaflet
                        );

                    }}
                );


                // =========================================
                // Affichage du contrôle lorsque Satellite
                // est sélectionné
                // =========================================

                // Surveille l'activation d'une couche.
                //
                // Satellite étant un overlay,
                // Leaflet déclenche "overlayadd".
                {carte.get_name()}.on(
                    "overlayadd",
                    function(e) {{

                        // Vérifie si la couche ajoutée
                        // est la couche Satellite.
                        if (e.layer === {satellite.get_name()}) {{

                            // Affiche le contrôle d'opacité.
                            controle.style.display = "block";

                        }}

                    }}
                );


                // =========================================
                // Masquage du contrôle lorsque Satellite
                // est désélectionné
                // =========================================

                // Surveille la désactivation d'une couche.
                //
                // Lorsque Satellite est décoché,
                // Leaflet déclenche "overlayremove".
                {carte.get_name()}.on(
                    "overlayremove",
                    function(e) {{

                        // Vérifie si la couche retirée
                        // est la couche Satellite.
                        if (e.layer === {satellite.get_name()}) {{

                            // Cache le contrôle d'opacité.
                            controle.style.display = "none";

                        }}

                    }}
                );

            }}
        );

    </script>
    """

    # Ajoute le JavaScript dans la carte.
    carte.get_root().html.add_child(
        folium.Element(script)
    )


# =========================================================
# Recherche d'une adresse
# =========================================================

def ajouter_recherche_adresse(carte):

    # Crée la zone de recherche.
    #
    # Elle permet à l'utilisateur de saisir
    # une adresse directement sur la carte.
    html = """
    <div
        id="recherche_adresse"
        style="
            position: absolute;
            top: 10px;
            left: 50px;
            z-index: 9999;
            background: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.4);
            font-size: 13px;
        "
    >

        <label for="adresse">
            <b>Rechercher une adresse</b>
        </label>

        <br>

        <input
            id="adresse"
            type="text"
            placeholder="Ex : 10 rue de la Gare, Saint-Malo"
            style="
                width: 260px;
                padding: 5px;
                margin-top: 5px;
            "
        >

        <button
            id="bouton_recherche"
            style="
                padding: 5px 8px;
                margin-left: 4px;
                cursor: pointer;
            "
        >
            🔍
        </button>

        <div
            id="message_recherche"
            style="
                margin-top: 5px;
                font-size: 12px;
            "
        >
        </div>

    </div>
    """

    # Ajoute la zone de recherche à la carte.
    carte.get_root().html.add_child(
        folium.Element(html)
    )


    # =====================================================
    # JavaScript de recherche
    # =====================================================

    script = f"""
    <script>

        document.addEventListener(
            "DOMContentLoaded",
            function() {{

                // Récupère le champ d'adresse.
                var champAdresse = document.getElementById(
                    "adresse"
                );

                // Récupère le bouton de recherche.
                var boutonRecherche = document.getElementById(
                    "bouton_recherche"
                );

                // Récupère la zone de message.
                var message = document.getElementById(
                    "message_recherche"
                );


                // =========================================
                // Fonction de recherche
                // =========================================

                function rechercherAdresse() {{

                    // Récupère l'adresse saisie.
                    var adresse = champAdresse.value.trim();

                    // Vérifie que l'utilisateur
                    // a bien saisi une adresse.
                    if (adresse === "") {{

                        message.innerHTML =
                            "Veuillez saisir une adresse.";

                        return;
                    }}


                    // Affiche un message pendant la recherche.
                    message.innerHTML =
                        "Recherche en cours...";


                    // =====================================
                    // Appel de l'API Nominatim
                    // =====================================

                    // encodeURIComponent() transforme
                    // l'adresse en texte utilisable dans une URL.
                    var url =
                        "https://nominatim.openstreetmap.org/search"
                        + "?format=json"
                        + "&q="
                        + encodeURIComponent(adresse)
                        + "&limit=1";


                    // Envoie la requête à Nominatim.
                    fetch(url, {{

                        // Indique que nous voulons
                        // recevoir une réponse JSON.
                        headers: {{

                            "Accept":
                                "application/json"

                        }}

                    }})

                    // Transforme la réponse en JSON.
                    .then(function(response) {{

                        return response.json();

                    }})

                    // Traite le résultat.
                    .then(function(resultats) {{

                        // Vérifie si une adresse a été trouvée.
                        if (resultats.length === 0) {{

                            message.innerHTML =
                                "Adresse introuvable.";

                            return;
                        }}


                        // Récupère le premier résultat.
                        var resultat = resultats[0];


                        // Convertit la latitude en nombre.
                        var latitude =
                            parseFloat(resultat.lat);


                        // Convertit la longitude en nombre.
                        var longitude =
                            parseFloat(resultat.lon);


                        // =================================
                        // Déplacement de la carte
                        // =================================

                        // Centre la carte sur l'adresse.
                        {carte.get_name()}.setView(
                            [latitude, longitude],
                            17
                        );


                        // =================================
                        // Marqueur de l'adresse
                        // =================================

                        // Supprime l'ancien marqueur
                        // s'il existe.
                        if (
                            window.marqueurAdresse
                        ) {{

                            {carte.get_name()}.removeLayer(
                                window.marqueurAdresse
                            );

                        }}


                        // Crée le nouveau marqueur.
                        window.marqueurAdresse =
                            L.marker(
                                [latitude, longitude]
                            )
                            .addTo(
                                {carte.get_name()}
                            );


                        // Ajoute une fenêtre d'information
                        // au marqueur.
                        window.marqueurAdresse.bindPopup(
                            "<b>Adresse recherchée</b><br>"
                            + resultat.display_name
                        );


                        // Ouvre automatiquement la fenêtre.
                        window.marqueurAdresse.openPopup();


                        // Affiche un message de confirmation.
                        message.innerHTML =
                            "Adresse trouvée.";

                    }})

                    // Gère les erreurs réseau.
                    .catch(function(erreur) {{

                        console.error(erreur);

                        message.innerHTML =
                            "Erreur lors de la recherche.";

                    }});

                }}


                // =========================================
                // Recherche avec le bouton
                // =========================================

                boutonRecherche.addEventListener(
                    "click",
                    function() {{

                        rechercherAdresse();

                    }}
                );


                // =========================================
                // Recherche avec la touche Entrée
                // =========================================

                champAdresse.addEventListener(
                    "keydown",
                    function(e) {{

                        if (e.key === "Enter") {{

                            rechercherAdresse();

                        }}

                    }}
                );

            }}
        );

    </script>
    """

    # Ajoute le JavaScript dans la carte.
    carte.get_root().html.add_child(
        folium.Element(script)
    )


# =========================================================
# Ajout de la couche Transactions DVF
# =========================================================

def ajouter_transactions(carte, gdf):

    # Crée une couche indépendante
    # pour les transactions DVF.
    couche_transactions = folium.FeatureGroup(
        name="Transactions DVF"
    )

    # Parcourt toutes les transactions.
    for _, transaction in gdf.iterrows():

        # Ignore les transactions sans coordonnées.
        if (
            pd.isna(transaction["latitude"])
            or pd.isna(transaction["longitude"])
        ):
            continue

        # Crée la fenêtre d'information.
        popup = folium.Popup(
            f"""
            <b>Commune :</b> {transaction["nom_commune"]}<br>
            <b>Type :</b> {transaction["type_local"]}<br>
            <b>Prix :</b> {transaction["valeur_fonciere"]:,.0f} €<br>
            <b>Surface :</b> {transaction["surface_reelle_bati"]:.0f} m²<br>
            <b>Prix au m² :</b> {transaction["prix_m2"]:,.0f} €/m²<br>
            <b>Date :</b> {transaction["date_mutation"]}
            """,
            max_width=300
        )

        # Crée un point sur la carte.
        folium.CircleMarker(
            location=[
                transaction["latitude"],
                transaction["longitude"]
            ],
            radius=5,
            popup=popup
        ).add_to(couche_transactions)

    # Ajoute la couche des transactions à la carte.
    couche_transactions.add_to(carte)

    return carte


# =========================================================
# Lancement du programme
# =========================================================

if __name__ == "__main__":

    # Charge les données nettoyées.
    df = load_data()

    # Transforme les données en GeoDataFrame.
    gdf = create_geodataframe(df)

    # Affiche quelques lignes pour vérifier les données.
    print(gdf.head())

    # Affiche quelques géométries pour vérifier
    # la création des points géographiques.
    print(gdf.geometry.head())

    # Crée la carte interactive.
    carte, satellite = creer_carte_interactive(
        gdf
    )

    # Ajoute le contrôle d'opacité du satellite.
    ajouter_controle_opacite(
        carte,
        satellite
    )

    # Ajoute la recherche d'adresse.
    ajouter_recherche_adresse(
        carte
    )

    # Ajoute les transactions DVF.
    carte = ajouter_transactions(
        carte,
        gdf
    )

    # Ajoute le sélecteur de couches.
    folium.LayerControl().add_to(carte)

    # Enregistre la carte au format HTML.
    carte.save(
        "data/processed/carte_dvf.html"
    )

    # Affiche un message de confirmation.
    print(
        "Carte interactive créée : "
        "data/processed/carte_dvf.html"
    )