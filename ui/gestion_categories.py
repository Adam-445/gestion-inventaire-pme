import tkinter as tk
from tkinter import messagebox, ttk
from database.requetes import (
    creer_categorie,
    modifier_categorie,
    obtenir_toutes_categories,
    supprimer_categorie,
)

# ---------- Variables Globales de Thème ----------
COULEUR_FOND = "#f8ffe8"  # Couleur de fond principale
COULEUR_TEXTE = "black"  # Couleur du texte des titres et libellés
COULEUR_BOUTON = "#94FFC4"  # Vert clair
COULEUR_SURVOL = "#23B866"  # Vert foncé (survol / actif)
COULEUR_SUPPR = "#F44336"  # Rouge suppression
POLICE_BOUTON = ("Bahnschrift", 12, "bold")
ESPACE_X, ESPACE_Y = 5, 5
LARGEUR_CHAMP = 30


class GestionCategoriesFrame(tk.Frame):
    """Interface graphique pour la gestion des catégories."""

    def __init__(self, master=None):
        super().__init__(master, bg=COULEUR_FOND)
        self.pack(fill="both", expand=True)
        self._creer_interface()
        self._charger_categories()

    # ---------- Construction de l’interface ----------
    def _creer_interface(self):
        """Crée tous les éléments graphiques de la fenêtre."""
        self._creer_titre_principal()
        self._creer_formulaire()
        self._creer_tableau()
        self._creer_boutons_action()

    def _creer_titre_principal(self):
        """Affiche le titre principal."""
        self._creer_label(
            "Gestion des Catégories", taille=16, style="bold", couleur=COULEUR_TEXTE
        ).pack(pady=(20, 10))

    def _creer_formulaire(self):
        """Crée le formulaire d’ajout de catégorie."""
        cadre_formulaire = tk.Frame(
            self, bd=2, relief=tk.GROOVE, padx=20, pady=20, bg=COULEUR_FOND
        )
        cadre_formulaire.pack(pady=10, padx=20)
        cadre_formulaire.grid_columnconfigure(0, weight=1)
        cadre_formulaire.grid_columnconfigure(1, weight=2)

        self.nom_entry = self._creer_champ_saisi(
            cadre_formulaire, "Nom de la Catégorie :", 0, couleur_texte=COULEUR_TEXTE
        )
        self.desc_entry = self._creer_champ_saisi(
            cadre_formulaire, "Description :", 1, couleur_texte=COULEUR_TEXTE
        )

        self._creer_bouton(
            cadre_formulaire,
            "Ajouter Catégorie",
            self._ajouter_categorie,
            ligne=2,
            colonne=1,
            alignement="e",
            bg=COULEUR_BOUTON,
            fg=COULEUR_TEXTE,
            bg_actif=COULEUR_SURVOL,
        )

    def _creer_tableau(self):
        """Crée le tableau affichant la liste des catégories."""
        self._creer_label(
            "Liste des Catégories", taille=14, couleur=COULEUR_TEXTE
        ).pack(pady=(20, 10))

        self.tree = self._creer_treeview(
            colonnes=("ID", "Nom", "Description"),
            entetes=("ID", "Nom", "Description"),
            largeurs=(50, 150, 250),
        )
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

    def _creer_boutons_action(self):
        """Crée les boutons de modification et suppression."""
        cadre_actions = tk.Frame(self, bg=COULEUR_FOND)
        cadre_actions.pack(pady=10)

        self._creer_bouton(
            cadre_actions,
            "Modifier",
            self._ouvrir_fenetre_modification,
            cote="left",
            marge_x=5,
            bg=COULEUR_BOUTON,
            fg=COULEUR_TEXTE,
            bg_actif=COULEUR_SURVOL,
        )
        self._creer_bouton(
            cadre_actions,
            "Supprimer",
            self._confirmer_suppression,
            cote="left",
            marge_x=5,
            bg=COULEUR_SUPPR,
            fg=COULEUR_TEXTE,
        )

    # ---------- Fonctions utilitaires de création d’éléments ----------
    def _creer_label(self, texte, taille=12, style="normal", couleur="black"):
        """Crée un label simple."""
        return tk.Label(
            self,
            text=texte,
            font=("Montserrat", taille, style),
            bg=COULEUR_FOND,
            fg=couleur,
        )

    def _creer_champ_saisi(self, parent, texte_label, ligne, couleur_texte="black"):
        """Crée un label + champ de saisie alignés en grille."""
        tk.Label(
            parent,
            text=texte_label,
            font=("Montserrat", 12, "bold"),
            bg=COULEUR_FOND,
            fg=couleur_texte,
        ).grid(row=ligne, column=0, padx=ESPACE_X, pady=ESPACE_Y, sticky="w")
        entree = tk.Entry(parent, width=LARGEUR_CHAMP)
        entree.grid(row=ligne, column=1, padx=ESPACE_X, pady=ESPACE_Y)
        return entree

    def _creer_bouton(
        self,
        parent,
        texte,
        commande,
        ligne=None,
        colonne=None,
        alignement=None,
        cote=None,
        marge_x=0,
        bg=None,
        fg=None,
        bg_actif=None,
    ):
        """Crée un bouton stylé et gère le survol."""
        bouton = tk.Button(
            parent,
            text=texte,
            command=commande,
            bg=bg,
            fg=fg,
            font=POLICE_BOUTON,
            padx=10,
            pady=5,
            activebackground=bg_actif,
            cursor="hand2",
        )
        if ligne is not None and colonne is not None:
            bouton.grid(row=ligne, column=colonne, sticky=alignement, pady=ESPACE_Y)
        elif cote:
            bouton.pack(side=cote, padx=marge_x, pady=ESPACE_Y)
        else:
            bouton.pack(pady=ESPACE_Y)

        if bg_actif:
            bouton.bind("<Enter>", lambda e: bouton.config(bg=bg_actif))
            bouton.bind("<Leave>", lambda e: bouton.config(bg=bg))
        return bouton

    def _creer_treeview(self, colonnes, entetes, largeurs):
        """Crée un TreeView configuré."""
        cadre_tree = tk.Frame(self, bg=COULEUR_FOND)
        cadre_tree.pack(fill="both", expand=True, padx=20)
        tree = ttk.Treeview(cadre_tree, columns=colonnes, show="headings")

        for col, entete, largeur in zip(colonnes, entetes, largeurs):
            tree.heading(col, text=entete)
            alignement = "center" if col == "ID" else "w"
            tree.column(col, width=largeur, anchor=alignement)
        return tree

    # ---------- Gestion de la base de données ----------
    def _charger_categories(self):
        """Charge toutes les catégories depuis la base."""
        self.tree.delete(*self.tree.get_children())
        try:
            categories = obtenir_toutes_categories() or []
            for cat in categories:
                id_cat = cat["categorie_id"] if "categorie_id" in cat.keys() else cat[0]
                nom_cat = cat["nom"] if "nom" in cat.keys() else cat[1]
                desc_cat = cat["description"] if "description" in cat.keys() else cat[2]
                self.tree.insert("", tk.END, values=(id_cat, nom_cat, desc_cat))
        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible de charger les catégories : {e}"
            )

    def _ajouter_categorie(self):
        """Ajoute une nouvelle catégorie."""
        nom = self.nom_entry.get().strip()
        desc = self.desc_entry.get().strip()
        if not nom:
            messagebox.showwarning(
                "Entrée Invalide", "Le nom de la catégorie est requis."
            )
            return
        try:
            new_id = creer_categorie(nom, desc)
            messagebox.showinfo("Succès", f"Catégorie '{nom}' (ID: {new_id}) ajoutée.")
            self._charger_categories()
            self.nom_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l’ajout : {e}")

    def _categorie_selectionnee(self):
        """Retourne la catégorie actuellement sélectionnée dans le tableau."""
        item = self.tree.focus()
        if not item:
            messagebox.showwarning(
                "Sélection requise", "Veuillez sélectionner une catégorie."
            )
            return None
        valeurs = self.tree.item(item, "values")
        try:
            cat_id = int(valeurs[0])
        except (ValueError, TypeError):
            cat_id = valeurs[0]
        return {"id": cat_id, "nom": valeurs[1], "description": valeurs[2]}

    def _confirmer_suppression(self):
        """Demande confirmation avant suppression."""
        cat = self._categorie_selectionnee()
        if not cat:
            return
        if messagebox.askyesno(
            "Confirmation", f"Supprimer '{cat['nom']}' (ID {cat['id']}) ?"
        ):
            try:
                supprimer_categorie(cat["id"])
                messagebox.showinfo("Succès", f"Catégorie '{cat['nom']}' supprimée.")
                self._charger_categories()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")

    def _ouvrir_fenetre_modification(self):
        """Ouvre la fenêtre de modification pour une catégorie."""
        cat = self._categorie_selectionnee()
        if not cat:
            return

        fenetre = tk.Toplevel(self.master)
        fenetre.title(f"Modifier Catégorie : {cat['nom']}")
        fenetre.transient(self.master)
        fenetre.grab_set()
        fenetre.configure(bg=COULEUR_FOND)

        var_nom = tk.StringVar(value=cat["nom"])
        var_desc = tk.StringVar(value=cat["description"])

        self._ajouter_champ_dialogue(fenetre, "Nom :", var_nom, 0)
        self._ajouter_champ_dialogue(fenetre, "Description :", var_desc, 1)

        self._creer_bouton(
            fenetre,
            "Sauvegarder",
            lambda: self._sauvegarder_modifications(
                fenetre, cat["id"], var_nom, var_desc
            ),
            ligne=2,
            colonne=1,
            bg=COULEUR_BOUTON,
            fg=COULEUR_TEXTE,
            bg_actif=COULEUR_SURVOL,
        )

    def _ajouter_champ_dialogue(self, fenetre, texte, variable, ligne):
        """Ajoute un champ label + entrée dans la fenêtre de modification."""
        tk.Label(
            fenetre,
            text=texte,
            font=("Montserrat", 12, "bold"),
            bg=COULEUR_FOND,
            fg=COULEUR_TEXTE,
        ).grid(row=ligne, column=0, sticky="w", padx=ESPACE_X, pady=ESPACE_Y)
        tk.Entry(fenetre, textvariable=variable, width=LARGEUR_CHAMP).grid(
            row=ligne, column=1, padx=ESPACE_X, pady=ESPACE_Y
        )

    def _sauvegarder_modifications(self, fenetre, cat_id, var_nom, var_desc):
        """Sauvegarde les modifications apportées à une catégorie."""
        nouveau_nom = var_nom.get().strip()
        nouvelle_desc = var_desc.get().strip()
        if not nouveau_nom:
            messagebox.showwarning("Invalide", "Le nom ne peut pas être vide.")
            return
        try:
            if modifier_categorie(cat_id, nouveau_nom, nouvelle_desc):
                messagebox.showinfo("Succès", "Catégorie mise à jour avec succès.")
                self._charger_categories()
                fenetre.destroy()
            else:
                messagebox.showerror("Erreur", "La modification n’a pas été appliquée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour : {e}")
