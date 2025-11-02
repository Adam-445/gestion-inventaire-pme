import tkinter as tk
from tkinter import messagebox, ttk
from database.requetes import (
    creer_produit,
    modifier_produit,
    obtenir_produit,
    obtenir_tous_produits,
    obtenir_toutes_categories,
    rechercher_produits,
    supprimer_produit,
)

# -------------------- Thème Global --------------------
COULEUR_FOND = "#f8ffe8"
COULEUR_BOUTON = "#94FFC4"
COULEUR_TEXTE_BOUTON = "white"
COULEUR_BOUTON_ACTIVE = "#23B866"
POLICE_BOUTON = ("Bahnschrift", 12, "bold")
MARGE_X = 15
MARGE_Y = 10
LARGEUR_CHAMP = 35
LIGNE_PAIRE = "#ffffff"
LIGNE_IMPAIRE = "#e6ffe6"


class GestionProduitsFrame(tk.Frame):
    """Interface de gestion des produits."""

    def __init__(self, parent=None):
        super().__init__(parent, bg=COULEUR_FOND)
        self.pack(fill="both", expand=True)
        self._creer_interface()
        self._charger_produits()

    # -------------------- Création de l'interface --------------------
    def _creer_interface(self):
        self._creer_titre("Gestion des Produits")
        cadre_superieur = self._creer_cadre_superieur()
        self._creer_zone_recherche(cadre_superieur)
        self._creer_boutons_actions(cadre_superieur)
        self._creer_liste_produits()

    def _creer_titre(self, texte):
        tk.Label(
            self, text=texte, font=("Bahnschrift", 16, "bold"), bg=COULEUR_FOND
        ).pack(pady=15)

    def _creer_cadre_superieur(self):
        cadre = tk.Frame(self, bg=COULEUR_FOND)
        cadre.pack(fill="x", pady=10, padx=20)
        return cadre

    def _creer_zone_recherche(self, cadre):
        tk.Label(cadre, text="Recherche :", bg=COULEUR_FOND).pack(side="left", padx=5)
        self.var_recherche = tk.StringVar()
        tk.Entry(cadre, textvariable=self.var_recherche, width=30).pack(
            side="left", padx=5
        )
        self._creer_bouton(
            cadre,
            "Rechercher",
            lambda: self._charger_produits(self.var_recherche.get()),
        ).pack(side="left", padx=5)

    def _creer_boutons_actions(self, cadre):
        cadre_actions = tk.Frame(cadre, bg=COULEUR_FOND)
        cadre_actions.pack(side="right")
        self._creer_bouton(
            cadre_actions, "Ajouter Produit", self._ouvrir_dialogue_ajout
        ).pack(side="left", padx=5)
        self._creer_bouton(
            cadre_actions, "Modifier", self._ouvrir_dialogue_modification
        ).pack(side="left", padx=5)
        self._creer_bouton(
            cadre_actions, "Supprimer", self._confirmer_suppression, bg="#F44336"
        ).pack(side="left", padx=5)

    def _creer_liste_produits(self):
        colonnes = ("ID", "Nom", "Catégorie", "Code", "Prix", "Stock", "Stock Min")
        self.table = self._configurer_table(colonnes)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

    # -------------------- Composants réutilisables --------------------
    def _creer_bouton(self, parent, texte, commande, bg=None):
        bouton = tk.Button(
            parent,
            text=texte,
            command=commande,
            bg=bg or COULEUR_BOUTON,
            fg=COULEUR_TEXTE_BOUTON,
            activebackground=COULEUR_BOUTON_ACTIVE,
            font=POLICE_BOUTON,
            cursor="hand2",
        )
        # Effet survol
        bouton.bind("<Enter>", lambda e: bouton.config(bg=COULEUR_BOUTON_ACTIVE))
        bouton.bind("<Leave>", lambda e: bouton.config(bg=bg or COULEUR_BOUTON))
        return bouton

    def _configurer_table(self, colonnes):
        cadre_table = tk.Frame(self, bg=COULEUR_FOND)
        cadre_table.pack(fill="both", expand=True)

        table = ttk.Treeview(cadre_table, columns=colonnes, show="headings")
        for col in colonnes:
            table.heading(col, text=col)
            align = "center" if col in ("ID", "Stock", "Stock Min") else "w"
            largeur = 50 if col == "ID" else 150 if col == "Nom" else 100
            table.column(col, width=largeur, anchor=align)

        table.tag_configure("pair", background=LIGNE_PAIRE)
        table.tag_configure("impair", background=LIGNE_IMPAIRE)
        return table

    # -------------------- Chargement des données --------------------
    def _charger_produits(self, recherche=None):
        self.table.delete(*self.table.get_children())
        try:
            produits = (
                rechercher_produits(recherche) if recherche else obtenir_tous_produits()
            )
            produits = [dict(p) for p in (produits or [])]

            for i, prod in enumerate(produits):
                etiquette = "pair" if i % 2 == 0 else "impair"
                prix = self._formatter_prix(prod.get("prix_unitaire"))
                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        prod.get("produit_id"),
                        prod.get("nom"),
                        prod.get("nom_categorie", "N/A"),
                        prod.get("code_barre", ""),
                        prix,
                        prod.get("stock_actuel", 0),
                        prod.get("stock_minimum", 0),
                    ),
                    tags=(etiquette,),
                )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les produits : {e}")

    def _formatter_prix(self, valeur):
        try:
            return f"{float(valeur or 0):.2f}"
        except Exception:
            return "0.00"

    # -------------------- Gestion des produits --------------------
    def _get_id_selectionne(self):
        element = self.table.focus()
        if not element:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit.")
            return None
        try:
            return int(self.table.item(element, "values")[0])
        except Exception:
            messagebox.showwarning("Erreur", "ID produit invalide.")
            return None

    def _confirmer_suppression(self):
        produit_id = self._get_id_selectionne()
        if produit_id is None:
            return
        nom = self.table.item(self.table.focus(), "values")[1]
        if messagebox.askyesno(
            "Confirmation", f"Supprimer '{nom}' (ID: {produit_id}) ?"
        ):
            try:
                if supprimer_produit(produit_id):
                    messagebox.showinfo("Succès", "Produit supprimé avec succès.")
                    self._charger_produits()
                else:
                    messagebox.showerror("Erreur", "Suppression impossible.")
            except Exception as e:
                messagebox.showerror("Erreur", f"{e}")

    # -------------------- Dialogues (Ajout / Modification) --------------------
    def _ouvrir_dialogue_ajout(self):
        self._ouvrir_dialogue_produit("Ajouter un Produit")

    def _ouvrir_dialogue_modification(self):
        produit_id = self._get_id_selectionne()
        if produit_id:
            self._ouvrir_dialogue_produit("Modifier un Produit", produit_id)

    def _ouvrir_dialogue_produit(self, titre, produit_id=None):
        fenetre = tk.Toplevel(self.master)
        fenetre.title(titre)
        fenetre.transient(self.master)
        fenetre.grab_set()

        cadre_formulaire = tk.Frame(fenetre, padx=MARGE_X, pady=MARGE_Y)
        cadre_formulaire.pack(padx=MARGE_X, pady=MARGE_Y)

        categories, noms_categories, correspondance = self._charger_categories()
        vars_prod = self._creer_variables_produit(produit_id)

        self._creer_champs_formulaire(cadre_formulaire, vars_prod)
        self._creer_liste_categories(
            cadre_formulaire, noms_categories, correspondance, vars_prod
        )
        self._creer_bouton_sauvegarde(cadre_formulaire, produit_id, vars_prod, fenetre)

    # -------------------- Sous-fonctions pour le dialogue --------------------
    def _charger_categories(self):
        try:
            categories = obtenir_toutes_categories() or []
            categories = [dict(c) for c in categories]
        except Exception:
            categories = []
        noms = [c["nom"] for c in categories]
        correspondance = {c["nom"]: c["categorie_id"] for c in categories}
        return categories, noms, correspondance

    def _creer_variables_produit(self, produit_id):
        vars_prod = {
            "nom": tk.StringVar(),
            "code_barre": tk.StringVar(),
            "prix_unitaire": tk.StringVar(value="0.00"),
            "stock_actuel": tk.StringVar(value="0"),
            "stock_minimum": tk.StringVar(value="0"),
            "fournisseur": tk.StringVar(),
            "description": tk.StringVar(),
            "categorie_nom": tk.StringVar(),
            "categorie_id": None,
        }

        if produit_id:
            data = obtenir_produit(produit_id)
            if data:
                data = dict(data)
                for cle, val in data.items():
                    if cle in vars_prod and isinstance(vars_prod[cle], tk.StringVar):
                        vars_prod[cle].set(val if val is not None else "")
                vars_prod["categorie_id"] = data.get("categorie_id")
        return vars_prod

    def _creer_champs_formulaire(self, parent, vars_prod):
        champs = [
            ("Nom du Produit :", "nom"),
            ("Code Barre :", "code_barre"),
            ("Prix Unitaire :", "prix_unitaire"),
            ("Stock Actuel :", "stock_actuel"),
            ("Stock Minimum :", "stock_minimum"),
            ("Fournisseur :", "fournisseur"),
            ("Description :", "description"),
        ]
        for i, (label, cle) in enumerate(champs):
            tk.Label(parent, text=label).grid(
                row=i, column=0, sticky="w", padx=5, pady=2
            )
            tk.Entry(parent, textvariable=vars_prod[cle], width=LARGEUR_CHAMP).grid(
                row=i, column=1, padx=5, pady=2
            )

    def _creer_liste_categories(self, parent, noms, correspondance, vars_prod):
        tk.Label(parent, text="Catégorie :").grid(
            row=7, column=0, sticky="w", padx=5, pady=2
        )
        combo = ttk.Combobox(
            parent,
            textvariable=vars_prod["categorie_nom"],
            values=noms,
            width=LARGEUR_CHAMP - 2,
            state="readonly",
        )
        combo.grid(row=7, column=1, padx=5, pady=2)

        if noms and not vars_prod["categorie_nom"].get():
            combo.set(noms[0])
            vars_prod["categorie_id"] = correspondance[noms[0]]

        combo.bind(
            "<<ComboboxSelected>>",
            lambda e: vars_prod.update(
                {"categorie_id": correspondance[vars_prod["categorie_nom"].get()]}
            ),
        )

    def _creer_bouton_sauvegarde(self, parent, produit_id, vars_prod, fenetre):
        def sauvegarder():
            if not self._valider_champs(vars_prod):
                return
            donnees = self._extraire_donnees(vars_prod)
            try:
                if produit_id:
                    modifier_produit(produit_id, **donnees)
                    messagebox.showinfo("Succès", "Produit mis à jour.")
                else:
                    creer_produit(**donnees)
                    messagebox.showinfo("Succès", "Produit ajouté.")
                self._charger_produits()
                fenetre.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur : {e}")

        tk.Button(
            parent,
            text="Sauvegarder",
            command=sauvegarder,
            bg=COULEUR_BOUTON,
            fg=COULEUR_TEXTE_BOUTON,
        ).grid(row=8, column=1, pady=10)

    def _valider_champs(self, vars_prod):
        if not vars_prod["nom"].get().strip() or not vars_prod["categorie_id"]:
            messagebox.showwarning("Validation", "Nom et Catégorie requis.")
            return False
        try:
            float(vars_prod["prix_unitaire"].get())
            int(vars_prod["stock_actuel"].get())
            int(vars_prod["stock_minimum"].get())
        except ValueError:
            messagebox.showwarning(
                "Validation", "Vérifiez les champs numériques (Prix, Stock)."
            )
            return False
        return True

    def _extraire_donnees(self, vars_prod):
        return {
            "nom": vars_prod["nom"].get().strip(),
            "categorie_id": vars_prod["categorie_id"],
            "code_barre": vars_prod["code_barre"].get(),
            "prix_unitaire": float(vars_prod["prix_unitaire"].get()),
            "stock_actuel": int(vars_prod["stock_actuel"].get()),
            "stock_minimum": int(vars_prod["stock_minimum"].get()),
            "fournisseur": vars_prod["fournisseur"].get(),
            "description": vars_prod["description"].get(),
        }
