import json
from pathlib import Path


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    filepath = Path("data") / f"{table_name}.json"

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    filepath = data_dir / f"{table_name}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def parse_value(value):
    value = value.strip()

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    if (
        len(value) >= 2
        and value[0] == value[-1]
        and value[0] in ('"', "'")
    ):
        return value[1:-1]

    try:
        return int(value)
    except ValueError:
        return value


def parse_values(values_text):
    values = []
    current = ""
    quote = None

    for char in values_text:
        if char in ('"', "'"):
            if quote is None:
                quote = char
            elif quote == char:
                quote = None

            current += char

        elif char == "," and quote is None:
            values.append(parse_value(current))
            current = ""

        else:
            current += char

    if quote is not None:
        raise ValueError("Незакрытые кавычки в значениях.")

    values.append(parse_value(current))

    return values


def parse_where_clause(text):
    parts = text.partition("=")

    if not parts[1]:
        raise ValueError("Условие должно содержать знак =.")

    column_name = parts[0].strip()
    value_text = parts[2].strip()

    if not column_name or not value_text:
        raise ValueError("Не указано имя столбца или значение.")

    return {column_name: parse_value(value_text)}


def delete_table_data(table_name):
    filepath = Path("data") / f"{table_name}.json"

    if filepath.exists():
        filepath.unlink()
