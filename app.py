import streamlit as st

# 1. INITIALISATION (Sécurité anti-bug)
if 'page' not in st.session_state: st.session_state.page = "home"
if 'motif' not in st.session_state: st.session_state.motif = None
if 'res' not in st.session_state: st.session_state.res = None

st.set_page_config(page_title="La Maison France Santé", page_icon="🇫🇷")

# 2. DICTIONNAIRE SÉMANTIQUE (Moteur de recherche 80% des cas)
KEYWORDS_DB = {
    "Cardio / Circulation": ["coeur", "palpitation", "tension", "poitrine", "bras gauche", "infarctus", "souffle"],
    "Abdominale (Ventre)": ["ventre", "estomac", "diarrhée", "gastro", "constipation", "nausée", "vomir", "foie", "appendicite"],
    "ORL & Respiratoire": ["gorge", "toux", "rhume", "angine", "nez", "sinus", "bronches", "grippe", "respirer", "apnée"],
    "Oreilles (Audition)": ["oreille", "otite", "bouchon", "bourdonnement", "acouphène", "surdité", "entendre", "vertige"],
    "Traumatologie": ["cheville", "genou", "chute", "entorse", "pied", "fracture", "poignet", "épaule", "choc", "bosse"],
    "Infection Urinaire": ["pipi", "brûlure", "cystite", "reins", "vessie", "sang urines"],
    "Neurologie & Dos": ["dos", "tête", "migraine", "paralysie", "fourmillements", "lumbago", "nuque", "sciatique", "avc"],
    "Ophtalmologie": ["oeil", "vision", "rouge", "paupière", "conjonctivite", "flou", "double", "voir"],
    "Dentaire": ["dent", "gencive", "mâchoire", "carie", "abcès", "dent de sagesse"],
    "Dermatologie": ["peau", "bouton", "éruption", "plaie", "grain de beauté", "démangeaison", "eczéma", "tache"],
    "Pédiatrie": ["enfant", "bébé", "nourrisson", "poussée dentaire", "pleurs", "couche"],
    "Santé Mentale": ["triste", "angoisse", "suicide", "sommeil", "dépression", "burnout", "panique", "stress"]
}

def detecter_intelligent(texte):
    t = texte.lower()
    for motif, mots in KEYWORDS_DB.items():
        if any(m in t for m in mots): return motif
    return None

