workspace {

    model {
        user = person "Пользователь" {
            description "Человек, который регистрируется на сайте, добавляет доклады и участвует в конференциях."
        }

        conferenceAdmin = person "Организатор конференции" {
            description "Человек, который организует конференции и управляет докладами."
        }

        system = softwareSystem "Conference Website" {
            description "Система для управления пользователями, докладами и конференциями."
            
            webapp = container "Frontend" {
                technology "HTML, CSS, JavaScript"
                description "Пользовательский интерфейс для работы с сайтом конференции."
            }

            api = container "Backend" {
                technology "Spring Boot, REST API"
                description "Серверное приложение, которое обрабатывает запросы пользователей и организаторов."
            }

            database = container "Database" {
                technology "PostgreSQL"
                description "Хранилище данных для пользователей, докладов и конференций."
            }

            user -> webapp "Использует для работы с системой"
            webapp -> api "Отправляет запросы"
            api -> database "Читает и записывает данные"
            conferenceAdmin -> webapp "Использует для управления конференциями"
        }
    }

    views {
        systemContext system {
            include *
            autolayout lr
        }

        container system {
            include *
            autolayout lr
        }

        dynamic system "add_presentation_to_conference" {
            user -> webapp "Добавляет новый доклад"
            webapp -> api "Отправляет запрос на создание доклада"
            api -> database "Сохраняет доклад"
            conferenceAdmin -> webapp "Добавляет доклад в конференцию"
            webapp -> api "Отправляет запрос на добавление доклада в конференцию"
            api -> database "Обновляет данные о конференции"
            
            autolayout lr
        }

        theme default
    }
}
