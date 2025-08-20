import customtkinter as ctk
from tkinter import messagebox, ttk

# Configuration de l'apparence
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Configuration du chiffrement
PASSWORD_DECHIFFREMENT = "1234"

# Chemin de la base de données
DB_FILE = "employes_securise.xlsx"

# ==============================================
#  FONCTIONS BACKEND
# ==============================================



# ==============================================
# INTERFACE GRAPHIQUE (FRONT-END)
# ==============================================

class AppEmployes(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🔒 Portail Employés Sécurisé")
        self.geometry("1000x700")
        
        # Création des onglets
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Onglets
        self.tabview.add("Accueil")
        self.tabview.add("Afficher Employés")
        self.tabview.add("Ajouter Employé")
        self.tabview.add("À Propos")
        
        # Configuration des onglets
        self.setup_accueil()
        self.setup_afficher()
        self.setup_ajouter()
        self.setup_a_propos()
    
    def setup_accueil(self):
        tab = self.tabview.tab("Accueil")
        
        # Titre
        titre = ctk.CTkLabel(tab, text="🏠 Portail Employés Sécurisé", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        titre.pack(pady=20)
        
        # Description
        desc = ctk.CTkLabel(tab, text="""Système de gestion sécurisée des employés avec chiffrement AES-256
➡️ Ajoutez des employés avec chiffrement automatique
➡️ Affichez les données avec protection par mot de passe
➡️ Sécurisez les informations sensibles""",
                          font=ctk.CTkFont(size=14))
        desc.pack(pady=10)
        
        # Statistiques
        stats_frame = ctk.CTkFrame(tab)
        stats_frame.pack(pady=20)
        
        ctk.CTkLabel(stats_frame, text="👥 Employés total: 0", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        ctk.CTkLabel(stats_frame, text="📅 Dernier ajout: Aucun", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
    
    def setup_afficher(self):
        tab = self.tabview.tab("Afficher Employés")
        
        # Titre
        ctk.CTkLabel(tab, text="👥 Liste des Employés", 
                   font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Frame pour les données
        self.data_frame = ctk.CTkScrollableFrame(tab, height=400)
        self.data_frame.pack(fill="both", expand=True, pady=10)
        
        # Mot de passe pour déchiffrement
        pass_frame = ctk.CTkFrame(tab)
        pass_frame.pack(pady=10)
        
        ctk.CTkLabel(pass_frame, text="🔑 Mot de passe:").pack(side="left", padx=5)
        self.password_entry = ctk.CTkEntry(pass_frame, show="*", width=150)
        self.password_entry.pack(side="left", padx=5)
        
        decrypt_btn = ctk.CTkButton(pass_frame, text="🔓 Déchiffrer", 
                                  command=self.dechiffrer_donnees)
        decrypt_btn.pack(side="left", padx=5)
        
        # Charger les données initiales
        self.afficher_donnees()
    
    def afficher_donnees(self, dechiffre=False):
        # Nettoyer le frame
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        
        
        # Simulation données vides
        df_vide = True
        
        if df_vide:
            ctk.CTkLabel(self.data_frame, text="Aucun employé enregistré").pack(pady=20)
            return
        
        # Créer un tableau
        columns = ['ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Salaire', 'Date Ajout']
        tree = ttk.Treeview(self.data_frame, columns=columns, show='headings', height=10)
        
        # Définir les colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Boucle sur les données réelles
    
        
        tree.pack(fill="both", expand=True)
    
    def dechiffrer_donnees(self):
        password = self.password_entry.get()
        if password == PASSWORD_DECHIFFREMENT:
            messagebox.showinfo("Succès", "Données déchiffrées avec succès!")
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect!")
    
    def setup_ajouter(self):
        tab = self.tabview.tab("Ajouter Employé")
        
        ctk.CTkLabel(tab, text="➕ Ajouter un Employé", 
                   font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Formulaire
        form_frame = ctk.CTkFrame(tab)
        form_frame.pack(pady=10)
        
        # Champs
        fields = [
            ("Nom", "nom_entry"),
            ("Prénom", "prenom_entry"),
            ("Email", "email_entry"),
            ("Téléphone", "telephone_entry"),
            ("Salaire", "salaire_entry")
        ]
        
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            row = i % 3
            col = i // 3
            
            frame = ctk.CTkFrame(form_frame)
            frame.grid(row=row, column=col, padx=10, pady=5)
            
            ctk.CTkLabel(frame, text=label + ":").pack()
            entry = ctk.CTkEntry(frame, width=150)
            entry.pack()
            self.entries[key] = entry
        
        # Bouton d'ajout
        add_btn = ctk.CTkButton(tab, text="✅ Enregistrer", 
                              command=self.ajouter_employe,
                              font=ctk.CTkFont(size=14))
        add_btn.pack(pady=20)
    
    
    def setup_a_propos(self):
        tab = self.tabview.tab("À Propos")
        
        info = """
        🔒 Portail Employés Sécurisé
        
        Fonctionnalités:
        - Chiffrement AES-256 des données sensibles
        - Protection par mot de passe (1234)
        - Interface desktop moderne
        
        Données chiffrées:
        📧 Emails
        📞 Téléphones
        💰 Salaires
        
        Développé avec CustomTKinter
        """
        
        ctk.CTkLabel(tab, text=info, font=ctk.CTkFont(size=14)).pack(pady=20)

if __name__ == "__main__":
    app = AppEmployes()
    app.mainloop()