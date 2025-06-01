import nltk
from nltk.corpus import words
import re
import streamlit as st
import joblib
import random


# Ensure you have the word list from NLTK
nltk.download('words')

# Load the set of valid English words
valid_words = set(words.words())

# Function to check if the text is gibberish
def is_gibberish(text):
    if re.fullmatch(r'[\d\s\W]+', text):
        return True
    words_in_text = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    if not words_in_text:
        return True
    real_word_count = sum(1 for word in words_in_text if word in valid_words)
    return real_word_count / len(words_in_text) < 0.5  # allow up to 50% unknown

# Load trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Streamlit setup
st.set_page_config(page_title="Sentiment Analyzer🧠", layout="wide")

st.markdown("""
    <style>
            center-title {
    font-size: 100px;
    font-weight: bold;
    text-align: center;
}

/* Increase the font size for the subtitle */
.subtitle {
    font-size: 40px;
    text-align: center;
}
    .stApp {
        background: linear-gradient(135deg, #ffc0cb, #ffe6f0);
        background-size: 400% 400%;
        animation: gradient-shine 8s ease infinite;
    }

    @keyframes gradient-shine {
        0% {background-position: 0% 50%}
        50% {background-position: 100% 50%}
        100% {background-position: 0% 50%}
    }

    .positive-glow, .negative-glow, .neutral-glow {
        font-size:40px;
        color: black;
        display: inline-block;
        font-weight: bold;
    }

    .positive-glow {
        text-shadow: 0 0 10px #2ecc71, 0 0 20px #2ecc71;
        animation: pulse-positive 1.5s infinite;
    }

    .negative-glow {
        text-shadow: 0 0 10px #e74c3c, 0 0 20px #e74c3c;
        animation: pulse-negative 1.5s infinite;
    }

    .neutral-glow {
        text-shadow: 0 0 10px #f1c40f, 0 0 20px #f39c12;
        animation: pulse-neutral 1.5s infinite;
    }

    @keyframes pulse-positive {
        0%, 100% {transform: scale(1);}
        50% {transform: scale(1.05);}
    }

    @keyframes pulse-negative {
        0%, 100% {transform: scale(1);}
        50% {transform: scale(1.05);}
    }

    @keyframes pulse-neutral {
        0%, 100% {transform: scale(1);}
        50% {transform: scale(1.05);}
    }

    @keyframes pop-in {
        0% { transform: scale(0.5); opacity: 0; }
        60% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); }
    }
     sentiment_word{
            font-size: 100px;
            
            }

    .sentiment-result {
        font-size: 10px;
        margin-top: 20px;
        padding: 10px;
        border-radius: 30px;
        text-align: center;
        border: 2px solid black;
        background-color: rgba(255, 255, 255, 0.7);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        animation: pop-in 0.6s ease-out;
    }

    .emoji-burst {
        position: fixed;
        font-size: 1000px;
        animation: burst-fade 2s ease forwards;
        z-index: 9999;
    }

    @keyframes burst-fade {
        0% {transform: scale(0); opacity: 0;}
        30% {transform: scale(1.5); opacity: 1;}
        100% {transform: scale(0.8); opacity: 0;}
    }

    .small-emoji {
        position: fixed;
        font-size: 20px;
        animation: blink-emoji 2s ease-in-out forwards;
    }

    @keyframes blink-emoji {
        0% { opacity: 0; }
        30% { opacity: 1; }
        100% { opacity: 0; }
    }

    input[type="text"] {
        border: none !important;
        border-radius: 1000px important;
        box-shadow: 0 0 15px #ff69b4 !important;
        padding: 10px;
        font-size: 28px;
        font-weight: bold;
        background-color: #fffafc;
    }

    div[data-baseweb="button"] button {
        color: white;
        font-size: 24px;
        font-weight: bold;
        border-radius: 100px;
        padding: 30px 50px;
        border: none;
        transition: all 0.3s ease;
        margin: 0 auto;
        background-color: #ff69b4 !important;
    }

    div[data-baseweb="button"] {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    .center-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 32px;
        font-weight: normal;
    }
    </style>
""", unsafe_allow_html=True)

POSITIVE_WORDS = ["Amazing", "Fantastic", "Brilliant", "Wonderful", "Excellent", "Joyful", "Happy", "Love", "Perfect", "Awesome", "Fresh"]
NEGATIVE_WORDS = ["Terrible", "Awful", "Horrible", "Bad", "Worst", "Sad", "Angry", "Hate", "Disgusting", "Ugly", "Look ugly", "sad"]
NEUTRAL_WORDS = ["Okay", "Alright", "Fine", "Average", "Meh", "Neutral", "So-so", "Normal", "Regular", "Standard", "Fair","Either"]

