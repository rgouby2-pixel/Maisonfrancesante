import streamlit as st

# Configuration de la page pour mobile
st.set_page_config(page_title="La Maison France Santé", page_icon="🇫🇷")

# Style CSS pour que ça ressemble à une vraie App iOS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .emergency { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🇫🇷 La Maison France Santé")
st.subheader("Votre assistant d'orientation médicale")

# Initialisation du questionnaire
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.symptomes = []

# ÉTAPE 1 : Choix du symptôme principal
if st.session_state.step == 1:
    st.write("### Quel est votre symptôme principal ?")
    option = st.selectbox("Sélectionnez...", ["Choisir", "Mal de gorge", "Douleur abdominale", "Difficulté à respirer"])
    
    if option != "Choisir":
        if option == "Difficulté à respirer":
            st.error("⚠️ URGENCE : Appelez immédiatement le 15.")
            st.button("📞 APPELER LE 15", on_click=None)
        else:
            st.session_state.symptome_principal = option
            st.session_state.step = 2
            st.rerun()

# ÉTAPE 2 : Questions dynamiques
elif st.session_state.step == 2:
    st.write(f"### Analyse : {st.session_state.symptome_principal}")
    fievre = st.radio("Avez-vous de la fièvre (>38°C) ?", ["Non", "Oui"])
    duree = st.slider("Depuis combien de jours ?", 1, 10, 1)

    if st.button("Valider l'analyse"):
        st.session_state.fievre = fievre
        st.session_state.duree = duree
        st.session_state.step = 3
        st.rerun()

# ÉTAPE 3 : Résultat et Boutons Business
elif st.session_state.step == 3:
    st.success("✅ Analyse terminée")
    
    if st.session_state.symptome_principal == "Mal de gorge" and st.session_state.fievre == "Oui":
        st.warning("🩺 **Diagnostic probable : Angine**")
        st.write("Le protocole HAS recommande un test en pharmacie.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🏥 Trouver une Pharmacie", "https://www.google.com/maps/search/pharmacie")
        with col2:
            st.link_button("👨‍⚕️ RDV Doctolib", "https://www.doctolib.fr")
            
    else:
        st.write("### Orientation : Médecine Générale")
        st.link_button("📅 Prendre RDV (Doctolib)", "https://www.doctolib.fr")

    if st.button("Recommencer"):
        st.session_state.step = 1
        st.rerun()
