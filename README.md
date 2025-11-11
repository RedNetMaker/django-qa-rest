# django-qa-rest
Тестовое задание для собеседования

## Docker Setup

This project is containerized with Docker Compose and uses PostgreSQL as the database.

### Prerequisites
- Docker
- Docker Compose

### Getting Started

1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your settings (optional, defaults are provided).

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Run migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Create a superuser (optional):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. Access the application:
   - Django app: http://localhost:8000
   - PostgreSQL: localhost:5432

### Useful Commands

- Stop containers: `docker-compose down`
- View logs: `docker-compose logs -f`
- Run Django management commands: `docker-compose exec web python manage.py <command>`
- Access Django shell: `docker-compose exec web python manage.py shell`
- Access PostgreSQL: `docker-compose exec db psql -U django_user -d django_db`