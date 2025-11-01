import tkinter as tk
from tkinter import ttk, messagebox
from database.requetes import (
    obtenir_statistiques_inventaire,
    obtenir_mouvements_recents,
)

# ---------- Thème ----------
COULEUR_FOND = "#f7ffee"
COULEUR_CARTE = "white"
COULEUR_BORDURE_CARTE = "#d9d9d9"
COULEUR_TEXTE_VERT = "#23B866"

COULEUR_BOUTON = "#23B866"
COULEUR_BOUTON_CLIQUE = "white"
COULEUR_TEXTE_BOUTON = "white"
COULEUR_BOUTON_ACTIVE = "#19A25C"

POLICE_TITRE = ("Bahnschrift", 16, "bold")
POLICE_CARTE_LABEL = ("Bahnschrift", 12)
POLICE_CARTE_VALEUR = ("Bahnschrift", 18, "bold")
POLICE_BOUTON = ("Bahnschrift", 11, "bold")

COULEUR_LIGNE_PAIR = "#ffffff"
COULEUR_LIGNE_IMPAIR = "#f2f7f2"


# ---------- Tableau de bord ----------
class DashboardFrame(tk.Frame):
    """Tableau de bord de l’inventaire."""

    def __init__(self, master=None):
        super().__init__(master, bg=COULEUR_FOND)
        self.pack(fill="both", expand=True)
        self.creer_interface()
        self.charger_donnees()

    # ---------- Interface ----------
    def creer_interface(self):
        self.creer_titre()
        self.creer_cartes_stats()
        self.creer_table_mouvements()
        self.creer_bouton_rafraichir()

    def creer_titre(self):
        tk.Label(
            self,
            text="Tableau de Bord - Inventaire",
            font=POLICE_TITRE,
            bg=COULEUR_FOND,
        ).pack(pady=20)

    # ---------- Cartes statistiques ----------
    def creer_cartes_stats(self):
        cadre_cartes = tk.Frame(self, bg=COULEUR_FOND)
        cadre_cartes.pack(fill="x", padx=30)

        self.carte_total_produits = self.creer_carte(cadre_cartes, "Produits Totaux")
        self.carte_valeur_totale = self.creer_carte(cadre_cartes, "Valeur Totale (€)")
        self.carte_produits_alerte = self.creer_carte(
            cadre_cartes, "Produits en Alerte"
        )

        self.carte_total_produits.pack(side="left", expand=True, padx=40, pady=20)
        self.carte_valeur_totale.pack(side="left", expand=True, padx=40, pady=20)
        self.carte_produits_alerte.pack(side="left", expand=True, padx=40, pady=20)

    def creer_carte(self, parent, titre):
        # Cadre principal de la carte
        cadre = tk.Frame(
            parent,
            bg=COULEUR_CARTE,
            highlightbackground=COULEUR_BORDURE_CARTE,
            highlightthickness=1,
            relief="solid",
            bd=0,
        )

        # Cadre interne pour le padding
        cadre_interne = tk.Frame(cadre, bg=COULEUR_CARTE, padx=20, pady=15)
        cadre_interne.pack(fill="both", expand=True)

        # Label du titre
        tk.Label(
            cadre_interne,
            text=titre,
            font=POLICE_CARTE_LABEL,
            bg=COULEUR_CARTE,
            anchor="w",
            justify="left",
        ).pack(fill="x", pady=(0, 10))

        # Label de la valeur
        valeur = tk.Label(
            cadre_interne,
            text="0",
            font=POLICE_CARTE_VALEUR,
            bg=COULEUR_CARTE,
            fg=COULEUR_TEXTE_VERT,
        )
        valeur.pack()

        cadre.valeur_label = valeur
        return cadre

    # ---------- Table des mouvements ----------
    def creer_table_mouvements(self):
        tk.Label(
            self,
            text="Derniers Mouvements de Stock",
            font=("Montserrat", 14, "bold"),
            bg=COULEUR_FOND,
        ).pack(pady=(30, 10))

        colonnes = ("ID", "Produit", "Type", "Quantité", "Date", "Utilisateur")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings")

        for col in colonnes:
            self.tree.heading(col, text=col)
            ancrage = "center" if col in ("ID", "Quantité", "Date") else "w"
            largeur = 110 if col in ("ID", "Quantité") else 160
            self.tree.column(col, anchor=ancrage, width=largeur)

        self.tree.tag_configure("pair", background=COULEUR_LIGNE_PAIR)
        self.tree.tag_configure("impair", background=COULEUR_LIGNE_IMPAIR)

        self.tree.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    # ---------- Bouton Rafraîchir ----------
    def creer_bouton_rafraichir(self):
        bouton = tk.Button(
            self,
            text="🔄 Rafraîchir les données",
            font=POLICE_BOUTON,
            bg=COULEUR_BOUTON,
            fg=COULEUR_TEXTE_BOUTON,
            activebackground=COULEUR_BOUTON_ACTIVE,
            relief="flat",
            cursor="hand2",
            command=lambda: self._clic_bouton(bouton, self.charger_donnees),
        )
        bouton.pack(pady=(0, 20))

    def _clic_bouton(self, bouton, commande):
        """Change le bouton en blanc au clic puis exécute la commande."""
        couleur_origine = bouton.cget("bg")
        bouton.config(bg=COULEUR_BOUTON_CLIQUE)
        self.after(150, lambda: bouton.config(bg=couleur_origine))
        commande()

    # ---------- Données ----------
    def charger_donnees(self):
        try:
            stats = obtenir_statistiques_inventaire()
            if not stats:
                raise Exception("Aucune donnée reçue depuis la base.")

            self.carte_total_produits.valeur_label.config(
                text=str(stats["nombre_produits"])
            )
            self.carte_valeur_totale.valeur_label.config(
                text=f"{stats['valeur_totale']:.2f} €"
            )
            self.carte_produits_alerte.valeur_label.config(
                text=str(stats["produits_alerte"])
            )

            self.charger_mouvements_recents()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le dashboard :\n{e}")

    def charger_mouvements_recents(self):
        self.tree.delete(*self.tree.get_children())
        mouvements = obtenir_mouvements_recents(10)

        for i, mvt in enumerate(mouvements):
            tag = "pair" if i % 2 == 0 else "impair"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    mvt["mouvement_id"],
                    mvt.get("nom_produit", "N/A"),
                    mvt["type_mouvement"],
                    mvt["quantite"],
                    mvt["date_mouvement"],
                    mvt.get("utilisateur", "Admin"),
                ),
                tags=(tag,),
            )
