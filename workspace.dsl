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

            # Контейнер для пользователей
            usersContext = container "Users Context" {
                technology "Spring Boot, REST API"
                description "Контекст для управления пользователями: регистрация и поиск."

                userService = component "UserService" {
                    technology "Spring Service"
                    description "Сервис управления пользователями (создание и поиск пользователей)."
                }
            }

            # Контейнер для докладов
            talksContext = container "Talks Context" {
                technology "Spring Boot, REST API"
                description "Контекст для управления докладами: создание и поиск докладов."

                talkService = component "TalkService" {
                    technology "Spring Service"
                    description "Сервис управления докладами (создание и поиск докладов)."
                }
            }

            # Контейнер для конференций
            conferencesContext = container "Conferences Context" {
                technology "Spring Boot, REST API"
                description "Контекст для управления конференциями: создание конференций и добавление докладов."

                conferenceService = component "ConferenceService" {
                    technology "Spring Service"
                    description "Сервис управления конференциями (создание конференций, добавление докладов)."
                }
            }

            # База данных для пользователей
            usersDb = container "Users Database" {
                technology "PostgreSQL"
                description "База данных для хранения информации о пользователях."
            }

            # База данных для докладов
            talksDb = container "Talks Database" {
                technology "PostgreSQL"
                description "База данных для хранения информации о докладах."
            }

            # База данных для конференций
            conferencesDb = container "Conferences Database" {
                technology "PostgreSQL"
                description "База данных для хранения информации о конференциях."
            }

            # Взаимодействие между пользователями и контекстом
            user -> usersContext "Регистрируется и ищет других пользователей"
            usersContext -> usersDb "Читает и записывает данные пользователей"

            # Взаимодействие между докладами и контекстом
            user -> talksContext "Создает и ищет доклады"
            talksContext -> talksDb "Читает и записывает данные докладов"

            # Взаимодействие между конференциями и контекстом
            conferenceAdmin -> conferencesContext "Создает конференции и добавляет доклады"
            conferencesContext -> conferencesDb "Читает и записывает данные о конференциях"
            conferencesContext -> talksContext "Добавляет доклады в конференцию"
        }
    }

    views {
        # Диаграмма контекста системы
        systemContext system {
            include *
            autolayout lr
        }

        # Диаграмма контейнеров
        container system {
            include *
            autolayout lr
        }

        # Динамическая диаграмма "Добавление доклада в конференцию"
        dynamic system "add_presentation_to_conference" {
            user -> usersContext "Создает нового пользователя"
            user -> talksContext "Создает новый доклад"
            conferenceAdmin -> conferencesContext "Добавляет доклад в конференцию"
            conferencesContext -> talksContext "Привязывает доклад к конференции"
            
            autolayout lr
        }

        theme default
    }
}
