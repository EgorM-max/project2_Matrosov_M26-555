# Primitive DB

Primitive DB — консольное приложение на Python, имитирующее базовые операции управления таблицами базы данных.

Проект разработан на Python 3.12 с использованием менеджера пакетов `uv`.

## Возможности

- Создание таблиц с помощью команды `create_table`.
- Удаление таблиц с помощью команды `drop_table`.
- Просмотр списка таблиц через `list_tables`.
- Проверка типов данных столбцов: `int`, `str`, `bool`.
- Автоматическое добавление столбца `ID:int`.
- Сохранение структуры таблиц в JSON-файл `db_meta.json`.
- Загрузка сохранённых таблиц при повторном запуске.

## Установка

Клонировать репозиторий:

```bash
git clone https://github.com/EgorM-max/project2_Matrosov_M26-555.git
```

Перейти в папку проекта:

```bash
cd project2_Matrosov_M26-555
```

Установить зависимости:

```bash
uv sync
```

## Запуск

Основная команда:

```bash
uv run database
```

Дополнительная команда:

```bash
uv run project
```

## Команды приложения

| Команда | Описание |
|---|---|
| `create_table users name:str age:int` | Создать таблицу |
| `drop_table users` | Удалить таблицу |
| `list_tables` | Показать существующие таблицы |
| `help` | Показать справку |
| `exit` | Завершить приложение |

## Пример использования

```text
Введите команду: create_table users name:str age:int
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int

Введите команду: list_tables
- users

Введите команду: drop_table users
Таблица "users" успешно удалена.

Введите команду: exit
Выход из программы.
```

## Проверка качества кода

```bash
uv run ruff check .
```

## Сборка пакета

```bash
uv build
```

## Структура проекта

```text
src/
└── primitive_db/
    ├── __init__.py
    ├── core.py
    ├── engine.py
    ├── main.py
    └── utils.py
```
