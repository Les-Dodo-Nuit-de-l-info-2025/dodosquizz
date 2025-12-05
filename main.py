import streamlit as st
import time

# Page Configuration
st.set_page_config(
    page_title="Streamlit Quiz Challenge",
    page_icon="🧠",
    layout="centered"
)

# --- Session State Initialization ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {} 
if 'answer_submitted' not in st.session_state:
    st.session_state.answer_submitted = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

def start_quiz():
    st.session_state.quiz_started = True
    st.rerun()

# --- Define Themes ---
if st.session_state.dark_mode:
    theme = {
        "bg_color": "#0E1117",
        "text_color": "#FAFAFA",
        "card_bg": "#262730",
        "card_border": "#3b3d45",
        "option_bg": "#1d2026",
        "option_hover": "#2d313a",
        "success_bg": "#1b4d2e",
        "success_text": "#a5d6a7",
        "success_border": "#2e7d32",
        "error_bg": "#4a1c1c",
        "error_text": "#ef9a9a",
        "error_border": "#b71c1c",
        "info_bg": "#0d305c",
        "info_text": "#90caf9",
        "info_border": "#1565c0",
        "sources_bg": "#3e320a",
        "sources_text": "#ffe082",
        "sources_border": "#856404",
        "link_color": "#FFD700",
        "btn_shadow": "rgba(255, 255, 255, 0.1)",
        "radio_label_bg": "#262730",
        "btn_bg": "#FFD700",          
        "btn_text": "#0E1117",        
        "btn_hover": "#e6c200"
    }
    btn_label = "☀️ Mode Clair"
else:
    theme = {
        "bg_color": "#FFFFFF",
        "text_color": "#2c3e50",
        "card_bg": "#f0f2f6",
        "card_border": "#f0f2f6",
        "option_bg": "#ffffff",
        "option_hover": "#f8fff9",
        "success_bg": "#d4edda",
        "success_text": "#155724",
        "success_border": "#c3e6cb",
        "error_bg": "#f8d7da",
        "error_text": "#721c24",
        "error_border": "#f5c6cb",
        "info_bg": "#cce5ff",
        "info_text": "#004085",
        "info_border": "#b8daff",
        "sources_bg": "#fff3cd",
        "sources_text": "#856404",
        "sources_border": "#ffeeba",
        "link_color": "#533f03",
        "btn_shadow": "rgba(0,0,0,0.1)",
        "radio_label_bg": "#ffffff",
        "btn_bg": "#FFD700",
        "btn_text": "#2c3e50",
        "btn_hover": "#ffe033"
    }
    btn_label = "🌙 Mode Sombre"

# --- Custom CSS (Dynamic) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&display=swap');

    html, body, [class*="css"], font, span, div, p, h1, h2, h3, h4, h5, h6, .stMarkdown, .stButton button, .stRadio label {{
        font-family: 'Fredoka', sans-serif !important;
    }}

    html, body, [class*="css"]  {{
        color: {theme['text_color']};
        background-color: {theme['bg_color']};
    }}
    
    .stApp {{
        background-color: {theme['bg_color']};
    }}

    h1, h2, h3, h4, h5, p, span, div {{
        color: {theme['text_color']};
    }}

    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px {theme['btn_shadow']};
        transition: all 0.2s;
        background-color: {theme['btn_bg']} !important;
        color: {theme['btn_text']} !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 8px {theme['btn_shadow']};
        background-color: {theme['btn_hover']} !important;
    }}

    .stProgress > div > div > div > div {{
        background-color: #4CAF50;
    }}

    .question-box {{
        background-color: {theme['card_bg']};
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 2px 4px {theme['btn_shadow']};
    }}
    .question-box h3 {{
        font-weight: 600;
        margin: 0;
        color: {theme['text_color']} !important;
    }}
    
    /* Landing Page Specifics */
    .landing-title {{
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 20px;
        color: {theme['text_color']};
    }}
    .landing-subtitle {{
        font-size: 1.5rem !important;
        text-align: center;
        margin-bottom: 40px;
        opacity: 0.9;
    }}
    .landing-emoji {{
        font-size: 5rem;
        text-align: center;
        display: block;
        margin-bottom: 20px;
    }}

    .stRadio > label {{
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: {theme['text_color']} !important;
        background-color: {theme['radio_label_bg']};
        padding: 10px 20px;
        border-radius: 20px;
        margin-bottom: 20px;
        display: inline-block;
        border: 2px solid {theme['card_border']};
        box-shadow: 0 2px 4px {theme['btn_shadow']};
    }}

    div[role="radiogroup"] > label {{
        background-color: {theme['option_bg']};
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 2px solid {theme['card_border']};
        transition: all 0.2s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
    }}
    
    div[role="radiogroup"] > label p {{
        color: {theme['text_color']} !important;
        font-weight: 500;
    }}

    div[role="radiogroup"] > label:hover {{
        background-color: {theme['option_hover']};
        border-color: #4CAF50;
        transform: translateX(5px);
        box-shadow: 0 2px 5px {theme['btn_shadow']};
    }}

    .success-msg {{
        color: {theme['success_text']};
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        background-color: {theme['success_bg']};
        border: 1px solid {theme['success_border']};
        margin-bottom: 15px;
    }}
    .error-msg {{
        color: {theme['error_text']};
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        background-color: {theme['error_bg']};
        border: 1px solid {theme['error_border']};
        margin-bottom: 15px;
    }}
    .correct-msg {{
        background-color: {theme['info_bg']};
        color: {theme['info_text']};
        padding: 15px;
        border-radius: 10px;
        border: 1px solid {theme['info_border']};
        text-align: center;
        margin-top: 10px;
        font-weight: bold;
    }}
    
    .sources-box {{
        background-color: {theme['sources_bg']};
        color: {theme['sources_text']};
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {theme['sources_border']};
        margin-top: 15px;
        margin-bottom: 30px;
    }}
    .sources-box h5 {{
        font-weight: bold;
        margin-top: 0;
        color: {theme['sources_text']} !important;
    }}
    .sources-box a {{
        color: {theme['link_color']} !important;
        text-decoration: underline;
        font-weight: 600;
    }}
    
    .explanation-box {{
        color: {theme['text_color']}; 
        background-color: {theme['card_bg']}; 
        padding: 10px; 
        border-radius: 5px; 
        margin-top: 10px;
        border: 1px solid {theme['card_border']};
    }}
    </style>
