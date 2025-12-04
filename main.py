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
    /* Import de la police Fredoka (très ronde et ludique) */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&display=swap');

    /* Application de la police à toute l'app */
    html, body, [class*="css"]  {
        font-family: 'Fredoka', sans-serif;
    }

    /* Style général des boutons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }

    /* Couleur de la barre de progression */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }

    /* Boîte de la question */
    .question-box {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .question-box h3 {
        font-weight: 600;
        margin: 0;
    }

    /* --- STYLING DES OPTIONS (Boutons Radio) --- */
    
    /* Le label "Choisissez une réponse :" style badge/bulle */
    .stRadio > label {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2c3e50;
        background-color: #ffffff;
        padding: 10px 20px;
        border-radius: 20px; /* Forme de pilule */
        margin-bottom: 20px;
        display: inline-block; /* S'adapte à la taille du texte */
        border: 2px solid #eef2f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Les options elles-mêmes (transformées en cartes) */
    div[role="radiogroup"] > label {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 2px solid #eef2f6;
        transition: all 0.2s ease;
        cursor: pointer;
        display: flex; /* Assure un bon alignement */
        align-items: center;
        width: 100%; /* Force la largeur à 100% pour uniformiser */
        box-sizing: border-box;
    }

    /* Effet au survol des options */
    div[role="radiogroup"] > label:hover {
        background-color: #f8fff9;
        border-color: #4CAF50;
        transform: translateX(5px); /* Petite animation vers la droite */
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Messages de feedback */
    .success-msg {
        color: #155724;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin-bottom: 15px;
    }
    .error-msg {
        color: #721c24;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        margin-bottom: 15px;
    }
    .correct-msg {
        background-color: #cce5ff;
        color: #004085;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #b8daff;
        text-align: center;
        margin-top: 10px;
        font-weight: bold;
    }
    
    /* Boîte des sources */
    .sources-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ffeeba;
        margin-top: 15px;
        margin-bottom: 30px;
    }
    .sources-box h5 {
        font-weight: bold;
        margin-top: 0;
    }
    .sources-box a {
        color: #533f03 !important;
        text-decoration: underline;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- Quiz Data ---
# Questions sur l'indépendance numérique et la vie privée
QUESTIONS = [
    {
        "question": "Quel robot conversationnel ne stocke pas vos données lorsque vous discutez avec lui ?",
        "options": ["ChatGPT", "Gemini", "Copilot AI", "Aucun"],
        "answer": "Aucun",
        "explanation": "Tous les modèles de chat modernes conservent au minimum des traces techniques (logs, métadonnées, usage) pour améliorer les services ou surveiller l’usage. Aucun ne fonctionne en interaction directe sans captation minimale.",
        "sources": [
            "https://openai.com/privacy",
            "https://policies.google.com/privacy",
            "https://privacy.microsoft.com/"
        ]
    },
    {
        "question": "Quel logiciel bureautique libre et gratuit permet de créer des documents, des présentations et des feuilles de calcul sans dépendre d’un service en ligne ?",
        "options": ["Microsoft Office 365", "Google Docs", "LibreOffice", "WPS Office"],
        "answer": "LibreOffice",
        "explanation": "LibreOffice est une suite bureautique libre, fonctionnant hors-ligne, et ne nécessitant pas de compte en ligne. Elle est développée par The Document Foundation.",
        "sources": [
            "https://www.libreoffice.org/discover/libreoffice/",
            "https://www.documentfoundation.org/"
        ]
    },
    {
        "question": "Quelle est une alternative libre et open-source majeure aux systèmes Windows et macOS ?",
        "options": ["Android", "iOS", "Linux", "MS-DOS"],
        "answer": "Linux",
        "explanation": "Linux est un système d'exploitation libre (open-source) qui vous donne le contrôle total sur votre machine sans envoyer de données à une entreprise tierce.",
        "sources": [
            "https://www.kernel.org/",
            "https://www.gnu.org/philosophy/free-sw.en.html"
        ]
    },
    {
        "question": "Quel navigateur web est développé par une fondation à but non lucratif et protège par défaut contre le pistage ?",
        "options": ["Google Chrome", "Mozilla Firefox", "Microsoft Edge", "Safari"],
        "answer": "Mozilla Firefox",
        "explanation": "Firefox est développé par la fondation Mozilla. Contrairement à Chrome ou Edge, son modèle économique ne repose pas sur la vente de vos données publicitaires.",
        "sources": [
            "https://www.mozilla.org/fr/about/",
            "https://www.mozilla.org/en-US/firefox/features/privacy/"
        ]
    },
    {
        "question": "Quel moteur de recherche promet de ne pas tracer vos requêtes ni de créer de profil publicitaire ?",
        "options": ["Google", "Bing", "DuckDuckGo", "Yahoo"],
        "answer": "DuckDuckGo",
        "explanation": "DuckDuckGo (ou Qwant en France) est un moteur de recherche qui respecte la vie privée en ne stockant pas votre historique de recherche.",
        "sources": [
            "https://duckduckgo.com/privacy",
            "https://www.qwant.com/privacy"
        ]
    },

    # --- QUESTIONS PLUS AVANCÉES ---

    {
        "question": "Dans le cycle de vie d’un ordinateur portable, quelle phase représente en moyenne l’impact carbone le plus élevé ?",
        "options": ["Son transport jusqu'au magasin", "Son utilisation quotidienne", "Sa fabrication", "Son recyclage en fin de vie"],
        "answer": "Sa fabrication",
        "explanation": "Plus de 70 % de l'impact carbone d’un ordinateur provient de la fabrication, en raison de l’extraction de métaux rares, de la production de composants et de l’assemblage.",
        "sources": [
            "https://www.data.gouv.fr/fr/reuses/quelle-est-lempreinte-carbone-dun-ordinateur-portable/",
            "https://www.greenit.fr/2011/02/10/quelle-est-l-empreinte-carbone-d-un-ordinateur/"
        ]
    },
    {
        "question": "Pourquoi le reconditionnement est écologiquement plus vertueux que le recyclage pur ?",
        "options": [
            "Parce que recycler consomme plus d'énergie et détruit les composants",
            "Parce que les machines recyclées sont revendues plus cher",
            "Parce que les matériaux recyclés sont de moindre qualité",
            "Parce que le reconditionnement supprime toute pollution"
        ],
        "answer": "Parce que recycler consomme plus d'énergie et détruit les composants",
        "explanation": "Le recyclage implique concassage, fusion et séparation chimique. Reconditionner évite la refabrication des composants, ce qui économise énergie et ressources.",
        "sources": [
            "https://weeefund.fr/2021/06/18/comment-mesurer-limpact-environnemental-du-reemploi-dun-ordinateur/",
            "https://www.ademe.fr/publications/economie-circulaire"
        ]
    },
    {
        "question": "Quel type de contenu en ligne est le plus consommateur d'énergie par utilisateur ?",
        "options": ["Le mail texte sans pièce jointe", "L’écoute d’un podcast", "Le streaming vidéo HD", "La navigation sur un site statique"],
        "answer": "Le streaming vidéo HD",
        "explanation": "Les vidéos HD nécessitent jusqu'à 100 fois plus de données qu’un contenu audio, sollicitant les serveurs et réseaux sur de longues durées.",
        "sources": [
            "https://theshiftproject.org/wp-content/uploads/2019/07/carbon-impacts-of-video-streaming-report-shift-project.pdf",
            "https://www.hellocarbo.com/blog/calculer/impact-du-numerique-sur-l-environnement/"
        ]
    },
    {
        "question": "Pourquoi la suppression régulière de données stockées dans le cloud réduit réellement l’impact environnemental ?",
        "options": [
            "Parce que les serveurs remplacent automatiquement les fichiers supprimés",
            "Parce que moins de données signifie moins de serveurs actifs",
            "Parce que le cloud fonctionne sur les appareils personnels",
            "Parce que les données supprimées ralentissent internet"
        ],
        "answer": "Parce que moins de données signifie moins de serveurs actifs",
        "explanation": "L'hébergement de données nécessite du stockage redondant et donc davantage de machines maintenues sous tension, refroidies et alimentées.",
        "sources": [
            "https://www.greenit.fr/2020/06/10/impact-stockage-mail-cloud/",
            "https://theshiftproject.org/"
        ]
    },
    {
        "question": "Quel facteur explique principalement l’empreinte énergétique des centres de données (datacenters) ?",
        "options": [
            "Le nettoyage quotidien des équipements",
            "Le refroidissement permanent des serveurs",
            "Le coût de leurs matériaux de construction",
            "La taille des bâtiments"
        ],
        "answer": "Le refroidissement permanent des serveurs",
        "explanation": "Les serveurs doivent rester sous ~27°C pour fonctionner. Le refroidissement représente parfois plus de la moitié de leur consommation électrique.",
        "sources": [
            "https://opera-energie.com/consommation-energie-datacenter/",
            "https://www.iea.org/reports/data-centres-and-data-transmission-networks"
        ]
    },
    {
        "question": "Quel indicateur environnemental correspond à l’énergie totale consommée tout au long de la fabrication d’un objet numérique ?",
        "options": [
            "L'énergie grise",
            "La puissance brute",
            "La consommation thermique",
            "La charge de calcul"
        ],
        "answer": "L'énergie grise",
        "explanation": "L’énergie grise inclut extraction des métaux, transport, assemblage, tests et fin de vie : c’est l'indicateur principal pour l’impact matériel du numérique.",
        "sources": [
            "https://en.wikipedia.org/wiki/Embodied_energy",
            "https://www.techcarbonstandard.org/technology-categories/lifecycle/embodied"
        ]
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
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False

# --- Helper Functions ---

def restart_quiz():
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False
    st.session_state.user_answers = {}
    st.session_state.answer_submitted = False
    st.rerun()

def submit_answer():
    # Get the current selection
    choice = st.session_state.get(f"q_{st.session_state.current_question_index}")
    
    if not choice:
        st.warning("Veuillez choisir une réponse avant de valider.")
        return

    # Record the answer
    current_idx = st.session_state.current_question_index
    correct_answer = QUESTIONS[current_idx]['answer']
    st.session_state.user_answers[current_idx] = choice

    # Check correctness
    if choice == correct_answer:
        st.session_state.score += 1
    
    # Mark as submitted, but don't move to next question yet
    st.session_state.answer_submitted = True
    st.rerun()

def next_question():
    # Move to next question and reset submitted state
    if st.session_state.current_question_index < len(QUESTIONS) - 1:
        st.session_state.current_question_index += 1
        st.session_state.answer_submitted = False
    else:
        st.session_state.quiz_complete = True
    st.rerun()

# --- Main App Interface ---

st.title("🛡️ Quiz : Souveraineté Numérique")
# Petit ajustement ici pour que le texte soit visible sur fond coloré (géré par CSS global, mais on peut forcer si besoin)
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
        st.success(f"🎉 Bravo ! Vous avez obtenu {st.session_state.score} sur {len(QUESTIONS)} ({score_percentage:.2f}%)")
    elif score_percentage >= 50:
        st.info(f"👍 Pas mal ! Vous avez obtenu {st.session_state.score} sur {len(QUESTIONS)} ({score_percentage:.2f}%)")
    else:
        st.error(f"😅 Continuez à apprendre ! Vous avez obtenu {st.session_state.score} sur {len(QUESTIONS)} ({score_percentage:.2f}%)")
    
    st.subheader("Récapitulatif de vos réponses :")
    
    for i, q in enumerate(QUESTIONS):
        user_choice = st.session_state.user_answers.get(i)
        is_correct = user_choice == q['answer']
        
        with st.expander(f"Q{i+1}: {q['question']}", expanded=False):
            if is_correct:
                st.markdown(f"<div class='success-msg'>✅ Votre réponse : {user_choice}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='error-msg'>❌ Votre réponse : {user_choice}</div>", unsafe_allow_html=True)
                # Affichage de la bonne réponse dans une boîte dédiée
                st.markdown(f"<div class='correct-msg'>👉 Bonne réponse : {q['answer']}</div>", unsafe_allow_html=True)
            
            # Explication
            st.markdown(f"<div style='color: #333; background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin-top: 10px;'>ℹ️ <b>Explication :</b> {q['explanation']}</div>", unsafe_allow_html=True)
            
            # Section SOURCES
            if "sources" in q and q["sources"]:
                # Construction du HTML pour la boîte des sources
                sources_html = "<div class='sources-box'><h5>📚 Pour aller plus loin :</h5><ul>"
                for source in q["sources"]:
                    sources_html += f"<li><a href='{source}' target='_blank'>{source}</a></li>"
                sources_html += "</ul></div>"
                st.markdown(sources_html, unsafe_allow_html=True)

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
    # On désactive les choix si la réponse a déjà été soumise
    choice = st.radio(
        "Choisissez une réponse :",
        question_data['options'],
        key=f"q_{st.session_state.current_question_index}",
        index=None,
        disabled=st.session_state.answer_submitted
    )
    
    # --- Immediate Feedback Section ---
    if st.session_state.answer_submitted:
        # Check if the submitted answer was correct
        user_choice = st.session_state.user_answers.get(st.session_state.current_question_index)
        correct_answer = question_data['answer']
        
        if user_choice == correct_answer:
            st.markdown(f"<div class='success-msg'>✅ Correct !</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='error-msg'>❌ Incorrect !</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='correct-msg'>👉 Bonne réponse : {correct_answer}</div>", unsafe_allow_html=True)
            
        # Explication immédiate
        st.markdown(f"<div style='color: #333; background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin-top: 10px;'>ℹ️ <b>Explication :</b> {question_data['explanation']}</div>", unsafe_allow_html=True)
            
        # Sources immédiates
        if "sources" in question_data and question_data["sources"]:
            sources_html = "<div class='sources-box'><h5>📚 Pour aller plus loin :</h5><ul>"
            for source in question_data["sources"]:
                sources_html += f"<li><a href='{source}' target='_blank'>{source}</a></li>"
            sources_html += "</ul></div>"
            st.markdown(sources_html, unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    # --- Buttons (Switch between Valid and Next) ---
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.session_state.answer_submitted:
            # Show "Next" button
            if st.session_state.current_question_index < len(QUESTIONS) - 1:
                if st.button("Question Suivante ➡"):
                    next_question()
            else:
                if st.button("Voir les résultats 🏁"):
                    next_question()
        else:
            # Show "Submit" button
            if st.button("Valider ➡"):
                submit_answer()
    with col2:
        pass