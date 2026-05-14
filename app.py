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
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration de la page
st.set_page_config(
    page_title="Mariage Hugo & Sonate",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Bannière photo
st.markdown("""
<style>

.banner-container {
    position: relative;
    width: 100%;
    height: 520px;
    overflow: hidden;
    border-radius: 0 0 30px 30px;
    margin-bottom: 2rem;
}

.banner-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.72);
}

.banner-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
}

.banner-text h1 {
    font-family: Georgia, serif;
    font-size: 4rem;
    margin-bottom: 1rem;
    letter-spacing: 2px;
}

.banner-text p {
    font-size: 1.3rem;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)

# Style CSS personnalisé
st.markdown("""
<style>

/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500&display=swap');

/* Fond général */
.stApp {
    background:
        linear-gradient(rgba(255,255,255,0.82), rgba(255,255,255,0.82)),
        url("https://images.unsplash.com/photo-1519741497674-611481863552?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* Container principal */
.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Titres */
.stApp::before {
    content:"";
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:url("https://www.transparenttextures.com/patterns/floral-white.png");
    opacity:0.15;
    pointer-events:none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}            

.title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 5rem !important;
    font-weight: 600;
    text-align: center;
    color: #3e2f2f;
    margin-bottom: 0rem !important;
    letter-spacing: 2px;
}

.subtitle {
    font-family: 'Cormorant Garamond', serif;
    text-align: center;
    color: #7b6d6d;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Cartes */
.section-card {
    animation: fadeUp 0.8s ease;
}

@keyframes fadeUp {
    from {
        opacity:0;
        transform:translateY(20px);
    }
    to {
        opacity:1;
        transform:translateY(0);
    }
}
            
.section-card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(8px);
    padding: 2rem;
    border-radius: 24px;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.4);
}

/* Titres sections */
.section-title {
    font-family: 'Cormorant Garamond', serif;
    color: #4b3b3b;
    font-size: 2rem;
    margin-bottom: 1rem;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 14px !important;
    border: 1px solid #e3dede !important;
    padding: 0.7rem !important;
    background-color: rgba(255,255,255,0.9) !important;
}

/* Radio + checkbox */
.stRadio label,
.stCheckbox label {
    font-family: 'Cormorant Garamond', serif;
}

/* Bouton */
.stButton > button {
    width: 100%;
    border-radius: 50px;
    border: none;
    background: linear-gradient(135deg, #b76e79, #d9a5b3);
    color: white;
    font-size: 1.1rem;
    padding: 0.9rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 6px 18px rgba(183,110,121,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(183,110,121,0.45);
}

/* Séparateurs */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #d8c3c8, transparent);
    margin: 2rem 0;
}

/* Messages */
.stSuccess {
    border-radius: 18px;
}

/* Mobile */
@media (max-width: 768px) {
    .title {
        font-size: 3.2rem !important;
    }

    .section-card {
        padding: 1.3rem;
    }
}

</style>
""", unsafe_allow_html=True)

def send_confirmation_email(to_email, prenom, data):

    sender_email = st.secrets["gcp_service_account"]["EMAIL_ADDRESS"]
    sender_password = st.secrets["gcp_service_account"]["EMAIL_PASSWORD"]

    subject = "💍 Confirmation RSVP — Mariage Hugo & Sonate"

    html = f"""
    <html>
    <body style="
        font-family: Georgia, serif;
        background-color:#f8f5f1;
        color:#2c3e50;
        padding:40px;
    ">

        <div style="
            max-width:700px;
            margin:auto;
            background:white;
            border-radius:20px;
            padding:40px;
            box-shadow:0 10px 30px rgba(0,0,0,0.08);
        ">

            <h1 style="
                text-align:center;
                color:#b08d57;
                font-size:42px;
                margin-bottom:10px;
            ">
                💍 Hugo & Sonate
            </h1>

            <p style="
                text-align:center;
                font-size:18px;
                color:#7f8c8d;
                margin-bottom:40px;
            ">
                Merci d’avoir répondu à notre invitation 🌺
            </p>

            <p style="font-size:18px;">
                Bonjour <strong>{prenom}</strong>,
            </p>

            <p style="line-height:1.8;">
                Nous avons bien reçu votre réponse pour notre mariage et nous sommes très heureux de pouvoir partager ce moment avec vous ❤️
            </p>

            <hr style="margin:30px 0; border:none; border-top:1px solid #eee;">

            <h2 style="color:#b08d57;">
                📋 Récapitulatif de votre réponse
            </h2>

            <ul style="line-height:2;">
                <li><strong>Présence :</strong> {data["presence"]}</li>
                <li><strong>Jours présents :</strong> {data["jours_presents"]}</li>
                <li><strong>Transport :</strong> {data["transport"]}</li>
                <li><strong>Hébergement :</strong> {data["camping"]}</li>
            </ul>

            <hr style="margin:30px 0; border:none; border-top:1px solid #eee;">

            <h2 style="color:#b08d57;">
                📍 Informations pratiques
            </h2>

            <p style="line-height:1.8;">
                <strong>Date :</strong> 3 juillet 2027<br>
                <strong>Lieu :</strong> Château de Bois Charmant, 17380 Les Nouillers, France
            </p>

            <hr style="margin:30px 0; border:none; border-top:1px solid #eee;">

            <h2 style="color:#b08d57;">
                🎨 Dress code
            </h2>

            <p style="line-height:1.8;">
                Les tenues entièrement noires sont proscrites 🖤🚫<br>
                Venez colorés, élégants, lumineux et festifs 🌺
            </p>

            <div style="
                margin-top:50px;
                padding:25px;
                background:#f8f5f1;
                border-radius:15px;
                text-align:center;
            ">
                <p style="font-size:20px; margin-bottom:10px;">
                    Nous avons tellement hâte de célébrer avec vous ❤️
                </p>

                <p style="
                    color:#7f8c8d;
                    font-size:16px;
                ">
                    Hugo & Sonate
                </p>
            </div>

            <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center">
                <img src="https://raw.githubusercontent.com/hugotalentino/wedding-rsvp/main/banner2.jpg"
                    style="
                        width:100%;
                        max-width:500px;
                        border-radius:20px;
                        margin:25px 0;
                        box-shadow:0 8px 20px rgba(0,0,0,0.15);
                    ">
                </td>
            </tr>
            </table>
        </div>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, sender_password)

        server.sendmail(
            sender_email,
            to_email,
            msg.as_string()
        )

        server.quit()

    except Exception as e:
        st.error(f"Erreur email : {e}")

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
            "vegetarien", "vegan", "sans_gluten", "allergie",
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
            data["allergie"],
            data["message"],
            data["date_reponse"]
        ]

        sheet.append_row(row)

    except Exception as e:
        st.error(f"Erreur sauvegarde : {e}")

def show_rsvp_form():
    """Affiche le formulaire de RSVP"""
    st.markdown("""
    <div class="banner-container">
        <img src="https://raw.githubusercontent.com/hugotalentino/wedding-rsvp/main/banner.jpg">
        
        <div class="banner-text">
            <h1>Hugo & Sonate</h1>
            <p>3 Juillet 2027 • Château de Bois Charmant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding-top:1rem; padding-bottom:2rem;">
        <div class="title">Hugo & Sonate</div>
        <div style="
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.8rem;
            color:#8c6f75;
            margin-top:-10px;
        ">
            3 juillet 2027
        </div>
    </div>
    """, unsafe_allow_html=True)
    mariage = datetime(2027, 7, 3)
    today = datetime.now()

    jours_restants = (mariage - today).days

    st.markdown(f"""
    <div style="
        text-align:center;
        padding:1.5rem;
        margin-bottom:2rem;
        background: rgba(255,255,255,0.82);
        border-radius:20px;
        font-family:'Cormorant Garamond', serif;
        color:#7b6d6d;
        font-size:2rem;
    ">
    ⏳ Plus que <strong>{jours_restants}</strong> jours
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.90);
        padding: 2.5rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 35px rgba(0,0,0,0.08);
        text-align: center;
        line-height: 1.9;
        border: 1px solid rgba(176,141,87,0.15);
    ">

    <h2 style="
        font-family: Georgia, serif;
        color: #b08d57;
        font-size: 2.2rem;
        margin-bottom: 1.5rem;
        letter-spacing: 1px;
    ">
    À LIRE ATTENTIVEMENT
    </h2>

    <p style="
        font-size: 1.15rem;
        color: #444;
        margin-bottom: 1.5rem;
    ">
    Bienvenue à notre mariage 💍
    </p>

    <p style="
        font-size: 1.05rem;
        color: #555;
    ">
    Afin de préparer dans les meilleures conditions le plus beau jour de notre vie,
    nous avons besoin que vous répondiez à quelques questions 🌿
    </p>

    <div style="
        width: 80px;
        height: 2px;
        background: #d4b483;
        margin: 2rem auto;
    "></div>

    <p style="
        font-size: 1.1rem;
        color: #444;
    ">
    Votre présence sera notre plus beau cadeau ❤️
    </p>

    <p style="
        font-size: 1rem;
        color: #666;
    ">
    Quant aux grosses machines à café, services d’argenterie,
    lave-vaisselle et autres classiques du mariage…
    ils risqueraient malheureusement de ne pas survivre au voyage en avion ✈️
    </p>

    <p style="
        font-size: 1rem;
        color: #666;
    ">
    Si vous souhaitez tout de même nous gâter,
    une urne de participation financière sera présente sur le lieu de réception
    afin de contribuer à notre nouvelle aventure 🌿
    </p>

    </div>
    """, unsafe_allow_html=True)
    
    #st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    📍 Château de Bois Charmant, 15 Bois Charmant
    </div>

    <p style="color:#7b6d6d;">
    17380 Les Nouillers, France
    </p>
    """, unsafe_allow_html=True)

    st.components.v1.iframe(
        "https://maps.google.com/maps?q=Chateau%20de%20Bois%20Charmant%20Les%20Nouillers%20France&t=&z=13&ie=UTF8&iwloc=&output=embed",
        height=450
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("## 🌿 Vos coordonnées")
    
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
    dimanche = st.checkbox("Avant le vendredi")

    jours_selectionnes = []

    if vendredi:
        jours_selectionnes.append("Vendredi")

    if samedi:
        jours_selectionnes.append("Samedi")

    if dimanche:
        jours_selectionnes.append("Dimanche")
    
    if dimanche:
        jours_selectionnes.append("Avant le vendredi")

    st.markdown("---")
    st.markdown("## 🍽️ Allergies")

    allergie = st.text_area(
        "(Allergie aux parisiens, intolérance a l'architecture medievale, etc...)",
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
            ["Vendredi", "Samedi", "Autre"]
        )

        heure_arrivee = st.text_input(
            "Heure d'arrivée",
            placeholder="Ex : Jeudi 15h42"
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
        ["Non, un autre manoir m'attend", "Oui, au camping du chateau", "Oui, j'ai mon van", "Oui, les mariés m'on assigné une chambre/cabane"],
        horizontal=True
    )

    materiel_camping = ""

    if besoin_hebergement == "Oui, au camping du chateau":
        materiel_camping = st.text_area(
            "Matériel de camping qu'il te manquerait",
            placeholder="Ex: j'ai besoin d'une tente, matelas, sac de couchage..."
        )

    st.markdown("---")
    st.markdown("## 💬 Message")
    
    message = st.text_area(
        "Un petit mot pour les mariés ?",
        placeholder="Chanson à proposer, vœux, anecdote, blague..."
    )
    
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.88);
        backdrop-filter: blur(6px);
        padding: 2rem;
        border-radius: 24px;
        margin-top: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.4);
    ">

    <div style="
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        color: #b76e79;
        margin-bottom: 1rem;
    ">
        🌸 Dress code 🌸
    </div>

    <p style="
        font-size: 1.1rem;
        color: #5f5555;
        line-height: 1.8;
        font-family: 'Montserrat', sans-serif;
    ">

    Pour célébrer cette journée dans toute sa joie et sa lumière,  
    nous vous invitons à venir dans des tenues <strong>colorées, lumineuses et festives</strong>. 🌸🌿🌞

    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:1rem;">

    <span style="font-size:2rem;">🌸</span>
    <span style="font-size:2rem;">🌿</span>
    <span style="font-size:2rem;">🌞</span>
    <span style="font-size:2rem;">🧡</span>
    <span style="font-size:2rem;">💛</span>
    <span style="font-size:2rem;">🌺</span>

    </div>
    """, unsafe_allow_html=True)

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
                "allergie": allergie,
                "message": message,
                "date_reponse": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            save_response(data)
            send_confirmation_email(email, prenom, data)
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