""", unsafe_allow_html=True)

# --- Top Bar (Dark Mode Toggle) ---
col_header, col_btn = st.columns([6, 1])
with col_btn:
    if st.button(btn_label):
        toggle_theme()
        st.rerun()

# --- Quiz Data ---
QUESTIONS = [
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

# --- Helper Functions ---

def restart_quiz():
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False
    st.session_state.user_answers = {}
    st.session_state.answer_submitted = False
    st.session_state.quiz_started = False # Retour à la page de garde
    st.rerun()

def submit_answer():
    choice = st.session_state.get(f"q_{st.session_state.current_question_index}")
    if not choice:
        st.warning("Veuillez choisir une réponse avant de valider.")
        return
    current_idx = st.session_state.current_question_index
    correct_answer = QUESTIONS[current_idx]['answer']
    st.session_state.user_answers[current_idx] = choice
    if choice == correct_answer:
        st.session_state.score += 1
    st.session_state.answer_submitted = True
    st.rerun()

def next_question():
    if st.session_state.current_question_index < len(QUESTIONS) - 1:
        st.session_state.current_question_index += 1
        st.session_state.answer_submitted = False
    else:
        st.session_state.quiz_complete = True
    st.rerun()

# --- Main App Logic (Landing Page vs Quiz) ---

if not st.session_state.quiz_started:
    # --- PAGE DE GARDE (LANDING PAGE) ---
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<span class='landing-emoji'>🛡️</span>", unsafe_allow_html=True)
    st.markdown("<h1 class='landing-title'>Souveraineté Numérique</h1>", unsafe_allow_html=True)
    st.markdown("<p class='landing-subtitle'>Reprenez le contrôle de vos données et découvrez les alternatives libres.</p>", unsafe_allow_html=True)
    
    col_spacer_left, col_btn_center, col_spacer_right = st.columns([1, 2, 1])
    with col_btn_center:
        st.write("") # Spacer
        if st.button("Commencer l'aventure 🚀"):
            start_quiz()
    
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; opacity: 0.7;'>
            <p>Ce quiz interactif de <b>10 questions</b> testera vos connaissances sur :</p>
            <p>🔒 La vie privée &nbsp;&nbsp; • &nbsp;&nbsp; 🐧 L'Open Source &nbsp;&nbsp; • &nbsp;&nbsp; 🌱 L'écologie numérique</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- APPLICATION QUIZ ---
    
    # Progress Bar
    if not st.session_state.quiz_complete:
        progress = (st.session_state.current_question_index / len(QUESTIONS))
        st.progress(progress)
        st.caption(f"Question {st.session_state.current_question_index + 1} sur {len(QUESTIONS)}")

    st.divider()

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
                    st.markdown(f"<div class='correct-msg'>👉 Bonne réponse : {q['answer']}</div>", unsafe_allow_html=True)
                
                st.markdown(f"<div class='explanation-box'>ℹ️ <b>Explication :</b> {q['explanation']}</div>", unsafe_allow_html=True)
                
                if "sources" in q and q["sources"]:
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
        choice = st.radio(
            "Choisissez une réponse :",
            question_data['options'],
            key=f"q_{st.session_state.current_question_index}",
            index=None,
            disabled=st.session_state.answer_submitted
        )
        
        # --- Immediate Feedback Section ---
        if st.session_state.answer_submitted:
            user_choice = st.session_state.user_answers.get(st.session_state.current_question_index)
            correct_answer = question_data['answer']
            
            if user_choice == correct_answer:
                st.markdown(f"<div class='success-msg'>✅ Correct !</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='error-msg'>❌ Incorrect !</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='correct-msg'>👉 Bonne réponse : {correct_answer}</div>", unsafe_allow_html=True)
                
            st.markdown(f"<div class='explanation-box'>ℹ️ <b>Explication :</b> {question_data['explanation']}</div>", unsafe_allow_html=True)
                
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
                if st.session_state.current_question_index < len(QUESTIONS) - 1:
                    if st.button("Question Suivante ➡"):
                        next_question()
                else:
                    if st.button("Voir les résultats 🏁"):
                        next_question()
            else:
                if st.button("Valider ➡"):
                    submit_answer()
        with col2:
            pass