from .gestionnaire_bd import Database
from datetime import datetime

db = Database()

def get_all_categories() -> list[dict]:
    # Récupére toutes les cotégories.
    sql = "SELECT categorie_id, nom, description, date_creation FROM CATEGORIES ORDER BY nom"
    cur = db.execute(sql)
    categories = [dict(row) for row in cur.fetchall()]
    return categories

def create_category(nom:str, description: str) -> int:
    #Ajoute une nouvelle catégorie et retourne son ID
    date_creation = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql="""
    INSERT INTO CATEGORIES (nom, description, date_creation)
    VALUES(?, ?, ?)
    """

    params = (nom, description, date_creation)

    cur = db.execute(sql, params)

    return cur.lastrowid

def update_category(cat_id:int, nom:str, description: str)-> None:
    #modifie les informations d'une catégorie existante.
    sql = """
    UPDATE CATEGORIES
    SET nom = ?, description =?
    WHERE categorie_id = ?
    """
    params = (nom, description, cat_id)
    db.execute(sql,params)

def delete_category(cat_id:int) -> None:
    #supprime une catégorie par son id
    sql = "DELETE FROM CATEGORIES WHERE categorie_id = ?"
    params = (cat_id,)
    db.execute(sql,params)

def get_all_products() -> list[dict]:
    """Récupère tous les produits avec le nom de leur catégorie."""
    sql = """
    SELECT 
        p.produit_id, p.nom, p.code_barre, p.prix_unitaire, 
        p.stock_actuel, p.stock_minimum, p.fournisseur, p.description,
        c.nom as categorie_nom, c.categorie_id
    FROM PRODUITS p
    LEFT JOIN CATEGORIES c ON p.categorie_id = c.categorie_id
    ORDER BY p.nom
    """
    cur = db.execute(sql)
    products = [dict(row) for row in cur.fetchall()]
    return products

def get_product_by_id(product_id: int) -> dict | None:
    """Récupère un produit par son ID."""
    sql = "SELECT * FROM PRODUITS WHERE produit_id = ?"
    cur = db.execute(sql, (product_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def create_product(data: dict) -> int:
    """Ajoute un nouveau produit. 'data' doit contenir les clés du schéma."""
    # Assurez-vous d'avoir 'from datetime import datetime' au début du fichier
    date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """
    INSERT INTO PRODUITS (
        nom, categorie_id, code_barre, prix_unitaire, stock_minimum, fournisseur, description, date_ajout
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data.get('nom'), 
        data.get('categorie_id'), 
        data.get('code_barre'), 
        data.get('prix_unitaire', 0.0), 
        data.get('stock_minimum', 0), 
        data.get('fournisseur'), 
        data.get('description'), 
        date_ajout
    )
    cur = db.execute(sql, params)
    return cur.lastrowid

def delete_product(product_id: int) -> None:
    """Supprime un produit par son ID."""
    sql = "DELETE FROM PRODUITS WHERE produit_id = ?"
    db.execute(sql, (product_id,))

def update_product(product_id: int, **fields) -> None:
    if not fields:
        return
    set_clauses = [f"{key} = ?" for key in fields.keys()]
    sql = f"UPDATE PRODUITS SET {', '.join(set_clauses)} WHERE produit_id = ?"
    params = tuple(fields.values()) + (product_id,)
    
    db.execute(sql, params)