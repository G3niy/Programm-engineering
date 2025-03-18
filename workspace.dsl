workspace {
    name "System of orders and services"
    !identifiers hierarchical

    model {
        user = person "User" { 
            description "Пользователь в системе создания заказов с услугами" 
        }
        orderMakingStorage = softwareSystem "Система хранения и наполнения заказов" {
            description "Регистрация пользователей, создание и хранение услуг и заказов"
            authenticationContainer = container "Система аутентификации" {
                description "Сервис для создания авторизации пользователей и управления ими"
                technology "FastAPI, Language: Python"
            }
            serviceContainer = container "Система услуг" {
                description "Система заполнения и поиска услуг"
                technology "FastAPI, Language: Python"
            }
            ordersContainer = container "Система заказов" {
                description "Система создания и управления заказами"
                technology "FastAPI, Language: Python"
            }
            userDataBase = container "База данных пользователей" {
                description "Хранение данных пользователей и управление ими"
                technology "PostgreSQL"
            }
            ordersAndServicesDataBase = container "База данных услуг и заказов" {
                description "База данных заказов и услуг и управление ими"
                technology "Amazon DynamoDB"
            //1 - Создание нового пользователя
            user -> authenticationContainer "Проходит процесс регистрации"
            authenticationContainer -> userDataBase "Сохраняет пользователя в систему"
            //2 - Поиск пользователя по логину
            user -> authenticationContainer "Поиск пользователя по логину"
            authenticationContainer -> userDataBase "Возвращение пользователя по логину"
            //3 - Поиск пользователя по маске имя и фамилии
            user -> authenticationContainer "Поиск пользователя по маске имени и фамилии"
            authenticationContainer -> userDataBase "Возвращение пользователя по маске имени и фамилии"
            //4 - Создание услуги
            user -> authenticationContainer "Авторизация пользователя"
            authenticationContainer -> userDataBase "Создание сессии для пользователя"
            userDataBase -> serviceContainer "Создание услуги пользователем"
            serviceContainer -> ordersAndServicesDataBase "Сохранение услуги за пользователем"
            //5 - Получение списка услуг
            userDataBase -> serviceContainer "Поиск услуг для пользователя"
            serviceContainer -> ordersAndServicesDataBase "Получение списка услуг для пользователя"
            //6 - Добавление услуг в заказ
            serviceContainer -> ordersContainer "Добавление услуги в заказ"
            ordersContainer -> ordersAndServicesDataBase "Сохранение заказа за пользователем"
            //7 - Получение заказа для пользователя
            userDataBase -> ordersContainer "Поиск заказа"
            ordersContainer -> ordersAndServicesDataBase "Получение заказа для пользователя"

            //Side relations
            ordersAndServicesDataBase -> user "Подтверждение заказа"
            userDataBase -> ordersContainer "Закрепление за пользователем заявки на заказ"
        }
    }
}

    views {
        themes default

        systemContext orderMakingStorage {
            include *
            autolayout lr
        }

        container orderMakingStorage {
            include *
            autolayout lr
        }
        dynamic orderMakingStorage "services_to_order" "Добавление услуг в заказ новым пользователем" {
            autoLayout lr
            user -> orderMakingStorage.authenticationContainer "Регистрация пользователя"
            orderMakingStorage.authenticationContainer -> orderMakingStorage.userDataBase "Сохранение пользователя в базу данных"
            orderMakingStorage.userDataBase -> orderMakingStorage.serviceContainer "Создание услуги пользователем"
            orderMakingStorage.userDataBase -> orderMakingStorage.ordersContainer "Закрепление за пользователем заявки на заказ"
            orderMakingStorage.serviceContainer -> orderMakingStorage.ordersContainer "Добавление услуги в заказ"
            orderMakingStorage.ordersContainer -> orderMakingStorage.ordersAndServicesDataBase "Сохранение заказа за пользователем"
        }
    }
    
}
