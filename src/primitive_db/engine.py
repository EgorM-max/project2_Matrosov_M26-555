import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata


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

        else:
            print(f'Функции "{command}" нет. Попробуйте снова.')
