import tkinter as tk
from ui.gestion_categories import GestionCategoriesFrame
from ui.gestion_produits import GestionProduitsFrame

class MainWindow(tk.Frame):
    # fenetre principale de l'application
    def __init__(self,master = None):
        super().__init__(master)
        self.master.title("Systéme de Gestion d'Inventaire pour PME")
        self.pack(fill="both", expand=True)

        self.current_frame = None
        self.create_widgets()
        self.show_frame("CATEGORIES") # afficher la vue catzgorie au demarrage
    
    def create_widgets(self):
        # barre navigation
        nav_bar = tk.Frame(self, bd=2, relief=tk.RAISED)
        nav_bar.pack(side="top",fill="x")

        tk.Button(nav_bar, text ="Accueil (Dashboard)", command=lambda:print("Dashboard non implémenté")).pack(side="left",padx=5,pady=5)
        tk.Button(nav_bar, text="Produits", command=lambda: self.show_frame("PRODUITS")).pack(side="left", padx=5, pady=5)
        tk.Button(nav_bar, text="Catégories", command=lambda: self.show_frame("CATEGORIES")).pack(side="left", padx=5, pady=5)
        tk.Button(nav_bar, text="Mouvements", command=lambda: print("Mouvements non implémentés")).pack(side="left", padx=5, pady=5)
    def show_frame(self,name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        if name == "CATEGORIES": 
            frame = GestionCategoriesFrame(self)
        
        elif name == "PRODUITS":
            frame = GestionProduitsFrame(self)
        else:
            frame = tk.Frame(self)
            tk.Label(frame,text=f"Vue {name} à inplémenter").pack(padx=20,pady=20)
        
        frame.pack(fill = "both", expand=True)
        self.current_frame=frame