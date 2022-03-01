# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
correct = False
while (not correct):
    ip = input('Введите IP-адрес\n')
    ip = ip.split('.')

    incorrect = False
    for i in ip:
        if i.isdigit():
            if (int(i) < 0 or int(i) > 255):
                incorrect = True
                break
        else:
            incorrect = True
            break

    if (incorrect):
        print('Неправильный IP-адрес')
    else:
        correct = True
        if 1 < int(ip[0]) < 223:
            print('unicast')
        elif 224 < int(ip[0]) < 239:
            print('multicast')
        elif int(ip[0]) == 255 and int(ip[1]) == 255 and int(ip[2]) == 255 and int(ip[3]) == 255:
            print('local broadcast')
        elif int(ip[0]) == 0 and int(ip[1]) == 0 and int(ip[2]) == 0 and int(ip[3]) == 0:
            print('unassigned')
        else:
            print('unused')
