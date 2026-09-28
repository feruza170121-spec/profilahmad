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
    # Әдепкі қолданушы (тек сіз кіретін логин мен пароль)
    if not os.path.exists(USERS_FILE):
        default_users = {"admin": "secret123"}  # Логин мен парольді осы жерден өзгерте аласыз
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, ensure_ascii=False, indent=4)
            
    # Бастапқы тест сұрақтары
    if not os.path.exists(TESTS_FILE):
        default_tests = [
            {
                "id": 1,
                "question": "Python тілінде тізім (list) қандай жақшамен анықталады?",
                "options": ["{}", "[]", "()", "<>"],
                "answer": "[]"
            },
            {
                "id": 2,
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

# Деректерді оқу/жазу функциялары
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

# --- КІРУ (ЛОГИН) ПАРАҒЫ (Тіркелу алынып тасталды) ---
def login_page():
    st.title("🔐 Жеке Кабинетке Кіру")
    st.info("Жүйе тек иесіне арналған. Тіркелу функциясы өшірілген.")
    
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

# --- ТЕСТ ТАПСЫРУ ЖӘНЕ БАСҚАРУ БӨЛІМІ ---
def main_app():
    st.sidebar.title(f"Қош келдіңіз, {st.session_state.username}!")
    menu = st.sidebar.radio("Мәзір", ["Тест тапсыру", "Сұрақ қосу / Өзгерту", "Нәтижелерді көру"])
    
    if st.sidebar.button("Жүйеден шығу"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
        
    tests = load_data(TESTS_FILE)
    
    if menu == "Тест тапсыру":
        st.title("📝 Тест тапсыру")
        
        if not tests:
            st.warning("Әзірге тест сұрақтары жоқ.")
            return
            
        score = 0
        with st.form("test_execution_form"):
            user_answers = {}
            for i, q in enumerate(tests):
                st.markdown(f"**{i+1}. {q['question']}**")
                user_answers[q['id']] = st.radio("Жауапты таңдаңыз:", q['options'], key=f"q_{q['id']}")
                st.write("---")
                
            submitted = st.form_submit_button("Нәтижені тапсыру")
            
            if submitted:
                for q in tests:
                    if user_answers.get(q['id']) == q['answer']:
                        score += 1
                
                result_text = f"Тест аяқталды! Нәтижеңіз: {score} / {len(tests)}"
                st.success(result_text)
                
                # Нәтижені JSON-ға сақтау
                results = load_data(RESULTS_FILE)
                results.append({"user": st.session_state.username, "score": f"{score}/{len(tests)}"})
                save_data(RESULTS_FILE, results)

    elif menu == "Сұрақ қосу / Өзгерту":
        st.title("➕ Жаңа сұрақ қосу")
        
        with st.form("add_question_form"):
            new_q = st.text_input("Сұрақ мәтіні")
            opt1 = st.text_input("1-ші нұсқа")
            opt2 = st.text_input("2-ші нұсқа")
            opt3 = st.text_input("3-ші нұсқа")
            opt4 = st.text_input("4-ші нұсқа")
            correct_ans = st.text_input("Дұрыс жауап (жоғарыдағы нұсқалардың білдей біреуін жазыңыз)")
            
            add_submitted = st.form_submit_button("Сұрақты сақтау")
            
            if add_submitted:
                if new_q and opt1 and opt2 and correct_ans:
                    new_id = tests[-1]["id"] + 1 if tests else 1
                    new_question_data = {
                        "id": new_id,
                        "question": new_q,
                        "options": [opt1, opt2, opt3, opt4],
                        "answer": correct_ans
                    }
                    tests.append(new_question_data)
                    save_data(TESTS_FILE, tests)
                    st.success("Сәтті қосылды! (JSON файлына жазылды)")
                else:
                    st.error("Барлық міндетті өрістерді толтырыңыз!")

    elif menu == "Нәтижелерді көру":
        st.title("📊 Сақталған нәтижелер")
        results = load_data(RESULTS_FILE)
        if results:
            for r in results:
                st.write(f"👤 Қолданушы: **{r['user']}** | 🎯 Нәтиже: **{r['score']}**")
        else:
            st.info("Әзірге нәтижелер жоқ.")

# Бағдарлама логикасы
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
