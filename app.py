import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
import hashlib
import random
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
from PIL import Image
import os
import base64

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="🌾 Gram Seva - Smart Village Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS - Dark Green Theme ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fef9f0 0%, #f5ede3 100%);
    }
    .stSidebar {
        background: linear-gradient(180deg, #0d2b0d 0%, #1a4a1a 50%, #2d6b2d 100%) !important;
    }
    .stSidebar * {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    .stSidebar .stSelectbox div {
        color: #000000 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0d2b0d !important;
        font-family: 'Georgia', serif !important;
        font-weight: 700 !important;
    }
    .stTextInput label, .stTextArea label, .stNumberInput label, .stSelectbox label {
        color: #0d2b0d !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    p, span, div, li, .stMarkdown {
        color: #0d2b0d !important;
        font-weight: 500 !important;
    }
    .stSidebar p, .stSidebar span, .stSidebar div {
        color: #ffffff !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0d2b0d 0%, #1a4a1a 50%, #2d6b2d 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 35px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, #1a4a1a 0%, #2d6b2d 50%, #3d8a3d 100%) !important;
    }
    .village-card {
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1) !important;
        border-left: 6px solid #0d2b0d !important;
        margin: 10px 0 !important;
    }
    .success-box {
        background: #d4edda !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border-left: 6px solid #28a745 !important;
        color: #155724 !important;
    }
    .warning-box {
        background: #fff3cd !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border-left: 6px solid #ffc107 !important;
        color: #856404 !important;
    }
    .info-box {
        background: #d1ecf1 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border-left: 6px solid #17a2b8 !important;
        color: #0c5460 !important;
    }
    .stat-card {
        background: #ffffff !important;
        padding: 20px !important;
        border-radius: 15px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        border-bottom: 5px solid #0d2b0d !important;
    }
    .stat-number {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #0d2b0d !important;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: #ffffff !important;
        border: 2px solid #0d2b0d !important;
        border-radius: 10px !important;
        color: #0d2b0d !important;
        font-weight: 600 !important;
        padding: 12px !important;
    }
    .stSelectbox div {
        background: #ffffff !important;
        border-radius: 10px !important;
        border: 2px solid #0d2b0d !important;
        color: #0d2b0d !important;
    }
    .stDataFrame {
        background: #ffffff !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LANGUAGE SETUP ====================
LANGUAGES = {
    "English": "en",
    "हिंदी": "hi",
    "తెలుగు": "te"
}

def translate_text(text, dest_lang):
    """Translate text to target language using deep-translator"""
    if dest_lang == "en" or not text:
        return text
    try:
        translator = GoogleTranslator(source='auto', target=dest_lang)
        return translator.translate(text)
    except:
        return text

def translate_ui(lang):
    """UI translations for different languages"""
    translations = {
        "en": {
            "app_title": "🌾 Gram Seva - Smart Village Assistant",
            "subtitle": "Empowering Rural India with AI & Data Science",
            "dashboard": "🏠 Dashboard",
            "meetings": "📹 Meeting Videos",
            "complaints": "🗣️ Complaints",
            "schemes": "✅ Schemes",
            "ai_predictor": "🤖 AI Predictor",
            "reports": "📊 Reports",
            "login": "🔐 Login",
            "username": "Username",
            "password": "Password",
            "register": "📝 Register",
            "logout": "🚪 Logout",
            "submit": "📤 Submit",
            "register_complaint": "📝 Register Complaint",
            "your_name": "👤 Your Name",
            "phone": "📱 Phone Number",
            "village": "📍 Village Name",
            "category": "📂 Category",
            "describe": "📝 Describe your complaint",
            "upload_image": "📸 Upload Image (Optional)",
            "speak": "🎤 Speak Complaint",
            "check_eligibility": "🔍 Check Eligibility",
            "income": "💰 Annual Income (₹)",
            "occupation": "👨‍🌾 Occupation",
            "predict": "🔮 Predict Priority",
            "tracking_id": "📌 Tracking ID",
            "priority": "⚡ Priority",
            "sentiment": "💬 Sentiment",
            "status": "Status",
            "date": "Date",
            "resolved": "✅ Resolved",
            "pending": "⏳ Pending",
            "total": "📋 Total"
        },
        "hi": {
            "app_title": "🌾 ग्राम सेवा - स्मार्ट गांव सहायक",
            "subtitle": "एआई और डेटा विज्ञान के साथ सशक्त ग्रामीण भारत",
            "dashboard": "🏠 डैशबोर्ड",
            "meetings": "📹 बैठक वीडियो",
            "complaints": "🗣️ शिकायतें",
            "schemes": "✅ योजनाएं",
            "ai_predictor": "🤖 एआई भविष्यवक्ता",
            "reports": "📊 रिपोर्ट",
            "login": "🔐 लॉगिन",
            "username": "उपयोगकर्ता नाम",
            "password": "पासवर्ड",
            "register": "📝 पंजीकरण",
            "logout": "🚪 लॉगआउट",
            "submit": "📤 जमा करें",
            "register_complaint": "📝 शिकायत दर्ज करें",
            "your_name": "👤 आपका नाम",
            "phone": "📱 फोन नंबर",
            "village": "📍 गांव का नाम",
            "category": "📂 श्रेणी",
            "describe": "📝 अपनी शिकायत लिखें",
            "upload_image": "📸 फोटो अपलोड करें (वैकल्पिक)",
            "speak": "🎤 शिकायत बोलें",
            "check_eligibility": "🔍 पात्रता जांचें",
            "income": "💰 वार्षिक आय (₹)",
            "occupation": "👨‍🌾 व्यवसाय",
            "predict": "🔮 प्राथमिकता भविष्यवाणी",
            "tracking_id": "📌 ट्रैकिंग आईडी",
            "priority": "⚡ प्राथमिकता",
            "sentiment": "💬 भावना",
            "status": "स्थिति",
            "date": "तारीख",
            "resolved": "✅ हल किया गया",
            "pending": "⏳ लंबित",
            "total": "📋 कुल"
        },
        "te": {
            "app_title": "🌾 గ్రామ సేవ - స్మార్ట్ గ్రామ అసిస్టెంట్",
            "subtitle": "AI మరియు డేటా సైన్స్ తో సాధికార గ్రామీణ భారత్",
            "dashboard": "🏠 డాష్‌బోర్డ్",
            "meetings": "📹 సమావేశ వీడియోలు",
            "complaints": "🗣️ ఫిర్యాదులు",
            "schemes": "✅ పథకాలు",
            "ai_predictor": "🤖 AI ప్రిడిక్టర్",
            "reports": "📊 నివేదికలు",
            "login": "🔐 లాగిన్",
            "username": "వినియోగదారు పేరు",
            "password": "పాస్‌వర్డ్",
            "register": "📝 నమోదు",
            "logout": "🚪 లాగౌట్",
            "submit": "📤 సమర్పించండి",
            "register_complaint": "📝 ఫిర్యాదు నమోదు",
            "your_name": "👤 మీ పేరు",
            "phone": "📱 ఫోన్ నంబర్",
            "village": "📍 గ్రామం పేరు",
            "category": "📂 వర్గం",
            "describe": "📝 మీ ఫిర్యాదు వివరించండి",
            "upload_image": "📸 ఫోటో అప్‌లోడ్ చేయండి (ఐచ్ఛికం)",
            "speak": "🎤 ఫిర్యాదు మాట్లాడండి",
            "check_eligibility": "🔍 అర్హత తనిఖీ చేయండి",
            "income": "💰 వార్షిక ఆదాయం (₹)",
            "occupation": "👨‍🌾 వృత్తి",
            "predict": "🔮 ప్రాధాన్యత అంచనా",
            "tracking_id": "📌 ట్రాకింగ్ ID",
            "priority": "⚡ ప్రాధాన్యత",
            "sentiment": "💬 సెంటిమెంట్",
            "status": "స్థితి",
            "date": "తేదీ",
            "resolved": "✅ పరిష్కరించబడింది",
            "pending": "⏳ పెండింగ్",
            "total": "📋 మొత్తం"
        }
    }
    return translations.get(lang, translations["en"])

# ==================== DATABASE SETUP ====================
def init_db():
    conn = sqlite3.connect('gram_seva.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE, password TEXT,
                  role TEXT, village TEXT, created_at TEXT)''')
    
    # Complaints table with image support
    c.execute('''CREATE TABLE IF NOT EXISTS complaints
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, phone TEXT, village TEXT,
                  category TEXT, description TEXT,
                  priority TEXT, sentiment TEXT,
                  language TEXT, status TEXT,
                  date TEXT, tracking_id TEXT,
                  image_path TEXT, voice_text TEXT,
                  resolved_date TEXT, resolved_by TEXT)''')
    
    # Meeting videos table
    c.execute('''CREATE TABLE IF NOT EXISTS meetings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT, description TEXT,
                  video_path TEXT, uploaded_by TEXT,
                  village TEXT, date TEXT, views INTEGER)''')
    
    # Schemes table
    c.execute('''CREATE TABLE IF NOT EXISTS schemes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, name_hi TEXT, name_te TEXT,
                  benefit TEXT, benefit_hi TEXT, benefit_te TEXT,
                  min_income INTEGER, max_income INTEGER,
                  occupation TEXT, document TEXT, application_link TEXT)''')
    
    # Insert users
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        users_data = [
            ("admin", hashlib.sha256("admin123".encode()).hexdigest(), "admin", "Gram Seva HQ"),
            ("ramesh", hashlib.sha256("ramesh123".encode()).hexdigest(), "villager", "Ramgram"),
            ("sita", hashlib.sha256("sita123".encode()).hexdigest(), "villager", "Shantinagar"),
            ("raju", hashlib.sha256("raju123".encode()).hexdigest(), "villager", "Green Valley"),
            ("lakshmi", hashlib.sha256("lakshmi123".encode()).hexdigest(), "villager", "Sundarpur"),
            ("sarpanch", hashlib.sha256("sarpanch123".encode()).hexdigest(), "sarpanch", "Ramgram"),
            ("secretary", hashlib.sha256("secretary123".encode()).hexdigest(), "secretary", "Gram Seva HQ"),
        ]
        for user in users_data:
            c.execute("INSERT INTO users (username, password, role, village, created_at) VALUES (?,?,?,?,?)",
                      (user[0], user[1], user[2], user[3], datetime.now().strftime('%Y-%m-%d %H:%M')))
    
    # Insert schemes
    c.execute("SELECT COUNT(*) FROM schemes")
    if c.fetchone()[0] == 0:
        schemes_data = [
            ("PM-KISAN", "पीएम-किसान", "పీఎం-కిసాన్", 
             "₹6,000 per year for farmers", "किसानों के लिए ₹6,000 सालाना", "రైతులకు సంవత్సరానికి ₹6,000",
             0, 100000, "farmer", "Aadhar, Bank Account", "https://pmkisan.gov.in"),
            ("PMAY-G", "पीएम आवास योजना", "పీఎం ఆవాస్ యోజన", 
             "₹1.20 lakh for house construction", "घर निर्माण के लिए ₹1.20 लाख", "ఇల్లు నిర్మాణానికి ₹1.20 లక్షలు",
             0, 50000, "any", "Aadhar, Income Certificate", "https://pmayg.nic.in"),
            ("Crop Insurance", "फसल बीमा", "పంట భీమా", 
             "Low premium crop coverage", "कम प्रीमियम पर फसल कवरेज", "తక్కువ ప్రీమియం పంట కవరేజీ",
             0, 200000, "farmer", "Land Records", "https://pmfby.gov.in"),
            ("Ration Card", "राशन कार्ड", "రేషన్ కార్డు", 
             "Subsidized food grains", "सब्सिडी वाले खाद्यान्न", "సబ్సిడీ ఆహార ధాన్యాలు",
             0, 30000, "any", "Aadhar, Residence Proof", "https://nfsa.gov.in"),
            ("Skill Development", "कौशल विकास", "నైపుణ్య అభివృద్ధి", 
             "Free vocational training", "मुफ्त व्यावसायिक प्रशिक्षण", "ఉచిత వృత్తి శిక్షణ",
             0, 150000, "any", "Aadhar, Education Certificate", "https://msde.gov.in"),
            ("MGNREGA", "मनरेगा", "మన్రేగా", 
             "100 days guaranteed employment", "100 दिन की गारंटी रोजगार", "100 రోజుల హామీ ఉద్యోగం",
             0, 50000, "laborer", "Aadhar, Bank Account", "https://nrega.nic.in"),
        ]
        c.executemany('''INSERT INTO schemes 
                      (name, name_hi, name_te, benefit, benefit_hi, benefit_te,
                       min_income, max_income, occupation, document, application_link)
                      VALUES (?,?,?,?,?,?,?,?,?,?,?)''', schemes_data)
    
    conn.commit()
    conn.close()

init_db()

# ==================== HELPER FUNCTIONS ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_tracking_id():
    return f"GR{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(10,99)}"

def analyze_sentiment(text):
    positive_words = ['good', 'nice', 'help', 'great', 'thanks', 'excellent', 'happy']
    negative_words = ['bad', 'broken', 'problem', 'issue', 'urgent', 'emergency', 'damage']
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    if neg_count > pos_count:
        return "Urgent 🔴"
    elif pos_count > neg_count:
        return "Positive 😊"
    else:
        return "Neutral 🟡"

def predict_priority(text, category):
    high_priority_words = ['accident', 'injured', 'water', 'broken', 'collapse', 'emergency', 'flood', 'fire']
    medium_priority_words = ['repair', 'fix', 'damage', 'issue', 'problem']
    text_lower = text.lower()
    high_count = sum(1 for word in high_priority_words if word in text_lower)
    medium_count = sum(1 for word in medium_priority_words if word in text_lower)
    if high_count >= 1:
        return "High 🔴"
    elif medium_count >= 1 or category in ["Water", "Electricity"]:
        return "Medium 🟡"
    else:
        return "Low 🟢"

def speech_to_text_widget():
    audio = mic_recorder(start_prompt="🎤 Speak", stop_prompt="⏹ Stop", key='voice')
    if audio:
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(io.BytesIO(audio['bytes'])) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
        except Exception:
            return "Could not understand audio"
    return None

# ==================== AUTHENTICATION ====================
def login():
    st.sidebar.image("https://img.icons8.com/color/96/000000/india.png", width=80)
    st.sidebar.title("🌾 Gram Seva")
    st.sidebar.markdown("---")
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
    
    if not st.session_state.logged_in:
        st.sidebar.subheader("🔐 Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            login_btn = st.button("Login", use_container_width=True)
        with col2:
            show_register = st.button("New User?", use_container_width=True)
        
        if login_btn:
            if username and password:
                conn = sqlite3.connect('gram_seva.db')
                c = conn.cursor()
                hashed = hash_password(password)
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
                user = c.fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.role = user[3]
                    st.session_state.village = user[4]
                    st.sidebar.success(f"✅ Welcome {username}!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Invalid credentials")
            else:
                st.sidebar.warning("Please fill all fields")
        
        if show_register:
            st.sidebar.markdown("---")
            st.sidebar.subheader("📝 Register")
            new_username = st.sidebar.text_input("Choose Username")
            new_password = st.sidebar.text_input("Choose Password", type="password")
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            role = st.sidebar.selectbox("Role", ["villager", "sarpanch", "secretary"])
            village = st.sidebar.text_input("Village Name")
            
            if st.sidebar.button("Register", use_container_width=True):
                if new_username and new_password and village:
                    if new_password == confirm_password:
                        conn = sqlite3.connect('gram_seva.db')
                        c = conn.cursor()
                        c.execute("SELECT * FROM users WHERE username=?", (new_username,))
                        if c.fetchone():
                            st.sidebar.error("❌ Username exists!")
                        else:
                            hashed = hash_password(new_password)
                            c.execute("INSERT INTO users (username, password, role, village, created_at) VALUES (?,?,?,?,?)",
                                      (new_username, hashed, role, village, datetime.now().strftime('%Y-%m-%d %H:%M')))
                            conn.commit()
                            conn.close()
                            st.sidebar.success("✅ Registered! Please login.")
                            st.rerun()
                    else:
                        st.sidebar.error("❌ Passwords don't match!")
                else:
                    st.sidebar.warning("Please fill all fields")
        return False
    return True

def logout():
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

# ==================== VILLAGER DASHBOARD ====================
def villager_dashboard(lang, ui):
    st.success(f"👋 Welcome {st.session_state.username}!")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        ui["complaints"], ui["schemes"], ui["ai_predictor"], 
        "📹 Meeting Videos", "📊 My Complaints"
    ])
    
    with tab1:
        st.header(ui["register_complaint"])
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(ui["your_name"])
            phone = st.text_input(ui["phone"])
            village = st.text_input(ui["village"], value=st.session_state.village)

            st.write(ui["speak"])
            voice_text = speech_to_text_widget()
            if voice_text and "error" not in voice_text.lower():
                st.session_state['voice_text'] = voice_text
                st.success(f"Heard: {voice_text}")

        with col2:
            categories = ["Road", "Water", "Electricity", "Garbage", "Health", "Other"]
            category = st.selectbox(ui["category"], categories)
            default_text = st.session_state.get('voice_text', '')
            complaint_text = st.text_area(ui["describe"], height=100, value=default_text)
            uploaded_image = st.file_uploader(ui["upload_image"], type=['jpg', 'jpeg', 'png'])


            
            if st.button(ui["submit"], use_container_width=True):
                if name and complaint_text:
                    priority = predict_priority(complaint_text, category)
                    sentiment = analyze_sentiment(complaint_text)
                    tracking_id = generate_tracking_id()
                    
                    image_path = None
                    if uploaded_image:
                        os.makedirs("uploads", exist_ok=True)
                        image_path = f"uploads/{tracking_id}.jpg"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_image.getbuffer())
                    
                    conn = sqlite3.connect('gram_seva.db')
                    c = conn.cursor()
                    c.execute('''INSERT INTO complaints 
                              (name, phone, village, category, description, priority, sentiment, 
                               language, status, date, tracking_id, image_path, voice_text)
                              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (name, phone, village, category, complaint_text, priority, sentiment,
                               lang, "Registered", datetime.now().strftime('%Y-%m-%d %H:%M'), 
                               tracking_id, image_path, complaint_text))
                    conn.commit()
                    conn.close()
                    
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ <strong>Complaint Registered!</strong><br>
                        📌 {ui["tracking_id"]}: <strong>{tracking_id}</strong><br>
                        ⚡ {ui["priority"]}: {priority}<br>
                        💬 {ui["sentiment"]}: {sentiment}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if uploaded_image:
                        st.image(uploaded_image, caption="Uploaded Image", width=200)
                    
                    st.session_state['voice_text'] = ''
                else:
                    st.warning("⚠️ Please fill all fields")
    
    with tab2:
        st.header(ui["check_eligibility"])
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input(ui["income"], min_value=0, max_value=1000000, step=10000)
        with col2:
            occupation = st.selectbox(ui["occupation"], ["farmer", "laborer", "business", "student", "other"])
        
        if st.button(ui["check_eligibility"], use_container_width=True):
            if income > 0:
                conn = sqlite3.connect('gram_seva.db')
                c = conn.cursor()
                c.execute('''SELECT * FROM schemes WHERE min_income <= ? AND max_income >= ?
                          AND (occupation = ? OR occupation = 'any')''', (income, income, occupation))
                results = c.fetchall()
                conn.close()
                if results:
                    for scheme in results:
                        name = scheme[1] if lang == "en" else scheme[2] if lang == "हिंदी" else scheme[3]
                        benefit = scheme[4] if lang == "en" else scheme[5] if lang == "हिंदी" else scheme[6]
                        st.markdown(f"""
                        <div class="village-card">
                            <h4>{name}</h4>
                            <p>💡 {benefit}</p>
                            <p>📄 Documents: {scheme[9]}</p>
                            <a href="{scheme[10]}" target="_blank">🔗 Apply Online</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No schemes found")
            else:
                st.warning("Please enter income")
    
    with tab3:
        st.header(ui["ai_predictor"])
        col1, col2 = st.columns(2)
        with col1:
            complaint_text = st.text_area("Describe the complaint", height=100)
            category = st.selectbox("Category", ["Road", "Water", "Electricity", "Garbage", "Health", "Other"])
        with col2:
            if st.button(ui["predict"], use_container_width=True):
                if complaint_text:
                    priority = predict_priority(complaint_text, category)
                    sentiment = analyze_sentiment(complaint_text)
                    st.markdown(f"""
                    <div class="village-card">
                        <h3>📊 Analysis</h3>
                        <p><strong>Priority:</strong> {priority}</p>
                        <p><strong>Sentiment:</strong> {sentiment}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Enter complaint text")
    
    with tab4:
        st.header("📹 Village Meeting Videos")
        conn = sqlite3.connect('gram_seva.db')
        videos = pd.read_sql(f"SELECT * FROM meetings WHERE village='{st.session_state.village}' OR village='All' ORDER BY date DESC", conn)
        conn.close()
        
        if not videos.empty:
            for _, video in videos.iterrows():
                st.markdown(f"""
                <div class="village-card">
                    <h4>📹 {video['title']}</h4>
                    <p>{video['description']}</p>
                    <p><small>📅 {video['date']} | 👤 {video['uploaded_by']}</small></p>
                </div>
                """, unsafe_allow_html=True)
                
                if video['video_path'] and os.path.exists(video['video_path']):
                    st.video(video['video_path'])
                else:
                    st.info("📹 Video not available locally. Contact Sarpanch.")
        else:
            st.info("No meeting videos available for your village")
    
    with tab5:
        st.header("📊 My Complaints")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql(f"SELECT tracking_id, category, description, priority, status, date FROM complaints WHERE village='{st.session_state.village}' ORDER BY date DESC", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No complaints registered yet")

# ==================== SARPANCH DASHBOARD ====================
def sarpanch_dashboard(lang, ui):
    st.success(f"👋 Welcome {st.session_state.username}!")
    st.info("📋 View complaints and upload meeting videos for your village")
    
    tab1, tab2, tab3 = st.tabs(["📋 Complaints", "✅ Resolve", "📹 Upload Meeting Video"])
    
    with tab1:
        st.header("📋 Village Complaints")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql(f"SELECT * FROM complaints WHERE village='{st.session_state.village}' ORDER BY date DESC", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", len(df))
            with col2:
                pending = len(df[df['status'] == 'Registered'])
                st.metric("Pending", pending)
            with col3:
                resolved = len(df[df['status'] == 'Resolved'])
                st.metric("Resolved", resolved)
            
            for _, row in df.iterrows():
                if row['image_path'] and os.path.exists(row['image_path']):
                    st.image(row['image_path'], caption=f"Image for {row['tracking_id']}", width=200)
        else:
            st.info("No complaints in your village")
    
    with tab2:
        st.header("✅ Resolve Complaints")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql(f"SELECT id, tracking_id, name, category, description, priority, status, image_path FROM complaints WHERE village='{st.session_state.village}' AND status='Registered'", conn)
        conn.close()
        
        if not df.empty:
            tracking_ids = df['tracking_id'].tolist()
            selected = st.selectbox("Select complaint to resolve", tracking_ids)
            
            if selected:
                complaint = df[df['tracking_id'] == selected].iloc[0]
                st.markdown(f"""
                <div class="village-card">
                    <h4>📌 {complaint['name']}</h4>
                    <p><strong>Category:</strong> {complaint['category']}</p>
                    <p><strong>Priority:</strong> {complaint['priority']}</p>
                    <p><strong>Description:</strong> {complaint['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if complaint['image_path'] and os.path.exists(complaint['image_path']):
                    st.image(complaint['image_path'], caption="Complaint Image", width=300)
                
                if st.button("✅ Mark as Resolved", use_container_width=True):
                    conn = sqlite3.connect('gram_seva.db')
                    c = conn.cursor()
                    c.execute("UPDATE complaints SET status='Resolved', resolved_date=?, resolved_by=? WHERE id=?",
                              (datetime.now().strftime('%Y-%m-%d %H:%M'), st.session_state.username, complaint['id']))
                    conn.commit()
                    conn.close()
                    st.success("✅ Complaint marked as Resolved!")
                    st.rerun()
        else:
            st.info("🎉 No pending complaints!")
    
    with tab3:
        st.header("📹 Upload Meeting Video")
        video_title = st.text_input("Video Title")
        video_description = st.text_area("Description")
        video_file = st.file_uploader("Upload Video (MP4)", type=['mp4', 'avi', 'mov'])
        
        if st.button("📤 Upload Video", use_container_width=True):
            if video_title and video_file:
                os.makedirs("videos", exist_ok=True)
                video_path = f"videos/{datetime.now().strftime('%Y%m%d%H%M%S')}_{video_file.name}"
                with open(video_path, "wb") as f:
                    f.write(video_file.getbuffer())
                
                conn = sqlite3.connect('gram_seva.db')
                c = conn.cursor()
                c.execute("INSERT INTO meetings (title, description, video_path, uploaded_by, village, date, views) VALUES (?,?,?,?,?,?,?)",
                          (video_title, video_description, video_path, st.session_state.username, 
                           st.session_state.village, datetime.now().strftime('%Y-%m-%d %H:%M'), 0))
                conn.commit()
                conn.close()
                st.success("✅ Video uploaded successfully!")
                st.video(video_path)
            else:
                st.warning("Please fill all fields")

# ==================== SECRETARY DASHBOARD ====================
def secretary_dashboard(lang, ui):
    st.success(f"👋 Welcome {st.session_state.username}!")
    
    tab1, tab2 = st.tabs(["📝 Meeting Minutes", "📊 All Complaints"])
    
    with tab1:
        st.header("📝 Meeting Minutes Generator")
        uploaded_file = st.file_uploader("📂 Upload meeting audio", type=['wav', 'mp3'])
        if uploaded_file:
            st.success("✅ File uploaded!")
            sample_summary = "Meeting held on June 30, 2026. 15 villagers attended. Decisions: ₹2 lakh approved for pond repair. Next meeting: July 15."
            st.subheader("📋 Summary")
            st.markdown(f'<div class="village-card">{translate_text(sample_summary, LANGUAGES[lang])}</div>', unsafe_allow_html=True)
    
    with tab2:
        st.header("📊 All Complaints")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql("SELECT * FROM complaints ORDER BY date DESC", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            col1, col2 = st.columns(2)
            with col1:
                status_counts = df['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                category_counts = df['category'].value_counts()
                fig = px.bar(category_counts, x=category_counts.index, y=category_counts.values)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No complaints registered")

# ==================== ADMIN DASHBOARD ====================
def admin_dashboard(lang, ui):
    st.success(f"👋 Welcome Admin!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 All Complaints", "👥 Users", "📊 Reports"])
    
    with tab1:
        conn = sqlite3.connect('gram_seva.db')
        complaints_df = pd.read_sql("SELECT * FROM complaints ORDER BY date DESC LIMIT 100", conn)
        schemes_df = pd.read_sql("SELECT * FROM schemes", conn)
        users_df = pd.read_sql("SELECT * FROM users", conn)
        meetings_df = pd.read_sql("SELECT * FROM meetings", conn)
        conn.close()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:30px;">📋</div>
                <div class="stat-number">{len(complaints_df)}</div>
                <div>Total Complaints</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            pending = len(complaints_df[complaints_df['status'] == 'Registered']) if not complaints_df.empty else 0
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:30px;">⏳</div>
                <div class="stat-number">{pending}</div>
                <div>Pending</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            resolved = len(complaints_df[complaints_df['status'] == 'Resolved']) if not complaints_df.empty else 0
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:30px;">✅</div>
                <div class="stat-number">{resolved}</div>
                <div>Resolved</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:30px;">👥</div>
                <div class="stat-number">{len(users_df)}</div>
                <div>Users</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if not complaints_df.empty:
                category_counts = complaints_df['category'].value_counts()
                fig = px.pie(values=category_counts.values, names=category_counts.index)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if not complaints_df.empty:
                complaints_df['month'] = pd.to_datetime(complaints_df['date']).dt.strftime('%b %Y')
                monthly = complaints_df.groupby('month').size().reset_index(name='count')
                fig = px.line(monthly, x='month', y='count', markers=True)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("📋 All Complaints")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql("SELECT * FROM complaints ORDER BY date DESC", conn)
        conn.close()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            pending = df[df['status'] == 'Registered']
            if not pending.empty:
                selected = st.selectbox("Select complaint to resolve", pending['tracking_id'].tolist())
                if selected:
                    complaint = pending[pending['tracking_id'] == selected].iloc[0]
                    if st.button("✅ Mark as Resolved"):
                        conn = sqlite3.connect('gram_seva.db')
                        c = conn.cursor()
                        c.execute("UPDATE complaints SET status='Resolved', resolved_date=?, resolved_by=? WHERE id=?",
                                  (datetime.now().strftime('%Y-%m-%d %H:%M'), "Admin", complaint['id']))
                        conn.commit()
                        conn.close()
                        st.success("✅ Resolved!")
                        st.rerun()
        else:
            st.info("No complaints")
    
    with tab3:
        st.header("👥 Registered Users")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql("SELECT username, role, village, created_at FROM users", conn)
        conn.close()
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab4:
        st.header("📊 Reports")
        conn = sqlite3.connect('gram_seva.db')
        df = pd.read_sql("SELECT * FROM complaints", conn)
        conn.close()
        if not df.empty:
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Full Report CSV", data=csv, 
                             file_name=f"report_{datetime.now().strftime('%Y%m%d')}.csv", 
                             mime="text/csv", use_container_width=True)

# ==================== MAIN APP ====================
def main():
    if not login():
        st.stop()
    
    logout()
    
    lang = st.sidebar.selectbox("🌍 Select Language", ["English", "हिंदी", "తెలుగు"])
    ui = translate_ui(lang)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="background:rgba(255,255,255,0.1);padding:10px;border-radius:10px;">
        <small>👤 {st.session_state.username}</small><br>
        <small>🏘️ {st.session_state.role.upper()}</small><br>
        <small>📍 {st.session_state.village}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.title(translate_text(ui["app_title"], LANGUAGES[lang]))
    st.markdown(f'<p style="color:#555;">{translate_text(ui["subtitle"], LANGUAGES[lang])}</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    role = st.session_state.role
    
    if role == "villager":
        villager_dashboard(lang, ui)
    elif role == "sarpanch":
        sarpanch_dashboard(lang, ui)
    elif role == "secretary":
        secretary_dashboard(lang, ui)
    elif role == "admin":
        admin_dashboard(lang, ui)
    else:
        st.warning("Unknown role")

if __name__ == "__main__":
    main()
