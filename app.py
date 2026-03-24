import streamlit as st

# 1. INITIALISATION DES VARIABLES
if 'page' not in st.session_state: st.session_state.page = "home"
if 'motif' not in st.session_state: st.session_state.motif = None
if 'res' not in st.session_state: st.session_state.res = None

st.set_page_config(page_title="Maison France Santé - Expert V3", page_icon="🇫🇷")

# 2. LOGIQUE DE RECHERCHE PAR MOTS-CLÉS
def detecter_motif(texte):
    t = texte.lower()
    mapping = {
        "ventre": "Abdominale (Ventre)", "estomac": "Abdominale (Ventre)", "diarrhée": "Abdominale (Ventre)", "gastro": "Abdominale (Ventre)",
        "gorge": "ORL & Respiratoire", "toux": "ORL & Respiratoire", "rhume": "ORL & Respiratoire", "angine": "ORL & Respiratoire",
        "cheville": "Traumatologie", "genou": "Traumatologie", "chute": "Traumatologie", "entorse": "Traumatologie", "pied": "Traumatologie",
        "pipi": "Infection Urinaire", "brûlure": "Infection Urinaire", "cystite": "Infection Urinaire",
        "dos": "Neurologie & Dos", "tête": "Neurologie & Dos", "migraine": "Neurologie & Dos",
        "oeil": "Ophtalmologie", "vision": "Ophtalmologie", "rouge": "Ophtalmologie",
        "dent": "Dentaire", "gencive": "Dentaire", "mâchoire": "Dentaire",
        "enfant": "Pédiatrie", "bébé": "Pédiatrie",
        "triste": "Santé Mentale", "angoisse": "Santé Mentale", "suicide": "Santé Mentale"
    }
    for k, v in mapping.items():
        if k in t: return v
    return None

# 3. BASE DE DONNÉES MÉDICALE COMPLÈTE (10 MODULES)
DATA_PRO = {
    "Traumatologie": {
        "q": ["Déformation ou membre anormal ?", "Impossible de faire 4 pas ?", "Simple bleu ou douleur légère ?"],
        "logic": lambda q: "🚨 URGENCE TRAUMATO (15)" if q[0] else ("👨‍⚕️ MEDECIN (Radio)" if q[1] else "🏥 PHARMACIE (Glace/Repos)")
    },
    "Abdominale (Ventre)": {
        "q": ["Ventre dur / Sang dans les selles ?", "Vomissements ou Diarrhée persistante ?", "Diarrhée simple / Ballonnements ?"],
        "logic": lambda q: "🚨 URGENCE CHIRURGICALE (15)" if q[0] else ("👨‍⚕️ MEDECIN (Déshydratation)" if q[1] else "🏥 PHARMACIE (Conseil)")
    },
    "ORL & Respiratoire": {
        "q": ["Mal à respirer / Sifflement ?", "Forte fièvre + Gorge bloquée ?", "Nez qui coule / Toux simple ?"],
        "logic": lambda q: "🚨 URGENCE RESPIRATOIRE (15)" if q[0] else ("🏥 PHARMACIE (Test TROD)" if q[1] else "💊 PHARMACIE")
    },
    "Infection Urinaire": {
        "q": ["Fièvre / Douleur dos ?", "Sang dans les urines ?", "Brûlure simple au pipi ?"],
        "logic": lambda q: "🚨 URGENCE (Reins)" if q[0] else ("👨‍⚕️ MEDECIN (Analyse)" if q[1] else "🏥 PHARMACIE (Cystite)")
    },
    "Neurologie & Dos": {
        "q": ["Paralysie / Confusion ?", "Chute sur le dos ?", "Lumbago / Mal de dos simple ?"],
        "logic": lambda q: "🚨 URGENCE NEURO (15)" if q[0] else ("👨‍⚕️ MEDECIN" if q[1] else "🏥 PHARMACIE")
    },
    "Ophtalmologie": {
        "q": ["Perte de vision / Douleur vive ?", "Corps étranger ?", "Œil rouge ou qui gratte ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO" if q[0] else ("👨‍⚕️ MEDECIN" if q[1] else "🏥 PHARMACIE")
    },
    "Dentaire": {
        "q": ["Joue gonflée / Fièvre ?", "Dent cassée ?", "Sensibilité au froid/chaud ?"],
        "logic": lambda q: "🚨 URGENCE DENTAIRE" if q[0] else ("🦷 DENTISTE" if q[1] else "🏥 PHARMACIE")
    },
    "Pédiatrie": {
        "q": ["Enfant prostré / Refuse boire ?", "Fièvre > 39°C ?", "Poussée dentaire / Rhume ?"],
        "logic": lambda q: "🚨 URGENCE PÉDIATRIQUE" if q[0] else ("👨‍⚕️ PÉDIATRE" if q[1] else "🏥 PHARMACIE")
    },
    "Santé Mentale": {
        "q": ["Idées noires / Mise en danger ?", "Anxiété empêchant de dormir ?", "Stress passager ?"],
        "logic": lambda q: "📞 APPEL 3114 (Urgence)" if q[0] else ("👨‍⚕️ PSY" if q[1] else "🏥 PHARMACIE")
    },
    "Dermatologie": {
        "q": ["Purpura (taches rouges fixes) ?", "Éruption + Fièvre ?", "Boutons simples / Rougeurs ?"],
        "logic": lambda q: "🚨 URGENCE DERMATO" if q[0] or q[1] else "🏥 PHARMACIE"
    }
}

# 4. INTERFACE
st.title("🇫🇷 La Maison France Santé")

if st.session_state.page == "home":
    st.write("### Décrivez votre symptôme")
    user_input = st.text_input("Ex: J'ai mal au ventre et de la diarrhée", "")
    
    if user_input:
        detection = detecter_motif(user_input)
        if detection:
            st.info(f"Analyse suggérée : **{detection}**")
            if st.button(f"Lancer le diagnostic {detection}"):
                st.session_state.motif = detection
                st.session_state.page = "quiz"
                st.rerun()
        else:
            st.warning("Précisez votre recherche (mots-clés : dos, gorge, oeil, dent...)")

    st.write("---")
    st.write("### Ou sélectionnez manuellement")
    choix = st.selectbox("Catégories", ["Choisir..."] + list(DATA_PRO.keys()))
    if choix != "Choisir..." and st.button("Valider le choix"):
        st.session_state.motif = choix
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### Diagnostic : {st.session_state.motif}")
    qs = DATA_PRO[st.session_state.motif]["q"]
    reps = [st.checkbox(q, key=f"q_{i}") for i, q in enumerate(qs)]
    
    if st.button("Calculer l'orientation"):
        st.session_state.res = DATA_PRO[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    st.write("### Résultat & Orientation")
    st.success(f"**{st.session_state.res}**")
    
    if "🚨" in st.session_state.res:
        st.error("Contactez immédiatement le 15.")
    elif "PHARMACIE" in st.session_state.res:
        st.info("💡 Économie Sécu : 26,50€")
        st.link_button("📍 Trouver une pharmacie", "https://www.google.com/maps/search/pharmacie")
    
    if st.button("Nouvelle analyse"):
        st.session_state.page = "home"
        st.rerun()
