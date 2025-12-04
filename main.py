import streamlit as st
import time

# Page Configuration
st.set_page_config(
    page_title="Streamlit Quiz Challenge",
    page_icon="🧠",
    layout="centered"
)

# --- Custom CSS for better styling ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    .success-msg {
        color: #4CAF50;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        background-color: #dff0d8;
    }
    .error-msg {
        color: #D32F2F;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        background-color: #fdecea;
    }
    </style>
""", unsafe_allow_html=True)

# --- Quiz Data ---
# Questions sur l'indépendance numérique et la vie privée
QUESTIONS = [
    {
        "question": "Quelle est une alternative libre et open-source majeure aux systèmes Windows et macOS ?",
        "options": ["Android", "iOS", "Linux", "MS-DOS"],
        "answer": "Linux",
        "explanation": "Linux est un système d'exploitation libre (open-source) qui vous donne le contrôle total sur votre machine sans envoyer de données à une entreprise tierce."
    },
    {
        "question": "Quel navigateur web est développé par une fondation à but non lucratif et protège par défaut contre le pistage ?",
        "options": ["Google Chrome", "Mozilla Firefox", "Microsoft Edge", "Safari"],
        "answer": "Mozilla Firefox",
        "explanation": "Firefox est développé par la fondation Mozilla. Contrairement à Chrome ou Edge, son modèle économique ne repose pas sur la vente de vos données publicitaires."
    },
    {
        "question": "Quel moteur de recherche promet de ne pas tracer vos requêtes ni de créer de profil publicitaire ?",
        "options": ["Google", "Bing", "DuckDuckGo", "Yahoo"],
        "answer": "DuckDuckGo",
        "explanation": "DuckDuckGo (ou Qwant en France) est un moteur de recherche qui respecte la vie privée en ne stockant pas votre historique de recherche."
    },
    {
        "question": "Quelle application de messagerie est recommandée par les experts pour son chiffrement de bout en bout et sa collecte minimale de métadonnées ?",
        "options": ["WhatsApp", "Signal", "Facebook Messenger", "Telegram"],
        "answer": "Signal",
        "explanation": "Signal est une application open-source gérée par une fondation. Elle ne collecte pratiquement aucune métadonnée sur ses utilisateurs, contrairement à WhatsApp."
    },
    {
        "question": "Pour remplacer Google Drive ou Dropbox en gardant la maîtrise de ses données, quelle solution d'auto-hébergement est populaire ?",
        "options": ["Nextcloud", "iCloud", "OneDrive", "WeTransfer"],
        "answer": "Nextcloud",
        "explanation": "Nextcloud est une suite logicielle libre que vous pouvez installer sur votre propre serveur (ou chez un hébergeur de confiance) pour stocker vos fichiers, contacts et agendas."
    },
    {
        "question": "Quel service d'e-mail chiffré, basé en Suisse, est une alternative courante à Gmail pour protéger sa correspondance ?",
        "options": ["Outlook", "Proton Mail", "Yahoo Mail", "Orange Mail"],
        "answer": "Proton Mail",
        "explanation": "Proton Mail utilise le chiffrement de bout en bout et est protégé par les lois suisses sur la vie privée, offrant une sécurité supérieure aux géants du web."
    },
    {
        "question": "Sur Android, quel magasin d'applications alternatif ne propose que des logiciels libres et open-source (FOSS) ?",
        "options": ["Google Play Store", "Amazon Appstore", "F-Droid", "Samsung Galaxy Store"],
        "answer": "F-Droid",
        "explanation": "F-Droid est un catalogue d'applications libres pour Android. Il ne nécessite pas de compte et respecte votre vie privée (pas de tracking)."
    },
    {
        "question": "Quelle plateforme vidéo fédérée et décentralisée permet de visionner du contenu sans passer par l'algorithme de YouTube ?",
        "options": ["Dailymotion", "Twitch", "PeerTube", "Vimeo"],
        "answer": "PeerTube",
        "explanation": "PeerTube est un logiciel qui permet de créer des plateformes vidéo interconnectées. Il n'y a pas d'entité centrale qui contrôle ce que vous regardez."
    },
    {
        "question": "Quelle est l'alternative collaborative et libre à Google Maps, construite par des volontaires ?",
        "options": ["OpenStreetMap", "Waze", "Apple Maps", "Mappy"],
        "answer": "OpenStreetMap",
        "explanation": "OpenStreetMap (OSM) est le 'Wikipédia des cartes'. C'est une base de données géographique libre et gratuite, utilisée par de nombreuses applications comme OsmAnd ou Organic Maps."
    },
    {
        "question": "Que signifie l'acronyme GAFAM, qui désigne les géants dont on cherche souvent à s'émanciper ?",
        "options": ["Global Association For Advanced Machines", "Google Amazon Facebook Apple Microsoft", "Groupe d'Action Pour la Formation aux Métiers", "Google Apple Facebook Amazon Mozilla"],
        "answer": "Google Amazon Facebook Apple Microsoft",
        "explanation": "Cet acronyme regroupe les cinq géants américains du numérique qui dominent le marché et collectent massivement des données personnelles."
    }
]

# --- Session State Initialization ---
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {} # Stores {index: user_choice}

# --- Helper Functions ---

def restart_quiz():
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False
    st.session_state.user_answers = {}
    st.rerun()

def submit_answer():
    # Get the current selection
    choice = st.session_state.get(f"q_{st.session_state.current_question_index}")
    
    if not choice:
        st.warning("Please select an answer before proceeding.")
        return

    # Record the answer
    current_idx = st.session_state.current_question_index
    correct_answer = QUESTIONS[current_idx]['answer']
    st.session_state.user_answers[current_idx] = choice

    # Check correctness
    if choice == correct_answer:
        st.session_state.score += 1
    
    # Move to next or finish
    if st.session_state.current_question_index < len(QUESTIONS) - 1:
        st.session_state.current_question_index += 1
    else:
        st.session_state.quiz_complete = True
    
    st.rerun()

# --- Main App Interface ---

st.title("🛡️ Quiz : Souveraineté Numérique")
st.write("Testez vos connaissances pour vous libérer des géants du numérique !")

# Progress Bar
if not st.session_state.quiz_complete:
    progress = (st.session_state.current_question_index / len(QUESTIONS))
    st.progress(progress)
    st.caption(f"Question {st.session_state.current_question_index + 1} sur {len(QUESTIONS)}")

st.divider()

# --- Logic: Display Question or Results ---

if st.session_state.quiz_complete:
    # --- Results Screen ---
    score_percentage = (st.session_state.score / len(QUESTIONS)) * 100
    
    if score_percentage >= 80:
        st.balloons()
        st.success(f"🎉 Bravo ! Vous avez obtenu {st.session_state.score} sur {len(QUESTIONS)} ({score_percentage}%)")
    elif score_percentage >= 50:
        st.info(f"👍 Pas mal ! Vous avez obtenu {st.session_state.score} sur {len(QUESTIONS)} ({score_percentage}%)")
    else:
        st.error(f"😅 Continuez à apprendre ! Vous avez obtenu {st.session_state.score} sur {len(QUESTIONS)} ({score_percentage}%)")
    
    st.subheader("Récapitulatif de vos réponses :")
    
    for i, q in enumerate(QUESTIONS):
        user_choice = st.session_state.user_answers.get(i)
        is_correct = user_choice == q['answer']
        
        with st.expander(f"Q{i+1}: {q['question']}", expanded=False):
            if is_correct:
                st.markdown(f"<div class='success-msg'>✅ Votre réponse : {user_choice}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='error-msg'>❌ Votre réponse : {user_choice}</div>", unsafe_allow_html=True)
                st.write(f"**Bonne réponse :** {q['answer']}")
            
            st.info(f"ℹ️ **Explication :** {q['explanation']}")

    st.divider()
    if st.button("🔄 Recommencer le Quiz"):
        restart_quiz()

else:
    # --- Question Screen ---
    question_data = QUESTIONS[st.session_state.current_question_index]
    
    # Display Question
    st.markdown(f"""
        <div class="question-box">
            <h3>{question_data['question']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Display Options
    # We use a unique key based on the index so Streamlit resets the widget for new questions
    choice = st.radio(
        "Choisissez une réponse :",
        question_data['options'],
        key=f"q_{st.session_state.current_question_index}",
        index=None # No default selection
    )
    
    st.write("") # Spacer
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Valider ➡"):
            submit_answer()
    with col2:
        # Just filling space
        pass

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit")