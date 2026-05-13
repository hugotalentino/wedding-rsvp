"""
Wedding RSVP Application
"""

import streamlit as st
import qrcode
from PIL import Image
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration de la page
st.set_page_config(
    page_title="Mariage Hugo & Sonate",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Fichier de stockage des réponses
DATA_FILE = "responses.csv"

# Style CSS personnalisé
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    .stApp {
        background: transparent;
    }
    .title {
        font-family: 'Georgia', serif;
        font-size: 3rem !important;
        color: #2c3e50 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    .subtitle {
        font-family: 'Georgia', serif;
        font-size: 1.5rem !important;
        color: #7f8c8d !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .success-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
    }
    .qr-container {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    .heart {
        color: #e74c3c;
        font-size: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def connect_to_google_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"],
        scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Wedding_RSVP").sheet1

    return sheet

def load_responses():
    try:
        sheet = connect_to_google_sheet()

        data = sheet.get_all_records()

        if data:
            return pd.DataFrame(data)

        return pd.DataFrame(columns=[
            "nom", "prenom", "email", "telephone", "presence", "jours_presents",
            "transport", "arrivee_train", "commentaire_train", "camping", "materiel_camping",
            "vegetarien", "vegan", "sans_gluten", "autres_regimes",
            "message", "date_reponse"
        ])

    except Exception as e:
        st.error(f"Erreur chargement Google Sheets : {e}")

        return pd.DataFrame()


def save_response(data):
    try:
        sheet = connect_to_google_sheet()

        row = [
            data["nom"],
            data["prenom"],
            data["email"],
            data["telephone"],
            data["presence"],
            data["jours_presents"],
            data["transport"],
            data["arrivee_train"],
            data["commentaire_train"],
            data["camping"],
            data["materiel_camping"],
            data["autres_regimes"],
            data["message"],
            data["date_reponse"]
        ]

        sheet.append_row(row)

    except Exception as e:
        st.error(f"Erreur sauvegarde : {e}")

def show_rsvp_form():
    """Affiche le formulaire de RSVP"""
    st.markdown('<p class="title">💍 Hugo & Sonate</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.88);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        text-align: center;
        line-height: 1.8;
    ">

    <h2 style="
        font-family: Georgia, serif;
        color: #2c3e50;
        margin-bottom: 1rem;
    ">
    ✨Bienvenue à notre mariage✨
    </h2>

    <p style="
        font-size: 1.1rem;
        color: #555;
    ">
    Nous avons immensément hâte de célébrer ce moment unique avec vous 💍
    </p>

    <p style="
        font-size: 1rem;
        color: #666;
        margin-top: 1.5rem;
    ">
    Votre présence sera, de loin, le plus beau des cadeaux. ❤️
    </p>

    <p style="
        font-size: 1rem;
        color: #666;
    ">
    Comme nous aimons voyager léger dans nos aventures à venir, 
    les machines à café, services d’argenterie et autres grands classiques des listes de mariage 
    risqueraient d’avoir du mal à nous suivre dans nos périples.
    </p>

    <p style="
        font-size: 1rem;
        color: #666;
    ">
    Si vous souhaitez malgré tout nous gâter, une urne sera présente sur le lieu de réception. 
    Elle contribuera à nos futurs projets et à ce nouveau chapitre de notre vie ✨
    </p>

    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        text-align:center;
        margin-bottom:2rem;
    ">
    <h3>📅 3 juillet 2027</h3>
    <h3>📍 Château de Bois Charmant, 15 Bois Charmant, 17380 Les Nouillers, France</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    #with st.form("rsvp_form", clear_on_submit=True):
    st.markdown("## ✨ Vos coordonnées")
    
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom *", placeholder="Votre nom")
    with col2:
        prenom = st.text_input("Prénom *", placeholder="Votre prénom")
    
    email = st.text_input("Email *", placeholder="votre@email.com")
    telephone = st.text_input("Téléphone (optionnel)", placeholder="...")
    
    st.markdown("---")
    st.markdown("## 🎉 Votre présence")
    
    presence = st.radio(
        "Seriez-vous présent(e) à notre mariage ? *",
        ["Oui, avec plaisir !", "Non, je ne pourrai pas venir"],
        horizontal=True
    )
    st.markdown("---")
    st.markdown("## 📅 Quels jours serez-vous présents ?")

    vendredi = st.checkbox("Vendredi (préparation, répétition, dîner)")
    samedi = st.checkbox("Samedi (mariage 💍)")
    dimanche = st.checkbox("Dimanche (brunch, rangement)")

    jours_selectionnes = []

    if vendredi:
        jours_selectionnes.append("Vendredi")

    if samedi:
        jours_selectionnes.append("Samedi")

    if dimanche:
        jours_selectionnes.append("Dimanche")

    st.markdown("---")
    st.markdown("## 🍽️ Allergie")

    autres_regimes = st.text_area(
        "Allergie aux parisiens, intolérance a l'architecture medievale, etc...)",
        placeholder="Précisez si nécessaire..."
    )
    
    st.markdown("---")
    st.markdown("## 🚗 Logistique")

    transport = st.selectbox(
        "Comment viendrez-vous ?",
        ["Voiture", "Train", "Covoiturage", "Autre"]
    )

    commentaire_train = ""

    if transport == "Train":

        st.markdown("### 🚆 Arrivée en train")

        jour_arrivee = st.selectbox(
            "Quel jour arrivez-vous ?",
            ["Vendredi", "Samedi"]
        )

        heure_arrivee = st.text_input(
            "Heure d'arrivée",
            placeholder="Ex : 15h42"
        )

        gare_arrivee = st.text_input(
            "Gare d'arrivée",
            placeholder="Ex : Gare de Surgères"
        )

        commentaire_train = f"{jour_arrivee} - {heure_arrivee} - {gare_arrivee}"

        st.warning(
            "⚠️ Nous ne pourrons malheureusement pas venir chercher des invités à la gare le jour du mariage. Nous vous recommandons fortement une arrivée le vendredi afin de faciliter l'organisation et les déplacements."
        )
    
    besoin_hebergement = st.radio(
        "Dormez vous au chateau ?",
        ["Non, un autre manoir m'attend", "Oui, au camping du chateau", "Oui, j'ai mon vanne", "Oui, les mariés m'on assigné une chambre/cabane"],
        horizontal=True
    )

    materiel_camping = ""

    if besoin_hebergement == "Oui, au camping du chateau":
        materiel_camping = st.text_area(
            "Matériel de camping manquant",
            placeholder="Ex: j'ai besoin d'une tente, matelas, sac de couchage..."
        )

    st.markdown("---")
    st.markdown("## 💬 Message")
    
    message = st.text_area(
        "Un petit mot pour les mariés ?",
        placeholder="Félicitations, vœux, anecdote..."
    )
    
    #submitted = st.form_submit_button("💌 Envoyer ma réponse", type="primary")
    submitted = st.button("💌 Envoyer ma réponse", type="primary")

    if submitted:
        if not nom or not prenom or not email:
            st.error("Merci de remplir tous les champs obligatoires (*)")
        else:
            data = {
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "telephone": telephone,
                "presence": presence,
                "jours_presents": ", ".join(jours_selectionnes),
                "transport": transport,
                "arrivee_train": "Oui" if transport == "Train" else "Non",
                "commentaire_train": commentaire_train,
                "camping": besoin_hebergement,
                "materiel_camping": materiel_camping,
                "autres_regimes": autres_regimes,
                "message": message,
                "date_reponse": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            save_response(data)
            st.markdown("""
            <div class="success-message">
                <h2>💕 Merci pour votre réponse !</h2>
                <p>Nous avons hâte de vous voir à notre mariage !</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()



def main():
    """Point d'entrée principal"""  
    show_rsvp_form()


if __name__ == "__main__":
    main()