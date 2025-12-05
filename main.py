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
        "bg_color": "#0B0E14",          # Noir bleuté professionnel
        "text_color": "#F8F8F8",        # Blanc doux très lisible
        "card_bg": "#1A1E26",           # Gris foncé bleuté
        "card_border": "#343A40",

        "option_bg": "#1C212B",
        "option_hover": "#2B3340",

        "success_bg": "#153A29",
        "success_text": "#A5F2C1",
        "success_border": "#2BC56D",

        "error_bg": "#3A1515",
        "error_text": "#FF9999",
        "error_border": "#E44444",

        "info_bg": "#11263F",
        "info_text": "#96C9FF",
        "info_border": "#468FE3",

        "sources_bg": "#2E230C",
        "sources_text": "#FFD78D",
        "sources_border": "#7A5C1E",

        "link_color": "#B58CFF",

        "btn_shadow": "rgba(255,255,255,0.08)",
        "radio_label_bg": "#1A1E26",

        "btn_bg": "#6A49C9",
        "btn_text": "#FFFFFF",
        "btn_hover": "#8459FF",
    }

    btn_label = "☀️"
else:
    theme = {
        "bg_color": "#FFFFFF",
        "text_color": "#2B2B2B",
        "card_bg": "#F2F4FA",       # Bleu lavé moderne
        "card_border": "#E7E9F0",

        "option_bg": "#FFFFFF",
        "option_hover": "#F6F2FE",   # Léger violet clair hover

        "success_bg": "#D6FFEA",
        "success_text": "#105C35",
        "success_border": "#4AD771",

        "error_bg": "#FFE1E1",
        "error_text": "#8B1F1F",
        "error_border": "#E37474",

        "info_bg": "#DCECFF",
        "info_text": "#0E3A71",
        "info_border": "#80BAFF",

        "sources_bg": "#FFF7D1",
        "sources_text": "#705003",
        "sources_border": "#FFD972",

        "link_color": "#3B2077",

        "btn_shadow": "rgba(0,0,0,0.1)",
        "radio_label_bg": "#FFFFFF",

        "btn_bg": "#6A49C9",
        "btn_text": "#FFFFFF",
        "btn_hover": "#8459FF",
    }

    btn_label = "🌙"


