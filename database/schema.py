TOUTES_LES_TABLES = {
    "categories": """
    CREATE TABLE IF NOT EXISTS categories (
        categorie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        description TEXT,
        date_creation TEXT
    );
    """,
    "produits": """
    CREATE TABLE IF NOT EXISTS produits (
        produit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        categorie_id INTEGER,
        code_barre TEXT UNIQUE,
        prix_unitaire REAL NOT NULL,
        stock_actuel INTEGER DEFAULT 0,
        stock_minimum INTEGER DEFAULT 0,
        fournisseur TEXT,
        description TEXT,
        date_ajout TEXT,
        FOREIGN KEY (categorie_id) REFERENCES categories(categorie_id)
    );
    """,
    "mouvements_stock": """
    CREATE TABLE IF NOT EXISTS mouvements_stock (
        mouvement_id INTEGER PRIMARY KEY AUTOINCREMENT,
        produit_id INTEGER NOT NULL,
        type_mouvement TEXT NOT NULL,
        quantite INTEGER NOT NULL,
        motif TEXT,
        utilisateur TEXT,
        date_mouvement TEXT NOT NULL,
        remarques TEXT,
        FOREIGN KEY (produit_id) REFERENCES produits(produit_id)
    );
    """,
}
