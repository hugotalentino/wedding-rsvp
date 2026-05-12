# 💍 Wedding RSVP - Application de gestion des invités

Une application élégante pour gérer les confirmations de présence à votre mariage.

## ✨ Fonctionnalités

- **QR Code automatique** - Générez un QR code à scanner pour accéder au formulaire
- **Formulaire complet** - Vos invités peuvent indiquer :
  - Leur présence
  - Le nombre de personnes
  - Restrictions alimentaires (végétarien, végan, sans gluten, autres)
  - Mode de transport
  - Besoin d'hébergement
- **Dashboard Admin** - Visualisez en temps réel :
  - Nombre de présents/absents
  - Graphiques des restrictions alimentaires
  - Statistiques de transport
  - Besoins d'hébergement
  - Messages des invités
  - Export CSV

## 🚀 Installation

```bash
cd wedding-rsvp
pip install -r requirements.txt
```

## 🎯 Utilisation

### Lancement local
```bash
streamlit run app.py
```

L'application sera accessible à `http://localhost:8501`

### Déploiement (pour rendre le QR code accessible)

**Option 1 - Streamlit Cloud (Gratuit)**
1. Poussez le code sur GitHub
2. Connectez votre repo sur [streamlit.io](https://streamlit.io)
3. Votre app sera en ligne avec une URL

**Option 2 - Heroku**
```bash
heroku create mon-mariage-rsvp
git push heroku main
```

## 📱 QR Code

Le QR code pointe vers l'URL de votre application déployée.
Dans le fichier `app.py`, modifiez cette ligne :

```python
url = "http://localhost:8501"  # Remplacez par votre URL de production
```

## 📋 Structure

```
wedding-rsvp/
├── app.py              # Application principale
├── requirements.txt    # Dépendances
├── responses.csv       # Données des invités (créé automatiquement)
└── README.md          # Ce fichier
```

## 🎨 Personnalisation

Modifiez les constantes dans `app.py` :
- `DATA_FILE` - Nom du fichier de données
- Dates et lieu du mariage
- Noms des mariés

## 📊 Dashboard

Accédez au dashboard via le menu latéral pour voir :
- Statistiques en temps réel
- Graphiques interactifs
- Liste filtrable des invités
- Export des données