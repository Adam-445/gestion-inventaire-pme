import tkinter as tk
from ui.gestion_categories import GestionCategoriesFrame
from ui.gestion_produits import GestionProduitsFrame
from ui.gestion_Mouvement import GestionMouvementsFrame
from ui.gestion_dashboard import DashboardFrame

# ----------------- Variables Globales du Thème -----------------
COULEUR_FOND_FENETRE = "#caf084"  #  Variable pour le fond général de la fenêtre
COULEUR_FOND_NAV = "#caf084"  # Fond de la barre de navigation
COULEUR_BOUTON = "#94FFC4"  # Couleur par défaut des boutons
COULEUR_TEXTE_BOUTON = "white"  # Couleur du texte du bouton
COULEUR_BOUTON_ACTIF = "#23B866"  # Couleur quand le bouton est cliqué ou survolé
COULEUR_TEXTE_BOUTON_ACTIF = "white"
COULEUR_FOND_OMBRE = "#FF0000"  # Fond de l'encadrement (effet d'ombre)
POLICE_BOUTON = ("Bahnschrift", 12, "bold")

MARGE_NAV_X = 20
MARGE_NAV_Y = 30
MARGE_BOUTON_X = 15
MARGE_BOUTON_Y = 5
MARGE_CONTENEUR_X = 8
MARGE_CONTENEUR_Y = 5


# ----------------- Classe BarreNavigation -----------------
class BarreNavigation(tk.Frame):
    """Barre de navigation supérieure contenant les boutons principaux."""

    def __init__(self, parent, sur_clic_navigation):
        super().__init__(parent, bg=COULEUR_FOND_NAV)
        self.pack(side="top", fill="x", padx=MARGE_NAV_X, pady=MARGE_NAV_Y)
        self.sur_clic_navigation = sur_clic_navigation
        self._creer_boutons_navigation()

    # ---- Création des boutons de navigation ----
    def _creer_boutons_navigation(self):
        boutons = [
            {"texte": "Accueil", "vue": "TABLEAU_DE_BORD"},
            {"texte": "Produits", "vue": "PRODUITS"},
            {"texte": "Catégories", "vue": "CATEGORIES"},
            {"texte": "Mouvements", "vue": "MOUVEMENTS"},
        ]

        for bouton in boutons:
            self._ajouter_bouton(
                texte=bouton["texte"],
                commande=lambda v=bouton["vue"]: self.sur_clic_navigation(v),
            )

    # ---- Fonction pour créer un bouton stylisé ----
    def _ajouter_bouton(self, texte, commande):
        conteneur = tk.Frame(self, bg=COULEUR_FOND_OMBRE)
        conteneur.pack(side="left", padx=MARGE_CONTENEUR_X, pady=MARGE_CONTENEUR_Y)

        bouton = tk.Button(
            conteneur,
            text=texte,
            command=commande,
            bg=COULEUR_BOUTON,
            fg=COULEUR_TEXTE_BOUTON,
            activebackground=COULEUR_BOUTON_ACTIF,
            activeforeground=COULEUR_TEXTE_BOUTON_ACTIF,
            relief="raised",
            padx=MARGE_BOUTON_X,
            pady=MARGE_BOUTON_Y,
            font=POLICE_BOUTON,
            cursor="hand2",
        )
        bouton.pack()

        # Effet de survol
        bouton.bind("<Enter>", lambda e: bouton.config(bg=COULEUR_BOUTON_ACTIF))
        bouton.bind("<Leave>", lambda e: bouton.config(bg=COULEUR_BOUTON))
        return bouton


# ----------------- Classe FenetrePrincipale -----------------
class FenetrePrincipale(tk.Frame):
    """Fenêtre principale de l'application avec navigation dynamique."""

    VUES = {
        "CATEGORIES": GestionCategoriesFrame,
        "PRODUITS": GestionProduitsFrame,
        "MOUVEMENTS": GestionMouvementsFrame,
        "TABLEAU_DE_BORD": DashboardFrame,
    }

    def __init__(self, parent=None):
        super().__init__(parent, bg=COULEUR_FOND_FENETRE)
        self.master.title("Système de Gestion d'Inventaire pour PME")
        self.pack(fill="both", expand=True)

        # Initialisation des composants
        self.vue_actuelle = None
        self.barre_navigation = self._creer_barre_navigation()
        self.conteneur_contenu = self._creer_conteneur_contenu()

        # Affiche la vue par défaut
        self.afficher_vue("CATEGORIES")

    # ---- Création de la barre de navigation ----
    def _creer_barre_navigation(self):
        return BarreNavigation(self, self.afficher_vue)

    # ---- Création du conteneur de contenu ----
    def _creer_conteneur_contenu(self):
        conteneur = tk.Frame(self, bg=COULEUR_FOND_FENETRE)
        conteneur.pack(fill="both", expand=True)
        return conteneur

    # ---- Affiche la vue sélectionnée ----
    def afficher_vue(self, nom_vue):
        self._detruire_vue_actuelle()
        self._charger_nouvelle_vue(nom_vue)

    # ---- Détruit la vue précédente ----
    def _detruire_vue_actuelle(self):
        if self.vue_actuelle:
            self.vue_actuelle.destroy()

    # ---- Charge la nouvelle vue ----
    def _charger_nouvelle_vue(self, nom_vue):
        classe_vue = self.VUES.get(nom_vue, tk.Frame)
        vue = (
            classe_vue(self.conteneur_contenu)
            if classe_vue != tk.Frame
            else self._creer_vue_vide(nom_vue)
        )
        vue.pack(fill="both", expand=True)
        self.vue_actuelle = vue

    # ---- Vue par défaut si non implémentée ----
    def _creer_vue_vide(self, nom_vue):
        frame = tk.Frame(self.conteneur_contenu, bg=COULEUR_FOND_FENETRE)
        tk.Label(frame, text=f"Vue {nom_vue} à implémenter").pack(padx=20, pady=20)
        return frame


# ----------------- Point d'entrée -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FenetrePrincipale(root)
    app.pack(fill="both", expand=True)
    root.configure(bg=COULEUR_FOND_FENETRE)
    root.mainloop()