# 3. BASE DE DONNÉES MÉDICALE (Logique de triage)
DATA_PRO = {
    "Cardio / Circulation": {
        "q": ["Douleur/Serrage poitrine ?", "Douleur bras ou mâchoire ?", "Essoufflement brutal ?", "Palpitations rapides ?"],
        "logic": lambda q: "🚨 URGENCE CARDIAQUE (15)" if q[0] or q[1] or q[2] else "👨‍⚕️ MEDECIN (Bilan Cardio)"
    },
    "Abdominale (Ventre)": {
        "q": ["Ventre dur / Sang selles ?", "Vomissements ou Diarrhée ?", "Ballonnement / Gaz ?"],
        "logic": lambda q: "🚨 URGENCE CHIRURGICALE (15)" if q[0] else ("👨‍⚕️ MEDECIN (Déshydratation)" if q[1] else "🏥 PHARMACIE")
    },
    "ORL & Respiratoire": {
        "q": ["Mal à respirer / Sifflement ?", "Fièvre + Gorge bloquée ?", "Nez qui coule / Toux ?"],
        "logic": lambda q: "🚨 URGENCE (15)" if q[0] else ("🏥 PHARMACIE (Test TROD)" if q[1] else "💊 PHARMACIE")
    },
    "Oreilles (Audition)": {
        "q": ["Baisse audition brutale ?", "Douleur + Nuque raide ?", "Sensation bouchée / Vertige ?"],
        "logic": lambda q: "🚨 URGENCE ORL" if q[0] or q[1] else "🏥 PHARMACIE (Conseil)"
    },
    "Traumatologie": {
        "q": ["Membre déformé ?", "Impossible de faire 4 pas ?", "Simple bleu / Douleur légère ?"],
        "logic": lambda q: "🚨 URGENCE TRAUMATO (15)" if q[0] else ("👨‍⚕️ MEDECIN (Radio)" if q[1] else "🏥 PHARMACIE")
    },
    "Infection Urinaire": {
        "q": ["Fièvre / Douleur dos ?", "Sang dans les urines ?", "Brûlure simple ?"],
        "logic": lambda q: "🚨 URGENCE (Reins)" if q[0] or q[1] else "🏥 PHARMACIE (Cystite)"
    },
    "Neurologie & Dos": {
        "q": ["Paralysie / Confusion ?", "Chute sur le dos ?", "Mal de dos simple ?"],
        "logic": lambda q: "🚨 URGENCE NEURO (15)" if q[0] else "👨‍⚕️ MEDECIN / KINE"
    },
    "Ophtalmologie": {
        "q": ["Perte vision / Douleur vive ?", "Corps étranger ?", "Oeil rouge ?"],
        "logic": lambda q: "🚨 URGENCE OPHTALMO" if q[0] else "🏥 PHARMACIE"
    },
    "Dentaire": {
        "q": ["Joue gonflée / Fièvre ?", "Dent cassée ?", "Sensibilité ?"],
        "logic": lambda q: "🚨 URGENCE DENTAIRE" if q[0] else "🦷 DENTISTE"
    },
    "Dermatologie": {
        "q": ["Taches rouges fixes ?", "Éruption + Fièvre ?", "Démangeaison simple ?"],
        "logic": lambda q: "🚨 URGENCE DERMATO" if q[0] or q[1] else "🏥 PHARMACIE"
    },
    "Pédiatrie": {
        "q": ["Enfant mou / Refuse boire ?", "Fièvre > 39°C ?", "Rhume / Pousse dentaire ?"],
        "logic": lambda q: "🚨 URGENCE PEDIATRIQUE" if q[0] else "👨‍⚕️ PEDIATRE"
    },
    "Santé Mentale": {
        "q": ["Idées noires ?", "Anxiété forte ?", "Stress passager ?"],
        "logic": lambda q: "📞 APPEL 3114 (Urgence)" if q[0] else "👨‍⚕️ PSY / MEDECIN"
    }
}

# 4. INTERFACE
st.title("🇫🇷 La Maison France Santé")
st.caption("Intelligence de Régulation Citoyenne")

if st.session_state.page == "home":
    st.write("### 💬 Que ressentez-vous ?")
    u_input = st.text_input("Décrivez vos symptômes...", placeholder="Ex: J'ai mal à la gorge")
    
    if u_input:
        detec = detecter_intelligent(u_input)
        if detec:
            st.info(f"Analyse suggérée : **{detec}**")
            if st.button(f"Lancer le protocole {detec}"):
                st.session_state.motif, st.session_state.page = detec, "quiz"
                st.rerun()
    
    st.write("---")
    choix = st.selectbox("Ou sélectionnez manuellement :", ["Choisir..."] + list(DATA_PRO.keys()))
    if choix != "Choisir..." and st.button("Valider"):
        st.session_state.motif, st.session_state.page = choix, "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### Analyse : {st.session_state.motif}")
    qs = DATA_PRO[st.session_state.motif]["q"]
    reps = [st.checkbox(q, key=f"q_{i}") for i, q in enumerate(qs)]
    if st.button("Calculer l'orientation"):
        st.session_state.res, st.session_state.page = DATA_PRO[st.session_state.motif]["logic"](reps), "fin"
        st.rerun()

elif st.session_state.page == "fin":
    st.write("### Votre Parcours de Soins")
    st.success(f"**{st.session_state.res}**")
    if "🚨" in st.session_state.res: st.error("Appelez immédiatement le 15.")
    elif "PHARMACIE" in st.session_state.res:
        st.info("💡 Économie estimée : 26,50€")
        st.link_button("📍 Trouver une pharmacie", "https://www.google.com/maps/search/pharmacie")
    if st.button("Nouvelle analyse"):
        st.session_state.page = "home"
        st.rerun()
