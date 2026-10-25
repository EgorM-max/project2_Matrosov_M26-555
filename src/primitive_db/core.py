"""Основные операции с таблицами и записями базы данных."""
from primitive_db.constants import VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создать таблицу с указанными столбцами и типами данных."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = ["ID:int"]
    column_names = {"ID"}

    for column in columns:
        parts = column.split(":")

        if len(parts) != 2:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = parts

        if not column_name or column_type not in VALID_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        if column_name in column_names:
            print(f'Ошибка: Столбец "{column_name}" уже существует.')
            return metadata

        column_names.add(column_name)
        table_columns.append(column)

    metadata[table_name] = table_columns

    print(
        f'Таблица "{table_name}" успешно создана со столбцами: '
        f'{", ".join(table_columns)}'
    )

    return metadata


@handle_db_errors
@confirm_action("удаление таблицы") 
def drop_table(metadata, table_name):
    """Удалить таблицу из метаданных базы данных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавить запись в таблицу с автоматическим присвоением ID."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        print("Ошибка: Количество значений не соответствует количеству столбцов.")
        return None

    record = {}

    for column, value in zip(columns, values):
        column_name, column_type = column.split(":")

        if column_type == "int":
            if type(value) is not int:
                print(f"Ошибка: Столбец {column_name} ожидает тип int.")
                return None

        elif column_type == "str":
            if type(value) is not str:
                print(f"Ошибка: Столбец {column_name} ожидает тип str.")
                return None

        elif column_type == "bool":
            if type(value) is not bool:
                print(f"Ошибка: Столбец {column_name} ожидает тип bool.")
                return None

        record[column_name] = value

    table_data = load_table_data(table_name)

    record["ID"] = max(
        (row["ID"] for row in table_data),
        default=0,
    ) + 1

    table_data.append(record)

    print(
        f'Запись с ID={record["ID"]} успешно добавлена '
        f'в таблицу "{table_name}".'
    )

    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Получить записи таблицы с необязательной фильтрацией."""
    if where_clause is None:
        return table_data

    result = []

    for record in table_data:
        matches = True

        for column_name, value in where_clause.items():
            if column_name not in record or record[column_name] != value:
                matches = False
                break

        if matches:
            result.append(record)

    return result


@handle_db_errors
def update(table_data, set_clause, where_clause, columns):
    """Изменить значения записей, соответствующих условию."""
    column_types = {}

    for column in columns:
        column_name, column_type = column.split(":")
        column_types[column_name] = column_type

    for column_name, value in set_clause.items():
        if column_name == "ID":
            print("Ошибка: Нельзя изменять системный столбец ID.")
            return None

        if column_name not in column_types:
            print(f'Ошибка: Столбец "{column_name}" не существует.')
            return None

        expected_type = column_types[column_name]

        if type(value).__name__ != expected_type:
            print(f"Ошибка: Столбец {column_name} ожидает тип {expected_type}.")
            return None

    for column_name, value in where_clause.items():
        if column_name not in column_types:
            print(f'Ошибка: Столбец "{column_name}" не существует.')
            return None

        expected_type = column_types[column_name]

        if type(value).__name__ != expected_type:
            print(f"Ошибка: Столбец {column_name} ожидает тип {expected_type}.")
            return None

    updated_count = 0

    for record in table_data:
        matches = True

        for column_name, value in where_clause.items():
            if record.get(column_name) != value:
                matches = False
                break

        if matches:
            for column_name, value in set_clause.items():
                record[column_name] = value

            updated_count += 1

    print(f"Обновлено записей: {updated_count}")

    return table_data


@handle_db_errors
@confirm_action("удаление таблицы") 
def delete(table_data, where_clause):
    """Удалить записи таблицы, соответствующие условию."""
    remaining_records = []
    deleted_count = 0

    for record in table_data:
        matches = True

        for column_name, value in where_clause.items():
            if column_name not in record or record[column_name] != value:
                matches = False
                break

        if matches:
            deleted_count += 1
        else:
            remaining_records.append(record)

    print(f"Удалено записей: {deleted_count}")

    return remaining_records


@handle_db_errors
def get_table_info(metadata, table_name):
    """Вывести структуру таблицы и количество записей."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name]
    table_data = load_table_data(table_name)

    print(f"Таблица: {table_name}")
    print("Столбцы:")

    for column in columns:
        column_name, column_type = column.split(":")
        print(f"- {column_name} ({column_type})")

    print(f"Количество записей: {len(table_data)}")
    
