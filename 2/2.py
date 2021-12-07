"""
2. Написати функцію, яка приймає два параметри: ім'я файлу та кількість символів.

   На екран повинен вивестись список із трьома блоками - символи з початку, із середини та з кінця файлу.

   Кількість символів в блоках - та, яка введена в другому параметрі.

   Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі (наприклад, файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?)

   В репозиторій додайте і ті файли, по яким робили тести.

   Як визначати середину файлу (з якої брать необхідні символи) - кількість символів поділити навпіл, а отримане "вікно" символів відцентрувати щодо середини файла і взяти необхідну кількість. В разі необхідності заокруглення одного чи обох параметрів - дивіться на свій розсуд.

   Наприклад:

   █ █ █ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ ░ █ █ █    - правильно

                     ⏫ центр

   █ █ █ ░ ░ ░ ░ ░ ░ █ █ █ ░ ░ ░ ░ █ █ █    - неправильно

                     ⏫ центр
"""


def file_parser_func(file_name: str, char_number: int):
    if type(file_name).__name__ != "str":
        raise TypeError("'{0}' object cannot be interpreted as string".format(type(file_name).__name__ ))
    if type(char_number).__name__ != "int":
        raise TypeError("'{0}' object cannot be interpreted as an integer".format(type(char_number).__name__))

    try:
        file = open(file_name, "r")
    except IOError:
        raise IOError("File does not appear to exist.")

    file_content = file.read()
    file_text_size = len(file_content)

    if char_number > file_text_size:
        raise OverflowError("Entered size {0} is bigger file size {1}".format(char_number, file_text_size))
    elif char_number > round(file_text_size / 3):
        raise OverflowError("Entered size {0} is bigger 1/3 of file size {1}".format(char_number, round(file_text_size / 3)))

    file_middle = round(file_text_size / 2)
    char_num = char_number
    middle_subs_begin = 0
    middle_subs_end = 0

    file_begin_str = None
    file_middle_str = None
    file_end_str = None

    if char_num % 2 != 0:
        char_num = round((char_number - 1) / 2)
        middle_subs_begin = file_middle - char_num
        middle_subs_end = (file_middle + char_num) + 1
    else:
        char_num = int(char_number / 2)
        middle_subs_begin = file_middle - char_num
        middle_subs_end = file_middle + char_num

    file_begin_str = file_content[0: char_number]
    file_middle_str = file_content[middle_subs_begin: middle_subs_end:]
    file_end_str = file_content[char_number * -1:]

#    print("File content: {0}".format(file_content)) # -> debug only print
    print(file_begin_str, file_middle_str, file_end_str)
    print("Entered block size: {0}".format(char_number))
    print("block 1 size: {0}".format(len(file_begin_str)))
    print("block 2 size: {0}".format(len(file_middle_str)))
    print("block 3 size: {0}".format(len(file_end_str)))

    file.close()


file_parser_func("test.txt", 10)