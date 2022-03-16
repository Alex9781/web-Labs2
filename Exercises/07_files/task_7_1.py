# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

file = open('Lab1\\07_files\\ospf.txt', 'r', encoding='UTF-8')

template = """
    Prefix                {:15}
    AD/Metric             {:15}
    Next-Hop              {:15}
    Last update           {:15}
    Outbound Interface    {:15}
"""

for line in file:
    ospf = line.split()
    ospf.remove('O')
    ospf.remove('via')
    ospf[1] = ospf[1].strip('[]')
    ospf[2] = ospf[2].strip(',')
    ospf[3] = ospf[3].strip(',')
    print(template.format(ospf[0], ospf[1], ospf[2], ospf[3], ospf[4]))
