import tkinter as tk
from tkinter import ttk, messagebox
from database.requetes import *
class GestionProduitsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_products()

    def create_widgets(self):
        tk.Label(self, text="Gestion des Produits", font=("Arial", 16, "bold")).pack(pady=10)

        top_frame = tk.Frame(self, padx=10)
        top_frame.pack(fill="x", padx=20)

        # Recherche 
        tk.Label(top_frame, text="Recherche:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.search_var, width=30).pack(side="left", padx=5)
        tk.Button(top_frame, text="Rechercher", command=lambda: print("Recherche à implémenter")).pack(side="left", padx=5)
        
        # Boutons d'action
        tk.Button(top_frame, text="Ajouter Produit", command=self.open_add_dialog, bg="#008CBA", fg="white").pack(side="right", padx=5)
        tk.Button(top_frame, text="Supprimer", command=self.confirm_delete).pack(side="right", padx=5)
        tk.Button(top_frame, text="Modifier", command=self.open_edit_dialog).pack(side="right", padx=5)


        # Tableau Treeview pour afficher les produits
        columns = ("ID", "Nom", "Catégorie", "Code", "Prix", "Stock", "Min Stock")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Configuration des en-têtes
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("ID", width=40, anchor='center')
        self.tree.column("Nom", width=150)
        self.tree.column("Catégorie", width=100)
        self.tree.column("Code", width=80)
        self.tree.column("Prix", width=70, anchor='e')
        self.tree.column("Stock", width=60, anchor='center')
        self.tree.column("Min Stock", width=70, anchor='center')

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)


    def load_products(self):
        """Charge et affiche les produits depuis la DB dans le Treeview."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        try:
            products = get_all_products()
            
            for prod in products:
                self.tree.insert("", tk.END, values=(
                    prod['produit_id'], 
                    prod['nom'], 
                    prod.get('categorie_nom', 'N/A'),
                    prod.get('code_barre', ''), 
                    f"{prod['prix_unitaire']:.2f}",
                    prod['stock_actuel'],
                    prod['stock_minimum']
                ))
                
        except Exception as e:
            messagebox.showerror("Erreur DB", f"Impossible de charger les produits : {e}")
    
    def open_add_dialog(self):
        """Ouvre un dialogue pour ajouter un nouveau produit."""
        
        try:
            categories = get_all_categories() 
        except Exception as e:
            messagebox.showerror("Erreur DB", f"Impossible de charger les catégories pour l'ajout : {e}")
            return
            
        if not categories:
            messagebox.showwarning("Attention", "Veuillez créer des catégories avant d'ajouter des produits.")
            return

        dialog = tk.Toplevel(self.master)
        dialog.title("Ajouter un nouveau produit")
        dialog.transient(self.master)

        form_frame = tk.Frame(dialog, padx=10, pady=10)
        form_frame.pack(padx=10, pady=10)

        vars_prod = {
            'nom': tk.StringVar(),
            'code_barre': tk.StringVar(),
            'prix_unitaire': tk.StringVar(value="0.00"),
            'stock_minimum': tk.StringVar(value="0"),
            'fournisseur': tk.StringVar(),
            'description': tk.StringVar(),
            'categorie_nom': tk.StringVar(),
            'categorie_id': None
        }
        
        category_names = [cat['nom'] for cat in categories]
        category_map = {cat['nom']: cat['categorie_id'] for cat in categories}

        fields = [
            ("Nom du Produit:", 'nom', 0),
            ("Code Barre:", 'code_barre', 1),
            ("Prix Unitaire:", 'prix_unitaire', 2),
            ("Stock Minimum:", 'stock_minimum', 3),
            ("Fournisseur:", 'fournisseur', 4),
            ("Description:", 'description', 5)
        ]

        for i, (label_text, var_name, row) in enumerate(fields):
            tk.Label(form_frame, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            tk.Entry(form_frame, textvariable=vars_prod[var_name], width=35).grid(row=row, column=1, padx=5, pady=2)
        
        tk.Label(form_frame, text="Catégorie:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        category_combo = ttk.Combobox(form_frame, textvariable=vars_prod['categorie_nom'], values=category_names, width=33, state="readonly")
        category_combo.grid(row=6, column=1, padx=5, pady=2)
        
        if category_names:
            category_combo.set(category_names[0])
            vars_prod['categorie_id'] = category_map[category_names[0]]

        def on_category_select(event):
            selected_name = vars_prod['categorie_nom'].get()
            vars_prod['categorie_id'] = category_map[selected_name]

        category_combo.bind("<<ComboboxSelected>>", on_category_select)

        def save_product():
            nom = vars_prod['nom'].get().strip()
            prix = vars_prod['prix_unitaire'].get()
            stock_min = vars_prod['stock_minimum'].get()
            
            if not nom or vars_prod['categorie_id'] is None:
                messagebox.showwarning("Validation", "Le Nom et la Catégorie sont obligatoires.")
                return
            
            try:
                prix_float = float(prix)
                stock_min_int = int(stock_min)
            except ValueError:
                messagebox.showwarning("Validation", "Le Prix et le Stock Min. doivent être des nombres valides.")
                return

            product_data = {
                'nom': nom,
                'categorie_id': vars_prod['categorie_id'],
                'code_barre': vars_prod['code_barre'].get(),
                'prix_unitaire': prix_float,
                'stock_minimum': stock_min_int,
                'fournisseur': vars_prod['fournisseur'].get(),
                'description': vars_prod['description'].get()
            }
            
            try:
                create_product(product_data)
                messagebox.showinfo("Succès", f"Produit '{nom}' ajouté avec succès.")
                self.load_products()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erreur DB", f"Erreur lors de l'ajout : {e}")

        tk.Button(dialog, text="Ajouter et Fermer", command=save_product, bg="#4CAF50", fg="white").pack(pady=10)
        
        dialog.grab_set()
        self.master.wait_window(dialog)

    def get_selected_product_id(self):
        """Récupère l'ID du produit sélectionné."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un produit.")
            return None

        return int(self.tree.item(selected_item, 'values')[0]) 

    def confirm_delete(self):
        """Supprime le produit sélectionné."""
        product_id = self.get_selected_product_id()
        if product_id is None:
            return

        product_name = self.tree.item(self.tree.focus(), 'values')[1]

        if messagebox.askyesno("Confirmation de Suppression", 
                               f"Êtes-vous sûr de vouloir supprimer le produit '{product_name}' (ID: {product_id})?"):
            try:
                delete_product(product_id)
                messagebox.showinfo("Succès", f"Produit '{product_name}' supprimé.")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer le produit : {e}")


    def get_selected_product_details(self):
        """Récupère les détails complets du produit sélectionné via la DB."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner un produit à modifier.")
            return None
        
        values = self.tree.item(selected_item, 'values')
        product_id = int(values[0])
        category_name = values[2] 
        
        try:
            full_data = get_product_by_id(product_id) 
            
            full_data['category_name'] = category_name 
            return full_data
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les détails du produit : {e}")
            return None

    def open_edit_dialog(self):
        selected_prod = self.get_selected_product_details()
        if not selected_prod:
            return

        try:
            categories = get_all_categories() 
        except Exception: return

        category_names = [cat['nom'] for cat in categories]
        category_map = {cat['nom']: cat['categorie_id'] for cat in categories}

        dialog = tk.Toplevel(self.master)
        dialog.title(f"Modifier Produit: {selected_prod['nom']}")
        dialog.transient(self.master)
        form_frame = tk.Frame(dialog, padx=10, pady=10)
        form_frame.pack(padx=10, pady=10)

        vars_prod = {
            'nom': tk.StringVar(value=selected_prod['nom']),
            'code_barre': tk.StringVar(value=selected_prod['code_barre'] or ""),
            'prix_unitaire': tk.StringVar(value=f"{selected_prod['prix_unitaire']:.2f}"),
            'stock_actuel': tk.StringVar(value=str(selected_prod['stock_actuel'])), 
            'stock_minimum': tk.StringVar(value=str(selected_prod['stock_minimum'])),
            'fournisseur': tk.StringVar(value=selected_prod['fournisseur'] or ""),
            'description': tk.StringVar(value=selected_prod['description'] or ""),
            'categorie_nom': tk.StringVar(value=selected_prod['category_name']),
            'categorie_id': selected_prod['categorie_id']
        }

        fields = [
            ("Nom du Produit:", 'nom', 0),
            ("Code Barre:", 'code_barre', 1),
            ("Prix Unitaire:", 'prix_unitaire', 2),
            ("Stock Actuel:", 'stock_actuel', 3), 
            ("Stock Minimum:", 'stock_minimum', 4),
            ("Fournisseur:", 'fournisseur', 5),
            ("Description:", 'description', 6)
        ]

        for i, (label_text, var_name, row) in enumerate(fields):
            tk.Label(form_frame, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            tk.Entry(form_frame, textvariable=vars_prod[var_name], width=35).grid(row=row, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Catégorie:").grid(row=7, column=0, sticky="w", padx=5, pady=2)
        category_combo = ttk.Combobox(form_frame, textvariable=vars_prod['categorie_nom'], values=category_names, width=33, state="readonly")
        category_combo.grid(row=7, column=1, padx=5, pady=2)

        category_combo.bind("<<ComboboxSelected>>", 
                            lambda event: vars_prod.update({'categorie_id': category_map[vars_prod['categorie_nom'].get()]}))


        def save_changes():

            try:
                new_data = {
                    'nom': vars_prod['nom'].get().strip(),
                    'categorie_id': vars_prod['categorie_id'],
                    'code_barre': vars_prod['code_barre'].get(),
                    'prix_unitaire': float(vars_prod['prix_unitaire'].get()),
                    'stock_actuel': int(vars_prod['stock_actuel'].get()), 
                    'stock_minimum': int(vars_prod['stock_minimum'].get()),
                    'fournisseur': vars_prod['fournisseur'].get(),
                    'description': vars_prod['description'].get()
                }
            except ValueError:
                messagebox.showwarning("Validation", "Veuillez vérifier les champs numériques (Prix, Stock Actuel, Stock Min.).")
                return

            if not new_data['nom']:
                messagebox.showwarning("Validation", "Le Nom ne peut pas être vide.")
                return

            try:

                update_product(selected_prod['produit_id'], **new_data) 
                messagebox.showinfo("Succès", "Produit mis à jour.")
                self.load_products() 
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de modification : {e}")

        tk.Button(dialog, text="Sauvegarder", command=save_changes, bg="#FFC107", fg="black").grid(row=8, column=1, pady=10)
        dialog.grab_set()
        self.master.wait_window(dialog)