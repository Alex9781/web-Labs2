# -*- coding: utf-8 -*-
"""
Задание 7.3

Скрипт должен обрабатывать записи в файле CAM_table.txt. Каждая строка,
где есть MAC-адрес, должна быть обработана таким образом, чтобы
на стандартный поток вывода была выведена таблица вида:

100      01bb.c580.7000      Gi0/1
200      0a4b.c380.7c00      Gi0/2
300      a2ab.c5a0.700e      Gi0/3
10       0a1b.1c80.7000      Gi0/4
500      02b1.3c80.7b00      Gi0/5
200      1a4b.c580.7000      Gi0/6
300      0a1b.5c80.70f0      Gi0/7
10       01ab.c5d0.70d0      Gi0/8
1000     0a4b.c380.7d00      Gi0/9


Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

file = open('Lab1\\07_files\\CAM_table.txt', 'r', encoding='UTF-8')
result = ''
template = """
    {:<7}{:14}   {}
"""
for line in file:
    if (line == '\n' or line == ''): 
        continue
    if (line[1].isdigit()):
        line = line.replace('DYNAMIC', '')
        line = line.split()
        result += template.format(line[0], line[1], line[2])

print(result.replace('\n\n', '\n'))
