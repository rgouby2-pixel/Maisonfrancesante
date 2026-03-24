import streamlit as st

# Configuration de l'affichage mobile
st.set_page_config(page_title="La Maison France Santé", page_icon="🇫🇷", layout="centered")

# Design aux couleurs de "La Maison France" (Bleu, Blanc, Rouge / Institutionnel)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 15px; height: 3.8em; font-weight: bold; font-size: 1.1em; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); border: 2px solid #0055a4; }
    div[data-testid="stMetricValue"] { color: #0055a4; }
    .main { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES MÉDICALE ENRICHIE ---
SITUATIONS = {
    "Mal de gorge / Toux": {
        "questions": ["Fièvre > 38.5°C ?", "Difficulté à avaler / respirer ?", "Ganglions gonflés dans le cou ?", "Absence de toux ?"],
        "aide": "Une angine bactérienne peut souvent être traitée directement via un test en pharmacie.",
        "logic": lambda q: "URGENCE" if q[1] else ("PHARMACIE (Test TROD)" if q[0] and q[3] else "MEDECIN (Auscultation)")
    },
    "Douleur Abdominale": {
        "questions": ["Douleur vive en bas à droite ?", "Ventre dur ou contracté ?", "Fièvre ou vomissements ?", "Douleur apparue brutalement ?"],
        "aide": "Attention aux signes d'appendicite ou d'occlusion.",
        "logic": lambda q: "URGENCE" if q[0] or q[1] or q[3] else "MEDECIN (Consultation digestive)"
    },
    "Infection Urinaire": {
        "questions": ["Brûlures persistantes ?", "Douleur dans le bas du dos (reins) ?", "Sang dans les urines ?", "Fièvre associée ?"],
        "aide": "Les pharmaciens peuvent désormais délivrer des antibiotiques pour les cystites simples sous protocole.",
        "logic": lambda q: "URGENCE" if q[1] or q[2] or q[3] else "PHARMACIE (Protocole Cystite)"
    },
    "Douleur Dos / Membres": {
        "questions": ["Suite à un choc violent ?", "Fourmillements / Perte de force ?", "Douleur qui bloque la marche ?", "Douleur qui réveille la nuit ?"],
        "aide": "Le triage permet de distinguer le lumbago simple de la hernie discale grave.",
        "logic": lambda q: "MEDECIN (Imagerie requise)" if q[0] or q[1] or q[3] else "PHARMACIE (Conseil Antalgique)"
    }
}

# --- LOGIQUE DE L'APPLICATION ---
if 'step' not in st.session_state:
    st.session_state.step = "accueil"

# ÉCRAN 1 : ACCUEIL & MOTIF
if st.session_state.step == "accueil":
    st.title("🇫🇷 La Maison France Santé")
    st.write("### Quel est le motif de votre analyse ?")
    
    choix = st.selectbox("Sélectionnez la zone concernée", ["Choisir..."] + list(SITUATIONS.keys()) + ["Autre / Urgence vitale"])
    
    if choix == "Autre / Urgence vitale":
        st.error("🚨 SI VOUS AVEZ UNE DOULEUR THORACIQUE OU DU MAL À RESPIRER :")
        st.button("📞 APPELER LE 15 IMMÉDIATEMENT", type="primary")
    elif choix != "Choisir...":
        st.session_state.motif = choix
        st.session_state.step = "questions"
        st.rerun()

# ÉCRAN 2 : QUESTIONNAIRE ADAPTATIF
elif st.session_state.step == "questions":
    st.title(f"Analyse : {st.session_state.motif}")
    st.info(SITUATIONS[st.session_state.motif]["aide"])
    
    questions = SITUATIONS[st.session_state.motif]["questions"]
    reponses = []
    
    st.write("#### Cochez les cases correspondantes :")
    for i, q in enumerate(questions):
        reponses.append(st.checkbox(q, key=f"q_{i}"))
    
    if st.button("OBTENIR L'ORIENTATION"):
        st.session_state.resultat = SITUATIONS[st.session_state.motif]["logic"](reponses)
        st.session_state.step = "resultat"
        st.rerun()

# ÉCRAN 3 : RÉSULTAT & BOUTONS BUSINESS
elif st.session_state.step == "resultat":
    res = st.session_state.resultat
    st.title("Résultat de l'analyse")
    
    if "URGENCE" in res:
        st.error(f"⚠️ {res}")
        st.write("Votre situation nécessite une prise en charge hospitalière immédiate.")
        st.button("📞 APPELER LE 15", type="primary")
    
    elif "PHARMACIE" in res:
        st.success(f"🏥 ORIENTATION : {res}")
        st.metric("Économie estimée pour la Sécu", "26,50 €")
        st.write("Le pharmacien peut traiter votre cas directement sans passer par un médecin.")
        st.link_button("📍 Trouver la pharmacie la plus proche", "https://www.google.com/maps/search/pharmacie")
    
    else:
        st.info(f"👨‍⚕️ ORIENTATION : {res}")
        st.write("Une consultation médicale est recommandée sous 48h.")
        st.link_button("📅 Prendre RDV sur Doctolib", "https://www.doctolib.fr")

    if st.button("🔄 Nouvelle analyse"):
        st.session_state.step = "accueil"
        st.rerun()
