import streamlit as st

# 1. Configuration et Style
st.set_page_config(page_title="La Maison France Santé", page_icon="🇫🇷")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .report-box { padding: 15px; border-radius: 10px; border: 1px solid #0055a4; background-color: #f0f4f8; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Données Médicale (Vérifiée sans erreurs de syntaxe)
DATA = {
    "Cardio / Respiratoire": {
        "q": ["Douleur/Oppression poitrine ?", "Essoufflement brutal ?", "Douleur bras ou mâchoire ?"],
        "logic": lambda q: "🚨 URGENCE VITALE (15)" if any(q) else "👨‍⚕️ MEDECIN (Bilan)"
    },
    "Mal de gorge / Toux": {
        "q": ["Fièvre > 38.5°C ?", "Difficulté à respirer ?", "Absence de toux ?", "Ganglions gonflés ?"],
        "logic": lambda q: "🚨 URGENCE (Respiratoire)" if q[1] else ("🏥 PHARMACIE (Test TROD)" if q[0] and q[2] else "💊 PHARMACIE (Conseil)")
    },
    "Douleur Abdominale": {
        "q": ["Douleur bas-droite ?", "Ventre dur ?", "Sang dans les selles ?", "Pas de gaz/selles ?"],
        "logic": lambda q: "🚨 URGENCE CHIRURGICALE" if any(q) else "👨‍⚕️ MEDECIN (Avis digestif)"
    },
    "Infection Urinaire": {
        "q": ["Douleur bas du dos ?", "Fièvre / Frissons ?", "Sang dans les urines ?"],
        "logic": lambda q: "🚨 URGENCE (Reins)" if any(q) else "🏥 PHARMACIE (Protocole Cystite)"
    },
    "Pédiatrie (Enfant)": {
        "q": ["Enfant prostré ?", "Taches rouges sur la peau ?", "Refuse de boire ?"],
        "logic": lambda q: "🚨 URGENCE PÉDIATRIQUE" if any(q) else "👨‍⚕️ PÉDIATRE (24h)"
    },
    "Ophtalmologie (Œil)": {
        "q": ["Baisse de vision ?", "Douleur intense ?", "Choc sur l'oeil ?", "Œil rouge/collé ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Lavage)"
    },
    "Dermatologie (Peau)": {
        "q": ["Fièvre + Boutons ?", "Extension très rapide ?", "Démangeaisons intenses ?"],
        "logic": lambda q: "👨‍⚕️ MEDECIN (Diagnostic)" if q[0] or q[1] else "🏥 PHARMACIE (Apaisement)"
    },
    "Dentaire": {
        "q": ["Joue gonflée ?", "Fièvre ?", "Difficulté à ouvrir la bouche ?"],
        "logic": lambda q: "🚨 URGENCE (Garde)" if any(q) else "🦷 DENTISTE (RDV)"
    },
    "Santé Mentale": {
        "q": ["Idées noires ?", "Détresse profonde ?", "Insomnie totale ?"],
        "logic": lambda q: "📞 APPEL 3114 (Suicide)" if q[0] else "👨‍⚕️ PSY / CMP"
    }
}

# 3. Logique de l'Interface
if 'page' not in st.session_state: st.session_state.page = "home"

st.title("🇫🇷 La Maison France Santé")

if st.session_state.page == "home":
    st.write("### 1. Choisissez votre motif")
    choix = st.selectbox("Rechercher...", ["Choisir..."] + list(DATA.keys()) + ["AUTRE URGENCE"])
    
    if choix == "AUTRE URGENCE":
        st.error("🚨 APPEL 15 IMMEDIAT")
    elif choix != "Choisir...":
        st.session_state.motif = choix
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### 2. Analyse : {st.session_state.motif}")
    qs = DATA[st.session_state.motif]["q"]
    reps = [st.checkbox(q, key=f"q_{i}") for i, q in enumerate(qs)]
    
    if st.button("CALCULER L'ORIENTATION"):
        st.session_state.res = DATA[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    st.write("### 3. Résultat & Orientation")
    st.markdown(f"<div class='report-box'><h2>{st.session_state.res}</h2></div>", unsafe_allow_html=True)
    
    if "URGENCE" in st.session_state.res or "15" in st.session_state.res:
        st.error("Ne prenez pas le volant. Appelez les secours.")
        st.button("📞 APPELER LE 15")
    elif "PHARMACIE" in st.session_state.res:
        st.success("Circuit Court : Pharmacie")
        st.info("💡 Économie Sécu : 26,50€")
        st.link_button("📍 Trouver l'officine la plus proche", "https://www.google.com/maps/search/pharmacie")
    else:
        st.info("Consultation requise.")
        st.link_button("📅 RDV Doctolib", "https://www.doctolib.fr")

    if st.button("🔄 Nouvelle analyse"):
        st.session_state.page = "home"
        st.rerun()
