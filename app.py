import streamlit as st

# 1. INITIALISATION
if 'page' not in st.session_state: st.session_state.page = "home"
if 'motif' not in st.session_state: st.session_state.motif = None

st.set_page_config(page_title="Maison France Santé - IA", page_icon="🇫🇷")

# 2. LOGIQUE DE RECHERCHE INTELLIGENTE
def detecter_motif(texte):
    texte = texte.lower()
    mapping = {
        "ventre": "Abdominale (Ventre)", "estomac": "Abdominale (Ventre)", "diarrhée": "Abdominale (Ventre)", "gastro": "Abdominale (Ventre)",
        "gorge": "ORL & Respiratoire", "toux": "ORL & Respiratoire", "rhume": "ORL & Respiratoire", "angine": "ORL & Respiratoire",
        "cheville": "Traumatologie (Choc, Chute)", "genou": "Traumatologie (Choc, Chute)", "chute": "Traumatologie (Choc, Chute)", "entorse": "Traumatologie (Choc, Chute)",
        "pipi": "Infection Urinaire", "brûlure": "Infection Urinaire", "urinaire": "Infection Urinaire",
        "dos": "Neurologie & Dos", "tête": "Neurologie & Dos", "migraine": "Neurologie & Dos",
        "oeil": "Ophtalmologie (Œil)", "vision": "Ophtalmologie (Œil)", "rouge": "Ophtalmologie (Œil)",
        "dent": "Dentaire", "gencive": "Dentaire", "mâchoire": "Dentaire",
        "enfant": "Pédiatrie (Enfant)", "bébé": "Pédiatrie (Enfant)",
        "triste": "Santé Mentale", "angoisse": "Santé Mentale", "sommeil": "Santé Mentale"
    }
    for cle, motif in mapping.items():
        if cle in texte: return motif
    return None

# 3. BASE DE DONNÉES (Version Simplifiée pour la démo)
DATA_PRO = {
    "Traumatologie (Choc, Chute)": ["Membre déformé ?", "Impossible de marcher ?", "Douleur supportable ?"],
    "Abdominale (Ventre)": ["Ventre dur / Sang ?", "Vomissements / Diarrhée ?", "Simple ballonnement ?"],
    "ORL & Respiratoire": ["Mal à respirer ?", "Forte fièvre + Gorge ?", "Nez qui coule / Toux simple ?"],
    "Infection Urinaire": ["Fièvre / Douleur dos ?", "Sang ?", "Brûlure simple ?"],
    "Neurologie & Dos": ["Paralysie / Confusion ?", "Chute sur le dos ?", "Lumbago simple ?"],
    "Ophtalmologie (Œil)": ["Perte vision ?", "Douleur vive ?", "Œil rouge ?"],
    "Dentaire": ["Visage gonflé ?", "Dent cassée ?", "Sensibilité simple ?"],
    "Pédiatrie (Enfant)": ["Ménage / Refuse boire ?", "Fièvre ?", "Poussée dentaire ?"],
    "Santé Mentale": ["Idées noires ?", "Grosse anxiété ?", "Stress passager ?"]
}

# 4. INTERFACE
st.title("🇫🇷 La Maison France Santé")

if st.session_state.page == "home":
    st.write("### Décrivez votre problème")
    user_input = st.text_input("Ex: J'ai mal à la gorge depuis 3 jours", "")
    
    if user_input:
        detection = detecter_motif(user_input)
        if detection:
            st.success(f"Analyse détectée : **{detection}**")
            if st.button(f"Commencer le diagnostic {detection}"):
                st.session_state.motif = detection
                st.session_state.page = "quiz"
                st.rerun()
        else:
            st.warning("Précisez votre recherche (ex: ventre, dos, gorge...)")

    st.write("---")
    st.write("### Ou choisissez manuellement")
    choix = st.selectbox("Catégories", ["Choisir..."] + list(DATA_PRO.keys()))
    if choix != "Choisir..." and st.button("Valider"):
        st.session_state.motif = choix
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### Diagnostic : {st.session_state.motif}")
    for q in DATA_PRO[st.session_state.motif]:
        st.checkbox(q)
    if st.button("Terminer"):
        st.session_state.page = "home"
        st.rerun()
