# django-qa-rest

REST API для системы вопросов и ответов (Q&A), построенная на Django и Django REST Framework.

## Описание проекта

Проект представляет собой RESTful API для управления вопросами и ответами. Пользователи могут:
- Создавать вопросы
- Просматривать список вопросов и детальную информацию о каждом вопросе
- Добавлять ответы на вопросы (требуется аутентификация)
- Удалять свои ответы
- Удалять вопросы (вместе со всеми ответами)

### Технологии

- **Django 5.2** - веб-фреймворк
- **Django REST Framework** - для создания REST API
- **PostgreSQL** - база данных
- **drf-yasg** - документация API (Swagger/OpenAPI)
- **Docker & Docker Compose** - контейнеризация

## Быстрый старт

### Требования

- Docker
- Docker Compose

### Запуск проекта

1. Клонируйте репозиторий и перейдите в директорию проекта:
   ```bash
   cd django-qa-rest
   ```

2. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up
   ```

   При первом запуске контейнеры будут автоматически собраны. После запуска контейнеров выполните миграции базы данных:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. (Опционально) Создайте суперпользователя для доступа к админ-панели:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Доступ к приложению

После запуска приложение будет доступно по следующим адресам:

- **API**: http://localhost:8000
- **Swagger UI** (интерактивная документация API): http://localhost:8000/swagger/
- **ReDoc** (альтернативная документация): http://localhost:8000/redoc/
- **Админ-панель Django**: http://localhost:8000/admin/
- **PostgreSQL**: localhost:5432

## API Endpoints

### Вопросы (Questions)

- `GET /questions/` - получить список всех вопросов
- `POST /questions/` - создать новый вопрос
- `GET /questions/<id>/` - получить вопрос со всеми ответами
- `DELETE /questions/<id>/` - удалить вопрос (вместе с ответами)

### Ответы (Answers)

- `POST /questions/<id>/answers/` - добавить ответ на вопрос (требуется аутентификация)
- `GET /answers/<id>/` - получить конкретный ответ
- `DELETE /answers/<id>/` - удалить ответ (только владелец ответа)

## Полезные команды

- **Остановить контейнеры**: `docker-compose down`
- **Просмотр логов**: `docker-compose logs -f`
- **Выполнить миграции**: `docker-compose exec web python manage.py migrate`
- **Создать суперпользователя**: `docker-compose exec web python manage.py createsuperuser`
- **Django shell**: `docker-compose exec web python manage.py shell`
- **Подключиться к PostgreSQL**: `docker-compose exec db psql -U django_user -d django_db`
- **Остановить и удалить volumes**: `docker-compose down -v`

## Настройка окружения

Проект использует переменные окружения с значениями по умолчанию. При необходимости вы можете создать файл `.env` в корне проекта:

```env
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=django_password
DB_HOST=db
DB_PORT=5432
```

Если файл `.env` не создан, будут использованы значения по умолчанию.