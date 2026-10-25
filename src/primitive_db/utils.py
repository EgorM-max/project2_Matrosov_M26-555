"""Вспомогательные функции для работы с файлами и кеширования."""
import json
from pathlib import Path

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загрузить метаданные таблиц из JSON-файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохранить метаданные таблиц в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    """Загрузить записи указанной таблицы из JSON-файла."""
    filepath = Path(DATA_DIR) / f"{table_name}.json"

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохранить записи указанной таблицы в JSON-файл."""
    data_dir = Path(DATA_DIR)
    data_dir.mkdir(exist_ok=True)

    filepath = data_dir / f"{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def delete_table_data(table_name):
    """Удалить JSON-файл с записями указанной таблицы."""
    filepath = Path(DATA_DIR) / f"{table_name}.json"

    if filepath.exists():
        filepath.unlink()



def create_cacher():
    """Создать функции кеширования запросов и очистки кеша."""
    cache = {}

    def cached_select(select_func, table_data, where_clause=None):
        """Получить результат запроса из кеша или выполнить поиск."""
        key = json.dumps(
            [table_data, where_clause],
            sort_keys=True,
            ensure_ascii=False,
        )

        if key in cache:
            print("Результат получен из кеша.")
            return [record.copy() for record in cache[key]]

        result = select_func(table_data, where_clause)

        if result is None:
            return None

        cache[key] = [record.copy() for record in result]
        print("Результат сохранён в кеш.")

        return result

    def clear_cache():
        """Удалить все сохранённые результаты запросов."""
        cache.clear()
        print("Кеш запросов очищен.")

    return cached_select, clear_cache


