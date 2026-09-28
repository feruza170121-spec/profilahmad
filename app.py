<!DOCTYPE html>
<html lang="kk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Жеке Инфо-Мат УБТ Базасы</title>
    <style>
        :root {
            --bg-color: #121212;
            --panel-bg: #1e1e1e;
            --accent-color: #ff5252;
            --text-color: #ffffff;
            --border-color: #333;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        .hidden { display: none !important; }

        /* Логин экраны */
        #login-screen {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: var(--bg-color);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 100;
        }
        .login-card {
            background-color: var(--panel-bg);
            padding: 30px;
            border-radius: 12px;
            width: 350px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            text-align: center;
        }
        .login-card h2 { color: var(--accent-color); margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; text-align: left; }
        .form-group label { display: block; margin-bottom: 5px; font-size: 14px; color: #aaa; }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            background-color: #2d2d2d;
            border: 1px solid var(--border-color);
            color: white;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 14px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: var(--accent-color);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: 0.2s;
        }
        button:hover { opacity: 0.9; }

        /* Негізгі интерфейс (Сайдбар + Контент) */
        sidebar {
            width: 280px;
            background-color: var(--panel-bg);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            padding: 20px;
            box-sizing: border-box;
        }
        .profile-box {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
        }
        .profile-avatar {
            width: 80px; height: 80px;
            border-radius: 50%;
            background-color: #333;
            margin: 0 auto 10px;
            overflow: hidden;
            border: 2px solid var(--accent-color);
        }
        .profile-avatar img { width: 100%; height: 100%; object-fit: cover; }
        .profile-name { font-size: 18px; font-weight: bold; }
        
        .nav-menu {
            margin-top: 20px;
            flex-grow: 1;
        }
        .nav-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background: transparent;
            color: #ccc;
            border: none;
            text-align: left;
            border-radius: 6px;
            margin-bottom: 5px;
            cursor: pointer;
        }
        .nav-btn:hover, .nav-btn.active {
            background-color: #2d2d2d;
            color: var(--accent-color);
        }

        main {
            flex-grow: 1;
            padding: 30px;
            overflow-y: auto;
            box-sizing: border-box;
        }
        .card {
            background-color: var(--panel-bg);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            margin-bottom: 20px;
        }
        
        /* Пәндер тізімі */
        .subject-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
        }
        .subject-card {
            background-color: #252525;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            transition: 0.2s;
        }
        .subject-card:hover {
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }
        .subject-card h3 { margin-top: 0; color: var(--accent-color); }

        /* Тест терезесі */
        .question-box { font-size: 18px; margin-bottom: 20px; }
        .options-list button {
            display: block;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            background-color: #2d2d2d;
            color: white;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            text-align: left;
            cursor: pointer;
        }
        .options-list button:hover { background-color: var(--accent-color); }
        
        /* Басқару элементтері */
        .delete-btn {
            background-color: #d32f2f;
            color: white;
            padding: 5px 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-top: 10px;
        }
    </style>
