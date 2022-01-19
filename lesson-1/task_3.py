"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""
words = '«attribute», «класс», «функция», «type»'.replace("«", "").replace("»", "").split(", ")
for word in words:
    try:
        print(bytes(word, 'ascii'))
    except UnicodeEncodeError:
        print(f"{word} cannot be transferred to bytes with b''")