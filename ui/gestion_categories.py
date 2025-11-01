import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.requetes import get_all_categories, create_category, update_category, delete_category

class GestionCategoriesFrame(tk.Frame):
    #Interface pour l'ajout et l'affichage des catzgories

    def __init__ (self, master=None):
        super().__init__(master)
        self.pack(fill="both",expand=True)
        self.create_widgets()
        self.load_categories()
    



    def create_widgets(self):
        #Titre
        tk.Label(self, text = "Gestion des Catégories", font=("Arial",16,"bold")).pack(pady=10)

        #Cadre pour l'ajout
        form_frame = tk.Frame(self, padx=10, pady=10, bd=2, relief=tk.GROOVE)
        form_frame.pack(pady=10, fill="x", padx=20)

        # Champs du formulaire
        tk.Label(form_frame, text="Nom de la Catégorie:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nom_entry = tk.Entry(form_frame, width=30)
        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.desc_entry = tk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Bouton d'ajout
        tk.Button(form_frame, text="Ajouter Catégorie", command=self.add_category, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10, sticky="e")

        tk.Label(self, text="Liste des Catégories", font=("Arial", 14)).pack(pady=10)
    
        self.list_box = tk.Text(self, height=10, width=50)
        self.list_box.pack(pady=10, padx=20)

        #cadre pour la liste des categories et les actions
        list_frame = tk.Frame(self, padx= 10, pady=10)
        list_frame.pack(pady=10, fill="both", expand=True, padx= 20)

        #Définition du Treeview 
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Nom", "Description"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Description", text="Description")
        
        #Configuration des largeurs
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Nom", width=150)
        self.tree.column("Description", width=250)
        
        self.tree.pack(side="top", fill="both", expand=True)

        #(Modifier/Supprimer)
        action_frame = tk.Frame(list_frame)
        action_frame.pack(side="bottom", fill="x", pady=5)
        
        tk.Button(action_frame, text="Modifier", command=self.open_edit_dialog).pack(side="left", padx=5)
        tk.Button(action_frame, text="Supprimer", command=self.confirm_delete, bg="#F44336", fg="white").pack(side="left", padx=5)





    def load_categories(self):
        """Charge et affiche les catégories depuis la base de données."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        try: 
            categories = get_all_categories()
            if not categories:
                return
            for cat in categories:
                self.tree.insert("",tk.END,values=(
                    cat['categorie_id'],
                    cat['nom'],
                    cat['description']
                ))
        except Exception as e:
            messagebox.showerror("Erreur DB",f"Impossible de charger les catégories:{e}")





    def add_category(self):
        """Ajoute une nouvelle catégorie dans la base de données."""
        nom = self.nom_entry.get().strip()
        description = self.desc_entry.get().strip()
        if not nom:
            messagebox.showwarning("Entrée Invalide", "Le nom de la catégorie ne peut pas être vide.")
            return
        try:
            new_id = create_category(nom, description)
            messagebox.showinfo("Succès", f"Catégorie '{nom}' (ID: {new_id}) ajoutée avec succès.")
            self.load_categories()
            self.nom_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erreur d'Ajout", f"Erreur lors de l'ajout de la catégorie : {e}")
        





    def get_selected_category(self):
        """Récupère l'ID et les valeurs de la catégorie sélectionnée."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Sélection requise", "Veuillez sélectionner une catégorie dans la liste.")
            return None
        values = self.tree.item(selected_item, 'values')
        return {'id': values[0], 'nom': values[1], 'description': values[2]}




    def confirm_delete(self):
        """Demande confirmation avant de supprimer la catégorie sélectionnée."""
        selected_cat = self.get_selected_category()
        if not selected_cat:
            return
        cat_id = int(selected_cat['id'])
        nom = selected_cat['nom']
        if messagebox.askyesno("Confirmation de Suppression", 
                               f"Êtes-vous sûr de vouloir supprimer la catégorie '{nom}' (ID: {cat_id})?"):
            try:
                delete_category(cat_id) 
                messagebox.showinfo("Succès", f"Catégorie '{nom}' supprimée.")
                self.load_categories()
            except Exception as e:
                messagebox.showerror("Erreur de Suppression", f"Impossible de supprimer la catégorie : {e}")


    def open_edit_dialog(self):
        """Ouvre un dialogue pour modifier la catégorie sélectionnée."""
        selected_cat = self.get_selected_category()
        if not selected_cat:
            return

        # Simple fenêtre de dialogue Tkinter
        dialog = tk.Toplevel(self.master)
        dialog.title(f"Modifier Catégorie: {selected_cat['nom']}")
        dialog.transient(self.master)
        
        tk.Label(dialog, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        name_var = tk.StringVar(value=selected_cat['nom'])
        name_entry = tk.Entry(dialog, textvariable=name_var)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        desc_var = tk.StringVar(value=selected_cat['description'])
        desc_entry = tk.Entry(dialog, textvariable=desc_var)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)

        def save_changes():
            new_name = name_var.get().strip()
            new_desc = desc_var.get().strip()

            if not new_name:
                messagebox.showwarning("Invalide", "Le nom ne peut pas être vide.")
                return

            try:
                # Appel à la fonction DB
                update_category(selected_cat['id'], new_name, new_desc) 
                messagebox.showinfo("Succès", "Catégorie mise à jour.")
                self.load_categories()
                dialog.destroy() 
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de modification : {e}")

        tk.Button(dialog, text="Sauvegarder", command=save_changes).grid(row=2, column=1, pady=10)
        dialog.grab_set()
        self.master.wait_window(dialog)