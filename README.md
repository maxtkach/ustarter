# UStarter
## Обов'язки
Женя: безпека та зв'язок бекенда з фронтом через Flask <br>
Влад: запроси та вивід <br>
Стас: API та структура БД <br>

## Запуск проекту
Для запуску проекту вам необхідно:
 1. Завантажити репозиторій
 2. Встановити необхідні бібліотеки `pip install -r requirements.txt`
 3. Запустити сайт `python3 app.py`
 4. Для перегляду сайту перейдіть на посилання у терміналі (`localhost:8080`)

## Структура проекту
<ul class="project-tree" style="list-style-type:none;margin: 0">
    <li><span><b>app.py</b></span></li>
    <li><span><b>database.db</b></span></li>
    <li>
        <span>static</span>
        <ul style="list-style-type:none;margin: 0">
            <li><span>js, css, scss, fonts, images</span></li>
            <!--li><span>js</span></li>
            <li><span>css</span></li>
            <li><span>scss</span></li>
            <li><span>fonts</span></li>
            <li><span>images</span></li-->
        </ul>
    </li>
    <li>
        <span>templates</span>
        <ul style="list-style-type:none;margin: 0">
            <li><span><b>index.html</b></span></li>
        </ul>
    </li>
</ul>

## TO DO:
- Зробити `requirements.txt`
- `favicon.ico`
- Зробити сторінку проекту, сторінку "усі проекти"
- Додати вибір категорії

## Нотатки
- `app.run(debug=True)` повинно бути змінено перед публікацією, задля уникнення вразливостей
- Усі коментарі повинні бути видалені або написані українською
- Вказання файлів

## Безпека
- Імена файлів при завантаженні
- DDoS, bruteforce атаки та подібні
- Можливі SQL та XSS ін'єкції
- Логи у вигляді `print`
- Паролі у простому вигляді
- Нема хешування
- Дозволи користувачів на локальному сховищі
- Заборона енумерації

<br>:3
