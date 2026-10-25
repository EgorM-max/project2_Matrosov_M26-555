def parse_value(value):
    """Преобразовать текстовое значение в int, bool или str."""
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
    """Разобрать список значений команды insert с учётом кавычек."""
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
    """Разобрать условие вида столбец = значение в словарь."""
    parts = text.partition("=")

    if not parts[1]:
        raise ValueError("Условие должно содержать знак =.")

    column_name = parts[0].strip()
    value_text = parts[2].strip()

    if not column_name or not value_text:
        raise ValueError("Не указано имя столбца или значение.")

    return {column_name: parse_value(value_text)}