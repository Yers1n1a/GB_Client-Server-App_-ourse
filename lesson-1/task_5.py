"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import subprocess
import chardet

args_1 = ['ping', 'yandex.ru']

subproc_ping = subprocess.Popen(args_1, stdout=subprocess.PIPE)

for line in subproc_ping.stdout:
    print(line.decode(chardet.detect(line)['encoding'].encode('utf-8').decode('utf-8')))

args_2 = ['ping', 'youtube.com']

subproc_ping2 = subprocess.Popen(args_2, stdout=subprocess.PIPE)

for line in subproc_ping2.stdout:
    print(line.decode(chardet.detect(line)['encoding'].encode('utf-8').decode('utf-8')))