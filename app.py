import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Инфо-Мат УБТ Базасы", layout="centered")

# Фонға сіз сұраған суретті толық қоятын CSS стилі
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                          url("https://static.vecteezy.com/system/resources/previews/003/181/982/non_2x/cyber-hacker-attack-background-skull-vector.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #00FF66;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(11, 11, 11, 0.95);
        padding-top: 15px;
        width: 350px !important;
    }
    [data-testid="stSidebar"] * {
        color: #00FF66 !important;
    }
    h1, h2, h3, p, label {
        color: #00FF66 !important;
    }
    .stButton>button {
        background-color: #111111;
        color: #00FF66;
        border: 1px solid #00FF66;
        border-radius: 4px;
        padding: 10px 14px;
        font-size: 16px;
        width: 100%;
        margin-bottom: 8px;
    }
    .stButton>button:hover {
        background-color: #00FF66;
        color: #000000;
    }
    .certificate {
        background: linear-gradient(135deg, #111111 0%, #000000 100%);
        border: 4px solid #00FF66;
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        transform: perspective(1000px) rotateX(3deg);
        box-shadow: 0 25px 50px rgba(0, 255, 102, 0.3), inset 0 0 30px rgba(0, 255, 102, 0.1);
        margin: 30px auto;
    }
    .certificate h2 {
        font-size: 32px !important;
        letter-spacing: 2px;
    }
    .certificate h1 {
        font-size: 44px !important;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.5);
    }
    .certificate p {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Сессиялық айнымалыларды инициализациялау
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = "Тажиддинов Ахмаджан"
if "avatar" not in st.session_state:
    st.session_state.avatar = "https://static.vecteezy.com/system/resources/previews/003/181/982/non_2x/cyber-hacker-attack-background-skull-vector.jpg"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Тесттер тізімі"

if "tests" not in st.session_state:
    st.session_state.tests = [
        {
            "id": 1,
            "subject": "Қазақстан тарихы",
            "title": "Қазақстан тарихы: Ежелгі кезең",
            "questions": [
                {
                    "question": "Көне түркі жазба ескерткіштерінің ішіндегі ең ірісі:",
                    "options": ["Күлтегін", "Тоныкөк", "Билге қаған", "Махмұт Қашғари"],
                    "correct": 0
                },
                {
                    "question": "Қарлұқ қағанаты өмір сүрген жылдар:",
                    "options": ["704–940 жж.", "552–603 жж.", "942–1212 жж.", "1465–1847 жж."],
                    "correct": 0
                }
            ]
        }
    ]

if "results" not in st.session_state:
    st.session_state.results = []

# Бастапқыда 0 болып тұруы үшін бұл тізімді бос қалдырамыз
if "score_140_history" not in st.session_state:
    st.session_state.score_140_history = []

# ----------------- ЛОГИН ЭКРАНЫ -----------------
if not st.session_state.logged_in:
    st.write("")
    st.write("")
    st.write("")
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<p style='text-align: center; font-size: 26px; margin-bottom: 25px;'><b>Ahmadjan Hello!</b></p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            entered_password = st.text_input("ПК паролі / PIN-код", type="password")
            submit_login = st.form_submit_button("Құлпын ашу")
            
            if submit_login:
                if entered_password == "7777":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Қате пароль! Әдепкі пароль: 7777")
                    
    st.stop()

# ----------------- НЕГІЗГІ ҚОСЫМША -----------------

if "active_test" in st.session_state and st.session_state.active_test:
    test = st.session_state.active_test
    st.header(f"Тест: {test['title']}")
    
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "marked_questions" not in st.session_state:
        st.session_state.marked_questions = set()

    total_questions = len(test["questions"])

    st.write("Сұрақтар нөмірі:")
    cols = st.columns(min(total_questions, 10))
    for idx in range(total_questions):
        col_idx = idx % 10
        with cols[col_idx]:
            btn_prefix = "📌 " if idx in st.session_state.marked_questions else ""
            if st.button(f"{btn_prefix}{idx+1}", key=f"q_num_{idx}", use_container_width=True):
                st.session_state.q_index = idx
                st.rerun()

    st.markdown("---")
    q_idx = st.session_state.q_index

    if q_idx < total_questions:
        q = test["questions"][q_idx]
        
        col_q_title, col_mark = st.columns([3, 1])
        with col_q_title:
            st.subheader(f"Сұрақ {q_idx + 1} / {total_questions}: {q['question']}")
        with col_mark:
            is_marked = q_idx in st.session_state.marked_questions
            mark_label = "⭐ Белгіленді" if is_marked else "☆ Белгілеу"
            if st.button(mark_label, key=f"mark_btn_{q_idx}"):
                if is_marked:
                    st.session_state.marked_questions.remove(q_idx)
                else:
                    st.session_state.marked_questions.add(q_idx)
                st.rerun()

        st.write("Жауапты таңдаңыз:")
        current_selected = st.session_state.user_answers.get(q_idx)

        for i, option in enumerate(q["options"]):
            btn_label = f"✅ {option}" if current_selected == i else f"{i+1}) {option}"
            if st.button(btn_label, key=f"opt_{q_idx}_{i}"):
                st.session_state.user_answers[q_idx] = i
                st.rerun()
                
        st.markdown("---")
        
        col_prev, col_next = st.columns(2)
        with col_prev:
            if q_idx > 0:
                if st.button("⬅️ Артқа"):
                    st.session_state.q_index -= 1
                    st.rerun()
        with col_next:
            if q_idx < total_questions - 1:
                if st.button("Келесі сұрақ ➡️"):
                    st.session_state.q_index += 1
                    st.rerun()
            else:
                if st.button("🏁 Тестті аяқтау"):
                    st.session_state.q_index = total_questions
                    st.rerun()

        st.write("")
        if st.button("❌ Тесттен шығу (Мәзірге қайту)"):
            del st.session_state.active_test
            del st.session_state.user_answers
            del st.session_state.marked_questions
            st.rerun()
    else:
        score = 0
        for idx, q_data in enumerate(test["questions"]):
            if st.session_state.user_answers.get(idx) == q_data["correct"]:
                score += 1
        
        total = total_questions
        percent = int((score / total) * 100) if total > 0 else 0
        
        if not st.session_state.results or st.session_state.results[-1]["title"] != test["title"]:
            st.session_state.results.append({
                "title": test["title"],
                "score": score,
                "total": total,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        st.markdown(f"""
            <div class="certificate">
                <h2>🏆 СЕРТИФИКАТ 🏆</h2>
                <p>Осы сертификат салтанатты түрде төмендегі азаматқа беріледі:</p>
                <h1 style="color: #ffffff; margin: 20px 0;">{st.session_state.username}</h1>
                <p><b>{test['title']}</b> тестін сәтті аяқтап, жоғары нәтиже көрсетті!</p>
                <hr style="border-color: #00FF66; margin: 30px 0;">
                <p style="font-size: 24px;">Жинаған ұпайыңыз: <b>{score} / {total} ({percent}%)</b></p>
                <p style="font-size: 14px; color: #888; margin-top: 30px;">Берілген күні: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Мәзірге қайту"):
            del st.session_state.active_test
            del st.session_state.user_answers
            del st.session_state.marked_questions
            st.rerun()
            
else:
    # Сайдбардағы Профиль және Мәзір
    st.sidebar.markdown("<p style='font-size: 32px; margin-bottom: 5px;'><b>Профиль</b></p>", unsafe_allow_html=True)
    
    st.sidebar.image(st.session_state.avatar, width=120)
    st.sidebar.markdown(f"<p style='font-size: 22px; margin-top: 5px; margin-bottom: 10px;'><b>{st.session_state.username}</b></p>", unsafe_allow_html=True)

    if st.sidebar.button("🔒 Жүйеден шығу (Құлыптау)", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("<p style='font-size: 18px; margin-bottom: 10px;'><b>Мәзір</b></p>", unsafe_allow_html=True)

    pages = ["Тесттер тізімі", "140 балдық статистика", "Сұрақ қосу", "Деректерді басқару (JSON)", "Менің нәтижелерім", "Профиль"]
    for p in pages:
        if st.sidebar.button(p, key=f"btn_{p}", use_container_width=True):
            st.session_state.current_page = p
            st.rerun()

    menu = st.session_state.current_page

    if menu == "Тесттер тізімі":
        st.header("Инфо-Мат Бағыты (Кезеңдерге бөлінген тесттер)")
        
        st.markdown("---")
        subjects = ["Қазақстан тарихы", "Математикалық сауаттылық", "Математика", "Информатика"]
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
                            st.session_state.user_answers = {}
                            st.session_state.marked_questions = set()
                            st.rerun()
                    with col2:
                        if st.button("Өшіру", key=f"del_{test['id']}"):
                            st.session_state.tests = [t for t in st.session_state.tests if t["id"] != test["id"]]
                            st.rerun()
                    st.markdown("---")

    elif menu == "140 балдық статистика":
        st.header("🎯 140 балдық жеке статистика және график")
        st.write("Бұл жерде башында барлық мәлімет 0 болып тұрады. Төменден өз нәтижелеріңізді енгізіп, графикті көтере аласыз[cite: 9].")
        
        st.markdown("---")
        
        # Балл енгізу панелі
        with st.form("add_140_score_main"):
            st.subheader("Жаңа нәтиже қосу")
            test_list_input = st.text_input("Тесттер тізімі / Нұсқа атауы", f"Нұсқа №{len(st.session_state.score_140_history)+1}")
            new_score = st.number_input("Жинаған балл (макс 140)", min_value=0, max_value=140, value=0)
            submitted_score = st.form_submit_button("Баллды қосу")
            if submitted_score:
                st.session_state.score_140_history.append({"test_list": test_list_input, "score": new_score})
                st.success("Балл сәтті қосылды!")
                st.rerun()
                
        st.markdown("---")
        st.subheader("📊 Баллдардың өсу графигі")
        if st.session_state.score_140_history:
            df_140 = pd.DataFrame(st.session_state.score_140_history)
            chart_df = df_140.set_index("test_list")[["score"]]
            st.line_chart(chart_df)
            
            st.subheader("📋 Енгізілген балдар тізімі")
            st.dataframe(df_140.rename(columns={"test_list": "Тесттер тізімі", "score": "Жинаған балл"}), use_container_width=True)
        else:
            st.info("Әзірге балдар енгізілмеді (График 0 де тұр). Жоғарыдан өз нәтижеңізді енгізіңіз!")
                
    elif menu == "Сұрақ қосу":
        st.header("Жаңа сұрақ немесе кезеңдік тест қосу")
        
        with st.form("add_question_form"):
            subject = st.selectbox("Бөлімді таңдаңыз", ["Қазақстан тарихы", "Математикалық сауаттылық", "Математика", "Информатика"])
            test_title = st.text_input("Тест атауы (Кезеңі)", "Мысалы: Қазақстан тарихы: Жаңа заман")
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
            st.info("Әзірге қосымша ішінде тапсырылған тест нәтижелері жоқ.")
        else:
            test_subject_map = {t["title"]: t["subject"] for t in st.session_state.tests}
            
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
            unique_subjects = df["Пәні"].unique()
            
            selected_subject = st.selectbox("Қай пәннің нәтижесін көргіңіз келеді?", unique_subjects)
            
            st.subheader(f"📖 Пән: {selected_subject}")
            subj_df = df[df["Пәні"] == selected_subject]
            
            chart_data = subj_df.reset_index(drop=True)[["Ұпай"]]
            st.line_chart(chart_data)
            
            st.dataframe(subj_df[["Тест атауы", "Ұпай", "Күні"]], use_container_width=True)

    elif menu == "Профиль":
        st.header("Профильді басқару және Фотоны өзгерту")
        
        with st.form("profile_settings_form"):
            new_name = st.text_input("Аты-жөніңіз", st.session_state.username)
            
            st.write("📸 Қалаған фотоңызды қою үшін төмендегі әдістердің бірін таңдаңыз:")
            photo_method = st.radio("Фото жүктеу тәсілі:", ["Компьютерден сурет жүктеу", "Интернеттен сурет сілтемесін (URL) жазу"])
            
            uploaded_image = None
            url_image = ""
            
            if photo_method == "Компьютерден сурет жүктеу":
                uploaded_image = st.file_uploader("Суретті таңдаңыз (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
            else:
                url_image = st.text_input("Сурет сілтемесін енгізіңіз (URL)", value="" if isinstance(st.session_state.avatar, str) else "")
            
            submitted_profile_changes = st.form_submit_button("Өзгерістерді сақтау")
            
            if submitted_profile_changes:
                st.session_state.username = new_name
                if photo_method == "Компьютерден сурет жүктеу" and uploaded_image is not None:
                    st.session_state.avatar = uploaded_image
                elif photo_method == "Интернеттен сурет сілтемесін (URL) жазу" and url_image.strip() != "":
                    st.session_state.avatar = url_image.strip()
                
                st.success("Профиль сәтті жаңартылды!")
                st.rerun()
