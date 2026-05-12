"""
Wedding RSVP Application
Un QR code élégant qui renvoie vers un formulaire de confirmation de présence.
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


def load_responses():
    """Charge les réponses depuis le fichier CSV"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        "nom", "prenom", "email", "presence", "nb_personnes",
        "vegetarien", "vegan", "sans_gluten", "autres_regimes",
        "transport", "besoin_hebergement", "nb_chambres",
        "message", "date_reponse"
    ])


def save_response(data):
    """Sauvegarde une nouvelle réponse"""
    df = load_responses()
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return df


def generate_qr_code(url):
    """Génère un QR code à partir d'une URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#2c3e50", back_color="white")
    
    # Convertir en bytes pour Streamlit
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


def show_rsvp_form():
    """Affiche le formulaire de RSVP"""
    st.markdown('<p class="title">💍 Hugo & Sonate</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Nous nous marions !</p>', unsafe_allow_html=True)
    
    st.markdown("### 📅 3 Juillet 2027")
    st.markdown("### 📍 Château de bois Charmant")
    st.markdown("---")
    
    with st.form("rsvp_form", clear_on_submit=True):
        st.markdown("## ✨ Vos coordonnées")
        
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom *", placeholder="Votre nom")
        with col2:
            prenom = st.text_input("Prénom *", placeholder="Votre prénom")
        
        email = st.text_input("Email *", placeholder="votre@email.com")
        
        st.markdown("---")
        st.markdown("## 🎉 Votre présence")
        
        presence = st.radio(
            "Seriez-vous présent(e) à notre mariage ? *",
            ["Oui, avec plaisir !", "Non, je ne pourrai pas venir"],
            horizontal=True
        )
        
        nb_personnes = 1
        if presence == "Oui, avec plaisir !":
            nb_personnes = st.number_input(
                "Nombre de personnes (vous incluse)",
                min_value=1, max_value=5, value=1
            )
        
        st.markdown("---")
        st.markdown("## 🍽️ Restrictions alimentaires")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            vegetarien = st.checkbox("Végétarien")
        with col2:
            vegan = st.checkbox("Végan")
        with col3:
            sans_gluten = st.checkbox("Sans gluten")
        
        autres_regimes = st.text_area(
            "Autres restrictions (allergies, intolérances, etc.)",
            placeholder="Précisez si nécessaire..."
        )
        
        st.markdown("---")
        st.markdown("## 🚗 Logistique")
        
        transport = st.selectbox(
            "Comment viendrez-vous ?",
            ["Voiture", "Train", "Covoiturage", "Autre"]
        )
        
        besoin_hebergement = st.radio(
            "Avez-vous besoin d'un hébergement ?",
            ["Non, je rentre chez moi", "Oui, j'ai besoin d'hébergement"],
            horizontal=True
        )
        
        nb_chambres = 0
        if besoin_hebergement == "Oui, j'ai besoin d'hébergement":
            nb_chambres = st.number_input(
                "Nombre de chambres nécessaires",
                min_value=1, max_value=3, value=1
            )
        
        st.markdown("---")
        st.markdown("## 💬 Message")
        
        message = st.text_area(
            "Un petit mot pour les mariés ?",
            placeholder="Félicitations, vœux, anecdote..."
        )
        
        submitted = st.form_submit_button("💌 Envoyer ma réponse", type="primary")
        
        if submitted:
            if not nom or not prenom or not email:
                st.error("Merci de remplir tous les champs obligatoires (*)")
            else:
                data = {
                    "nom": nom,
                    "prenom": prenom,
                    "email": email,
                    "presence": presence,
                    "nb_personnes": nb_personnes,
                    "vegetarien": vegetarien,
                    "vegan": vegan,
                    "sans_gluten": sans_gluten,
                    "autres_regimes": autres_regimes,
                    "transport": transport,
                    "besoin_hebergement": besoin_hebergement,
                    "nb_chambres": nb_chambres,
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


def show_qr_code():
    """Affiche le QR code seul"""
    st.markdown('<p class="title">💍 Scannez pour répondre</p>', unsafe_allow_html=True)
    
    # URL à personnaliser - mettre l'URL de déploiement
    url = "http://localhost:8501"
    
    qr_buffer = generate_qr_code(url)
    
    st.markdown('<div class="qr-container">', unsafe_allow_html=True)
    st.image(qr_buffer, caption="Scannez ce QR code pour confirmer votre présence", width=300)
    st.markdown(f"<p style='color: #7f8c8d; margin-top: 1rem;'>Ou cliquez ici: <a href='{url}'>{url}</a></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_dashboard():
    """Affiche le dashboard administrateur"""
    st.set_page_config(page_title="Dashboard Mariage", layout="wide")
    
    st.markdown("""
    <style>
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# 💍 Dashboard - Mariage Hugo & Sonate")
    st.markdown("---")
    
    df = load_responses()
    
    if df.empty:
        st.info("Aucune réponse pour le moment. Partagez le QR code !")
        return
    
    # Statistiques principales
    total_invites = len(df)
    presents = df[df['presence'].str.contains('Oui', na=False)]
    absents = df[df['presence'].str.contains('Non', na=False)]
    total_personnes = presents['nb_personnes'].sum() if not presents.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total réponses", total_invites)
    with col2:
        st.metric("Présents", len(presents))
    with col3:
        st.metric("Absents", len(absents))
    with col4:
        st.metric("Total personnes", total_personnes)
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🍽️ Restrictions alimentaires")
        if not presents.empty:
            restrictions_data = {
                'Type': ['Végétariens', 'Végan', 'Sans gluten'],
                'Nombre': [
                    presents['vegetarien'].sum(),
                    presents['vegan'].sum(),
                    presents['sans_gluten'].sum()
                ]
            }
            fig_restrictions = px.bar(
                restrictions_data, 
                x='Type', 
                y='Nombre',
                color='Type',
                color_discrete_sequence=['#2ecc71', '#27ae60', '#f39c12']
            )
            st.plotly_chart(fig_restrictions, use_container_width=True)
    
    with col2:
        st.subheader("🚗 Mode de transport")
        if not df.empty:
            transport_counts = df['transport'].value_counts()
            fig_transport = px.pie(
                values=transport_counts.values,
                names=transport_counts.index,
                title="Comment viennent-ils ?",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_transport, use_container_width=True)
    
    st.markdown("---")
    
    # Hébergement
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛏️ Besoins d'hébergement")
        if not presents.empty:
            hebergement = presents['besoin_hebergement'].value_counts()
            fig_heberg = px.pie(
                values=hebergement.values,
                names=hebergement.index,
                color_discrete_sequence=['#3498db', '#e74c3c']
            )
            st.plotly_chart(fig_heberg, use_container_width=True)
    
    with col2:
        st.subheader("🛏️ Chambres nécessaires")
        if not presents.empty:
            chambres = presents[presents['besoin_hebergement'].str.contains('Oui', na=False)]['nb_chambres'].sum()
            st.metric("Chambres totales", chambres)
    
    st.markdown("---")
    
    # Liste des invités
    st.subheader("📋 Liste des invités")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        filter_presence = st.selectbox("Filtrer par présence", ["Tous", "Présents", "Absents"])
    with col2:
        filter_heberg = st.selectbox("Filtrer par hébergement", ["Tous", "Avec hébergement", "Sans hébergement"])
    
    filtered_df = df.copy()
    if filter_presence == "Présents":
        filtered_df = filtered_df[filtered_df['presence'].str.contains('Oui', na=False)]
    elif filter_presence == "Absents":
        filtered_df = filtered_df[filtered_df['presence'].str.contains('Non', na=False)]
    
    if filter_heberg == "Avec hébergement":
        filtered_df = filtered_df[filtered_df['besoin_hebergement'].str.contains('Oui', na=False)]
    elif filter_heberg == "Sans hébergement":
        filtered_df = filtered_df[filtered_df['besoin_hebergement'].str.contains('Non', na=False)]
    
    st.dataframe(
        filtered_df[['nom', 'prenom', 'email', 'presence', 'nb_personnes', 'besoin_hebergement', 'date_reponse']],
        use_container_width=True
    )
    
    # Messages
    messages = df[df['message'].notna() & (df['message'] != '')]
    if not messages.empty:
        st.markdown("---")
        st.subheader("💬 Messages des invités")
        for _, msg in messages.iterrows():
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                <strong>{msg['prenom']} {msg['nom']}</strong> - {msg['date_reponse']}<br>
                <em>"{msg['message']}"</em>
            </div>
            """, unsafe_allow_html=True)
    
    # Export
    st.markdown("---")
    st.subheader("📥 Export")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Télécharger les réponses (CSV)",
        csv,
        "invites_mariage.csv",
        "text/csv"
    )


def main():
    """Point d'entrée principal"""
    # Menu de navigation
    menu = st.sidebar
    menu.title("💍 Menu")
    
    choix = menu.radio(
        "Navigation",
        ["Formulaire RSVP", "QR Code", "Dashboard Admin"]
    )
    
    if choix == "Formulaire RSVP":
        show_rsvp_form()
    elif choix == "QR Code":
        show_qr_code()
    elif choix == "Dashboard Admin":
        show_dashboard()


if __name__ == "__main__":
    main()