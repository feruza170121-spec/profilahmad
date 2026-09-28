import streamlit as st
import json
import os
import pandas as pd

# Беттің баптауы
st.set_page_config(page_title="Жеке Тест Платформасы", page_icon="🔐", layout="centered")

# --- ФАЙЛДАРДЫ БАСҚАРУ (JSON) ---
USERS_FILE = "users.json"
TESTS_FILE = "tests.json"
RESULTS_FILE = "results.json"

# Бастапқы файлдарды құру (егер жоқ болса)
def init_json_files():
    if not os.path.exists(USERS_FILE):
        default_users = {"admin": "secret123"}
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, ensure_ascii=False, indent=4)
            
    if not os.path.exists(TESTS_FILE):
        default_tests = [
            {
                "id": 1,
                "subject": "Математика",
                "question": "2 + 2 * 2 нәтижесі қанша?",
                "options": ["6", "8", "4", "2"],
                "answer": "6"
            },
            {
                "id": 2,
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
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

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
    menu = st.sidebar.radio("Мәзір", ["Тест тапсыру", "Сұрақ қосу / Өзгерту", "Нәтижелер", "Логин/Парольді өзгерту"])
    
    if st.sidebar.button("Жүйеден шығу"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.test_started = False
        st.session_state.selected_subject = None
        st.rerun()
        
    tests = load_data(TESTS_FILE)
    
    # 1. ПӘНДЕР БОЙЫНША БӨЛЕК ТЕСТ ТАПСЫРУ
    if menu == "Тест тапсыру":
        st.title("📝 Пәндік тест тапсыру")
        
        if not tests:
            st.warning("Әзірге тест сұрақтары жоқ.")
            return
            
        subjects = sorted(list(set(q.get("subject", "").strip() for q in tests if q.get("subject"))))
        
        if not subjects:
            st.warning("Базада пәндер көрсетілген сұрақтар жоқ.")
            return

        if not st.session_state.test_started:
            st.subheader("Өзіңізге қажетті пәнді таңдаңыз:")
            selected = st.selectbox("Пән:", subjects, key="subject_select")
            
            if st.button("Тестті бастау"):
                st.session_state.test_started = True
                st.session_state.selected_subject = selected
                st.rerun()
        else:
            current_sub = st.session_state.selected_subject
            st.subheader(f"📚 Таңдалған пән: {current_sub}")
            
            subject_tests = [q for q in tests if q.get("subject") == current_sub]
            
            if not subject_tests:
                st.warning(f"'{current_sub}' пәні бойынша әзірге сұрақтар жоқ.")
                if st.button("Бетті қайтару / Пән таңдауға оралу"):
                    st.session_state.test_started = False
                    st.rerun()
                return

            score = 0
            with st.form(f"test_form_{current_sub}"):
                user_answers = {}
                for i, q in enumerate(subject_tests):
                    st.markdown(f"**{i+1}. {q['question']}**")
                    options = q['options']
                    user_answers[q['id']] = st.radio("Жауапты таңдаңыз:", options, key=f"q_{q['id']}")
                    st.write("---")
                    
                submitted = st.form_submit_button("Тестті аяқтау және нәтижені көру")
                
                if submitted:
                    for q in subject_tests:
                        if user_answers.get(q['id']) == q['answer']:
                            score += 1
                    
                    result_str = f"{score} / {len(subject_tests)}"
                    st.balloons()
                    st.success(f"Тест аяқталды! Сіздің нәтижеңіз ({current_sub}): {result_str}")
                    
                    results = load_data(RESULTS_FILE)
                    results.append({
                        "user": st.session_state.username,
                        "subject": current_sub,
                        "score": result_str
                    })
                    save_data(RESULTS_FILE, results)
            
            if st.button("Басқа пән таңдауға қайту"):
                st.session_state.test_started = False
                st.rerun()

    # 2. СҰРАҚ ҚОСУ ЖӘНЕ ӨШІРУ
    elif menu == "Сұрақ қосу / Өзгерту":
        st.title("➕ Сұрақтарды басқару және өшіру")
        
        if "delete_q_id" in st.session_state:
            q_id_to_del = st.session_state.delete_q_id
            updated_tests = [q for q in tests if q["id"] != q_id_to_del]
            save_data(TESTS_FILE, updated_tests)
            del st.session_state.delete_q_id
            st.success("Сұрақ сәтті өшірілді!")
            st.rerun()

        tab1, tab2 = st.tabs(["Қолданыстағы сұрақтар", "Жаңа сұрақ қосу"])
        
        with tab1:
            st.subheader("Барлық сұрақтар тізімі")
            if not tests:
                st.info("Әзірге сұрақтар жоқ.")
            else:
                for q in tests:
                    with st.expander(f"[{q.get('subject', 'Билгісіз пән')}] ID: {q['id']} - {q['question'][:40]}..."):
                        st.markdown(f"**Пән:** {q.get('subject')}")
                        st.markdown(f"**Сұрақ:** {q['question']}")
                        st.markdown(f"**Нұсқалар:** {q['options']}")
                        st.markdown(f"**Дұрыс жауап:** {q['answer']}")
                        
                        if st.button("Сұрақты өшіру", key=f"del_{q['id']}"):
                            st.session_state.delete_q_id = q['id']
                            st.rerun()

        with tab2:
            st.subheader("Жаңа сұрақ қосу")
            with st.form("add_question_form"):
                subject_input = st.selectbox("Пәнді таңдаңыз немесе жазыңыз:", ["Математика", "Информатика", "Физика", "Тарих", "Ағылшын тілі"])
                custom_subject = st.text_input("Немесе жаңа пән атауын енгізіңіз (егер жоғарыда жоқ болса):")
                
                new_q = st.text_area("Сұрақ мәтіні")
                c1 = st.text_input("Нұсқа A")
                c2 = st.text_input("Нұсқа B")
                c3 = st.text_input("Нұсқа C")
                c4 = st.text_input("Нұсқа D")
                
                # МТІН ЖАЗУДЫҢ ОРНЫНА ТАҢДАУҒА АЙНАЛДЫРУ (selectbox)
                correct_ans_letter = st.selectbox("Дұрыс жауаптың әрпін таңдаңыз:", ["A", "B", "C", "D"])
                
                add_submitted = st.form_submit_button("Сұрақты сақтау")
                
                if add_submitted:
                    final_subject = custom_subject.strip() if custom_subject.strip() else subject_input
                    if final_subject and new_q and c1 and c2:
                        options_dict = {"A": c1, "B": c2, "C": c3, "D": c4}
                        selected_correct_text = options_dict.get(correct_ans_letter)
                        
                        if not selected_correct_text:
                            st.error("Таңдалған әріпке сәйкес келетін нұсқа бос болмауы тиіс!")
                        else:
                            new_id = max([q["id"] for q in tests], default=0) + 1
                            new_question_data = {
                                "id": new_id,
                                "subject": final_subject,
                                "question": new_q.strip(),
                                "options": [c1, c2, c3, c4],
                                "answer": selected_correct_text
                            }
                            tests.append(new_question_data)
                            save_data(TESTS_FILE, tests)
                            st.success("Сұрақ базаға сәтті қосылды!")
                    else:
                        st.error("Пән, сұрақ және кем дегенде A мен B нұсқаларын толтырыңыз!")

    # 3. НӘТИЖЕЛЕРДІ КӨРУ
    elif menu == "Нәтижелер":
        st.title("📊 Тест нәтижелері")
        results = load_data(RESULTS_FILE)
        if results:
            results_for_df = []
            for r in results:
                results_for_df.append({
                    "Қолданушы": r['user'],
                    "Пән": r.get('subject', 'Жалпы'),
                    "Ұпай": r['score']
                })
            st.dataframe(pd.DataFrame(results_for_df))
            
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
