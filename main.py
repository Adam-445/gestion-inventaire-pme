import tkinter as tk

from database.gestionnaire_bd import obtenir_gestionnaire
from ui.fenetre_principale import FenetrePrincipale


def main():
    # Initialise la base de donnees (creation des tables si necessaire)
    gestionnaire = obtenir_gestionnaire()
    print("Base de données initialisée avec succes")

    # Lancement de l'interface
    root = tk.Tk()
    app = FenetrePrincipale(root)
    root.mainloop()


if __name__ == "__main__":
    main()
