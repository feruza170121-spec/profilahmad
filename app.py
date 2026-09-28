import streamlit as st
import json
import os
import pandas as pd

# Беттің баптауы
st.set_page_config(page_title="Жеке Тест Платформасы", page_icon="🔐", layout="centered")

# --- CSS СТИЛЬДЕРІ: Жазуларды тағы да үлкейту және домалақтарды өшіру ---
st.markdown("""
    <style>
    /* Негізгі мәтіндер мен енгізу өрістерін едәуір үлкейту */
    html, body, [class*="css"] {
        font-size: 22px !important;
    }
    
    /* Тақырыптарды тағы да үлкейту */
    h1 {
        font-size: 3rem !important;
    }
    h2 {
        font-size: 2.5rem !important;
    }
    h3 {
        font-size: 2rem !important;
    }
    
    /* Тізімдердің шетіндегі домалақ белгілерді (bullet points) толық өшіру */
    ul, ol {
        list-style-type: none !important;
        padding-left: 0px !important;
    }
    
    li {
        list-style: none !important;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ФАЙЛДАРДЫ БАСҚАРУ (JSON) ---
USERS_FILE = "users.json"
TESTS_FILE = "tests.json"
RESULTS_FILE = "results.json"

# Бастапқы файлдарды құру және әрқашан дұрыс логин-парольді қамтамасыз ету
def init_json_files():
    default_users = {"admin": "secret123"}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
                if not isinstance(users, dict) or "admin" not in users:
                    users = default_users
                    with open(USERS_FILE, "w", encoding="utf-8") as wf:
                        json.dump(users, wf, ensure_ascii=False, indent=4)
        except:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(default_users, f, ensure_ascii=False, indent=4)
    else:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, ensure_ascii=False, indent=4)
            
    if not os.path.exists(TESTS_FILE):
        default_tests = [
            {
                "id": 1,
                "test_title": "Математикадан негізгі тест",
                "subject": "Математика",
                "question": "2 + 2 * 2 нәтижесі қанша?",
                "options": ["6", "8", "4", "2"],
                "answer": "6"
            },
            {
                "id": 2,
                "test_title": "Python негіздері",
                "subject": "Информатика",
                "question": "Python тілінде тізім (list) қандай жақшамен анықталады?",
                "options": ["{}", "[]", "()", "<>"],
                "answer": "[]"
            }
        ]
        with open(TESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_tests, f, ensure_ascii=False, indent=4)

    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

init_json_files()

def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Сессияны басқару
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "selected_test_title" not in st.session_state:
    st.session_state.selected_test_title = None

# --- КІРУ ПАРАҒЫ ---
def login_page():
    st.title("🔐 Жеке Кабинетке Кіру")
    users = load_data(USERS_FILE)
    
    if not isinstance(users, dict):
        users = {"admin": "secret123"}
        save_data(USERS_FILE, users)

    with st.form("login_form"):
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Кіру")
        
        if submitted:
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Сәтті кірдіңіз!")
                st.rerun()
            else:
                st.error("Қате логин немесе пароль!")

# --- НЕГІЗГІ ҚОСЫМША ---
def main_app():
    st.sidebar.title(f"Қош келдіңіз, {st.session_state.username}!")
    menu = st.sidebar.radio("Мәзір", ["Тесттер", "Сұрақ қосу / Өзгерту", "Нәтижелер", "Логин/Парольді өзгерту"])
    
    if st.sidebar.button("Жүйеден шығу"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.test_started = False
        st.session_state.selected_test_title = None
        st.rerun()
        
    tests = load_data(TESTS_FILE)
    
    # 1. ТЕСТТЕР БӨЛІМІ (АТАУЫ БОЙЫНША ТАПСЫРУ)
    if menu == "Тесттер":
        st.title("📝 Тесттер тізімі және тапсыру")
        
        if not tests:
            st.warning("Әзірге жасақталған тесттер жоқ.")
            return
            
        test_titles = sorted(list(set(q.get("test_title", "Атаусыз тест").strip() for q in tests if q.get("test_title"))))
        
        if not test_titles:
            st.warning("Базада тест атаулары табылмады.")
            return

        if not st.session_state.test_started:
            st.subheader("Тапсыру үшін тест атауын таңдаңыз:")
            selected_title = st.selectbox("Тест атауы:", test_titles, key="test_title_select")
            
            selected_tests_preview = [q for q in tests if q.get("test_title") == selected_title]
            st.info(f"Бұл тестте барлығы {len(selected_tests_preview)} сұрақ бар (Максимум 50 сұрақ).")
            
            if st.button("Тестті бастау"):
                st.session_state.test_started = True
                st.session_state.selected_test_title = selected_title
                st.rerun()
        else:
            current_title = st.session_state.selected_test_title
            st.subheader(f"📚 Тест атауы: {current_title}")
            
            current_test_questions = [q for q in tests if q.get("test_title") == current_title]
            
            if not current_test_questions:
                st.warning(f"'{current_title}' бойынша сұрақтар табылмады.")
                if st.button("Тесттер тізіміне оралу"):
                    st.session_state.test_started = False
                    st.rerun()
                return

            score = 0
            with st.form(f"test_form_{current_title}"):
                user_answers = {}
                for i, q in enumerate(current_test_questions):
                    st.markdown(f"**{i+1}. {q['question']}**")
                    options = q['options']
                    user_answers[q['id']] = st.radio("Жауапты таңдаңыз:", options, key=f"q_{q['id']}")
                    st.write("---")
                    
                submitted = st.form_submit_button("Тестті аяқтау және нәтижені көру")
                
                if submitted:
                    for q in current_test_questions:
                        if user_answers.get(q['id']) == q['answer']:
                            score += 1
                    
                    result_str = f"{score} / {len(current_test_questions)}"
                    st.success(f"Тест аяқталды! Сіздің нәтижеңіз ({current_title}): {result_str}")
                    
                    results = load_data(RESULTS_FILE)
                    results.append({
                        "user": st.session_state.username,
                        "test_title": current_title,
                        "score": score,
                        "total": len(current_test_questions),
                        "score_str": result_str
                    })
                    save_data(RESULTS_FILE, results)
            
            if st.button("Басқа тест таңдауға қайту"):
                st.session_state.test_started = False
                st.rerun()

    # 2. СҰРАҚ ҚОСУ ЖӘНЕ ӨШІРУ (МАКСИМУМ 50 СҰРАҚ ШЕКТЕУІМЕН)
    elif menu == "Сұрақ қосу / Өзгерту":
        st.title("➕ Тест құрастыру және сұрақтарды басқару")
        
        if "delete_q_id" in st.session_state:
            q_id_to_del = st.session_state.delete_q_id
            updated_tests = [q for q in tests if q["id"] != q_id_to_del]
            save_data(TESTS_FILE, updated_tests)
            del st.session_state.delete_q_id
            st.success("Сұрақ сәтті өшірілді!")
            st.rerun()

        tab1, tab2 = st.tabs(["Қолданыстағы сұрақтар", "Жаңа сұрақ қосу"])
        
        with tab1:
            st.subheader("Барлық сұрақтар мен тесттер тізімі")
            if not tests:
                st.info("Әзірге сұрақтар жоқ.")
            else:
                for q in tests:
                    t_title = q.get('test_title', 'Атаусыз тест')
                    with st.expander(f"[{t_title}] ID: {q['id']} - {q['question'][:40]}..."):
                        st.markdown(f"**Тест атауы:** {t_title}")
                        st.markdown(f"**Пән:** {q.get('subject', 'Көрсетілмеген')}")
                        st.markdown(f"**Сұрақ:** {q['question']}")
                        st.markdown(f"**Нұсқалар:** {q['options']}")
                        st.markdown(f"**Дұрыс жауап:** {q['answer']}")
                        
                        if st.button("Сұрақты өшіру", key=f"del_{q['id']}"):
                            st.session_state.delete_q_id = q['id']
                            st.rerun()

        with tab2:
            st.subheader("Жаңа сұрақ қосу (Әр тестке макс. 50 сұрақ)")
            
            with st.form("add_question_form"):
                st.markdown("### Тесттің атауы")
                test_title_input = st.text_input("Тест атауын енгізіңіз (мысалы: Физика 1-тоқсан):", value="")
                
                subject_input = st.selectbox("Пәні:", ["Математика", "Информатика", "Физика", "Тарих", "Ағылшын тілі", "Басқа"])
                
                new_q = st.text_area("Сұрақ мәтіні")
                c1 = st.text_input("Нұсқа A")
                c2 = st.text_input("Нұсқа B")
                c3 = st.text_input("Нұсқа C")
                c4 = st.text_input("Нұсқа D")
                
                correct_ans_letter = st.selectbox("Дұрыс жауаптың әрпін таңдаңыз:", ["A", "B", "C", "D"])
                
                add_submitted = st.form_submit_button("Сұрақты сақтау")
                
                if add_submitted:
                    final_test_title = test_title_input.strip() if test_title_input.strip() else "Атаусыз тест"
                    
                    current_count_in_test = len([q for q in tests if q.get("test_title") == final_test_title])
                    
                    if current_count_in_test >= 50:
                        st.error(f"❌ Кешіріңіз, '{final_test_title}' тест атауында сұрақтар саны максималды шектеуге (50 сұрақ) жетті!")
                    else:
                        if final_test_title and new_q and c1 and c2:
                            options_dict = {"A": c1, "B": c2, "C": c3, "D": c4}
                            selected_correct_text = options_dict.get(correct_ans_letter)
                            
                            if not selected_correct_text:
                                st.error("Таңдалған әріпке сәйкес келетін нұсқа бос болмауы тиіс!")
                            else:
                                new_id = max([q["id"] for q in tests], default=0) + 1
                                new_question_data = {
                                    "id": new_id,
                                    "test_title": final_test_title,
                                    "subject": subject_input,
                                    "question": new_q.strip(),
                                    "options": [c1, c2, c3, c4],
                                    "answer": selected_correct_text
                                }
                                tests.append(new_question_data)
                                save_data(TESTS_FILE, tests)
                                st.success(f"Сәтті қосылды! Бұл тестте қазір {current_count_in_test + 1} / 50 сұрақ бар.")
                        else:
                            st.error("Тест атауын, сұрақ пен кем дегенде A және B нұсқаларын толтырыңыз!")

    # 3. НӘТИЖЕЛЕРДІ СОЛДАН ОҢҒА ҚАРАЙ ӨСЕТІН/ТҮСЕТІН СЫЗЫҚТЫҚ ГРАФИК ТҮРІНДЕ КӨРСЕТУ
    elif menu == "Нәтижелер":
        st.title("📊 Тест нәтижелері (Хронологиялық сызықтық график)")
        results = load_data(RESULTS_FILE)
        
        if results:
            chart_data = []
            for idx, r in enumerate(results, start=1):
                score = r.get('score', 0)
                total = r.get('total', 50)
                percentage = (score / total) * 100 if total > 0 else 0
                
                if percentage < 50:
                    status = "🔴 Төмен (<50%)"
                elif percentage < 75:
                    status = "🟡 Орташа (50-74%)"
                else:
                    status = "🟢 Жақсы (≥75%)"

                step_name = f"{idx}. {r.get('test_title', 'Тест')} ({r.get('user', 'Қолданушы')})"

                chart_data.append({
                    "Қадам": step_name,
                    "Ұпай": score,
                    "Деңгейі": status
                })
            
            df = pd.DataFrame(chart_data)
            
            st.subheader("📈 Көтерілу және түсу динамикасы (Сол жақтан оң жаққа):")
            st.line_chart(df.set_index("Қадам")["Ұпай"])
            
            st.write("---")
            st.subheader("📋 Толық мәліметтер кестесі:")
            st.dataframe(df)
            
            if st.button("Барлық нәтижелерді тазарту"):
                save_data(RESULTS_FILE, [])
                st.rerun()
        else:
            st.info("Әзірге сақталған нәтижелер жоқ.")

    # 4. ЛОГИН ЖӘНЕ ПАРОЛЬДІ ӨЗГЕРТУ
    elif menu == "Логин/Парольді өзгерту":
        st.title("⚙️ Жеке деректерді өзгерту")
        
        users = load_data(USERS_FILE)
        current_user = st.session_state.username
        
        with st.form("change_credentials_form"):
            st.write("Логин немесе парольді өзгерту:")
            new_username = st.text_input("Жаңа логин", value=current_user)
            old_password = st.text_input("Қазіргі пароль", type="password")
            new_password = st.text_input("Жаңа пароль", type="password")
            
            update_submitted = st.form_submit_button("Өзгерістерді сақтау")
            
            if update_submitted:
                if users.get(current_user) == old_password:
                    if new_username.strip() and new_password.strip():
                        del users[current_user]
                        users[new_username] = new_password
                        save_data(USERS_FILE, users)
                        
                        st.session_state.username = new_username
                        st.success("Логин мен пароль сәтті өзгертілді! Қайта кіріңіз.")
                        st.session_state.logged_in = False
                        st.rerun()
                    else:
                        st.warning("Өрістер бос болмауы тиіс.")
                else:
                    st.error("Қазіргі пароль қате енгізілді!")

# Бағдарлама логикасы
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
