import sqlite3

from database.gestionnaire_bd import obtenir_connexion


def obtenir_valeur_inventaire() -> float:
    """
    Calcule la valeur totale de l'inventaire

    Returns:
        float: Valeur totale (stock_actuel * prix_unitaire pour tous les produits)
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT SUM(stock_actuel * prix_unitaire) as valeur_totale
            FROM produits
        """
        )
        resultat = cur.fetchone()
        return resultat["valeur_totale"] if resultat["valeur_totale"] else 0.0
    except sqlite3.Error as e:
        print(f"Erreur lors du calcul de la valeur de l'inventaire: {e}")
        return 0.0


def obtenir_statistiques_inventaire() -> dict:
    """
    Recupere des statistiques generales sur l'inventaire

    Returns:
        dict: Dictionnaire avec nombre_produits, valeur_totale, produits_alerte
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()

        # Nombre total de produits
        cur.execute("SELECT COUNT(*) as total FROM produits")
        nombre_produits = cur.fetchone()["total"]

        # Valeur totale
        valeur_totale = obtenir_valeur_inventaire()

        # Nombre de produits en alerte
        cur.execute(
            """
            SELECT COUNT(*) as alerte
            FROM produits
            WHERE stock_actuel < stock_minimum
        """
        )
        produits_alerte = cur.fetchone()["alerte"]

        return {
            "nombre_produits": nombre_produits,
            "valeur_totale": valeur_totale,
            "produits_alerte": produits_alerte,
        }

    except sqlite3.Error as e:
        print(f"Erreur lors du calcul des statistiques: {e}")
        return {"nombre_produits": 0, "valeur_totale": 0.0, "produits_alerte": 0}


def obtenir_mouvements_recents(limite: int = 10) -> list[dict]:
    """
    Recupere les mouvements les plus recents

    Args:
        limite (int): Nombre de mouvements a recuperer

    Returns:
        list: Derniers mouvements
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT m.*, p.nom as nom_produit
            FROM mouvements_stock m
            JOIN produits p ON m.produit_id = p.produit_id
            ORDER BY m.date_mouvement DESC
            LIMIT ?
        """,
            (limite,),
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des mouvements recents: {e}")
        return []
