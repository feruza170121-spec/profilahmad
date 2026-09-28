import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Инфо-Мат УБТ Базасы", layout="centered")

# Дизайн стилі
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00FF66;
    }
    .stButton>button {
        background-color: #1a1c24;
        color: #00FF66;
        border: 1px solid #00FF66;
        border-radius: 5px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #00FF66;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# Session state инициализациясы
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "tests" not in st.session_state:
    st.session_state.tests = [
        {
            "id": 1,
            "subject": "Қазақстан тарихы",
            "title": "Қазақстан тарихы: №1 Нұсқа",
            "questions": [
                {
                    "question": "Көне түркі жазба ескерткіштерінің ішіндегі ең ірісі:",
                    "options": ["Күлтегін", "Тоныкөк", "Билге қаған", "Махмұт Қашғари"],
                    "correct": 0
                }
            ]
        }
    ]

if "results" not in st.session_state:
    st.session_state.results = []

# --- ПАРОЛЬ ТЕКСЕРУ ---
if not st.session_state.logged_in:
    st.title("🔐 Жүйеге кіру")
    pwd = st.text_input("Парольді енгізіңіз (Hello)", type="password")
    if st.button("Кіру"):
        if pwd == "Hello":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Қате пароль! (Hello деп жазыңыз)")
    st.stop()

# --- БАС МӘЗІР ---
st.sidebar.title("Мәзір")
menu = st.sidebar.radio("Бөлімдер:", ["Тесттер тізімі", "Сұрақ қосу", "Деректерді сақтау / Жүктеу (JSON)"])

if menu == "Тесттер тізімі":
    st.header("📋 Тесттер тізімі")
    subject = st.selectbox("Пәнді таңдаңыз:", ["Қазақстан тарихы", "Математика", "Информатика", "Математикалық сауаттылық"])
    
    filtered = [t for t in st.session_state.tests if t["subject"] == subject]
    if not filtered:
        st.info("Бұл пөнде әзірге тесттер жоқ.")
    else:
        for t in filtered:
            st.subheader(t["title"])
            if st.button(f"Бастау: {t['title']}", key=f"start_{t['id']}"):
                st.session_state.active_test = t
                st.rerun()

elif menu == "Сұрақ қосу":
    st.header("➕ Жаңа сұрақ қосу")
    subj = st.selectbox("Пән:", ["Қазақстан тарихы", "Математика", "Информатика", "Математикалық сауаттылық"])
    t_title = st.text_input("Тест атауы", "Мысалы: Информатика 1-бөлім")
    q_text = st.text_area("Сұрақ мәтіні")
    opt0 = st.text_input("1-ші жауап")
    opt1 = st.text_input("2-ші жауап")
    opt2 = st.text_input("3-ші жауап")
    opt3 = st.text_input("4-ші жауап")
    correct_ans = st.selectbox("Дұрыс жауап нөмірі", [0, 1, 2, 3], format_func=lambda x: f"{x+1}-ші нұсқа")
    
    if st.button("Сұрақты сақтау"):
        if t_title and q_text and opt0 and opt1:
            existing = next((t for t in st.session_state.tests if t["title"] == t_title and t["subject"] == subj), None)
            new_q = {
                "question": q_text,
                "options": [opt0, opt1, opt2, opt3],
                "correct": correct_ans
            }
            if existing:
                existing["questions"].append(new_q)
            else:
                new_t = {
                    "id": len(st.session_state.tests) + 1,
                    "subject": subj,
                    "title": t_title,
                    "questions": [new_q]
                }
                st.session_state.tests.append(new_t)
            st.success("Сұрақ сәтті қосылды!")
        else:
            st.error("Барлық өрістерді толтырыңыз!")

elif menu == "Деректерді сақтау / Жүктеу (JSON)":
    st.header("💾 Деректерді сақтау және қалпына келтіру")
    st.warning("⚠️ Streamlit бұлтында деректер автоматты түрде өшіп қалуы мүмкін. Сұрақтарыңызды жоғалтпау үшін төмендегі батырма арқылы телефонға немесе компьютерге сақтап қойыңыз!")
    
    json_str = json.dumps(st.session_state.tests, ensure_ascii=False, indent=4)
    st.download_button(
        label="📥 Барлық тесттерді файлға сақтау (JSON)",
        data=json_str,
        file_name="ubt_tests_backup.json",
        mime="application/json"
    )
    
    st.markdown("---")
    uploaded = st.file_uploader("📂 Бұрын сақталған JSON файлын жүктеу", type=["json"])
    if uploaded:
        try:
            data = json.load(uploaded)
            st.session_state.tests = data
            st.success("Деректер сәтті қалпына келтірілді!")
            st.rerun()
        except Exception as e:
            st.error(f"Қате: {e}")

# --- ТЕСТІЛЕУ ПРОЦЕСІ ---
if "active_test" in st.session_state:
    test = st.session_state.active_test
    st.header(f"✍️ Тест: {test['title']}")
    
    if "q_idx" not in st.session_state:
        st.session_state.q_idx = 0
    if "user_ans" not in st.session_state:
        st.session_state.user_ans = {}
        
    q_idx = st.session_state.q_idx
    questions = test["questions"]
    
    if q_idx < len(questions):
        q = questions[q_idx]
        st.subheader(f"Сұрақ {q_idx + 1} / {len(questions)}")
        st.write(q["question"])
        
        selected = st.radio("Жауапты таңдаңыз:", q["options"], key=f"radio_{q_idx}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Келесі сұрақ"):
                ans_idx = q["options"].index(selected)
                st.session_state.user_ans[q_idx] = ans_idx
                st.session_state.q_idx += 1
                st.rerun()
        with c2:
            if st.button("Шығу"):
                del st.session_state.active_test
                del st.session_state.q_idx
                del st.session_state.user_ans
                st.rerun()
    else:
        # Нәтиже есептеу
        score = 0
        for idx, q in enumerate(questions):
            if st.session_state.user_ans.get(idx) == q["correct"]:
                score += 1
        
        st.success(f"🎉 Тест аяқталды! Сіздің нәтижеңіз: {score} / {len(questions)}")
        if st.button("Мәзірге оралу"):
            del st.session_state.active_test
            del st.session_state.q_idx
            del st.session_state.user_ans
            st.rerun()
