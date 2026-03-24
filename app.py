import streamlit as st

# 1. INITIALISATION
if 'page' not in st.session_state: st.session_state.page = "home"
if 'motif' not in st.session_state: st.session_state.motif = None
if 'res' not in st.session_state: st.session_state.res = None

st.set_page_config(page_title="Maison France Santé - Régulation", page_icon="🇫🇷")

# 2. STYLE
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 10px; border: 2px solid #0055a4; background-color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. MATRICE MÉDICALE HAUTE PRÉCISION
# Structure : [Symptômes VITAUX, Symptômes SÉRIEUX, Symptômes BÉNINS]
DATA_PRO = {
    "Traumatologie (Choc, Chute)": {
        "q": ["Membre déformé / Os visible ?", "Impossible de poser le pied / 4 pas ?", "Simple douleur ou bleu après un choc ?"],
        "logic": lambda q: "🚨 URGENCE TRAUMATO (15)" if q[0] else ("👨‍⚕️ MEDECIN (Radio requise)" if q[1] else "🏥 PHARMACIE (Glace / Repos)")
    },
    "Abdominale (Ventre)": {
        "q": ["Ventre dur / Sang dans les selles ?", "Vomissements ou Diarrhée persistante ?", "Ballonnements / Digestion difficile ?"],
        "logic": lambda q: "🚨 URGENCE CHIRURGICALE (15)" if q[0] else ("👨‍⚕️ MEDECIN (Risque déshydratation)" if q[1] else "🏥 PHARMACIE (Conseil Digestif)")
    },
    "ORL & Respiratoire": {
        "q": ["Difficulté à respirer / Sifflement ?", "Fièvre élevée + Gorge très douloureuse ?", "Nez qui coule / Toux simple ?"],
        "logic": lambda q: "🚨 URGENCE RESPIRATOIRE (15)" if q[0] else ("🏥 PHARMACIE (Test TROD Angine)" if q[1] else "💊 PHARMACIE (Symptomatique)")
    },
    "Infection Urinaire": {
        "q": ["Fièvre / Douleur dans le dos ?", "Sang dans les urines ?", "Envie fréquente / Brûlure simple ?"],
        "logic": lambda q: "🚨 URGENCE (Reins/15)" if q[0] else ("👨‍⚕️ MEDECIN (Analyse d'urine)" if q[1] else "🏥 PHARMACIE (Protocole Cystite)")
    },
    "Neurologie & Dos": {
        "q": ["Paralysie / Confusion / Incontinence ?", "Douleur dos suite à un choc ?", "Lumbago / Mal de dos habituel ?"],
        "logic": lambda q: "🚨 URGENCE NEURO (15)" if q[0] else ("👨‍⚕️ MEDECIN (Examen clinique)" if q[1] else "🏥 PHARMACIE (Antidouleur / Kiné)")
    },
    "Ophtalmologie (Œil)": {
        "q": ["Baisse de vision / Douleur vive ?", "Corps étranger dans l'œil ?", "Œil rouge / Démangeaisons ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO (15)" if q[0] else ("👨‍⚕️ MEDECIN (Contrôle)" if q[1] else "🏥 PHARMACIE (Lavage / Collyre)")
    },
    "Dentaire": {
        "q": ["Gonflement visage / Fièvre ?", "Dent cassée / Expulsée ?", "Sensibilité au chaud/froid ?"],
        "logic": lambda q: "🚨 URGENCE DENTAIRE" if q[0] else ("🦷 DENTISTE (RDV rapide)" if q[1] else "🏥 PHARMACIE (Gel gingival)")
    },
    "Dermatologie (Peau)": {
        "q": ["Taches rouges qui ne s'effacent pas ?", "Éruption avec fièvre ?", "Boutons / Rougeurs sans fièvre ?"],
        "logic": lambda q: "🚨 URGENCE DERMATO (15)" if q[0] or q[1] else "🏥 PHARMACIE (Conseil Dermato)"
    },
    "Pédiatrie (Enfant)": {
        "q": ["Enfant mou / Refuse de boire ?", "Fièvre > 39°C ?", "Rhume / Poussée dentaire ?"],
        "logic": lambda q: "🚨 URGENCE PÉDIATRIQUE (15)" if q[0] else ("👨‍⚕️ PÉDIATRE (Sous 24h)" if q[1] else "🏥 PHARMACIE (Conseil maman)")
    },
    "Santé Mentale": {
        "q": ["Idées noires / Mise en danger ?", "Anxiété empêchant de dormir ?", "Stress passager / Fatigue ?"],
        "logic": lambda q: "📞 APPEL 3114 (Urgence Psy)" if q[0] else ("👨‍⚕️ MEDECIN / PSY" if q[1] else "🏥 PHARMACIE (Phytothérapie)")
    }
}

# 4. INTERFACE
st.title("🇫🇷 La Maison France Santé")
st.caption("Aiguillage Intelligent - Redonner du temps médical aux Français")

if st.session_state.page == "home":
    st.write("### 1. Quel est votre motif ?")
    choix = st.selectbox("Choisir...", ["Choisir..."] + list(DATA_PRO.keys()))
    if st.button("Continuer"):
        if choix != "Choisir...":
            st.session_state.motif = choix
            st.session_state.page = "quiz"
            st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### 2. Analyse précise : {st.session_state.motif}")
    qs = DATA_PRO[st.session_state.motif]["q"]
    reps = [st.checkbox(q, key=f"c_{i}") for i, q in enumerate(qs)]
    
    if st.button("Calculer l'orientation"):
        st.session_state.res = DATA_PRO[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    st.write("### 3. Votre Parcours de Soins")
    st.markdown(f"<div class='report-box'><h2>{st.session_state.res}</h2></div>", unsafe_allow_html=True)
    
    if "🚨" in st.session_state.res:
        st.error("Contactez immédiatement les secours.")
        st.button("📞 APPELER LE 15")
    elif "PHARMACIE" in st.session_state.res:
        st.success("Orientation : Circuit Court Officinal. Gain de temps immédiat.")
        st.link_button("📍 Trouver une pharmacie", "https://www.google.com/maps/search/pharmacie")
    else:
        st.info("Une consultation médicale est recommandée.")
        st.link_button("📅 RDV Doctolib", "https://www.doctolib.fr")
    
    if st.button("🔄 Nouvelle analyse"):
        st.session_state.page = "home"
        st.rerun()
