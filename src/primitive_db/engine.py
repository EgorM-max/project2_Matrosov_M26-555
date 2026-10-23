import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    get_table_info,
    insert,
    select,
    update,
)
from primitive_db.utils import (
    delete_table_data,
    load_metadata,
    load_table_data,
    parse_values,
    parse_where_clause,
    save_metadata,
    save_table_data,
)


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print(
        "<command> create_table <имя_таблицы> "
        "<столбец1:тип> <столбец2:тип> ... - создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")
    print('<command> insert into <таблица> values (...) - добавить запись')
    print(
    "<command> select from <таблица> [where <столбец> = <значение>] "
    "- показать записи"
)
    print(
    "<command> update <таблица> set <столбец> = <значение> "
    "where <столбец> = <значение> - изменить записи"
)
    print(
    "<command> delete from <таблица> where <столбец> = <значение> "
    "- удалить записи"
)
    print("<command> info <таблица> - информация о таблице")



def run():
    print_help()

    while True:
        metadata = load_metadata("db_meta.json")

        user_input = prompt.string("\nВведите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка: Некорректный формат команды.")
            continue

        if not args:
            continue

        command = args[0]

        if command == "exit":
            print("Выход из программы.")
            break

        elif command == "help":
            print_help()

        elif command == "list_tables":
            if len(args) != 1:
                print("Ошибка: Команда list_tables не принимает аргументы.")
            elif metadata:
                for table_name in metadata:
                    print(f"- {table_name}")
            else:
                print("Таблиц пока нет.")

        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: Укажите имя таблицы и хотя бы один столбец.")
                continue

            table_name = args[1]
            columns = args[2:]

            if table_name in metadata:
                print(f'Ошибка: Таблица "{table_name}" уже существует.')
                continue

            metadata = create_table(metadata, table_name, columns)
            save_metadata("db_meta.json", metadata)

        elif command == "drop_table":
            if len(args) != 2:
                print("Ошибка: Укажите имя таблицы.")
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            metadata = drop_table(metadata, table_name)
            save_metadata("db_meta.json", metadata)
            delete_table_data(table_name)
        
        elif command == "insert":
            parts = user_input.strip().split(maxsplit=3)

            if len(parts) != 4 or parts[1].lower() != "into":
                print("Ошибка: Используйте insert into <таблица> values (...)")
                continue

            table_name = parts[2]
            values_part = parts[3].strip()

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            if not values_part.lower().startswith("values"):
                print("Ошибка: Ожидается ключевое слово values.")
                continue

            values_text = values_part[6:].strip()

            if not (values_text.startswith("(") and values_text.endswith(")")):
                print("Ошибка: Значения должны находиться в скобках.")
                continue

            values_text = values_text[1:-1]

            try:
                values = parse_values(values_text)
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

            table_data = insert(metadata, table_name, values)

            if table_data is not None:
                save_table_data(table_name, table_data)
            
        
        elif command == "select":
            parts = user_input.strip().split(maxsplit=3)

            if len(parts) < 3 or parts[1].lower() != "from":
                print("Ошибка: Используйте select from <таблица> [where условие]")
                continue

            table_name = parts[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            where_clause = None

            if len(parts) == 4:
                where_parts = parts[3].strip().split(maxsplit=1)

                if len(where_parts) != 2 or where_parts[0].lower() != "where":
                    print("Ошибка: Ожидается условие where <столбец> = <значение>.")
                    continue

                try:
                    where_clause = parse_where_clause(where_parts[1])
                except ValueError as error:
                    print(f"Ошибка: {error}")
                    continue

            columns = [
                column.split(":")[0]
                for column in metadata[table_name]
            ]

            if where_clause is not None:
                column_name = next(iter(where_clause))

                if column_name not in columns:
                    print(f'Ошибка: Столбец "{column_name}" не существует.')
                    continue

            table_data = load_table_data(table_name)
            records = select(table_data, where_clause)

            table = PrettyTable()
            table.field_names = columns

            for record in records:
                table.add_row([record.get(column) for column in columns])

            print(table)
        
        elif command == "update":
            parts = user_input.strip().split(maxsplit=3)

            if len(parts) != 4 or parts[2].lower() != "set":
                print(
                    "Ошибка: Используйте update <таблица> "
                    "set <столбец> = <значение> "
                    "where <столбец> = <значение>"
                )
                continue

            table_name = parts[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            set_and_where = parts[3].split(" where ", maxsplit=1)

            if len(set_and_where) != 2:
                print("Ошибка: Необходимо указать условие where.")
                continue

            try:
                set_clause = parse_where_clause(set_and_where[0])
                where_clause = parse_where_clause(set_and_where[1])
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

            table_data = load_table_data(table_name)

            updated_data = update(
                table_data,
                set_clause,
                where_clause,
                metadata[table_name],
            )

            if updated_data is not None:
                save_table_data(table_name, updated_data)
            
        elif command == "delete":
            parts = user_input.strip().split(maxsplit=4)

            if (
                len(parts) != 5
                or parts[1].lower() != "from"
                or parts[3].lower() != "where"
            ):
                print(
                    "Ошибка: Используйте delete from <таблица> "
                    "where <столбец> = <значение>"
                )
                continue

            table_name = parts[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            try:
                where_clause = parse_where_clause(parts[4])
            except ValueError as error:
                print(f"Ошибка: {error}")
                continue

            column_types = {}

            for column in metadata[table_name]:
                column_name, column_type = column.split(":")
                column_types[column_name] = column_type

            column_name, value = next(iter(where_clause.items()))

            if column_name not in column_types:
                print(f'Ошибка: Столбец "{column_name}" не существует.')
                continue

            expected_type = column_types[column_name]

            if type(value).__name__ != expected_type:
                print(
                    f"Ошибка: Столбец {column_name} "
                    f"ожидает тип {expected_type}."
                )
                continue

            table_data = load_table_data(table_name)
            remaining_data = delete(table_data, where_clause)
            save_table_data(table_name, remaining_data)
        
        elif command == "info":
            if len(args) != 2:
                print("Ошибка: Используйте info <имя_таблицы>")
                continue

            table_name = args[1]
            get_table_info(metadata, table_name)


        else:
            print(f'Функции "{command}" нет. Попробуйте снова.')