</head>
<body>

    <!-- ЛОГИН ЭКРАНЫ -->
    <div id="login-screen">
        <div class="login-card">
            <h2>Инфо-Мат Жүйесі</h2>
            <div class="form-group">
                <label>Логин:</label>
                <input type="text" id="login-user" placeholder="Логин енгізіңіз">
            </div>
            <div class="form-group">
                <label>Пароль:</label>
                <input type="password" id="login-pass" placeholder="Пароль енгізіңіз">
            </div>
            <button onclick="handleLogin()">Кіру</button>
            <p id="login-error" style="color: var(--accent-color); font-size: 13px; margin-top: 10px;"></p>
        </div>
    </div>

    <!-- БАСҚАРУ ПАНЕЛІ (САЙДБАР) -->
    <sidebar id="sidebar" class="hidden">
        <div class="profile-box">
            <div class="profile-avatar">
                <img id="user-avatar-img" src="https://via.placeholder.com/80" alt="Avatar">
            </div>
            <div class="profile-name" id="user-display-name">Админ</div>
        </div>
        <div class="nav-menu">
            <button class="nav-btn active" onclick="switchTab('subjects')">📚 Тесттер тізімі</button>
            <button class="nav-btn" onclick="switchTab('creator')">➕ Сұрақ / Тест қосу</button>
            <button class="nav-btn" onclick="switchTab('results')">📊 Менің нәтижелерім</button>
            <button class="nav-btn" onclick="switchTab('profile')">⚙️ Профильді баптау</button>
        </div>
        <button class="nav-btn" style="color: var(--accent-color);" onclick="logout()">Шығу</button>
    </sidebar>

    <!-- НЕГІЗГІ МАЗМҰН -->
    <main id="main-content" class="hidden">
        
        <!-- 1. ПӘНДЕР МЕН ТЕСТТЕР -->
        <div id="tab-subjects" class="tab-content">
            <h2>Инфо-Мат Бағыты (Әр тест 50 сұраққа дейін)</h2>
            <div class="subject-grid" id="subjects-container">
                <!-- Динамикалық түрде енгізілген тесттер осында түседі -->
            </div>
        </div>

        <!-- 2. СҰРАҚ ЖӘНЕ ТЕСТ ҚОСУ (АДМИН) -->
        <div id="tab-creator" class="tab-content hidden">
            <h2>Жаңа Тест немесе Сұрақ қосу</h2>
            <div class="card">
                <div class="form-group">
                    <label>Бөлімді таңдаңыз:</label>
                    <select id="new-subject">
                        <option value="Математика тарихы">Математика тарихы</option>
                        <option value="Математикалық сауаттылық">Математикалық сауаттылық</option>
                        <option value="Математика">Математика</option>
                        <option value="Информатика">Информатика</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Тест атауы:</label>
                    <input type="text" id="new-test-title" placeholder="Мысалы: №1 Тест немесе Логика негіздері">
                </div>
                <div class="form-group">
                    <label>Сұрақ мәтіні:</label>
                    <textarea id="new-question" rows="3" placeholder="Сұрақты жазыңыз..."></textarea>
                </div>
                <div class="form-group">
                    <label>1-ші жауап нұсқасы:</label>
                    <input type="text" id="opt-0">
                </div>
                <div class="form-group">
                    <label>2-ші жауап нұсқасы:</label>
                    <input type="text" id="opt-1">
                </div>
                <div class="form-group">
                    <label>3-ші жауап нұсқасы:</label>
                    <input type="text" id="opt-2">
                </div>
                <div class="form-group">
                    <label>4-ші жауап нұсқасы:</label>
                    <input type="text" id="opt-3">
                </div>
                <div class="form-group">
                    <label>Дұрыс жауапты белгілеңіз:</label>
                    <select id="correct-opt">
                        <option value="0">1-ші нұсқа дұрыс</option>
                        <option value="1">2-ші нұсқа дұрыс</option>
                        <option value="2">3-ші нұсқа дұрыс</option>
                        <option value="3">4-ші нұсқа дұрыс</option>
                    </select>
                </div>
                <button onclick="saveQuestionToTest()">Сұрақты сақтау / Қосу</button>
            </div>
        </div>

        <!-- 3. НӘТИЖЕЛЕР -->
        <div id="tab-results" class="tab-content hidden">
            <h2>Менің нәтижелерім</h2>
            <div class="card" id="results-list">
                <p>Әзірге тапсырылған тесттер жоқ.</p>
            </div>
        </div>

        <!-- 4. ПРОФИЛЬДІ БАПТАУ -->
        <div id="tab-profile" class="tab-content hidden">
            <h2>Профильді өңдеу</h2>
            <div class="card">
                <div class="form-group">
                    <label>Сіздің атауыңыз (Никнейм):</label>
                    <input type="text" id="profile-name-input" value="Админ">
                </div>
                <div class="form-group">
                    <label>Аватар сурет сілтемесі (URL):</label>
                    <input type="text" id="profile-avatar-input" placeholder="Сурет сілтемесін жабыстырыңыз">
                </div>
                <button onclick="updateProfile()">Сақтау</button>
            </div>
        </div>

        <!-- 5. ТЕСТТІ ӨТҮ (Динамикалық) -->
        <div id="tab-active-test" class="tab-content hidden">
            <button onclick="switchTab('subjects')" style="width: auto; padding: 5px 15px; margin-bottom: 15px;">← Артқа қайту</button>
            <div class="card">
                <h3 id="active-test-title">Тест атауы</h3>
                <div id="quiz-container-box">
                    <div class="question-box" id="active-q-text">Сұрақ...</div>
                    <div class="options-list" id="active-options"></div>
                </div>
            </div>
        </div>

    </main>

    <script>
        // Деректерді сақтау (localStorage арқылы браузерде сақталады)
        let appData = JSON.parse(localStorage.getItem('infomat_data')) || {
            username: "MyProfile",
            avatar: "https://via.placeholder.com/80",
            tests: [
                {
                    id: 1,
                    subject: "Математика тарихы",
                    title: "Математика тарихы: Бастапқы кезең (50 сұраққа дейін)",
                    questions: [
                        {
                            question: "Пифагор теоремасы қай халыққа ерте заманнан белгілі болған?",
                            options: ["Вавилон және Қытай", "Тек Грекия", "Рим империясы", "Мысыр ғана"],
                            correct: 0
                        }
                    ]
                },
                {
                    id: 2,
                    subject: "Математикалық сауаттылық",
                    title: "Логикалық есептер мен сандар тізбегі",
                    questions: [
                        {
                            question: "2, 4, 8, 16, ? келесі санды тап",
                            options: ["20", "24", "32", "64"],
                            correct: 2
                        }
                    ]
                },
                {
                    id: 3,
                    subject: "Математика",
                    title: "Алгебра және геометрия негіздері",
                    questions: [
                        {
                            question: "sin²(x) + cos²(x) неге тең?",
                            options: ["0", "1", "2", "-1"],
                            correct: 1
                        }
                    ]
                },
                {
                    id: 4,
                    subject: "Информатика",
                    title: "Python және Алгоритмдер",
                    questions: [
                        {
                            question: "Python тілінде цикл ашу операторы:",
                            options: ["loop", "for / while", "repeat", "if / else"],
                            correct: 1
                        }
                    ]
                }
            ],
            results: []
        };

        const correctUser = "admin";
        const correctPass = "12345"; // Өз қалауыңызша өзгерте аласыз

        function handleLogin() {
            let u = document.getElementById("login-user").value;
            let p = document.getElementById("login-pass").value;
            if(u === correctUser && p === correctPass) {
                document.getElementById("login-screen").classList.add("hidden");
                document.getElementById("sidebar").classList.remove("hidden");
                document.getElementById("main-content").classList.remove("hidden");
                renderUI();
            } else {
                document.getElementById("login-error").innerText = "Қате логин немесе пароль!";
            }
        }

        function logout() {
            document.getElementById("login-screen").classList.remove("hidden");
            document.getElementById("sidebar").classList.add("hidden");
            document.getElementById("main-content").classList.add("hidden");
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById('tab-' + tabId).classList.remove('hidden');
            if(tabId === 'subjects') renderSubjects();
            if(tabId === 'results') renderResults();
        }

        function renderUI() {
            document.getElementById("user-display-name").innerText = appData.username;
            document.getElementById("user-avatar-img").src = appData.avatar;
            document.getElementById("profile-name-input").value = appData.username;
            document.getElementById("profile-avatar-input").value = appData.avatar;
            renderSubjects();
        }

        function updateProfile() {
            appData.username = document.getElementById("profile-name-input").value;
            appData.avatar = document.getElementById("profile-avatar-input").value;
            localStorage.setItem('infomat_data', JSON.stringify(appData));
            renderUI();
            alert("Профиль сәтті жаңартылды!");
        }

        function renderSubjects() {
            let container = document.getElementById("subjects-container");
            container.innerHTML = "";
            
            appData.tests.forEach((test, index) => {
                let div = document.createElement("div");
                div.className = "subject-card";
                div.innerHTML = `
                    <span style="font-size: 12px; color: var(--accent-color);">${test.subject}</span>
                    <h3>${test.title}</h3>
                    <p style="font-size: 13px; color: #aaa;">Сұрақ саны: ${test.questions.length} / 50</p>
                    <button onclick="startTest(${test.id})" style="padding: 6px; font-size: 13px;">Тестті бастау</button>
                    <button class="delete-btn" onclick="deleteTest(${test.id})">Тестті өшіру</button>
                `;
                container.appendChild(div);
            });
        }

        function deleteTest(id) {
            if(confirm("Бұл тестті шынымен өшіргіңіз келе ме?")) {
                appData.tests = appData.tests.filter(t => t.id !== id);
                localStorage.setItem('infomat_data', JSON.stringify(appData));
                renderSubjects();
            }
        }

        function saveQuestionToTest() {
            let subject = document.getElementById("new-subject").value;
            let title = document.getElementById("new-test-title").value;
            let qText = document.getElementById("new-question").value;
            let opts = [
                document.getElementById("opt-0").value,
                document.getElementById("opt-1").value,
                document.getElementById("opt-2").value,
                document.getElementById("opt-3").value
            ];
            let correct = parseInt(document.getElementById("correct-opt").value);

            if(!title || !qText || opts.some(o => !o)) {
                alert("Барлық өрістерді толтырыңыз!");
                return;
            }

            let existingTest = appData.tests.find(t => t.title === title && t.subject === subject);
            let newQ = { question: qText, options: opts, correct: correct };

            if(existingTest) {
                if(existingTest.questions.length >= 50) {
                    alert("Бұл тестте 50 сұрақ толып қалды!");
                    return;
                }
                existingTest.questions.push(newQ);
            } else {
                let newTest = {
                    id: Date.now(),
                    subject: subject,
                    title: title,
                    questions: [newQ]
                };
                appData.tests.push(newTest);
            }

            localStorage.setItem('infomat_data', JSON.stringify(appData));
            alert("Сұрақ сәтті қосылды!");
            switchTab('subjects');
        }

        // Тест тапсыру логикасы
        let currentActiveTest = null;
        let currentQIndex = 0;
        let currentScore = 0;

        function startTest(id) {
            currentActiveTest = appData.tests.find(t => t.id === id);
            if(!currentActiveTest || currentActiveTest.questions.length === 0) {
                alert("Бұл тестте әзірге сұрақтар жоқ!");
                return;
            }
            currentQIndex = 0;
            currentScore = 0;
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.getElementById('tab-active-test').classList.remove('hidden');
            document.getElementById('active-test-title').innerText = currentActiveTest.title;
            loadActiveQuestion();
        }

        function loadActiveQuestion() {
            let q = currentActiveTest.questions[currentQIndex];
            document.getElementById('active-q-text').innerText = `${currentQIndex + 1}. ${q.question}`;
            let optBox = document.getElementById('active-options');
            optBox.innerHTML = "";

            q.options.forEach((opt, idx) => {
                let btn = document.createElement("button");
                btn.innerText = opt;
                btn.onclick = () => checkAnswer(idx, q.correct);
                optBox.appendChild(btn);
            });
        }

        function checkAnswer(selected, correct) {
            if(selected === correct) currentScore++;
            currentQIndex++;

            if(currentQIndex < currentActiveTest.questions.length) {
                loadActiveQuestion();
            } else {
                alert(`Тест аяқталды! Ұпайыңыз: ${currentScore} / ${currentActiveTest.questions.length}`);
                appData.results.push({
                    title: currentActiveTest.title,
                    score: currentScore,
                    total: currentActiveTest.questions.length,
                    date: new Date().toLocaleDateString()
                });
                localStorage.setItem('infomat_data', JSON.stringify(appData));
                switchTab('subjects');
            }
        }

        function renderResults() {
            let resBox = document.getElementById('results-list');
            if(appData.results.length === 0) {
                resBox.innerHTML = "<p>Әзірге нәтижелер жоқ.</p>";
                return;
            }
            resBox.innerHTML = appData.results.map(r => `
                <div style="border-bottom: 1px solid #333; padding: 10px 0;">
                    <strong>${r.title}</strong><br>
                    Нәтиже: ${r.score} / ${r.total} (${r.date})
                </div>
            `).join('');
        }
    </script>
</body>
</html>
