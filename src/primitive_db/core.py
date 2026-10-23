def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    valid_types = ("int", "str", "bool")
    table_columns = ["ID:int"]
    column_names = {"ID"}

    for column in columns:
        parts = column.split(":")

        if len(parts) != 2:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = parts

        if not column_name or column_type not in valid_types:
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


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata
