import sqlite3
from pathlib import Path

from config.parametres import DB_PATH  # importer le chemin défini
from database.schema import TOUTES_LES_TABLES


class GestionnaireBD:
    """Classe pour gerer la connexion a la bd"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connexion = None

    def connecter(self) -> sqlite3.Connection:
        """
        Etablit la connextion a la bd

        Returns:
            sqlite3.COnnection: Objet de connection
        """
        try:
            self.connexion = sqlite3.connect(self.db_path)
            self.connexion.row_factory = (
                sqlite3.Row
            )  # permet l'acces au colonnes par nom
            # active les contraintes des foreign keys
            self.connexion.execute("PRAGMA foreign_keys = ON")
            print(f"Connextion etablie a {self.db_path}")
            return self.connexion
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion: {e}")
            raise

    def initialiser_tables(self):
        """
        Cree toutes le tables si elles n'existent pas
        Doit etre appele apres connecter()
        """
        if not self.connexion:
            raise Exception("pas de connexion active. Appeler connecter() dabord")

        try:
            cur = self.connexion.cursor()

            for requete_table in TOUTES_LES_TABLES.values():
                cur.execute(requete_table)

            self.connexion.commit()
            print("toutes les tables ont ete crees avec succes")

        except sqlite3.Error as e:
            print(f"Erreur lors de la creation des tables: {e}")
            self.connexion.rollback()
            raise

    def fermer(self):
        """Ferme la connexion a la bd"""
        if self.connexion:
            self.connexion.close()
            print("Connexion fermee")

    def obtenir_connexion(self) -> sqlite3.Connection:
        """Retourne la connexin active"""
        if not self.connexion:
            raise RuntimeError("Pas de connexion active a la base de donnees")
        return self.connexion


# Instance globale du gestionnaire (singleton pattern)
_gestionnaire = None


def obtenir_gestionnaire() -> GestionnaireBD:
    """
    Retourne l'instance unique du gestionnaire de BD

    Returns:
        GestionnaireBD: Objet de classe GestionnaireBD
    """
    global _gestionnaire
    if _gestionnaire is None:
        _gestionnaire = GestionnaireBD()
        _gestionnaire.connecter()
        _gestionnaire.initialiser_tables()
    return _gestionnaire


def obtenir_connexion() -> sqlite3.Connection:
    """
    Fonction pour obtenir rapidement la connexion

    Returns:
        sqlite3.Connection: Connexion active
    """
    return obtenir_gestionnaire().obtenir_connexion()
