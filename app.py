import streamlit as st

st.set_page_config(page_title="Maison France Santé PRO", page_icon="🇫🇷")

# --- CATALOGUE MÉDICAL EXPERT ---
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

if 'page' not in st.session_state: st.session_state.page = "home"

if st.session_state.page == "home":
    motif = st.selectbox("Quel est votre problème ?", ["Choisir..."] + list(DATA_EXPERT.keys()))
    if motif != "Choisir...":
        st.session_state.motif = motif
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### Analyse : {st.session_state.motif}")
    qs = DATA_EXPERT[st.session_state.motif]["questions"]
    reps = [st.checkbox(q) for q in qs]
    
    if st.button("Valider l'analyse"):
        st.session_state.res = DATA_EXPERT[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    res = st.session_state.res
    if "URGENCE" in res or "15" in res:
        st.error(f"🚨 {res}")
        st.button("📞 APPELER LE 15 MAINTENANT")
    elif "PHARMACIE" in res:
        st.success(f"🏥 {res}")
        st.info("💡 Économie pour la Sécu : 26,50€")
        st.link_button("📍 Trouver une pharmacie", "https://www.google.com/maps/search/pharmacie")
    else:
        st.warning(f"👨‍⚕️ {res}")
        st.link_button("📅 Prendre RDV Doctolib", "https://www.doctolib.fr")
    
    if st.button("Recommencer"):
        st.session_state.page = "home"
        st.rerun()    "Problème de Peau / Éruption": {
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
