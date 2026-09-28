import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Инфо-Мат УБТ Базасы", layout="centered")

# Қара түсті және жасыл элементтерге арналған CSS стилі
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #00FF66;
    }
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
        padding-top: 5px;
        width: 220px !important;
    }
    [data-testid="stSidebar"] * {
        color: #00FF66 !important;
    }
    h1, h2, h3, p, label {
        color: #00FF66 !important;
    }
    .stButton>button {
        background-color: #222222;
        color: #00FF66;
        border: 1px solid #00FF66;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 13px;
    }
    .stButton>button:hover {
        background-color: #00FF66;
        color: #121212;
    }
    </style>
""", unsafe_allow_html=True)

if "username" not in st.session_state:
    st.session_state.username = "Аты-Жөніңіз"
if "avatar" not in st.session_state:
    st.session_state.avatar = "https://via.placeholder.com/40"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Тесттер тізімі"

if "tests" not in st.session_state:
    st.session_state.tests = [
        {
            "id": 1,
            "subject": "Математика тарихы",
            "title": "Математика тарихы: Ежелгі кезең",
            "questions": [
                {
                    "question": "Пифагор теоремасы қай халыққа ерте заманнан белгілі болған?",
                    "options": ["Вавилон және Қытай", "Тек Грекия", "Рим империясы", "Мысыр ғана"],
                    "correct": 0
                }
            ]
        },
        {
            "id": 2,
            "subject": "Математика тарихы",
            "title": "Математика тарихы: Орта ғасырлар және Шығыс ғалымдары",
            "questions": [
                {
                    "question": "Әл-Хорезми еңбегінен шыққан математикалық термин:",
                    "options": ["Алгебра", "Геометрия", "Арифметика", "Тригонометрия"],
                    "correct": 0
                }
            ]
        },
        {
            "id": 3,
            "subject": "Математикалық сауаттылық",
            "title": "Логикалық есептер мен сандар тізбегі",
            "questions": [
                {
                    "question": "2, 4, 8, 16, ? келесі санды тап",
                    "options": ["20", "24", "32", "64"],
                    "correct": 2
                }
            ]
        },
        {
            "id": 4,
            "subject": "Математика",
            "title": "Алгебра және геометрия негіздері",
            "questions": [
                {
                    "question": "sin²(x) + cos²(x) неге тең?",
                    "options": ["0", "1", "2", "-1"],
                    "correct": 1
                }
            ]
        },
        {
            "id": 5,
            "subject": "Информатика",
            "title": "Python және Алгоритмдер",
            "questions": [
                {
                    "question": "Python тілінде цикл ашу операторы:",
                    "options": ["loop", "for / while", "repeat", "if / else"],
                    "correct": 1
                }
            ]
        }
    ]

if "results" not in st.session_state:
    st.session_state.results = []

# Сайдбар бөлімі
st.sidebar.markdown("<p style='font-size: 13px; margin-bottom: 2px;'><b>Профиль</b></p>", unsafe_allow_html=True)
col_img, col_name = st.sidebar.columns([1, 3])
with col_img:
    st.image(st.session_state.avatar, width=30)
with col_name:
    st.markdown(f"<p style='font-size: 12px; margin: 0;'><b>{st.session_state.username}</b></p>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size: 13px; margin-bottom: 5px;'><b>Мәзір</b></p>", unsafe_allow_html=True)

pages = ["Тесттер тізімі", "Сұрақ қосу", "Деректерді басқару (JSON)", "Менің нәтижелерім", "Профильді баптау"]
for p in pages:
    if st.sidebar.button(p, key=f"btn_{p}", use_container_width=True):
        st.session_state.current_page = p
        if "active_test" in st.session_state:
            del st.session_state.active_test
        st.rerun()

menu = st.session_state.current_page

if menu == "Тесттер тізімі":
    st.header("Инфо-Мат Бағыты (Кезеңдерге бөлінген тесттер)")
    
    subjects = ["Математика тарихы", "Математикалық сауаттылық", "Математика", "Информатика"]
    selected_subject = st.selectbox("Бағытты / Пәнді таңдаңыз:", subjects)
    
    filtered_tests = [t for t in st.session_state.tests if t["subject"] == selected_subject]
    
    if not filtered_tests:
        st.info("Бұл бөлімде әзірге тесттер жоқ.")
    else:
        for test in filtered_tests:
            with st.container():
                st.subheader(test["title"])
                st.write(f"Сұрақ саны: {len(test['questions'])} / 50")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Бастау", key=f"start_{test['id']}"):
                        st.session_state.active_test = test
                        st.session_state.q_index = 0
                        st.session_state.score = 0
                        st.rerun()
                with col2:
                    if st.button("Өшіру", key=f"del_{test['id']}"):
                        st.session_state.tests = [t for t in st.session_state.tests if t["id"] != test["id"]]
                        st.rerun()
                st.markdown("---")
            
elif menu == "Сұрақ қосу":
    st.header("Жаңа сұрақ немесе кезеңдік тест қосу")
    
    with st.form("add_question_form"):
        subject = st.selectbox("Бөлімді таңдаңыз", ["Математика тарихы", "Математикалық сауаттылық", "Математика", "Информатика"])
        test_title = st.text_input("Тест атауы (Кезеңі)", "Мысалы: Математика тарихы: Жаңа заман")
        q_text = st.text_area("Сұрақ мәтіні")
        opt0 = st.text_input("1-ші жауап")
        opt1 = st.text_input("2-ші жауап")
        opt2 = st.text_input("3-ші жауап")
        opt3 = st.text_input("4-ші жауап")
        correct = st.selectbox("Дұрыс жауап", [0, 1, 2, 3], format_func=lambda x: f"{x+1}-ші нұсқа")
        
        submitted = st.form_submit_button("Сұрақты сақтау")
        if submitted:
            if test_title and q_text and opt0 and opt1 and opt2 and opt3:
                existing = next((t for t in st.session_state.tests if t["title"] == test_title and t["subject"] == subject), None)
                new_q = {"question": q_text, "options": [opt0, opt1, opt2, opt3], "correct": correct}
                if existing:
                    if len(existing["questions"]) >= 50:
                        st.error("Бұл тестте 50 сұрақ толып қалды!")
                    else:
                        existing["questions"].append(new_q)
                        st.success("Сұрақ сәтті қосылды!")
                else:
                    new_test = {
                        "id": len(st.session_state.tests) + 1,
                        "subject": subject,
                        "title": test_title,
                        "questions": [new_q]
                    }
                    st.session_state.tests.append(new_test)
                    st.success("Жаңа тест пен сұрақ сәтті қосылды!")
            else:
                st.error("Барлық өрістерді толтырыңыз!")

elif menu == "Деректерді басқару (JSON)":
    st.header("JSON арқылы деректерді сақтау және жүктеу")
    st.write("Барлық сұрақтар мен тесттерді JSON файлына сақтап, кейін қайта жүктей аласыз.")
    
    json_data = json.dumps(st.session_state.tests, ensure_ascii=False, indent=4)
    st.download_button(
        label="Тесттерді JSON файлына сақтау",
        data=json_data,
        file_name="infomat_tests.json",
        mime="application/json"
    )
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader("JSON файлын жүктеу арқылы қалпына келтіру", type=["json"])
    if uploaded_file is not None:
        try:
            loaded_tests = json.load(uploaded_file)
            if isinstance(loaded_tests, list):
                st.session_state.tests = loaded_tests
                st.success("Деректер сәтті жүктелді және жаңартылды!")
            else:
                st.error("Файл форматы қате!")
        except Exception as e:
            st.error(f"Қате орын алды: {e}")

elif menu == "Менің нәтижелерім":
    st.header("Менің нәтижелерім (Пәндер бойынша прогресс/регресс)")
    if not st.session_state.results:
        st.info("Әзірге тапсырылған тест нәтижелері жоқ. Тест тапсырып көріңіз!")
    else:
        # Нәтижелерді пәндер бойынша топтастыру үшін тесттер тізімінен пәнін анықтаймыз
        test_subject_map = {t["title"]: t["subject"] for t in st.session_state.tests}
        
        # Әр нәтижеге пән атауын қосамыз
        formatted_results = []
            for r in st.session_state.results:
            subj = test_subject_map.get(r["title"], "Басқа пәндер")
            formatted_results.append({
                "Пәні": subj,
                "Тест атауы": r["title"],
                "Ұпай": r["score"],
                "Күні": r["date"]
            })
            
        df = pd.DataFrame(formatted_results)
        
        # Қолжетімді пәндер тізімі
        unique_subjects = df["Пәні"].unique()
        
        for subj in unique_subjects:
            st.subheader(f"📖 Пән: {subj}")
            subj_df = df[df["Пәні"] == subj]
            
            # Сызықтық график көрсету (прогресс пен регрессті бақылау үшін)
            # Графикте х осі ретінде реттік номер немесе күні қолданылады
            chart_data = subj_df.reset_index(drop=True)[["Ұпай"]]
            st.line_chart(chart_data)
            
            # Деректер кестесін де қоса көрсетейік
            st.dataframe(subj_df[["Тест атауы", "Ұпай", "Күні"]], use_container_width=True)
            st.markdown("---")

elif menu == "Профильді баптау":
    st.header("Профильді өңдеу")
    new_name = st.text_input("Аты-жөніңіз", st.session_state.username)
    new_avatar = st.text_input("Аватар сурет сілтемесі (URL)", st.session_state.avatar)
    if st.button("Сақтау"):
        st.session_state.username = new_name
        st.session_state.avatar = new_avatar
        st.success("Профиль сәтті жаңартылды!")
        st.rerun()

if "active_test" in st.session_state and st.session_state.active_test:
    test = st.session_state.active_test
    st.header(f"Тест: {test['title']}")
    
    q_idx = st.session_state.q_index
    if q_idx < len(test["questions"]):
        q = test["questions"][q_idx]
        st.subheader(f"Сұрақ {q_idx + 1}: {q['question']}")
        choice = st.radio("Жауапты таңдаңыз:", q["options"], key=f"q_{q_idx}")
        
        if st.button("Жауапты беру"):
            selected_idx = q["options"].index(choice)
            if selected_idx == q["correct"]:
                st.session_state.score += 1
            st.session_state.q_index += 1
            st.rerun()
    else:
        st.success(f"Тест аяқталды! Сіздің жинаған ұпайыңыз: {st.session_state.score} / {len(test['questions'])}")
        if not st.session_state.results or st.session_state.results[-1]["title"] != test["title"]:
            st.session_state.results.append({
                "title": test["title"],
                "score": st.session_state.score,
                "total": len(test["questions"]),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        if st.button("Мәзірге қайту"):
            del st.session_state.active_test
            st.rerun()
