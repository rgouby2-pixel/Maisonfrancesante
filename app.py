import streamlit as st

# 1. INITIALISATION DE SÉCURITÉ (Doit être au tout début)
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'motif' not in st.session_state:
    st.session_state.motif = None
if 'res' not in st.session_state:
    st.session_state.res = None

# 2. Configuration
st.set_page_config(page_title="Maison France Santé - Expert", page_icon="🇫🇷")

# 3. Style CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 10px; border: 2px solid #0055a4; background-color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 4. Fonctions Logiques de Triage
def logic_standard(q): return "🚨 URGENCE (15)" if any(q) else "👨‍⚕️ MEDECIN (Consultation)"
def logic_traumato(q): return "🚨 URGENCE TRAUMATO (Radio/15)" if any(q) else "🏥 PHARMACIE (Protocole RICE)"
def logic_abdo(q):
    if q[0] or q[1] or q[4]: return "🚨 URGENCE CHIRURGICALE (15)"
    elif q[2] or q[3]: return "👨‍⚕️ MEDECIN (Risque déshydratation)"
    return "🏥 PHARMACIE (Conseil Digestif)"

# 5. MATRICE MÉDICALE (10 PATHOLOGIES)
DATA_SERIEUX = {
    "Traumatologie (Choc, Chute)": {
        "q": ["Membre déformé ?", "Impossible de faire 4 pas ?", "Douleur osseuse précise ?", "Membre bleu/froid ?"],
        "logic": logic_traumato
    },
    "Abdominale (Ventre)": {
        "q": ["Douleur brutale ?", "Ventre dur ?", "Vomissements répétés ?", "Diarrhée avec sang ?", "Arrêt des gaz/selles ?"],
        "logic": logic_abdo
    },
    "Infection Urinaire": {
        "q": ["Fièvre/Frissons ?", "Douleur au dos/reins ?", "Sang dans les urines ?", "Brûlures simples ?"],
        "logic": lambda q: "🚨 URGENCE (Reins)" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Cystite)"
    },
    "ORL & Respiratoire": {
        "q": ["Mal à respirer ?", "Sifflement ?", "Fièvre + Absence de toux ?", "Salive impossible à avaler ?"],
        "logic": lambda q: "🚨 URGENCE (15)" if q[0] or q[1] or q[3] else ("🏥 PHARMACIE (Test TROD)" if q[2] else "💊 PHARMACIE")
    },
    "Neurologie & Dos": {
        "q": ["Perte de force/sensibilité ?", "Incontinence soudaine ?", "Maux de tête foudroyants ?", "Chute sur le dos ?"],
        "logic": lambda q: "🚨 URGENCE NEURO" if any(q) else "👨‍⚕️ MEDECIN / KINÉ"
    },
    "Ophtalmologie (Œil)": {
        "q": ["Baisse de vision ?", "Douleur vive ?", "Choc direct ?", "Œil rouge et collé ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Lavage)"
    },
    "Dentaire": {
        "q": ["Joue gonflée ?", "Fièvre ?", "Difficulté à ouvrir la bouche ?", "Douleur persistante ?"],
        "logic": lambda q: "🚨 URGENCE DENTAIRE" if q[0] or q[1] or q[2] else "🦷 DENTISTE"
    },
    "Dermatologie (Peau)": {
        "q": ["Fièvre + Éruption ?", "Taches rouges (purpura) ?", "Démangeaisons intenses ?"],
        "logic": lambda q: "🚨 URGENCE DERMATO" if q[0] or q[1] else "🏥 PHARMACIE (Conseil)"
    },
    "Pédiatrie (Enfant)": {
        "q": ["Enfant mou/prostré ?", "Refuse de boire ?", "Fièvre > 39°C ?", "Taches sur la peau ?"],
        "logic": lambda q: "🚨 URGENCE PÉDIATRIQUE" if any(q) else "👨‍⚕️ PÉDIATRE"
    },
    "Santé Mentale": {
        "q": ["Idées noires/Mise en danger ?", "Crise d'angoisse ?", "Insomnie totale ?"],
        "logic": lambda q: "📞 APPEL 3114 (Urgence)" if q[0] else "👨‍⚕️ CONSULTATION"
    }
}

st.title("🇫🇷 La Maison France Santé")
st.caption("Système Expert d'Aiguillage National")

# NAVIGATION
if st.session_state.page == "home":
    st.write("### 1. Quel est votre motif ?")
    choix = st.selectbox("Choisir...", ["Choisir..."] + list(DATA_SERIEUX.keys()))
    if st.button("Continuer"):
        if choix != "Choisir...":
            st.session_state.motif = choix
            st.session_state.page = "quiz"
            st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### 2. Analyse : {st.session_state.motif}")
    qs = DATA_SERIEUX[st.session_state.motif]["q"]
    reps = [st.checkbox(q, key=f"c_{i}") for i, q in enumerate(qs)]
    
    if st.button("Calculer"):
        st.session_state.res = DATA_SERIEUX[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    st.write("### 3. Orientation")
    st.markdown(f"<div class='report-box'><h2>{st.session_state.res}</h2></div>", unsafe_allow_html=True)
    
    if "🚨" in st.session_state.res or "3114" in st.session_state.res:
        st.error("DANGER : Contactez le 15 immédiatement.")
    elif "PHARMACIE" in st.session_state.res:
        st.success("Orientation : Circuit Court (Officine)")
        st.link_button("📍 Trouver une pharmacie", "https://www.google.com/maps/search/pharmacie")
    
    if st.button("Nouvelle analyse"):
        st.session_state.page = "home"
        st.rerun()
