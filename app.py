import streamlit as st
import json
import os

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
                "subject": "Математика",
                "question": "Шеңбердің радиусы 5 болса, диаметрі неге тең?",
                "options": ["5", "10", "2.5", "20"],
                "answer": "10"
            },
            {
                "id": 3,
                "subject": "Информатика",
                "question": "Python тілінде тізім (list) қандай жақшамен анықталады?",
                "options": ["{}", "[]", "()", "<>"],
                "answer": "[]"
            },
            {
                "id": 4,
                "subject": "Информатика",
                "question": "Қазақстанның елордасы қай қала?",
                "options": ["Алматы", "Шымкент", "Астана", "Қарағанды"],
                "answer": "Астана"
            }
        ]
        with open(TESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_tests, f, ensure_ascii=False, indent=4)

    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

init_json_files()

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Сессияны басқару
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- КІРУ ПАРАҒЫ ---
def login_page():
    st.title("🔐 Жеке Кабинетке Кіру")
    users = load_data(USERS_FILE)
    
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
    menu = st.sidebar.radio("Мәзір", ["Тест тапсыру", "Сұрақ қосу", "Нәтижелер", "Логин/Парольді өзгерту"])
    
    if st.sidebar.button("Жүйеден шығу"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
        
    tests = load_data(TESTS_FILE)
    
    # 1. ПӘНДЕР БОЙЫНША БӨЛЕК ТЕСТ ТАПСЫРУ
    if menu == "Тест тапсыру":
        st.title("📝 Пәндер бойынша тест тапсыру")
        
        if not tests:
            st.warning("Әзірге тест сұрақтары жоқ.")
            return
            
        # Қолжетімді пәндер тізімін жинау
        subjects = list(set(q["subject"] for q in tests))
        selected_subject = st.selectbox("Пәнді таңдаңыз:", subjects)
        
        # Таңдалған пәннің сұрақтарын сүзу
        subject_tests = [q for q in tests if q["subject"] == selected_subject]
        
        st.write(f"Таңдалған пән: **{selected_subject}** (Сұрақтар саны: {len(subject_tests)})")
        
        score = 0
        with st.form(f"test_form_{selected_subject}"):
            user_answers = {}
            for i, q in enumerate(subject_tests):
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[q['id']] = st.radio("Жауапты таңдаңыз:", q['options'], key=f"q_{q['id']}")
                st.write("---")
                
            submitted = st.form_submit_button("Тестті аяқтау және нәтижені көру")
            
            if submitted:
                for q in subject_tests:
                    if user_answers.get(q['id']) == q['answer']:
                        score += 1
                
                result_str = f"{score} / {len(subject_tests)}"
                st.success(f"Тест аяқталды! Сіздің нәтижеңіз ({selected_subject}): {result_str}")
                
                # Нәтижені JSON-ға сақтау
                results = load_data(RESULTS_FILE)
                results.append({
                    "user": st.session_state.username,
                    "subject": selected_subject,
                    "score": result_str
                })
                save_data(RESULTS_FILE, results)

    # 2. СҰРАҚ ҚОСУ
    elif menu == "Сұрақ қосу":
        st.title("➕ Жаңа сұрақ қосу")
        
        with st.form("add_question_form"):
            subject_input = st.text_input("Пән атауы (мысалы: Математика, Тарих)")
            new_q = st.text_input("Сұрақ мәтіні")
            opt1 = st.text_input("1-ші нұсқа")
            opt2 = st.text_input("2-ші нұсқа")
            opt3 = st.text_input("3-ші нұсқа")
            opt4 = st.text_input("4-ші нұсқа")
            correct_ans = st.text_input("Дұрыс жауап (жоғарыдағы нұсқалардың дәл өзін жазыңыз)")
            
            add_submitted = st.form_submit_button("Сұрақты сақтау")
            
            if add_submitted:
                if subject_input and new_q and opt1 and opt2 and correct_ans:
                    new_id = tests[-1]["id"] + 1 if tests else 1
                    new_question_data = {
                        "id": new_id,
                        "subject": subject_input.strip(),
                        "question": new_q.strip(),
                        "options": [opt1, opt2, opt3, opt4],
                        "answer": correct_ans.strip()
                    }
                    tests.append(new_question_data)
                    save_data(TESTS_FILE, tests)
                    st.success("Сұрақ базаға сәтті қосылды!")
                else:
                    st.error("Барлық міндетті өрістерді толтырыңыз!")

    # 3. НӘТИЖЕЛЕРДІ КӨРУ
    elif menu == "Нәтижелер":
        st.title("📊 Тест нәтижелері")
        results = load_data(RESULTS_FILE)
        if results:
            for r in results:
                st.write(f"👤 Қолданушы: **{r['user']}** | 📚 Пән: **{r['subject']}** | 🎯 Нәтиже: **{r['score']}**")
        else:
            st.info("Әзірге сақталған нәтижелер жоқ.")

    # 4. ЛОГИН ЖӘНЕ ПАРОЛЬДІ ӨЗГЕРТУ
    elif menu == "Логин/Парольді өзгерту":
        st.title("⚙️ Жеке деректерді өзгерту")
        
        users = load_data(USERS_FILE)
        current_user = st.session_state.username
        
        with st.form("change_credentials_form"):
            st.write("Парольді немесе логинді өзгерту үшін төменгі өрістерді толтырыңыз:")
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
                        st.success("Логин мен пароль сәтті өзгертілді! Бетті жаңартыңыз.")
                    else:
                        st.warning("Өрістер бос болмауы тиіс.")
                else:
                    st.error("Қазіргі пароль қате енгізілді!")

# Бағдарлама логикасы
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
