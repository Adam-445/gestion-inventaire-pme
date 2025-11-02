import tkinter as tk
from tkinter import messagebox, ttk
from database.requetes import (
    creer_mouvement,
    obtenir_tous_mouvements,
    obtenir_mouvements_produit,
    obtenir_mouvements_par_date,
    obtenir_mouvements_par_type,
    obtenir_tous_produits,
)

# ---------- Variables Thématiques ----------
COULEUR_FOND_FENETRE = "#f8ffe8"
COULEUR_FOND_BOUTON = "#94FFC4"
COULEUR_TEXTE_BOUTON = "white"
COULEUR_BOUTON_ACTIVE = "#23B866"
COULEUR_BOUTON_CLIQUE = "white"
POLICE_BOUTON = ("Bahnschrift", 12, "bold")
LARGEUR_ENTREE = 15
MARGE_X = 15
MARGE_Y = 10


class GestionMouvementsFrame(tk.Frame):
    """Interface graphique pour la gestion des mouvements de stock."""

    def __init__(self, master=None):
        super().__init__(master, bg=COULEUR_FOND_FENETRE)
        self.pack(fill="both", expand=True)
        self.creer_interface()
        self.charger_mouvements(obtenir_tous_mouvements())

    # ---------- Interface principale ----------
    def creer_interface(self):
        self.creer_titre()
        self.creer_filtres()
        self.creer_tableau()

    def creer_titre(self):
        tk.Label(
            self,
            text="Gestion des Mouvements",
            font=("Bahnschrift", 16, "bold"),
            bg=COULEUR_FOND_FENETRE,
        ).pack(pady=15)

    def creer_filtres(self):
        cadre_filtre = tk.Frame(self, bg=COULEUR_FOND_FENETRE)
        cadre_filtre.pack(fill="x", padx=20, pady=10)

        self._ajouter_filtre_produit(cadre_filtre)
        self._ajouter_filtre_type(cadre_filtre)
        self._ajouter_filtre_dates(cadre_filtre)

        self.creer_bouton(cadre_filtre, "Filtrer", self.appliquer_filtres).pack(
            side="left", padx=5
        )
        self.creer_bouton(
            cadre_filtre, "Ajouter Mouvement", self.ouvrir_dialogue_ajout
        ).pack(side="right", padx=5)

    def _ajouter_filtre_produit(self, parent):
        tk.Label(parent, text="Produit ID :", bg=COULEUR_FOND_FENETRE).pack(
            side="left", padx=5
        )
        self.produit_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.produit_var, width=LARGEUR_ENTREE).pack(
            side="left", padx=5
        )

    def _ajouter_filtre_type(self, parent):
        tk.Label(parent, text="Type :", bg=COULEUR_FOND_FENETRE).pack(
            side="left", padx=5
        )
        self.type_var = tk.StringVar(value="TOUS")
        type_combo = ttk.Combobox(
            parent,
            textvariable=self.type_var,
            values=["TOUS", "ENTREE", "SORTIE"],
            width=LARGEUR_ENTREE,
            state="readonly",
        )
        type_combo.pack(side="left", padx=5)

    def _ajouter_filtre_dates(self, parent):
        tk.Label(parent, text="De :", bg=COULEUR_FOND_FENETRE).pack(side="left", padx=5)
        self.date_debut = tk.StringVar()
        tk.Entry(parent, textvariable=self.date_debut, width=LARGEUR_ENTREE).pack(
            side="left", padx=5
        )

        tk.Label(parent, text="À :", bg=COULEUR_FOND_FENETRE).pack(side="left", padx=5)
        self.date_fin = tk.StringVar()
        tk.Entry(parent, textvariable=self.date_fin, width=LARGEUR_ENTREE).pack(
            side="left", padx=5
        )

    def creer_bouton(self, parent, texte, commande):
        bouton = tk.Button(
            parent,
            text=texte,
            command=lambda: self._on_bouton_clic(bouton, commande),
            bg=COULEUR_FOND_BOUTON,
            fg=COULEUR_TEXTE_BOUTON,
            activebackground=COULEUR_BOUTON_ACTIVE,
            font=POLICE_BOUTON,
            cursor="hand2",
        )
        return bouton

    def _on_bouton_clic(self, bouton, commande):
        couleur_originale = bouton.cget("bg")
        bouton.config(bg=COULEUR_BOUTON_CLIQUE)
        self.after(150, lambda: bouton.config(bg=couleur_originale))
        commande()

    def creer_tableau(self):
        colonnes = (
            "ID",
            "Produit",
            "Type",
            "Quantité",
            "Motif",
            "Utilisateur",
            "Date",
            "Remarques",
        )
        cadre_tableau = tk.Frame(self, bg=COULEUR_FOND_FENETRE)
        cadre_tableau.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings")

        for col in colonnes:
            self.tree.heading(col, text=col)
            largeur = 50 if col == "ID" else 120
            ancrage = "center" if col in ("ID", "Quantité") else "w"
            self.tree.column(col, width=largeur, anchor=ancrage)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------- Chargement des données ----------
    def charger_mouvements(self, mouvements):
        self.tree.delete(*self.tree.get_children())
        mouvements_dict = [dict(m) for m in mouvements]

        for m in mouvements_dict:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    m["mouvement_id"],
                    m.get("nom_produit", "N/A"),
                    m["type_mouvement"],
                    m["quantite"],
                    m.get("motif", ""),
                    m.get("utilisateur", ""),
                    m["date_mouvement"],
                    m.get("remarques", ""),
                ),
            )

    # ---------- Gestion des filtres ----------
    def appliquer_filtres(self):
        type_filtre = self.type_var.get().strip()
        date_debut = self.date_debut.get().strip()
        date_fin = self.date_fin.get().strip()
        produit_id = self.produit_var.get().strip()

        mouvements = obtenir_tous_mouvements()

        if produit_id:
            try:
                pid = int(produit_id)
                mouvements = obtenir_mouvements_produit(pid)
            except ValueError:
                messagebox.showwarning("Erreur", "L’ID du produit doit être un nombre.")
                return

        if type_filtre in ["ENTREE", "SORTIE"]:
            mouvements = obtenir_mouvements_par_type(type_filtre)

        if date_debut and date_fin:
            mouvements = obtenir_mouvements_par_date(date_debut, date_fin)

        self.charger_mouvements(mouvements)

    # ---------- Dialogue d’ajout ----------
    def ouvrir_dialogue_ajout(self):
        dialogue = tk.Toplevel(self.master)
        dialogue.title("Ajouter un Mouvement")
        dialogue.transient(self.master)
        dialogue.grab_set()

        cadre = tk.Frame(dialogue, padx=MARGE_X, pady=MARGE_Y)
        cadre.pack(padx=MARGE_X, pady=MARGE_Y)

        self._remplir_dialogue(cadre, dialogue)

    def _remplir_dialogue(self, cadre, dialogue):
        try:
            produits = obtenir_tous_produits()
        except Exception:
            produits = []

        noms_produits = [f"{p['produit_id']} - {p['nom']}" for p in produits]
        map_produits = {
            f"{p['produit_id']} - {p['nom']}": p["produit_id"] for p in produits
        }

        vars_mouv = {
            "produit": tk.StringVar(),
            "type": tk.StringVar(value="ENTREE"),
            "quantite": tk.StringVar(value="0"),
            "motif": tk.StringVar(),
            "utilisateur": tk.StringVar(),
            "remarques": tk.StringVar(),
        }

        champs = [
            ("Produit :", "produit", ttk.Combobox, noms_produits),
            ("Type (ENTREE/SORTIE) :", "type", ttk.Combobox, ["ENTREE", "SORTIE"]),
            ("Quantité :", "quantite", tk.Entry),
            ("Motif :", "motif", tk.Entry),
            ("Utilisateur :", "utilisateur", tk.Entry),
            ("Remarques :", "remarques", tk.Entry),
        ]

        for i, (texte, nom, widget_type, *args) in enumerate(champs):
            tk.Label(cadre, text=texte).grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )
            if widget_type == ttk.Combobox:
                combo = ttk.Combobox(
                    cadre, textvariable=vars_mouv[nom], values=args[0], state="readonly"
                )
                combo.grid(row=i, column=1, padx=5, pady=2)
                if args[0]:
                    combo.set(args[0][0])
            else:
                tk.Entry(cadre, textvariable=vars_mouv[nom]).grid(
                    row=i, column=1, padx=5, pady=2
                )

        # ✅ Bouton Sauvegarder corrigé
        self.creer_bouton(
            cadre,
            "Sauvegarder",
            lambda: self._sauver_mouvement(vars_mouv, map_produits, dialogue),
        ).grid(row=len(champs), column=1, pady=10)

    def _sauver_mouvement(self, vars_mouv, map_produits, dialogue):
        """Valide et enregistre un nouveau mouvement."""
        try:
            produit_val = vars_mouv["produit"].get()
            produit_id = map_produits.get(produit_val)
            quantite = int(vars_mouv["quantite"].get())
            type_mouv = vars_mouv["type"].get()
            if not produit_id or quantite <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Validation", "Veuillez vérifier le produit, le type et la quantité."
            )
            return

        try:
            creer_mouvement(
                produit_id,
                type_mouv,
                quantite,
                vars_mouv["motif"].get(),
                vars_mouv["utilisateur"].get(),
                vars_mouv["remarques"].get(),
            )
            messagebox.showinfo("Succès", "Mouvement ajouté avec succès.")
            self.charger_mouvements(obtenir_tous_mouvements())
            dialogue.destroy()
        except Exception as e:
            messagebox.showerror("Erreur Base de Données", f"Erreur : {e}")
