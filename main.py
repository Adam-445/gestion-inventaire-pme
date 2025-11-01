import tkinter as tk
from ui.fenetre_principale import MainWindow
from database.gestionnaire_bd import Database
from database import schema # Importe les instruction SQL



def main():
    db = Database()
    #Créer une table si elle n'existent pas
    print(f"Tentative de connexion et création des tables dans : {db.db_path}")
    conn = db.connect()
    cur = conn.cursor()

    #Exécute les instructions dans "database/shema" 
    for stmt in schema.CREATE_TABLES:
        try:
            cur.execute(stmt)
        except Exception as e:
            print(f"Erreur lors de la création de la table : {e}")
            conn.rollback() #Annule les changements en cas d'erreur
            return # Arrété l'application
        
    conn.commit() # Confirme les créations de tables
    conn.close()
    print("Base de données et tables crées avec succés.")

    # Lancement de l'interface 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()