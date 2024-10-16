1. Для сайта конференции можно выделить следующие ключевые варианты использования:
Регистрация пользователей и добавление докладов:
Пользователь регистрируется на сайте с помощью логина, имени и фамилии.
Зарегистрированный пользователь добавляет новый доклад.
Пользователь может привязать свой доклад к одной или нескольким конференциям.
Поиск пользователей и получение информации о докладах:
Администратор или организатор может искать пользователей по логину или маске (имя и фамилия).
Пользователь или организатор конференции может просматривать список всех докладов, а также список докладов, привязанных к конкретной конференции.

2. Приоритеты можно распределить следующим образом:
Безопасность — очень важно защитить данные пользователей (например, личные данные, логины, пароли) и информацию о конференциях.
Производительность — важно, чтобы система обрабатывала запросы на поиск пользователей и докладов быстро, особенно если база данных будет расти.
Надежность — система должна быть устойчивой к сбоям и гарантировать доступность данных для всех пользователей в любое время.
Масштабируемость — в будущем можно ожидать роста числа пользователей и конференций, поэтому система должна быть легко масштабируемой.

4. Контейнеры:
Frontend — пользовательский интерфейс сайта.
Backend — серверная часть, которая отвечает за обработку логики (регистрация пользователей, управление докладами и конференциями).
Database — база данных для хранения пользователей, докладов и конференций.

5.Технологии уже проставлены в коде контейнеров выше:
Frontend — HTML, CSS, JavaScript.
Backend — Spring Boot, REST API.
Database — PostgreSQL.
Связи между контейнерами также указаны: фронтенд отправляет запросы на бэкенд, а бэкенд взаимодействует с базой данных.