import customtkinter as ctk
import pandas as pd
from cryptography.fernet import Fernet
import os
from tkinter import messagebox, ttk
from datetime import datetime

# Configuration de l'apparence
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Configuration du chiffrement
PASSWORD_DECHIFFREMENT = "1234"
DB_FILE = "employes_securise.xlsx"

def get_encryption_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as f:
            f.write(key)
        return key

KEY = get_encryption_key()
CIPHER = Fernet(KEY)

# Fonctions de chiffrement
def chiffrer(donnee):
    if pd.isna(donnee) or donnee == "":
        return donnee
    return CIPHER.encrypt(str(donnee).encode()).decode()

def dechiffrer(donnee_chiffree):
    if pd.isna(donnee_chiffree) or donnee_chiffree == "":
        return donnee_chiffree
    try:
        return CIPHER.decrypt(donnee_chiffree.encode()).decode()
    except:
        return "ERREUR_DECHIFFREMENT"

# Gestion de la base de données
def charger_base():
    if os.path.exists(DB_FILE):
        return pd.read_excel(DB_FILE)
    else:
        return pd.DataFrame(columns=['id', 'nom', 'prenom', 'email', 'telephone', 'salaire', 'date_ajout'])

def sauvegarder_base(df):
    df.to_excel(DB_FILE, index=False)

def ajouter_employe(nom, prenom, email, telephone, salaire):
    df = charger_base()
    nouvel_employe = {
        'id': len(df) + 1,
        'nom': nom,
        'prenom': prenom,
        'email': chiffrer(email),
        'telephone': chiffrer(telephone),
        'salaire': chiffrer(str(salaire)),
        'date_ajout': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    df = pd.concat([df, pd.DataFrame([nouvel_employe])], ignore_index=True)
    sauvegarder_base(df)
    return True

# Interface graphique
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
➡️ Sécurisez les informations senselles""",
                          font=ctk.CTkFont(size=14))
        desc.pack(pady=10)
        
        # Statistiques
        df = charger_base()
        stats_frame = ctk.CTkFrame(tab)
        stats_frame.pack(pady=20)
        
        ctk.CTkLabel(stats_frame, text=f"👥 Employés total: {len(df)}", 
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        if not df.empty:
            ctk.CTkLabel(stats_frame, text=f"📅 Dernier ajout: {df['date_ajout'].max()}", 
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
        
        df = charger_base()
        if df.empty:
            ctk.CTkLabel(self.data_frame, text="Aucun employé enregistré").pack(pady=20)
            return
        
        # Créer un tableau
        columns = ['ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Salaire', 'Date Ajout']
        tree = ttk.Treeview(self.data_frame, columns=columns, show='headings', height=10)
        
        # Définir les colonnes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Ajouter les données
        for _, row in df.iterrows():
            if dechiffre:
                email = dechiffrer(row['email'])
                telephone = dechiffrer(row['telephone'])
                salaire = dechiffrer(row['salaire'])
            else:
                email = "🔒 CHIFFRÉ"
                telephone = "🔒 CHIFFRÉ"
                salaire = "🔒 CHIFFRÉ"
            
            tree.insert("", "end", values=(
                row['id'], row['nom'], row['prenom'], 
                email, telephone, salaire, row['date_ajout']
            ))
        
        tree.pack(fill="both", expand=True)
    
    def dechiffrer_donnees(self):
        password = self.password_entry.get()
        if password == PASSWORD_DECHIFFREMENT:
            self.afficher_donnees(dechiffre=True)
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
    
    def ajouter_employe(self):
        données = {key: entry.get() for key, entry in self.entries.items()}
        
        if all(données.values()):
            try:
                ajouter_employe(
                    données['nom_entry'],
                    données['prenom_entry'],
                    données['email_entry'],
                    données['telephone_entry'],
                    float(données['salaire_entry'])
                )
                messagebox.showinfo("Succès", "Employé ajouté avec succès!")
                # Réinitialiser les champs
                for entry in self.entries.values():
                    entry.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        else:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
    
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