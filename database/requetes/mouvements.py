import sqlite3
from datetime import datetime

from database.gestionnaire_bd import obtenir_connexion


def creer_mouvement(
    produit_id: int,
    type_mouvement: str,
    quantite: int,
    motif: str = "",
    utilisateur: str = "",
    remarques: str = "",
) -> int | None:
    """
    Enregistre un mouvement de stock et met a jour le stock du produit

    Args:
        produit_id (int): ID du produit concerne
        type_mouvement (str): 'ENTREE' ou 'SORTIE'
        quantite (int): Quantite du mouvement
        motif (str): Motif du mouvement (Achat, Vente, etc.)
        utilisateur (str): Nom de l'utilisateur
        remarques (str): Remarques additionnelles

    Returns:
        int: ID du mouvement cree ou None si erreur
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Verifier que le type est valide
        if type_mouvement not in ["ENTREE", "SORTIE"]:
            print("Erreur: Type de mouvement invalide (doit etre 'ENTREE' ou 'SORTIE')")
            return None

        # Commencer une transaction
        cur.execute("BEGIN TRANSACTION")

        # Inserer le mouvement
        cur.execute(
            """
            INSERT INTO mouvements_stock (produit_id, type_mouvement, quantite,
                                         motif, utilisateur, date_mouvement, remarques)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                produit_id,
                type_mouvement,
                quantite,
                motif,
                utilisateur,
                date_actuelle,
                remarques,
            ),
        )

        mouvement_id = cur.lastrowid

        # Mettre a jour le stock du produit
        if type_mouvement == "ENTREE":
            cur.execute(
                """
                UPDATE produits
                SET stock_actuel = stock_actuel + ?
                WHERE produit_id = ?
            """,
                (quantite, produit_id),
            )
        else:  # SORTIE
            cur.execute(
                """
                UPDATE produits
                SET stock_actuel = stock_actuel - ?
                WHERE produit_id = ?
            """,
                (quantite, produit_id),
            )

        connexion.commit()
        return mouvement_id

    except sqlite3.Error as e:
        print(f"Erreur lors de la creation du mouvement: {e}")
        connexion.rollback()
        return None


def obtenir_tous_mouvements() -> list[dict]:
    """
    Recupere tous les mouvements de stock

    Returns:
        list: Liste de tous les mouvements avec noms des produits
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
        """
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des mouvements: {e}")
        return []


def obtenir_mouvements_produit(produit_id: int) -> list[dict]:
    """
    Recupere l'historique des mouvements d'un produit

    Args:
        produit_id (int): ID du produit

    Returns:
        list: Historique des mouvements du produit
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT m.*, p.nom as nom_produit
            FROM mouvements_stock m
            JOIN produits p ON m.produit_id = p.produit_id
            WHERE m.produit_id = ?
            ORDER BY date_mouvement DESC
        """,
            (produit_id,),
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des mouvements: {e}")
        return []


def obtenir_mouvements_par_date(date_debut: str, date_fin: str) -> list[dict]:
    """
    Recupere les mouvements dans une plage de dates

    Args:
        date_debut (str): Date de debut (format: YYYY-MM-DD)
        date_fin (str): Date de fin (format: YYYY-MM-DD)

    Returns:
        list: Mouvements dans la plage specifiee
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT m.*, p.nom as nom_produit
            FROM mouvements_stock m
            JOIN produits p ON m.produit_id = p.produit_id
            WHERE DATE(m.date_mouvement) BETWEEN ? AND ?
            ORDER BY m.date_mouvement DESC
        """,
            (date_debut, date_fin),
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des mouvements: {e}")
        return []


def obtenir_mouvements_par_type(type_mouvement: str) -> list[dict]:
    """
    Recupere les mouvements d'un type specifique

    Args:
        type_mouvement (str): 'ENTREE' ou 'SORTIE'

    Returns:
        list: Mouvements du type specifie
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT m.*, p.nom as nom_produit
            FROM mouvements_stock m
            JOIN produits p ON m.produit_id = p.produit_id
            WHERE m.type_mouvement = ?
            ORDER BY m.date_mouvement DESC
        """,
            (type_mouvement,),
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des mouvements: {e}")
        return []
