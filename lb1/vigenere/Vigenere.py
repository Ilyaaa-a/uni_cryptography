eng_alph = [chr(i) for i in range(97, 123)]
rus_alph = [chr(i) for i in range(1072, 1104)]
rus_alph.insert(6, 'ё')

ALPHABETS = {"EN": eng_alph, "RUS": rus_alph}

def check_key(key: str) -> str:
    if not key:
        raise ValueError("Ключ не должен быть пустым.")
    
    if key[0].lower() in eng_alph:
        alph = "EN"
    elif key[0].lower() in rus_alph:
        alph = "RUS"
    else:
        raise ValueError("Недопустимый символ в ключе.")
    
    for letter in key.lower():
        if letter not in ALPHABETS[alph]:
            raise ValueError("Недопустипый символ или смешение языков в ключе.")
    
    return alph
    

def vigenere_encrypt(text: str, key: str) -> str:
    alph = check_key(key)
    encrypted_text = ''
    text = list(text.lower())
    key = list(key.lower())
    position = 0 # шифр тратится только на буквы, другие символы скипаем
    for letter in text:
        if letter in ALPHABETS[alph]:
            shift = ALPHABETS[alph].index(letter) + ALPHABETS[alph].index(key[position % len(key)])
            new_letter = ALPHABETS[alph][shift % len(ALPHABETS[alph])]
            position += 1
            encrypted_text += new_letter
        else:
            encrypted_text += letter
    return encrypted_text

        

def vigenere_decrypt(text: str, key: str) -> str:
    alph = check_key(key)
    decrypted_text = ''
    text = list(text.lower())
    key = list(key.lower())
    position = 0 # ключ тратится только на буквы, другие символы скипаем
    for letter in text:
        if letter in ALPHABETS[alph]:
            # + len(), чтобы не получить отрицательное число
            shift = ALPHABETS[alph].index(letter) + len(ALPHABETS[alph]) - ALPHABETS[alph].index(key[position % len(key)])
            new_letter = ALPHABETS[alph][shift % len(ALPHABETS[alph])]
            position += 1
            decrypted_text += new_letter
        else:
            decrypted_text += letter
    return decrypted_text
 
 
def check_correctness(text: str, key: str) -> bool:
    # регистр приводится к нижнему, поэтому сравниваем с text.lower()
    return vigenere_decrypt(vigenere_encrypt(text, key), key) == text.lower()
 
 
def run_tests():
    tests = [
        ("криптография", "шифр", "гщэакччбшээп"), # контрольный пример из методички
        ("echpochmac", "samsa", "wcthouhysc"), # для англa
        ("Hello, World!", "key", "rijvs, uyvjn!"), # регистр + пробел и знаки
        ("Привет, мир! 2026", "Ёлка", None), # русский, ё в ключе, цифры
        ("яблоко", "я", "юакнйн"), # ключ Я - свдиг через начало алфавита
        ("Hello, мир!", "key", None), # буквы другого алфавита не трогаем
    ]
    for text, key, expected in tests:
        encrypted = vigenere_encrypt(text, key)
        if expected is not None:
            assert encrypted == expected, f"{text!r}: ожидали {expected!r}, получили {encrypted!r}"
        assert check_correctness(text, key), f"D(E(m)) != m для {text!r}"
        print(f"OK  {text!r} + {key!r} -> {encrypted!r}")
 
    # некорректные ключи должны отклоняться
    for bad_key in ["", "ab1", "abк", "123", "ключ!"]:
        try:
            vigenere_encrypt("текст", bad_key)
        except ValueError as error:
            print(f"OK  ключ {bad_key!r} отклонён: {error}")
        else:
            raise AssertionError(f"ключ {bad_key!r} должен был быть отклонён")
 


print("+++\tТесты\t+++")
run_tests()
print("+++\tВсе тесты пройдены\t+++\n")

mode = input("Режим (e - шифрование, d - расшифрование): ").strip().lower()
text = input("Текст: ")
key = input("Ключ: ")
try:
    if mode == "e":
        result = vigenere_encrypt(text, key)
        print("Шифртекст:", result)
        print("Проверка D(E(m)) = m:", check_correctness(text, key))
    elif mode == "d":
        result = vigenere_decrypt(text, key)
        print("Открытый текст:", result)
        print("Проверка E(D(c)) = c:", vigenere_encrypt(result, key) == text.lower())
    else:
        print("Нужно ввести e или d. (ENG)")
except ValueError as error:
    print("Ошибка:", error)