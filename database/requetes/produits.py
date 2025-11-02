import sqlite3
from datetime import datetime

from database.gestionnaire_bd import obtenir_connexion


def creer_produit(
    nom: str,
    prix_unitaire: float,
    categorie_id: int | None = None,
    code_barre: str | None = None,
    stock_actuel: int = 0,
    stock_minimum: int = 0,
    fournisseur: str = "",
    description: str = "",
) -> int | None:
    """
    Ajoute un nouveau produit

    Args:
        nom (str): Nom du produit
        prix_unitaire (float): Prix unitaire
        categorie_id (int): ID de la categorie (optionnel)
        code_barre (str): Code barre unique (optionnel)
        stock_actuel (int): Stock initial
        stock_minimum (int): Seuil d'alerte
        fournisseur (str): Nom du fournisseur
        description (str): Description du produit

    Returns:
        int: ID du produit cree ou None si erreur
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute(
            """
            INSERT INTO produits (nom, categorie_id, code_barre, prix_unitaire,
                                 stock_actuel, stock_minimum, fournisseur,
                                 description, date_ajout)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                nom,
                categorie_id,
                code_barre,
                prix_unitaire,
                stock_actuel,
                stock_minimum,
                fournisseur,
                description,
                date_actuelle,
            ),
        )

        connexion.commit()
        return cur.lastrowid

    except sqlite3.IntegrityError:
        print("Erreur: Code barre deja utilise ou categorie invalide")
        return None
    except sqlite3.Error as e:
        print(f"Erreur lors de la creation du produit: {e}")
        connexion.rollback()
        return None


def obtenir_tous_produits() -> list[dict]:
    """
    Recupere tous les produits avec leurs categories

    Returns:
        list: Liste de tous les produits
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT p.*, c.nom as nom_categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.categorie_id
            ORDER BY p.nom
        """
        )
        produits = [dict(row) for row in cur.fetchall()]
        return produits
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des produits: {e}")
        return []


def obtenir_produit(produit_id: int) -> dict | None:
    """
    Recupere un produit par son ID

    Args:
        produit_id (int): ID du produit

    Returns:
        dict: Donnees du produit ou None
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT p.*, c.nom as nom_categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.categorie_id
            WHERE p.produit_id = ?
        """,
            (produit_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation du produit: {e}")
        return None


def rechercher_produits(terme_recherche: str) -> list[dict]:
    """
    Recherche des produits par nom ou code barre

    Args:
        terme_recherche (str): Terme a rechercher

    Returns:
        list: Produits correspondants
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        terme = f"%{terme_recherche}%"
        cur.execute(
            """
            SELECT p.*, c.nom as nom_categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.categorie_id
            WHERE p.nom LIKE ? OR p.code_barre LIKE ?
            ORDER BY p.nom
        """,
            (terme, terme),
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recherche: {e}")
        return []


def obtenir_produits_par_categorie(categorie_id):
    """
    Recupere tous les produits d'une categorie

    Args:
        categorie_id (int): ID de la categorie

    Returns:
        list: Produits de la categorie
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT * FROM produits
            WHERE categorie_id = ?
            ORDER BY nom
        """,
            (categorie_id,),
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des produits: {e}")
        return []


def modifier_produit(produit_id: int, **kwargs) -> bool:
    """
    Modifie un produit existant

    Args:
        produit_id (int): ID du produit a modifier
        **kwargs: Champs a modifier (nom, prix_unitaire, stock_actuel, etc.)

    Returns:
        bool: True si modification reussie, False sinon
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()

        # Champs modifiables
        champs_autorises = [
            "nom",
            "categorie_id",
            "code_barre",
            "prix_unitaire",
            "stock_actuel",
            "stock_minimum",
            "fournisseur",
            "description",
        ]

        champs_a_modifier = []
        valeurs = []

        for champ, valeur in kwargs.items():
            if champ in champs_autorises:
                champs_a_modifier.append(f"{champ} = ?")
                valeurs.append(valeur)

        if not champs_a_modifier:
            return False

        valeurs.append(produit_id)
        requete = (
            f"UPDATE produits SET {', '.join(champs_a_modifier)} WHERE produit_id = ?"
        )

        cur.execute(requete, valeurs)
        connexion.commit()
        return cur.rowcount > 0

    except sqlite3.Error as e:
        print(f"Erreur lors de la modification du produit: {e}")
        connexion.rollback()
        return False


def supprimer_produit(produit_id: int) -> bool:
    """
    Supprime un produit
    Note: Tous les mouvements lies seront aussi supprimes (CASCADE)

    Args:
        produit_id (int): ID du produit a supprimer

    Returns:
        bool: True si suppression reussie, False sinon
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute("DELETE FROM produits WHERE produit_id = ?", (produit_id,))
        connexion.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression du produit: {e}")
        connexion.rollback()
        return False


def obtenir_produits_stock_faible() -> list[dict]:
    """
    Recupere tous les produits dont le stock est inferieur au minimum

    Returns:
        list: Produits necessitant un reapprovisionnement
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute(
            """
            SELECT p.*, c.nom as nom_categorie
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.categorie_id
            WHERE p.stock_actuel < p.stock_minimum
            ORDER BY (p.stock_actuel - p.stock_minimum)
        """
        )
        return [dict(row) for row in cur.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des produits a faible stock: {e}")
        return []
