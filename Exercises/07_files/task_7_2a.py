# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv

ignore = ["duplex", "alias", "configuration"]

file_name = argv[1]

result = ''

file = open(f'{file_name}', 'r', encoding='UTF-8')

for line in file:
    if (line.startswith('!')):
        continue
    else:
        if (set(ignore) & set(line.split())):
            continue
        else:
            result += line
print(result)
