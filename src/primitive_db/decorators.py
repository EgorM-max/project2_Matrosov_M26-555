"""Декораторы для обработки ошибок, подтверждения действий и измерения времени."""
import time
from functools import wraps


def handle_db_errors(func):
    """Обработать исключения, возникающие при выполнении функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Вызвать функцию и перехватить возникшие исключения."""
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
    """Создать декоратор для подтверждения действия пользователем."""

    def decorator(func):
        """Обернуть функцию проверкой подтверждения."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Запросить подтверждение перед выполнением функции."""

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
    """Измерить и вывести время выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Вызвать функцию и вывести продолжительность её выполнения."""
        
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
