import streamlit as st

st.set_page_config(page_title="Maison France Santé - Expert V3", page_icon="🇫🇷")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #0055a4; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 10px; border: 2px solid #0055a4; background-color: white; margin-bottom: 20px; }
    .stCheckbox { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTEUR DE DIAGNOSTIC HAUTE PRÉCISION ---
DATA_SERIEUX = {
    "Traumatologie (Chute, Choc, Entorse)": {
        "q": [
            "Déformation visible ou membre en position anormale ?",
            "Impossibilité totale de poser le pied ou de faire 4 pas ?",
            "Douleur osseuse très précise au toucher (cheville/poignet) ?",
            "Membre froid, bleu ou perte de sensibilité ?",
            "Le choc a eu lieu à la tête avec perte de connaissance ?"
        ],
        "logic": lambda q: "🚨 URGENCE TRAUMATO (Radio/15)" if any(q) else "🏥 PHARMACIE (Protocole RICE: Repos, Glace, Compression)"
    },
    "Abdominale & Digestif": {
        "q": [
            "Douleur brutale (type coup de poignard) ?",
            "Ventre dur/tendu (impossible à enfoncer) ?",
            "Vomissements répétés (impossible de boire) ?",
            "Diarrhée avec sang ou glaires ?",
            "Arrêt total des gaz et des selles (occlusion) ?"
        ],
        "logic": lambda q: "🚨 URGENCE CHIRURGICALE (15)" if q[0] or q[1] or q[4] else ("👨‍⚕️ MEDECIN (Risque déshydratation)" if q[2] or q[3] else "🏥 PHARMACIE (Conseil Digestif)")
    },
    "Infection Urinaire": {
        "q": [
            "Fièvre > 38.5°C ou Frissons ?",
            "Douleur aiguë dans le dos ou sur le côté (reins) ?",
            "Présence de sang visible dans les urines ?",
            "Brûlures lors de la miction sans autres signes ?"
        ],
        "logic": lambda q: "🚨 URGENCE (Risque Pyélonéphrite)" if q[0] or q[1] or q[2] else "🏥 PHARMACIE (Protocole Cystite)"
    },
    "ORL & Respiratoire": {
        "q": [
            "Difficulté réelle à respirer ou à parler ?",
            "Bruit siffleur à l'inspiration ?",
            "Fièvre élevée associée à une absence de toux ?",
            "Difficulté à avaler sa propre salive ?"
        ],
        "logic": lambda q: "🚨 URGENCE RESPIRATOIRE (15)" if q[0] or q[1] or q[3] else ("🏥 PHARMACIE (Test TROD Angine)" if q[2] else "💊 PHARMACIE (Symptomatique)")
    },
    "Neurologie & Dos": {
        "q": [
            "Perte de force ou de sensibilité dans un membre ?",
            "Incontinence soudaine (urinaire ou fécale) ?",
            "Céphalée brutale et inhabituelle (la pire de votre vie) ?",
            "Douleur dos suite à une chute importante ?"
        ],
        "logic": lambda q: "🚨 URGENCE NEURO (Risque AVC/Moelle)" if any(q) else "👨‍⚕️ MEDECIN / KINÉ"
    }
}

# --- LOGIQUE D'INTERFACE ---
if 'page' not in st.session_state: st.session_state.page = "home"

st.title("🇫🇷 La Maison France Santé")
st.caption("Aiguillage Médical Protocolé - Version Expert")

if st.session_state.page == "home":
    st.write("### 1. Quel est votre motif de consultation ?")
    choix = st.selectbox("Sélectionnez une catégorie", ["Choisir..."] + list(DATA_SERIEUX.keys()))
    
    if choix != "Choisir...":
        st.session_state.motif = choix
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":
    st.write(f"### 2. Analyse clinique : {st.session_state.motif}")
    st.info("Cochez uniquement si le symptôme est présent.")
    qs = DATA_SERIEUX[st.session_state.motif]["q"]
    reps = [st.checkbox(q, key=f"q_{i}") for i, q in enumerate(qs)]
    
    if st.button("ÉVALUER LA SITUATION"):
        st.session_state.res = DATA_SERIEUX[st.session_state.motif]["logic"](reps)
        st.session_state.page = "fin"
        st.rerun()

elif st.session_state.page == "fin":
    st.write("### 3. Orientation Recommandée")
    res = st.session_state.res
    st.markdown(f"<div class='report-box'><h2>{res}</h2></div>", unsafe_allow_html=True)
    
    if "🚨" in res:
        st.error("DANGER : Contactez immédiatement le 15 ou les urgences les plus proches.")
        st.button("📞 APPELER LE 15")
    elif "🏥 PHARMACIE" in res:
        st.success("ORIENTATION : Circuit Court (Officine).")
        st.info("💡 Économie estimée pour l'Assurance Maladie : 26,50€")
        st.link_button("📍 Trouver la pharmacie la plus proche", "
