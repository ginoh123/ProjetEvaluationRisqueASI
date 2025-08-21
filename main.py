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
        return "🔒 ERREUR"

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
        self.geometry("1100x750")
        
        # Création des onglets
        self.tabview = ctk.CTkTabview(self, width=1050, height=700)
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
        
        # Titre principal
        titre = ctk.CTkLabel(tab, text="🏠 Portail Employés Sécurisé", 
                           font=ctk.CTkFont(size=28, weight="bold"))
        titre.pack(pady=30)
        
        # Frame pour les statistiques
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(pady=20)
        
        df = charger_base()
        
        # Cartes statistiques
        cards_data = [
            {"text": "👥 Employés total", "value": len(df), "color": "#3B8ED0"},
            {"text": "📅 Dernier ajout", "value": df['date_ajout'].max() if not df.empty else "Aucun", "color": "#1F6AA5"},
            {"text": "🔒 Données sécurisées", "value": "AES-256", "color": "#144870"}
        ]
        
        for i, data in enumerate(cards_data):
            card = ctk.CTkFrame(stats_frame, width=250, height=120, fg_color=data["color"])
            card.grid(row=0, column=i, padx=15, pady=10)
            
            ctk.CTkLabel(card, text=data["text"], 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=str(data["value"]), 
                        font=ctk.CTkFont(size=20, weight="bold")).pack(pady=5)
        
        # Description
        desc_frame = ctk.CTkFrame(tab, fg_color="transparent")
        desc_frame.pack(pady=30, fill="x", padx=50)
        
        features = [
            "✅ Ajoutez des employés avec chiffrement automatique",
            "✅ Affichez les données avec protection par mot de passe",
            "✅ Sécurisez les informations sensibles (AES-256)",
            "✅ Interface moderne et intuitive"
        ]
        
        for feature in features:
            ctk.CTkLabel(desc_frame, text=feature, 
                        font=ctk.CTkFont(size=16), justify="left").pack(anchor="w", pady=8, padx=20)
        
        # Instructions
        instructions = ctk.CTkFrame(tab, fg_color="transparent")
        instructions.pack(pady=20)
        
        ctk.CTkLabel(instructions, text="🔑 Mot de passe pour déchiffrement: 1234", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
    
    def setup_afficher(self):
        tab = self.tabview.tab("Afficher Employés")
        
        # Titre
        ctk.CTkLabel(tab, text="👥 Liste des Employés", 
                   font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Frame pour le mot de passe
        pass_frame = ctk.CTkFrame(tab)
        pass_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(pass_frame, text="🔑 Mot de passe:").pack(side="left", padx=5)
        self.password_entry = ctk.CTkEntry(pass_frame, show="*", width=150)
        self.password_entry.pack(side="left", padx=5)
        
        decrypt_btn = ctk.CTkButton(pass_frame, text="🔓 Déchiffrer", 
                                  command=self.dechiffrer_donnees)
        decrypt_btn.pack(side="left", padx=5)
        
        # Frame pour le tableau avec barre de défilement
        table_frame = ctk.CTkFrame(tab)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Création du Treeview
        columns = ('ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Salaire', 'Date Ajout')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Définir les en-têtes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=100)
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des éléments
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Charger les données initiales
        self.afficher_donnees()
    
    def afficher_donnees(self, dechiffre=False):
        # Vider le treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        df = charger_base()
        if df.empty:
            return
        
        # Ajouter les données
        for _, row in df.iterrows():
            if dechiffre:
                email = dechiffrer(row['email'])
                telephone = dechiffrer(row['telephone'])
                salaire = dechiffrer(row['salaire'])
            else:
                # Afficher les valeurs cryptées au lieu de "CHIFFRÉ"
                email = row['email'][:20] + "..." if len(row['email']) > 20 else row['email']
                telephone = row['telephone'][:15] + "..." if len(row['telephone']) > 15 else row['telephone']
                salaire = row['salaire'][:10] + "..." if len(row['salaire']) > 10 else row['salaire']
            
            self.tree.insert("", "end", values=(
                row['id'], row['nom'], row['prenom'], 
                email, telephone, salaire, row['date_ajout']
            ))
    
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
                   font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        # Formulaire
        form_frame = ctk.CTkFrame(tab)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
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
            frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            frame.pack(pady=10, fill="x", padx=30)
            
            ctk.CTkLabel(frame, text=label + ":", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            entry = ctk.CTkEntry(frame, height=35, font=ctk.CTkFont(size=14))
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry
        
        # Bouton d'ajout
        add_btn = ctk.CTkButton(tab, text="✅ Enregistrer l'employé", 
                              command=self.ajouter_employe,
                              font=ctk.CTkFont(size=14, weight="bold"),
                              height=40)
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
                # Mettre à jour l'affichage
                self.afficher_donnees()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur: {str(e)}")
        else:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
    
    def setup_a_propos(self):
        tab = self.tabview.tab("À Propos")
        
        # Titre
        ctk.CTkLabel(tab, text="ℹ️ À Propos", 
                   font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        # Frame pour le contenu
        content_frame = ctk.CTkFrame(tab, fg_color="transparent")
        content_frame.pack(pady=10, padx=50)
        
        info_text = """
🔒 Portail Employés Sécurisé

Fonctionnalités:
• Chiffrement AES-256 des données sensibles
• Protection par mot de passe
• Interface desktop moderne

Données chiffrées:
📧 Emails
📞 Numéros de téléphone
💰 Salaires

Technologies utilisées:
• Python
• CustomTkinter
• Cryptography (Fernet)
• Pandas

Développé avec une attention particulière
à la sécurité des données personnelles.
        """
        
        ctk.CTkLabel(content_frame, text=info_text, 
                   font=ctk.CTkFont(size=14), justify="left").pack(pady=10)
        
        # Note de sécurité
        security_note = ctk.CTkFrame(tab, fg_color="#2B3D4D", corner_radius=10)
        security_note.pack(pady=20, padx=50, fill="x")
        
        ctk.CTkLabel(security_note, 
                   text="🔐 Note de sécurité: Vos données sont chiffrées avec un algorithme AES-256.\nSeules les personnes autorisées peuvent accéder aux informations sensibles.",
                   font=ctk.CTkFont(size=13), justify="center").pack(pady=15)

if __name__ == "__main__":
    app = AppEmployes()
    app.mainloop()