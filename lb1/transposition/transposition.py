def validate_key(key):
    if not key or any(type(number) is not int for number in key):
        raise ValueError("Ключ должен содержать целые числа от 1 до n.")
    if sorted(key) != list(range(1, len(key) + 1)):
        raise ValueError("Ключ должен быть перестановкой чисел от 1 до n без повторов.")


def encrypt(text, key):
    validate_key(key)
    text = text.replace(" ", "")
    n = len(key)
    # Исходные пробелы удалены, поэтому пробел-заполнитель однозначно удалим.
    text += " " * ((-len(text)) % n)
    result = []
    for start in range(0, len(text), n):
        block = text[start:start + n]
        for position in key:
            result.append(block[position - 1])
    return "".join(result)


def decrypt(text, key):
    validate_key(key)
    n = len(key)
    if len(text) % n != 0:
        raise ValueError("Длина шифротекста должна быть кратна длине ключа.")
    result = []
    for start in range(0, len(text), n):
        block = [""] * n
        for i, position in enumerate(key):
            block[position - 1] = text[start + i]
        result.extend(block)
    return "".join(result).rstrip(" ")


def main():
    text = input("Введите текст: ")
    try:
        key = [int(number) for number in input("Введите ключ через пробел (например, 3 1 4 2): ").split()]
        encrypted = encrypt(text, key)
        decrypted = decrypt(encrypted, key)
    except ValueError as error:
        print("Ошибка:", error)
        return

    # repr показывает пробелы-заполнители, в том числе в конце шифротекста.
    print("Шифротекст:", repr(encrypted))
    print("Расшифрованный текст:", decrypted)
    print("Проверка Dk(Ek(m)) = m (без исходных пробелов):", decrypted == text.replace(" ", ""))


if __name__ == "__main__":
    main()
