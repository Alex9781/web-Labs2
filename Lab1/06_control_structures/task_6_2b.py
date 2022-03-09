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
while True:
    ip = input("Введите IP а формате 10.0.1.1: ").split(".")

    correct = True

    if len(ip) != 4:
        correct = False

    for oct in ip:
        if not oct.isdigit():
            correct = False
            break
        if int(oct) < 0 or int(oct) > 255:
            correct = False
            break

    if correct:
        if 0 < int(ip[0]) and int(ip[0]) < 224:
            print("unicast")
        elif 223 < int(ip[0]) and int(ip[0]) < 239:
            print("multicast")
        elif ip == ["255", "255", "255", "255"]:
            print("local broadcast")
        elif ip == ["0", "0", "0", "0"]:
            print("unassigned")
        else:
            print("unused")
        break
    else:
        print("Неправильный IP-адрес")
        break
    