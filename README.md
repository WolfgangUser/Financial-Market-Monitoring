# Веб-сервис по мониторингу финансовых рынков

Проект разработан на **Python** с использованием **Django**, **Django REST Framework** и **PostgreSQL** (или SQLite для разработки). Реализован паттерн **MVC** (Model-View-Controller), где:
- **Model** — модели данных в `markets/models.py`
- **View** — бизнес-логика в `markets/views.py` и `markets/services.py`
- **Controller** — URL-маршрутизация и шаблоны

## Требования
- Python 3.8+
- PostgreSQL (опционально, по умолчанию используется SQLite)
- pip

## Установка и запуск с нуля

### 1. Клонирование или переход в директорию проекта
```bash
cd /workspace
```

### 2. Создание виртуального окружения (рекомендуется)
```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных
По умолчанию проект использует **SQLite**. Если вы хотите использовать **PostgreSQL**:

1. Установите PostgreSQL и создайте базу данных:
   ```sql
   CREATE DATABASE market_monitor;
   CREATE USER monitor_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE market_monitor TO monitor_user;
   ```

2. Измените настройки в `market_monitor/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'market_monitor',
           'USER': 'monitor_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### 5. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Загрузка демонстрационных данных
```bash
python init_data.py
```

### 7. Создание суперпользователя (для доступа к админ-панели)
```bash
python manage.py createsuperuser
```
Следуйте инструкциям для ввода имени пользователя, email и пароля.

### 8. Запуск сервера разработки
```bash
python manage.py runserver 0.0.0.0:8000
```

## Доступные разделы

- **Главная страница**: http://localhost:8000/
- **Активы**: http://localhost:8000/assets/
- **Новости**: http://localhost:8000/news/
- **Списки наблюдения**: http://localhost:8000/watchlists/
- **Админ-панель**: http://localhost:8000/admin/
- **API документация**: http://localhost:8000/api/

## API Endpoints

### Активы
- `GET /api/assets/` — список всех активов
- `GET /api/assets/<id>/` — детали актива
- `GET /api/assets/<id>/prices/` — исторические цены актива

### Новости
- `GET /api/news/` — список новостей
- `GET /api/news/<id>/` — детали новости

### Списки наблюдения
- `GET /api/watchlists/` — список списков наблюдения
- `POST /api/watchlists/` — создание нового списка
- `GET /api/watchlists/<id>/` — детали списка

## Структура проекта

```
/workspace
├── manage.py              # Управление проектом
├── requirements.txt       # Зависимости
├── init_data.py          # Скрипт загрузки демо-данных
├── db.sqlite3            # База данных SQLite
├── market_monitor/       # Основной проект Django
│   ├── settings.py       # Настройки проекта
│   ├── urls.py           # Корневая маршрутизация
│   └── ...
├── markets/              # Приложение рынка
│   ├── models.py         # Модели данных
│   ├── views.py          # Представления (логика)
│   ├── serializers.py    # Сериализаторы для API
│   ├── services.py       # Бизнес-логика
│   └── urls.py           # Маршрутизация приложения
├── templates/            # HTML-шаблоны
│   └── markets/          # Шаблоны приложения markets
└── static/               # Статические файлы (CSS, JS)
    ├── css/
    └── js/
```

## Особенности

- **Современный фронтенд**: адаптивный дизайн, анимации, интерактивные элементы
- **REST API**: полный набор endpoint'ов для работы с данными
- **Межстраничная навигация**: все страницы связаны между собой
- **Паттерн MVC**: четкое разделение ответственности между компонентами
- **Демо-данные**: предзагруженные активы, цены и новости для демонстрации

## Производство

Для развертывания в продакшене:
1. Установите `DEBUG = False` в `settings.py`
2. Настройте правильный `ALLOWED_HOSTS`
3. Используйте PostgreSQL вместо SQLite
4. Настройте веб-сервер (Nginx + Gunicorn)
5. Настройте сбор статических файлов: `python manage.py collectstatic`
