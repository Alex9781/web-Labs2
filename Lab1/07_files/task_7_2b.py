# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

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

output = open(f'./{argv[2]}', 'w')

output.write(result)
