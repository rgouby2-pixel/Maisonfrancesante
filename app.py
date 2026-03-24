import streamlit as st

# 1. Configuration de la page
st.set_page_config(page_title="Maison France Santé - Expert V3", page_icon="🇫🇷", layout="centered")

# 2. Style CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 10px; border: 2px solid #0055a4; background-color: white; margin-bottom: 20px; }
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Fonctions Logiques (Séparées pour la clarté)
def logic_traumato(q):
    return "🚨 URGENCE TRAUMATO (Radio/15)" if any(q) else "🏥 PHARMACIE (Protocole RICE: Repos, Glace, Compression)"

def logic_abdo(q):
    if q[0] or q[1] or q[4]:
        return "🚨 URGENCE CHIRURGICALE (15)"
    elif q[2] or q[3]:
        return "👨‍⚕️ MEDECIN (Risque déshydratation)"
    return "🏥 PHARMACIE (Conseil Digestif)"

def logic_urinaire(q):
    return "🚨 URGENCE (Risque Pyélonéphrite)" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Protocole Cystite)"

def logic_orl(q):
    if q[0] or q[1] or q[3]:
        return "🚨 URGENCE RESPIRATOIRE (15)"
    elif q[2]:
        return "🏥 PHARMACIE (Test TROD Angine)"
    return "💊 PHARMACIE (Symptomatique)"

def logic_neuro(q):
    return "🚨 URGENCE NEURO (Risque AVC/Moelle)" if any(q) else "👨‍⚕️ MEDECIN / KINÉ"

DATA_SERIEUX = {
    "Traumatologie (Choc, Chute)": {
        "q": ["Membre déformé ?", "Impossible de faire 4 pas ?", "Douleur osseuse précise ?", "Membre bleu/froid ?"],
        "logic": logic_traumato
    },
    "Abdominale (Ventre)": {
        "q": ["Douleur brutale ?", "Ventre dur ?", "Vomissements répétés ?", "Sang dans les selles ?", "Arrêt des gaz/selles ?"],
        "logic": logic_abdo
    },
    "Infection Urinaire": {
        "q": ["Fièvre/Frissons ?", "Douleur au dos/reins ?", "Sang dans les urines ?", "Brûlures simples ?"],
        "logic": logic_urinaire
    },
    "ORL & Respiratoire": {
        "q": ["Mal à respirer ?", "Sifflement ?", "Fièvre + Absence de toux ?", "Salive impossible à avaler ?"],
        "logic": logic_orl
    },
    "Neurologie & Dos": {
        "q": ["Perte de force/sensibilité ?", "Incontinence soudaine ?", "Maux de tête foudroyants ?", "Chute sur le dos ?"],
        "logic": logic_neuro
    },
    # --- NOUVEAUX MOTIFS AJOUTÉS ---
    "Ophtalmologie (Œil)": {
        "q": ["Baisse brutale de vision ?", "Douleur oculaire vive ?", "Choc direct sur l'œil ?", "Œil rouge et collé ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Nettoyage/Collyre)"
    },
    "Dentaire": {
        "q": ["Joue gonflée ?", "Fièvre ?", "Difficulté à ouvrir la bouche ?", "Douleur persistante ?"],
        "logic": lambda q: "🚨 URGENCE DENTAIRE (Garde)" if q[0] or q[1] or q[2] else "🦷 DENTISTE (RDV Classique)"
    },
    "Dermatologie (Peau)": {
        "q": ["Fièvre + Éruption ?", "Taches rouges persistantes (purpura) ?", "Démangeaisons intenses ?", "Brûlure étendue ?"],
        "logic": lambda q: "🚨 URGENCE DERMATO" if q[0] or q[1] else "🏥 PHARMACIE (Conseil/Crème)"
    },
    "Pédiatrie (Enfant)": {
        "q": ["Enfant mou/prostré ?", "Refuse de boire ?", "Fièvre > 39°C persistante ?", "Cris inconsolables ?"],
        "logic": lambda q: "🚨 URGENCE PÉDIATRIQUE" if q[0] or q[1] or q[2] else "👨‍⚕️ PÉDIATRE (Sous 24h)"
    },
    "Santé Mentale": {
        "q": ["Idées noires/Mise en danger ?", "Crise d'angoisse aiguë ?", "Insomnie totale (48h+) ?"],
        "logic": lambda q: "📞 APPEL 3114 (Urgence Psy)" if q[0] else "👨‍⚕️ CONSULTATION (CMP/Psy)"
    }
}
# --- ÉCRAN 1 : ACCUEIL ---
if st.session_state.page == "home":
    st.write("### 1. Quel est votre motif de consultation ?")
    choix = st.selectbox("Sélectionnez une catégorie", ["Choisir..."] + list(DATA_SERIEUX.keys()))
    
    if st.button("Continuer", key="btn_home"):
        if choix != "Choisir...":
            st.session_state.motif = choix
            st.session_state.page = "quiz"
            st.rerun()
        else:
            st.warning("Veuillez sélectionner une catégorie.")

# --- ÉCRAN 2 : QUIZ ---
elif st.session_state.page == "quiz":
    st.write(f"### 2. Analyse : {st.session_state.motif}")
    questions = DATA_SERIEUX[st.session_state.motif]["q"]
    
    reponses = []
    for i, q in enumerate(questions):
        reponses.append(st.checkbox(q, key=f"check_{i}"))
    
    if st.button("Calculer l'orientation"):
        # On passe la liste de booléens à la fonction logique correspondante
        resultat = DATA_SERIEUX[st.session_state.motif]["logic"](reponses)
        st.session_state.res = resultat
        st.session_state.page = "fin"
        st.rerun()
    
    if st.button("Retour"):
        st.session_state.page = "home"
        st.rerun()

# --- ÉCRAN 3 : RÉSULTAT ---
elif st.session_state.page == "fin":
    st.write("### 3. Résultat & Orientation")
    st.markdown(f"<div class='report-box'><h2>{st.session_state.res}</h2></div>", unsafe_allow_html=True)
    
    if "🚨" in st.session_state.res:
        st.error("DANGER : Contactez immédiatement le 15.")
        st.button("📞 APPELER LE 15")
    elif "🏥 PHARMACIE" in st.session_state.res:
        st.success("Orientation : Circuit Court (Officine)")
        st.info("💡 Économie Sécu : 26,50 €")
        st.link_button("📍 Trouver une pharmacie", "https://www.google.com/maps/search/pharmacie")
    else:
        st.info("Une consultation est recommandée.")
        st.link_button("📅 Prendre RDV Doctolib", "https://www.doctolib.fr")
    
    if st.button("Nouvelle analyse"):
        st.session_state.page = "home"
        st.session_state.motif = None
        st.session_state.res = None
        st.rerun()