ALWAYS_POSITIVE = {"amazing", "fantastic", "wonderful", "excellent", "happy", "love", "awesome", "perfect", "brilliant", "joyful", "fresh"}
ALWAYS_NEGATIVE = {"hate", "ugly", "disgusting", "not good", "horrible", "worst", "awful", "terrible", "angry", "bad", "look ugly", "sad"}

if "emoji_toggle" not in st.session_state:
    st.session_state["emoji_toggle"] = False

def get_sentiment(text):
    text_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))
    if words & ALWAYS_POSITIVE and words & ALWAYS_NEGATIVE:
        return "mixed", None
    elif words & ALWAYS_POSITIVE:
        return 1, None
    elif words & ALWAYS_NEGATIVE:
        return -1, None
    cleaned_input = text_lower.strip()
    vectorized_input = vectorizer.transform([cleaned_input])
    prediction = model.predict(vectorized_input)[0]
    return prediction, None

# Title and subtitle centered
st.markdown('<div class="center-title">Sentiment Analyzer🧠 </div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get the analysis of your sentence</div>', unsafe_allow_html=True)

user_input = st.text_input("", key="custom_input")

if st.button("Analyse"):
    st.session_state["show_result"] = True
    st.session_state["emoji_toggle"] = not st.session_state["emoji_toggle"]

if st.session_state.get("show_result", False):
    if not user_input.strip():
        st.warning("⚠️ Please enter a sentence.")
        st.session_state["show_result"] = False
    elif is_gibberish(user_input):
        st.error("❌ The sentiment cannot be predicted for meaningless text or numbers.")
        st.session_state["show_result"] = False
    else:
        sentiment, _ = get_sentiment(user_input)

        has_pos = any(word in user_input.lower() for word in ALWAYS_POSITIVE)
        has_neg = any(word in user_input.lower() for word in ALWAYS_NEGATIVE)

        if sentiment == "mixed":
            sentiment_word = "It is both positive as well as negative!!!"
            sentiment_display = f'<span class="neutral-glow">{sentiment_word}</span> ❤️😞'
            gradient = "linear-gradient(135deg, #2ecc71, #e74c3c)"
            button_color = "#a569bd"
            box_shadow = "0 0 15px #a569bd"
            emoji = "❤️😞"
        elif sentiment == 1:
            sentiment_word = "It is positive!!!!"
            sentiment_display = f'<span class="positive-glow">{sentiment_word}</span> ❤️'
            gradient = "linear-gradient(135deg, #2ecc71, #27ae60)"
            button_color = "#2ecc71"
            box_shadow = "0 0 15px #2ecc71"
            emoji = "❤️"
        elif sentiment == -1:
            sentiment_word = "oops It is negative!!!!"
            sentiment_display = f'<span class="negative-glow"   font="40px">{sentiment_word}</span> 😞'
            gradient = "linear-gradient(135deg, #e74c3c, #c0392b)"
            button_color = "#e74c3c"
            box_shadow = "0 0 15px #e74c3c"
            emoji = "😞"
        else:
            sentiment_word = "It is neutral!!!"
            sentiment_display = f'<span class="neutral-glow" font="40px">{sentiment_word}</span> 🙂'
            gradient = "linear-gradient(135deg, #f1c40f, #f39c12)"
            button_color = "#f1c40f"
            box_shadow = "0 0 15px #f1c40f"
            emoji = "🙂"

        st.markdown(f"""
            <style>
                .stApp {{
                    background: {gradient};
                }}
                input[type="text"] {{
                    box-shadow: {box_shadow} !important;
                    border-color: {button_color} !important;
                }}
                div[data-baseweb='button'] button {{
                    background-color: {button_color} !important;
                    color: white !important;
                }}
            </style>
        """, unsafe_allow_html=True)

        emoji_burst = ''.join([f"<div class='small-emoji' style='top:{random.randint(10, 90)}%; left:{random.randint(5, 95)}%; color:{button_color};'>{emoji}</div>" for _ in range(50)])

        if st.session_state.get("emoji_toggle", False):
            st.markdown(emoji_burst, unsafe_allow_html=True)

        st.markdown(f"""
            <div class='emoji-burst' style='font-size:100px; color:{button_color}; top:50%; left:50%; transform: translate(-50%, -50%); animation: burst-fade 2s ease forwards;'>
                {emoji}
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="sentiment-result" style="background-color:{button_color}; color:white;">
                <p style="font-size:35px; font-weight:bold;">Sentiment: {sentiment_display}</p>
            </div>
        """, unsafe_allow_html=True)
