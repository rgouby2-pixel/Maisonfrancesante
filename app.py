import streamlit as st

st.set_page_config(page_title="La Maison France Santé - Expert", page_icon="🇫🇷", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .main { background-color: #f8fafc; }
    .report-box { padding: 20px; border-radius: 10px; border: 1px solid #ddd; background-color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES MÉDICALE INTÉGRALE ---
DATA_COMPLET = {
    "Cardio / Respiratoire": {
        "questions": ["Douleur/Oppression dans la poitrine ?", "Essoufflement brutal au repos ?", "Douleur irradiant mâchoire ou bras gauche ?"],
        "logic": lambda q: "🚨 URGENCE VITALE (15)" if any(q) else "👨‍⚕️ MEDECIN (Bilan cardiaque)"
    },
    "Mal de gorge / Toux": {
        "questions": ["Fièvre > 38.5°C ?", "Difficulté à avaler / respirer ?", "Absence totale de toux ?", "Ganglions gonflés ?"],
        "logic": lambda q: "🚨 URGENCE (Risque respiratoire)" if q[1] else ("🏥 PHARMACIE (Test TROD Angine)" if q[0] and q[2] else "💊 PHARMACIE (Conseil/Sirop)")
    },
    "Douleur Abdominale": {
        "questions": ["Douleur intense en bas à droite ?", "Ventre dur / contracté ?", "Impossibilité d'émettre des gaz / selles ?", "Sang dans les selles ?"],
        "logic": lambda q: "🚨 URGENCE CHIRURGICALE" if any(q) else "👨‍⚕️ MEDECIN (Avis digestif)"
    },
    "Infection Urinaire": {
        "questions": ["Douleur dans le bas du dos / Reins ?", "Fièvre ou frissons ?", "Sang dans les urines ?", "Brûlures persistantes ?"],
        "logic": lambda q: "🚨 URGENCE (Risque Pyélonéphrite)" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Protocole Cystite)"
    },
    "Pédiatrie (Enfant)": {
        "questions": ["Enfant geignant ou prostré ?", "Taches rouges ne s'effaçant pas à la pression ?", "Refuse de boire / Signes de déshydratation ?"],
        "logic": lambda q: "🚨 URGENCE PÉDIATRIQUE" if any(q) else "👨‍⚕️ PÉDIATRE (Sous 24h)"
    },
    "Ophtalmologie (Œil)": {
        "questions": ["Baisse brutale de la vision ?", "Douleur oculaire intense ?", "Choc ou corps étranger ?", "Œil rouge et collé le matin ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Lavage/Antiseptique)"
    },
    "Dermatologie (Peau)": {
        "questions": ["Fièvre associée à l'éruption ?", "Boutons qui s'étendent très vite ?", "Démangeaisons insupportables ?"],
        "logic": lambda q: "👨‍⚕️ MEDECIN (Diagnostic requis)" if q[0] or q[1] else "🏥 PHARMACIE (Crème apaisante)"
    },
    "Dentaire": {
        "questions": ["Gonflement de la joue ?", "Fièvre ?", "Difficulté à ouvrir la bouche ?"],
        "logic": lambda q: "🚨 URGENCE (Dentiste de garde)" if any(q) else "🦷 DENTISTE (RDV classique)"
    },
    "Santé Mentale": {
        "questions": ["Idées noires ou mise en danger ?", "Détresse psychologique profonde ?", "Insomnie totale depuis plusieurs jours ?"],
        "logic": lambda q: "📞 APPEL 3114 (Prévention Suicide)" if q[0] else "👨‍⚕️ PSYCHOLOGUE / CMP"
    }
}

# --- APPLICATION LOGIC ---
if 'page' not in st.session_state: st.session_state.page = "home"

if st.session_state.page == "home":
    st.title("🇫🇷 La Maison France Santé")
    st.write("### 1. Quel est votre motif ?")
    choix = st.selectbox("Rechercher une pathologie...", ["Choisir..."] + list(DATA_COMPLET.keys()) + ["AUTRE URGENCE"])
    
    if choix == "AUTRE URGENCE":
        st.error("🚨 APPEL IMMÉDIAT AU 15")
    elif choix != "Choisir...":
        st.session_state.motif = choix
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.title(f"Analyse : {st.session_state.motif}")
    qs = DATA_COMPLET[st.session_state.motif]["questions"]
    reps = []
    for i, q in enumerate(qs):
        reps.append(st.checkbox(q, key=f"q_{i}"))
    
    if st.button("CALCULER L'ORIENTATION"):
        st.session_state.res = DATA_COMPLET[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    res = st.session_state.res
