# Telegram-бот на aiogram: Рабочий проект

Этот проект — Telegram-бот, написанный на Python с использованием фреймворка **aiogram** и **sqlalchemy** и базой данных **PostgreSQL**. Он демонстрирует базовые, необходимые для бизнеса возможности создания бота: команды, CRUD работа с базой данных Postgres, бесконечный автомат (FSM) для форм, логирование пользовательских действий. Я использовал постгрес но можно и sqlite, дело вкуса и предпочтений.

## 📖 Описание

Бот поддерживает следующие функции:
- Команды: `/start`, `/profile`, `/form`.
- **Menu-клавиатура** со всеми командами.
- **Inline-клавиатура** в форме для выбора пола и подтверждения/отмены данных.
- **FSM** для пошагового сбора данных (имя, возраст, пол, город).
- Логирование пользовательских сообщений и callback-запросов в файл `logs.txt`.
- **Orm**, написанная на sqlalchemy для масштабируемого сервиса, идеально подходящего под бизнес.

## 📂 Структура проекта

```
tg_bot1/                          # Корневая директория проекта
│
├── handlers/                     # Папка с обработчиками команд и сообщений
│   ├── __init__.py               # Экспортирует роутеры для подключения в tgbot.py
│   ├── form.py                   # Обработчик формы сбора данных (FSM)
│   ├── profile.py                # Обработчик команды /profile
│   └── start.py                  # Обработчик команды /start
│
├── database/                     # Папка для работы с базой данных
│   ├── database.py               # Настройка подключения к БД и базовые классы
│   ├── models.py                 # Модели SQLAlchemy (таблицы БД)
│   └── queries/
│       └── orm.py                # ORM-методы для работы с БД
│
├── middleware/                   # Middleware для обработки сообщений
│   └── logging_middleware.py     # Логирование действий пользователей
│
├── config.py                     # Конфигурация (токен бота, настройки БД)
├── tgbot.py                      # Главный файл для запуска бота
├── logs.txt                      # Файл логов пользовательских действий
├── requirements.txt              # Зависимости проекта
├── pyproject.toml                # Настройки линтера (Ruff)
└── README.md                     # Документация проекта
```

### Описание файлов
- **`config.py`**: Загружает токен бота из `.env` с помощью `python-dotenv`.
- **`tgbot.py`**: Инициализирует бот, подключает middleware и роутеры, запускает polling.
- **`middleware.py`**: Логирует пользовательские сообщения и callback-запросы в `logs.txt`.
- **`start.py`**: Обрабатывает `/start`, приветствуя пользователя по имени.
- **`hello.py`**: Обрабатывает `/hello`, отвечает "Саламжексон".
- **`menu.py`**: Создаёт reply-клавиатуру и обрабатывает выбор действий.
- **`form.py`**: Реализует форму с FSM для сбора данных (имя, возраст, пол, город).
- **`database.py`**: Настройка асинхронного движка SQLAlchemy и сессий.
- **`models.py`**: Определение моделей данных (таблиц БД).
- **`queries/orm.py`**: Методы для CRUD операций с БД.

## 🚀 Установка и запуск

### Требования
- Python 3.10+
- Библиотеки: `aiogram`, `python-dotenv`, `sqlalchemy`
- Токен бота от `@BotFather`
- БД на движке `postgresql`

### Установка
1. Клонируй репозиторий:
   ```bash
   git clone <ссылка_на_репозиторий>
   cd tg_bot1
   ```
2. Создай виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Установи зависимости:
   ```bash
   pip install aiogram python-dotenv
   ```
4. Создай файл `.env` в корне проекта и добавь токен и данные для загрузки БД:
   ```
   BOT_TOKEN=your_bot_token_here
   DB_HOST=your_host
   DB_PORT=your_port
   DB_USER=your_username
   DB_NAME=your_database_name
   DB_PASS=your_database_password
   ```
5. Запусти бот:
   ```bash
   python tgbot.py
   ```

### Проверка
- Отправь команды `/start`, `/form`, `/profile` в Telegram.
- Проверь `logs.txt` для записей вида:
  ```
  2025-06-22 12:34:56 | Message | User 123456789: /menu
  2025-06-22 12:35:00 | Callback | User 123456789: Callback: gender_male
  ```

### Логирование
Логирование в `middleware.py` записывает пользовательские действия в `logs.txt`.

- **Формат**:
  ```
  2025-06-22 12:34:56 | Message | User 123456789: /menu
  2025-06-22 12:35:00 | Callback | User 123456789: Callback: gender_male
  ```
- **Настройка**:
  ```python
  middleware_logger = logging.getLogger("bot_middleware")
  middleware_handler = logging.FileHandler("logs.txt")
  middleware_formatter = logging.Formatter(
      "%(asctime)s | %(log_type)s | User %(user_id)s: %(log_content)s"
  )
  middleware_handler.setFormatter(middleware_formatter)
  middleware_logger.addHandler(middleware_handler)
  middleware_logger.setLevel(logging.INFO)
  middleware_logger.propagate = False
  ```

