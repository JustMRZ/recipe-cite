# Сайт Рецептов

Сайт с рецептами, который позволяет пользователям сохранять измененные версии рецептов для личного использования.

## Инструменты

Для реализации проекта были использованы следующие технологии:

- **Python**
- **Django**
- **Redis**
- **Celery**
- **Amazon S3**
- **JavaScript**
- **HTML**
- **CSS**

### Реализованные функции:

- **Кэширование данных**: Использование **Redis** для кэширования часто используемых данных.
- **Очередь задач**: Реализация добавления новых рецептов через **Celery**.
- **Хранение изображений**: Сохранение изображений на **S3**.

## Функции программы

### Динамическая лента рецептов

Реализован функционал динамической подгрузки рецептов по мере пролистывания страницы.
![Прогрузка страницы](https://i.imgur.com/DX5MbGt.gif)

### Сортировка списка рецептов

Добавлена возможность сортировки рецептов по популярности и времени добавления. Также пользователи могут фильтровать рецепты по категориям и искать по названию.
![Сортировка данных](https://i.imgur.com/t5BnNcH.gif)

### Система аутентификации

На сайте реализована система аутентификации, включающая создание аккаунта, вход в аккаунт, восстановление и смену пароля.
![Аутентификация](https://i.imgur.com/Xl0BVKn.gif)

### Добавление новых рецептов

Пользователи могут добавлять новые рецепты. Изображения сохраняются на S3, а сам рецепт добавляется в очередь **Celery**, чтобы не задерживать пользователя.
![Добавление рецептов](https://i.imgur.com/NRz7gbE.gif)

### Редактирование рецептов

Добавлен функционал изменения и удаления рецептов. При редактировании рецепта изменения также добавляются в очередь **Celery**, а изображения сохраняются на S3.
![Редактирование рецептов](https://i.imgur.com/nmzezXS.gif)

### Сохранение рецептов в избранное

Пользователи могут добавлять рецепты в избранное. Перед сохранением у них есть возможность отредактировать текст рецепта, который будет виден только им.
![Сохранение рецептов](https://i.imgur.com/aNVIESO.gif)

### Система комментариев

Каждый рецепт может иметь комментарии от пользователей. Комментарии можно удалять или отмечать как "нравится". Для оптимизации хранения комментариев используется кэширование с помощью **Redis**.
![Комментарии](https://i.imgur.com/ECa07ZL.gif)

## Установка проекта

Для локального запуска сайта используйте **Docker**. Следуйте инструкциям ниже:

1. Скачайте проект с GitHub любым удобным способом.
2. Перейдите в папку `recipe_proj` в скачанном проекте и создайте файл `.env` (переменные окружения). Внутри этого файла добавьте две константы:

   - `S3_ACCESS_KEY`
   - `S3_SECRET_KEY`

   Введите данные от вашего S3 хранилища в соответствующие переменные.
3. Откройте терминал в корневой папке проекта и введите команду `docker-compose build` для установки всех зависимостей
4. После установки зависимостей, выполните миграции с помощью команды: `docker-compose run --rm web-app sh -c "python3 manage.py migrate"`
5. При необходимости, создайте суперпользователя командой: `docker-compose run --rm web-app sh -c "python3 manage.py createsuperuser"`
6. Запустите проект с помощью команды: `docker-compose up`
7. Откройте проект в браузере по адресу: `http://127.0.0.1:8000`