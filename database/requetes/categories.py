import sqlite3
from datetime import datetime

from database.gestionnaire_bd import obtenir_connexion


def creer_categorie(nom: str, description: str = "") -> int | None:
    """
    Ajoute une nouvelle categorie

    Args:
        nom (str): Nom de la categorie (unique)
        description (str): description optionelle

    Returns:
        int: ID de la categorie cree ou None sis erreur
    """
    connexion = obtenir_connexion()

    try:
        cur = connexion.cursor()
        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute(
            """
            INSERT INTO categories (nom, description, date_creation)
            VALUES (?, ?, ?)
        """,
            (nom, description, date_actuelle),
        )

        connexion.commit()
        return cur.lastrowid

    except sqlite3.IntegrityError:
        print(f"Erreur: la categorie '{nom}' existe deja")
        return None
    except sqlite3.Error as e:
        print(f"Erreur lors de la creation de la categorie: {e}")
        connexion.rollback()
        return None


def obtenir_toutes_categories() -> list[dict]:
    """
    REcupere toutes les categories

    Returns:
        list: Liste des dicts {categorie_id, nom, description, date_creation}
    """
    connexion = obtenir_connexion()
    try:
        cur = connexion.cursor()
        cur.execute("SELECT * FROM categories ORDER BY nom")
        categories = [dict(row) for row in cur.fetchall()]
        return categories
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation des categories: {e}")
        return []


def obtenir_categorie(categorie_id: int):
    """
    Recupere une categorie par son ID

    Args:
        categorie_id (int): ID de la categorie

    Returns:
        tuple: Donnees de la categorie ou None
    """
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()
        curseur.execute(
            "SELECT * FROM categories WHERE categorie_id = ?", (categorie_id,)
        )
        return curseur.fetchone()
    except sqlite3.Error as e:
        print(f"Erreur lors de la recuperation de la categorie: {e}")
        return None


def modifier_categorie(
    categorie_id: int, nom: str | None = None, description: str | None = None
) -> bool:
    """
    Modifie une categorie existante

    Args:
        categorie_id (int): ID de la categorie a modifier
        nom (str): Nouveau nom (optionnel)
        description (str): Nouvelle description (optionnel)

    Returns:
        bool: True si modification reussie, False sinon
    """
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()

        # Construire la requete dynamiquement selon les champs fournis
        champs_a_modifier = []
        valeurs = []

        if nom is not None:
            champs_a_modifier.append("nom = ?")
            valeurs.append(nom)

        if description is not None:
            champs_a_modifier.append("description = ?")
            valeurs.append(description)

        if not champs_a_modifier:
            return False

        valeurs.append(categorie_id)
        requete = f"""
            UPDATE categories SET {', '.join(champs_a_modifier)}
            WHERE categorie_id = ?
        """

        curseur.execute(requete, valeurs)
        connexion.commit()
        return curseur.rowcount > 0

    except sqlite3.Error as e:
        print(f"Erreur lors de la modification de la categorie: {e}")
        connexion.rollback()
        return False


def supprimer_categorie(categorie_id: int):
    """
    Supprime une categorie
    Note: Les produits lies auront leur categorie_id mis a NULL

    Args:
        categorie_id (int): ID de la categorie a supprimer

    Returns:
        bool: True si suppression reussie, False sinon
    """
    connexion = obtenir_connexion()
    try:
        curseur = connexion.cursor()
        curseur.execute(
            "DELETE FROM categories WHERE categorie_id = ?", (categorie_id,)
        )
        connexion.commit()
        return curseur.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la categorie: {e}")
        connexion.rollback()
        return False
