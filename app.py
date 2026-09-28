import streamlit as st

# Беттің баптауы
st.set_page_config(page_title="Тест платформасы", page_icon="📝", layout="centered")

# Сессияны басқару (қолданушының кіргенін тексеру үшін)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
# Тіркелген қолданушылар базасы (қазірше жадта сақталады)
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"} # Мысал үшін стандартты қолданушы

# Авторизация / Тіркелу парағы
def auth_page():
    st.title("🔐 Жеке кабинетке кіру")
    
    tab1, tab2 = st.tabs(["Кіру", "Тіркелу"])
    
    with tab1:
        st.subheader("Жүйеге кіру")
        login_user = st.text_input("Логин", key="login_user")
        login_pass = st.text_input("Пароль", type="password", key="login_pass")
        
        if st.button("Кіру"):
            if login_user in st.session_state.users and st.session_state.users[login_user] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success(f"Қош келдіңіз, {login_user}!")
                st.rerun()
            else:
                st.error("Логин или пароль қате!")
                
    with tab2:
        st.subheader("Жаңа аккаунт ашу")
        new_user = st.text_input("Жаңа логин", key="new_user")
        new_pass = st.text_input("Жаңа пароль", type="password", key="new_pass")
        
        if st.button("Тіркелу"):
            if new_user in st.session_state.users:
                st.warning("Бұл логин бос емес, басқасын таңдаңыз.")
            elif new_user.strip() == "" or new_pass.strip() == "":
                st.warning("Логин мен пароль бос болмауы керек.")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Сәтті тіркелдіңіз! Енді 'Кіру' бөлімі арқылы кіре аласыз.")

# Негізгі тест тапсыру бөлімі
def test_page():
    st.sidebar.title(f"Қош келдіңіз, {st.session_state.username}!")
    if st.sidebar.button("Шығу (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
        
    st.title("📝 ҰБТ / Тест тапсыру жүйесі")
    st.write("Төмендегі сұрақтарға жауап беріп, өзіңізді сынап көріңіз.")
    
    # Тест сұрақтарын осында өзгерте аласыз немесе қоса аласыз
    questions = [
        {
            "id": 1,
            "question": "Қазақстанның астанасы қай қала?",
            "options": ["Алматы", "Шымкент", "Астана", "Қарағанды"],
            "answer": "Астана"
        },
        {
            "id": 2,
            "question": "Python бағдарламалау тілі қашан шықты?",
            "options": ["1991", "1995", "2000", "1985"],
            "answer": "1991"
        }
    ]
    
    score = 0
    with st.form("test_form"):
        user_answers = {}
        for q in questions:
            st.markdown(f"**{q['id']}. {q['question']}**")
            user_answers[q['id']] = st.radio("Жауапты таңдаңыз:", q['options'], key=f"q_{q['id']}")
            st.write("---")
            
        submitted = st.form_submit_button("Нәтижені тексеру")
        
        if submitted:
            for q in questions:
                if user_answers[q['id']] == q['answer']:
                    score += 1
            st.success(f"Тест аяқталды! Сіздің жинаған ұпайыңыз: {score} / {len(questions)}")

# Бағдарламаның логикасы
if not st.session_state.logged_in:
    auth_page()
else:
    test_page()
