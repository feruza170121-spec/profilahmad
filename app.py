import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

# Беттің баптауы
st.set_page_config(page_title="Жеке Тест Платформасы", page_icon="🔐", layout="centered")

# --- CSS СТИЛЬДЕРІ ---
st.markdown("""
    <style>
    /* Негізгі мәтіндер мен енгізу өрістерін үлкейту */
    html, body, [class*="css"] {
        font-size: 22px !important;
    }
    
    /* Тақырыптарды үлкейту */
    h1 { font-size: 3rem !important; }
    h2 { font-size: 2.5rem !important; }
    h3 { font-size: 2rem !important; }
    
    /* Тізімдердің шетіндегі домалақ белгілерді толық өшіру */
    ul, ol, li {
        list-style: none !important;
        padding-left: 0px !important;
    }
    
    div[data-baseweb="radio"] div {
        accent-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# --- ФАЙЛДАРДЫ БАСҚАРУ (JSON) ---
USERS_FILE = "users.json"
TESTS_FILE = "tests.json"
RESULTS_FILE = "results.json"

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
                "id": i,
                "test_title": "Математикадан негізгі тест",
                "subject": "Математика",
                "question": f"Сұрақ №{i}: 2 + {i} нәтижесі қанша?",
                "options": [str(2+i), str(3+i), str(4+i), str(5+i)],
                "answer": str(2+i)
            } for i in range(1, 11)
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "selected_test_title" not in st.session_state:
    st.session_state.selected_test_title = None
if "test_finished" not in st.session_state:
    st.session_state.test_finished = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

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
        st.session_state.test_finished = False
        st.session_state.user_answers = {}
        st.rerun()
        
    tests = load_data(TESTS_FILE)
    
    # 1. ТЕСТТЕР БӨЛІМІ
    if menu == "Тесттер":
        
        # СЕРТИФИКАТ БӨЛІМІ
        if st.session_state.test_finished:
            res = st.session_state.last_result
            
            st.markdown("---")
            st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏆 СЕРТИФИКАТ 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 24px;'>Осы сертификат беріледі: <b>{res['user']}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 20px;'><b>'{res['test_title']}'</b> атты тестті сәтті аяқтағаны үшін.</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #2196F3;'>Жинаған ұпайыңыз: {res['score_str']}</h2>", unsafe_allow_html=True)
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Басқа тест таңдау"):
                    st.session_state.test_finished = False
                    st.session_state.test_started = False
                    st.session_state.selected_test_title = None
                    st.session_state.user_answers = {}
                    st.rerun()
            with col2:
                if st.button("🚪 Қайта кіру / Шығу"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.test_finished = False
                    st.session_state.test_started = False
                    st.session_state.user_answers = {}
                    st.rerun()
            return

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
            st.info(f"Бұл тестте барлығы {len(selected_tests_preview)} сұрақ бар.")
            
            if st.button("Тестті бастау"):
                st.session_state.test_started = True
                st.session_state.selected_test_title = selected_title
                st.session_state.current_question_index = 0
                st.session_state.user_answers = {}
                st.rerun()
        else:
            current_title = st.session_state.selected_test_title
            current_test_questions = [q for q in tests if q.get("test_title") == current_title]
            
            if not current_test_questions:
                st.warning(f"'{current_title}' бойынша сұрақтар табылмады.")
                if st.button("Тесттер тізіміне оралу"):
                    st.session_state.test_started = False
                    st.rerun()
                return

            st.subheader(f"📚 Тест атауы: {current_title}")

            # --- СҰРАҚТАР НӨМІРЛЕРІ ПАНЕЛІ ---
            st.write("Сұрақтар арасында өту үшін төмендегі батырмаларды басыңыз:")
            cols = st.columns(min(len(current_test_questions), 10))
            for idx, q_item in enumerate(current_test_questions):
                col_idx = idx % 10
                with cols[col_idx]:
                    btn_label = f"{idx + 1}"
                    if st.button(btn_label, key=f"q_btn_{idx}"):
                        st.session_state.current_question_index = idx
                        st.rerun()
            st.write("---")

            # Ағымдағы сұрақ
            idx = st.session_state.current_question_index
            q = current_test_questions[idx]
            
            st.markdown(f"**Сұрақ {idx + 1} / {len(current_test_questions)}:**")
            st.markdown(f"### {q['question']}")
            
            options = q['options']
            current_ans = st.session_state.user_answers.get(q['id'])
            
            default_ix = 0
            if current_ans in options:
                default_ix = options.index(current_ans)
                
            selected_option = st.radio("Жауапты таңдаңыз:", options, index=default_ix, key=f"radio_q_{q['id']}")
            st.session_state.user_answers[q['id']] = selected_option
            
            st.write("---")
            
            # Батырмалар
            c_prev, c_next, c_finish = st.columns([1, 1, 2])
            
            with c_prev:
                if idx > 0:
                    if st.button("⬅️ Артқа"):
                        st.session_state.current_question_index -= 1
                        st.rerun()
            with c_next:
                if idx < len(current_test_questions) - 1:
                    if st.button("Келесі ➡️"):
                        st.session_state.current_question_index += 1
                        st.rerun()
            with c_finish:
                if st.button("🏁 Тестті аяқтау және Сертификат алу"):
                    score = 0
                    for item in current_test_questions:
                        if st.session_state.user_answers.get(item['id']) == item['answer']:
                            score += 1
                    
                    result_str = f"{score} / {len(current_test_questions)}"
                    res_data = {
                        "user": st.session_state.username,
                        "test_title": current_title,
                        "score": score,
                        "total": len(current_test_questions),
                        "score_str": result_str
                    }
                    
                    results = load_data(RESULTS_FILE)
                    results.append(res_data)
                    save_data(RESULTS_FILE, results)
                    
                    st.session_state.last_result = res_data
                    st.session_state.test_finished = True
                    st.rerun()
            
            if st.button("Басқа тест таңдауға қайту"):
                st.session_state.test_started = False
                st.session_state.user_answers = {}
                st.rerun()

    # 2. СҰРАҚ ҚОСУ ЖӘНЕ ӨШІРУ
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
                test_title_input = st.text_input("Тест атауын енгізіңіз:", value="")
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
                        st.error(f"❌ Кешіріңіз, '{final_test_title}' тест атауында сұрақтар саны максималды шектеуге жетті!")
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
                                st.success("Сәтті қосылды!")
                        else:
                            st.error("Барлық міндетті өрістерді толтырыңыз!")

    # 3. НӘТИЖЕЛЕР ЖӘНЕ ГРАФИК
    elif menu == "Нәтижелер":
        st.title("📊 Тест нәтижелері және психологиялық график")
        
        accentuation_types = [
            "Демонстративный тип", "Застревающий тип", "Педантичный тип",
            "Возбудимый тип", "Гипертимный тип", "Дистимический тип",
            "Тревожно-боязливый тип", "Аффективно-экзальтированный тип",
            "Эмотивный тип", "Циклотимный тип"
        ]
        sample_scores = [10, 14, 14, 6, 6, 9, 12, 12, 12, 9]

        st.subheader("📈 Акцентуация профилінің графигі (Үлгі бойынша)")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(accentuation_types, sample_scores, marker='D', color='#2b5c8f', linewidth=2, markersize=6)
        ax.set_ylim(0, 16)
        ax.set_yticks(range(0, 18, 2))
        ax.grid(True, linestyle='-', alpha=0.6)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.write("---")
        st.subheader("📋 Қолданушылардың нәтижелер тізімі:")
        results = load_data(RESULTS_FILE)
        if results:
            df = pd.DataFrame(results)
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

if not st.session_state.logged_in:
    login_page()
else:
    main_app()
