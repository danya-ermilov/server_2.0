# 📌 MeetUp API

Бэкенд-сервис для приложения в стиле **MeetUp** — пользователи могут регистрироваться, авторизоваться, создавать события (или продукты), комментировать и взаимодействовать в реальном времени через WebSocket.  
Есть поддержка **корзины (Redis)** и **JWT-аутентификации**.  

---

## 📂 Структура проекта
```bash
├── main.py # Точка входа приложения FastAPI
├── migrate.py # Скрипт для миграций базы данных│
├── auth/ # Авторизация и работа с JWT
│ ├── dependencies.py
│ ├── hashing.py
│ └── jwt_handler.py
│
├── core/ # Ядро: кэш и утилиты
│ └── cache.py
│
├── crud/ # CRUD-операции
│ ├── carts.py
│ ├── comments.py
│ ├── tags.py
│ ├── products.py
│ └── users.py
│
├── db/ # Подключение к БД и Redis
│ ├── database.py
│ └── redis.py
│
├── models/ # SQLAlchemy модели
│ ├── cart.py
│ ├── comment.py
│ ├── tag.py
│ ├── product.py
│ └── user.py
│
├── routers/ # Роутеры API
│ ├── admins.py
│ ├── carts.py
│ ├── comments.py
│ ├── comments_ws.py # WebSocket для комментариев
│ ├── tags.py
│ ├── products.py
│ └── users.py
│
├── schemas/ # Pydantic-схемы
│ ├── products.py
│ └── users.py
│
└── services/ # Сервисы
  └── redis_cart.py
```
---

## 🚀 Функциональность

- 🔑 **Регистрация и авторизация**
  - JWT-токены
  - Хеширование паролей
  - Middleware для защиты эндпоинтов

- 👤 **Пользователи**
  - Регистрация и логин
  - Получение информации о профиле

- 📦 **Продукты / события**
  - CRUD (создание, чтение, обновление, удаление)
  - Список и поиск

- 💬 **Комментарии**
  - Обычные (REST)
  - WebSocket для комментариев в реальном времени

- 🛒 **Корзина**
  - Добавление и удаление товаров
  - Хранение в Redis

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/danya-ermilov/server_2.0.git
cd server_2.0
```
### 2. Создать виртуальное окружение и установить зависимости
```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```
### 3. Настроить переменные окружения, настроить миграции, запустить сервер
(см Wiki)


## 🛠️ Технологии
```bash
FastAPI — основной фреймворк
SQLAlchemy — ORM
PostgreSQL — база данных
Redis — кэш и корзины
JWT — авторизация
WebSocket — чат комментариев в реальном времени
