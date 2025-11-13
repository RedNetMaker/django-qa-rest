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

2. Создать .env из .env.example:
   ```bash
   cp .env.example .env
   ```

3. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

   При первом запуске контейнеры будут автоматически собраны. После запуска контейнеров выполните миграции базы данных:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. Создайте суперпользователя для доступа к админ-панели и api:
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

## Тестирование

Проект включает набор тестов для проверки функциональности API. Тесты написаны с использованием Django REST Framework's `APITestCase`.

### Запуск тестов

Для запуска всех тестов используйте команду:

```bash
docker-compose exec web python manage.py test
```

Для запуска тестов конкретного приложения:

```bash
docker-compose exec web python manage.py test qa
```

Для запуска конкретного тестового класса:

```bash
docker-compose exec web python manage.py test qa.tests.QuestionAPITestCase
```

Для запуска конкретного теста:

```bash
docker-compose exec web python manage.py test qa.tests.QuestionAPITestCase.test_get_questions_list_returns_all_questions
```

### Покрытие тестами

Тесты покрывают следующие сценарии:

**Вопросы (Questions):**
- Получение списка всех вопросов
- Создание нового вопроса
- Получение детальной информации о вопросе со всеми ответами
- Удаление вопроса (вместе со всеми связанными ответами)

**Ответы (Answers):**
- Создание ответа аутентифицированным пользователем
- Требование аутентификации для создания ответа
- Получение детальной информации об ответе
- Удаление ответа владельцем
- Запрет удаления ответа другим пользователем

## Полезные команды

- **Остановить контейнеры**: `docker-compose down`
- **Просмотр логов**: `docker-compose logs -f`
- **Выполнить миграции**: `docker-compose exec web python manage.py migrate`
- **Создать суперпользователя**: `docker-compose exec web python manage.py createsuperuser`
- **Django shell**: `docker-compose exec web python manage.py shell`
- **Подключиться к PostgreSQL**: `docker-compose exec db psql -U django_user -d django_db`
- **Остановить и удалить volumes**: `docker-compose down -v`