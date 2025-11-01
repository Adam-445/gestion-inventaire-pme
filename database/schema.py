# Définition du schéma de la base de données (SQLite)

CREATE_TABLES = [
    # TABLE 1: CATEGORIES
    """
    CREATE TABLE IF NOT EXISTS CATEGORIES (
        categorie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        description TEXT,
        date_creation TEXT
    );
    """,

    # TABLE 2: PRODUITS
    """
    CREATE TABLE IF NOT EXISTS PRODUITS (
        produit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        categorie_id INTEGER,
        code_barre TEXT UNIQUE,
        prix_unitaire REAL NOT NULL,
        stock_actuel INTEGER DEFAULT 0,
        stock_minimum INTEGER DEFAULT 0,
        fournisseur TEXT,
        description TEXT,
        date_ajout TEXT ,
        FOREIGN KEY (categorie_id) REFERENCES CATEGORIES(categorie_id)
    );
    """,

    # TABLE 3: MOUVEMENTS_STOCK
    """
    CREATE TABLE IF NOT EXISTS MOUVEMENTS_STOCK (
        mouvement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        produit_id INTEGER NOT NULL,
        type_mouvement TEXT NOT NULL CHECK(type_mouvement IN ('ENTREE', 'SORTIE')),
        quantite INTEGER NOT NULL,
        motif TEXT,
        utilisateur TEXT,
        date_mouvement TEXT ,
        remarques TEXT,
        FOREIGN KEY (produit_id) REFERENCES PRODUITS(produit_id)
    );
    """
]