# --- Custom CSS (Dynamic) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;600&display=swap');

    html, body, p, h1, h2, h3, h4, h5, h6, .stMarkdown, .stButton button, .stRadio label {{
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

    .stButton>button,
    .stButton>button span {{
        color: {theme['btn_text']} !important;
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
            "https://www.francenum.gouv.fr/formations/initiez-vous-linux",
            "https://video.echirolles.fr/w/hVykGUtRZqRen6eiutqRvQ"
        ]
    },
    {
        "question": "Quel phénomène peut rendre un appareil matériellement fonctionnel mais inutilisable faute de compatibilité ou de mises à jour ?",
        "options": [
            "L’obsolescence logicielle",
            "La surcharge énergétique",
            "Le redimensionnement matériel",
            "La virtualisation automatique"
        ],
        "answer": "L’obsolescence logicielle",
        "explanation": "L’obsolescence logicielle se produit lorsqu’un équipement encore fonctionnel ne reçoit plus de correctifs, de pilotes ou de mises à jour logicielles nécessaires à son utilisation. Cela pousse à remplacer l’appareil alors qu’il fonctionne encore matériellement.",
        "sources": [
            "https://tube.numerique.gouv.fr/w/wCyvx5RNXQrwBj6J378WTF",
            "https://www.radiofrance.fr/franceinter/podcasts/le-grand-reportage-de-france-inter/le-grand-reportage-du-mardi-14-octobre-2025-4136495"
        ]
    },
    {
        "question": "Quel navigateur web est développé par une fondation à but non lucratif et protège par défaut contre le pistage ?",
        "options": ["Google Chrome", "Mozilla Firefox", "Microsoft Edge", "Safari"],
        "answer": "Mozilla Firefox",
        "explanation": "Firefox est développé par la fondation Mozilla. Contrairement à Chrome ou Edge, son modèle économique ne repose pas sur la vente de vos données publicitaires.",
        "sources": [
            "https://www.mozilla.org/fr/about/",
            "https://www.lemonde.fr/pixels/article/2024/11/09/un-geste-politique-pourquoi-firefox-continue-d-etre-utilise-malgre-l-hegemonie-de-chrome_6384639_4408996.html"
        ]
    },
    {
        "question": "Quel moteur de recherche promet de ne pas tracer vos requêtes ni de créer de profil publicitaire ?",
        "options": ["Google", "Bing", "DuckDuckGo", "Yahoo"],
        "answer": "DuckDuckGo",
        "explanation": "DuckDuckGo (ou Qwant en France) est un moteur de recherche qui respecte la vie privée en ne stockant pas votre historique de recherche.",
        "sources": [
            "https://duckduckgo.com/privacy",
            "https://lesbases.anct.gouv.fr/ressources/decouvrir-les-principaux-moteurs-de-recherche"
        ]
    },
    {
        "question": "Dans le cycle de vie d’un ordinateur portable, quelle phase représente en moyenne l’impact carbone le plus élevé ?",
        "options": ["Son transport jusqu'au magasin", "Son utilisation quotidienne", "Sa fabrication", "Son recyclage en fin de vie"],
        "answer": "Sa fabrication",
        "explanation": "Plus de 70 % de l'impact carbone d’un ordinateur provient de la fabrication, en raison de l’extraction de métaux rares, de la production de composants et de l’assemblage.",
        "sources": [
            "https://www.data.gouv.fr/fr/reuses/quelle-est-lempreinte-carbone-dun-ordinateur-portable/"
        ]
    },
    {
        "question": "Quelle est la meilleure manière de faire durer son matériel informatique tout en réduisant son impact écologique ?",
        "options": [
            "Avec un ordinateur haut de gamme",
            "Le reconditionner ou remplacer les composants usés",
            "Multiplier les appareils pour répartir l’usage et éviter l’usure",
            "Installer davantage de logiciels pour optimiser les performances"
        ],
        "answer": "Le reconditionner ou remplacer les composants usés",
        "explanation": "Prolonger la durée de vie d’un appareil en réparant ou remplaçant les pièces permet d'éviter la fabrication d’un nouveau produit, qui représente la majeure partie de l’impact environnemental. Les autres comportements conduisent à une surconsommation et un impact plus élevé.",
        "sources": [
            "https://www.economie.gouv.fr/dgccrf/laction-de-la-dgccrf/les-enquetes/produits-reconditionnes-quels-engagements-vis-vis-du",
            "https://www.notre-environnement.gouv.fr/actualites/breves/article/une-seconde-vie-pour-le-materiel-informatique-de-l-etat-et-des-collectivites",
            "https://www.francenum.gouv.fr/guides-et-conseils/pilotage-de-lentreprise/materiel-informatique/comment-optimiser-la-gestion-de"
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
            "https://www.notre-environnement.gouv.fr/actualites/breves/article/quelle-est-la-consommation-d-electricite-des-datacenters-en-france",
            "https://www.statistiques.developpement-durable.gouv.fr/la-consommation-delectricite-des-centres-de-donnees-entre-2018-et-2023#:~:text=Ils%20consomment%20au%20total%20pr%C3%A8s,totale%20utilis%C3%A9e%20par%20ces%20infrastructures."
        ]
    },
    {
        "question": "Quel robot conversationnel ne stocke pas vos données lorsque vous discutez avec lui ?",
        "options": ["ChatGPT", "Gemini", "Copilot AI", "Aucun"],
        "answer": "Aucun",
        "explanation": "Tous les modèles de chat modernes conservent au minimum des traces techniques (logs, métadonnées, usage) pour améliorer les services ou surveiller l’usage. Aucun ne fonctionne en interaction directe sans captation minimale. Il est important de savoir qu'on peut s'opposer à la réutilisation de nos données !",
        "sources": [
            "https://www.cnil.fr/fr/ia-comment-sopposer-la-reutilisation-de-ses-donnees-personnelles-entrainement-agent-conversationnel#:~:text=application%20mobile,-La%20notion%20d&text=En%20savoir%20plus-,%2C%20rendez%2Dvous%20dans%20les%20%C2%AB%20Param%C3%A8tres%20%C2%BB%20du%20compte%2C,Activer%20le%20partage%20de%20donn%C3%A9es%20%C2%BB."
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

    # Bouton centré
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
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