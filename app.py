import streamlit as st

# Configuration de la page
st.set_page_config(page_title="La Maison France Santé PRO", page_icon="🇫🇷", layout="centered")

# --- CATALOGUE MÉDICAL EXPERT (Vérifié) ---
DATA_EXPERT = {
    "Cardio / Respiratoire": {
        "questions": ["Douleur dans la poitrine ?", "Essoufflement au repos ?", "Douleur qui va dans le bras ou la mâchoire ?"],
        "logic": lambda q: "URGENCE VITALE (15)" if any(q) else "MEDECIN (Bilan cardio)"
    },
    "Pédiatrie (Enfant)": {
        "questions": ["Fièvre > 39°C ?", "Taches rouges qui ne s'effacent pas sous le doigt ?", "Enfant mou ou grognon ?", "Refuse de boire ?"],
        "logic": lambda q: "URGENCE PÉDIATRIQUE" if q[1] or q[2] else "MEDECIN (Consultation 24h)"
    },
    "Gynécologie": {
        "questions": ["Saignements importants ?", "Douleur brutale et intense ?", "Possibilité de grossesse ?"],
        "logic": lambda q: "URGENCE GYNECO" if q[0] or q[1] else "MEDECIN / SAGE-FEMME"
    },
    "Santé Mentale": {
        "questions": ["Sentiment de détresse profonde ?", "Idées d'auto-suffisance ?", "Troubles du sommeil sévères ?"],
        "logic": lambda q: "APPEL 3114 (Prévention)" if q[1] else "CONSULTATION PSY / CMP"
    },
    "ORL / Gorge (Angine)": {
        "questions": ["Fièvre ?", "Difficulté à ouvrir la bouche ?", "Ganglions ?", "Absence de toux ?"],
        "logic": lambda q: "URGENCE" if q[1] else ("PHARMACIE (Test TROD)" if q[0] and q[3] else "REPOS / PHARMACIE")
    }
}

# --- INTERFACE UTILISATEUR ---
st.title("🇫🇷 La Maison France Santé")
st.subheader("Régulation Médicale Citoyenne")

# Initialisation de l'état de la session
if 'page' not in st.session_state:
    st.session_state.page = "home"

# ÉCRAN D'ACCUEIL
if st.session_state.page == "home":
    motif = st.selectbox("Quel est votre problème ?", ["Choisir..."] + list(DATA_EXPERT.keys()))
    if motif != "Choisir...":
        st.session_state.motif = motif
        st.session_state.page = "quiz"
        st.rerun()

# ÉCRAN DU QUESTIONNAIRE
elif st.session_state.page == "quiz":
    st.write(f"### Analyse : {st.session_state.motif}")
    qs = DATA_EXPERT[st.session_state.motif]["questions"]
    
    # Collecte des réponses
    reps = []
    for i, q in enumerate(qs):
        reps.append(st.checkbox(q, key=f"q_{i}"))
    
    if st.button("Valider l'analyse"):
        # Exécution de la fonction logic avec la liste des réponses
        st.session_state.res = DATA_EXPERT[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

# ÉCRAN DE RÉSULTAT
elif st.session_state.page == "fin":
    res = st.session_state.res
    st.write("### Résultat de l'analyse")
    
    if "URGENCE" in res or "15" in res or "3114" in res:
        st.error(f"🚨 {res}")
        st.write("Votre situation nécessite une prise en charge prioritaire.")
        st.button("📞 APPELER LES SECOURS")
    elif "PHARMACIE" in res:
        st.success(f"🏥 {res}")
        st
