import time
from functools import wraps


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except FileNotFoundError:
            print("Ошибка: Файл данных не найден.")

        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найдены.")

        except ValueError as error:
            print(f"Ошибка валидации: {error}")

        except Exception as error:
            print(f"Произошла непредвиденная ошибка: {error}")

        return None

    return wrapper


def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()

            if answer == "y":
                return func(*args, **kwargs)

            print("Операция отменена.")
            return None

        return wrapper

    return decorator


def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()

        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.monotonic()
            execution_time = end_time - start_time

            print(
                f"Функция {func.__name__} выполнялась "
                f"за {execution_time:.5f} секунд"
            )

    return wrapper
