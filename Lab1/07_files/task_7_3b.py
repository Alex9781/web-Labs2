# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

file = open('Lab1\\07_files\\CAM_table.txt', 'r', encoding='UTF-8')

vlan = input('Enter VLAN number: ')

results = []
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
        line[0] = int(line[0])
        if line[0] == int(vlan):
            results.append(line)

results.sort()

for i in results:
    result += template.format(i[0], i[1], i[2])

print(result.replace('\n\n', '\n'))
