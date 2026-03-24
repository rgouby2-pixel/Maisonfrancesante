import streamlit as st

st.set_page_config(page_title="La Maison France Santé", page_icon="🇫🇷", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .main { background-color: #f8fafc; }
    .report-box { padding: 20px; border-radius: 10px; border: 1px solid #ddd; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES MÉDICALE MASSIVE ---
# Cette base suit les recommandations de la HAS (Haute Autorité de Santé)
SITUATIONS_EXTENDED = {
    "Mal de gorge / Toux": {
        "questions": ["Fièvre > 38.5°C ?", "Difficulté à avaler / respirer ?", "Absence de toux ?", "Enfant de moins de 3 ans ?"],
        "logic": lambda q: "URGENCE" if q[1] else ("MEDECIN (Pédiatrie)" if q[3] else ("PHARMACIE (Test TROD)" if q[0] and q[2] else "PHARMACIE (Sirop/Conseil)"))
    },
    "Douleur Abdominale / Digestion": {
        "questions": ["Douleur intense en bas à droite ?", "Ventre dur comme du bois ?", "Sang dans les selles ?", "Impossibilité d'émettre des gaz ?"],
        "logic": lambda q: "URGENCE (Risque Chirurgical)" if any(q) else "PHARMACIE (Conseil Digestif / Gastro)"
    },
    "Infection Urinaire / Brûlures": {
        "questions": ["Douleur dans le bas du dos (reins) ?", "Fièvre ou frissons ?", "Sang dans les urines ?", "Êtes-vous enceinte ?"],
        "logic": lambda q: "URGENCE (Risque Pyélonéphrite)" if any(q) else "PHARMACIE (Protocole Cystite Direct)"
    },
    "Œil Rouge / Conjonctivite": {
        "questions": ["Baisse brutale de la vision ?", "Douleur oculaire intense ?", "Traumatisme ou choc sur l'oeil ?", "Sécrétions jaunes/collées ?"],
        "logic": lambda q: "URGENCE (Ophtalmo)" if q[0] or q[1] or q[2] else "PHARMACIE (Lavage / Antiseptique)"
    },
    "Douleur Dentaire": {
        "questions": ["Gonflement de la joue ou du cou ?", "Fièvre ?", "Difficulté à ouvrir la bouche ?", "Douleur suite à un choc ?"],
        "logic": lambda q: "URGENCE (Dentiste de garde)" if any(q[:3]) else "DENTISTE (RDV Classique)"
    },
    "Problème de Peau / Éruption": {
        "questions": ["Boutons qui ne blanchissent pas sous la pression ?", "Fièvre associée ?", "Démangeaisons insupportables ?", "Boutons suite à un nouveau médicament ?"],
        "logic": lambda q: "URGENCE (Risque Purpura)" if q[0] or q[1] else "PHARMACIE (Conseil Dermato)"
    },
    "Douleur Dos / Articulation": {
        "questions": ["Perte de sensibilité dans les jambes ?", "Incontinence soudaine ?", "Douleur suite à une chute ?", "Fourmillements persistants ?"],
        "logic": lambda q: "URGENCE (Risque Neurologique)" if q[0] or q[1] or q[3] else "MEDECIN / KINÉ"
    }
}

# --- APPLICATION ---
if 'step' not in st.session_state:
    st.session_state.step = "accueil"

if st.session_state.step == "accueil":
    st.title("🇫🇷 La Maison France Santé")
    st.write("### 1. Choisissez votre symptôme")
    
    choix = st.selectbox("Rechercher un motif...", ["Choisir..."] + list(SITUATIONS_EXTENDED.keys()) + ["Autre Urgence (Poitrine, Respiration...)"])
    
    if choix == "Autre Urgence (Poitrine, Respiration...)":
        st.error("🚨 APPEL IMMEDIAT AU 15")
    elif choix != "Choisir...":
        st.session_state.motif = choix
        st.session_state.step = "questions"
        st.rerun()

elif st.session_state.step == "questions":
    st.title(f"Analyse : {st.session_state.motif}")
    questions = SITUATIONS_EXTENDED[st.session_state.motif]["questions"]
    reponses = []
    
    st.write("#### Répondez avec précision :")
    for i, q in enumerate(questions):
        reponses.append(st.checkbox(q, key=f"q_{i}"))
    
    if st.button("CALCULER L'ORIENTATION"):
        st.session_state.resultat = SITUATIONS_EXTENDED[st.session_state.motif]["logic"](reponses)
        st.session_state.step = "resultat"
        st.rerun()

elif st.session_state.step == "resultat":
    res = st.session_state.resultat
    st.title("💡 Résultat de l'analyse")
    
    with st.container():
        st.markdown(f"<div class='report-box'><h3>{res}</h3></div>", unsafe_allow_html=True)
        
        if "URGENCE" in res:
            st.error("Contactez les secours. Ne prenez pas le volant.")
            st.button("📞 APPELER LE 15")
        elif "PHARMACIE" in res:
            st.success("Gain de temps : Votre pharmacien peut vous aider immédiatement.")
            st.link_button("📍 Trouver une pharmacie (Test/Conseil)", "https://www.google.com/maps/search/pharmacie")
        else:
            st.info("Prenez rendez-vous pour un examen complet.")
            st.link_button("📅 Prendre RDV sur Doctolib", "https://www.doctolib.fr")

    if st.button("🔄 Nouvelle analyse"):
        st.session_state.step = "accueil"
        st.rerun()
