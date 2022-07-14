import itertools
import sys
from random import randrange


def generate_combinations():
    '''
    Составление комбинаций из заданного набора букв.
    '''
    combinations_list = list(map(''.join, itertools.product('abcdef', repeat=4)))
    return combinations_list


def search_words(combinations_list):
    '''
    Поиск комбинаций совпадающих со словом из словаря.
    '''
    dictionary_list = []
    found_words = []

    with open('/usr/share/dict/american-english') as dictionary:
        for word in dictionary:
            dictionary_list.append(word.strip())

    for i in range(len(combinations_list)):
        if combinations_list[i] in dictionary_list:
            found_words.append(combinations_list[i])

    return found_words


def generate_mac(found_words):
    word_1 = found_words[randrange(len(found_words))]
    word_2 = found_words[randrange(len(found_words))]
    mac_address_part = word_1[0:2] + ':' + word_1[2:4] + ':' + word_2[0:2] + ':' + word_2[2:4] + ':'

    return mac_address_part


def main():
    mac_address_start = generate_mac(search_words(generate_combinations()))
    # range задает диапазон и количество генерируемых MAC-адресов.
    for i in range(1, 15):
        # Формирование полного МАС-адреса.
        # "{:02d}".format(i) -- заполнение нулями.
        mac_address_full = mac_address_start + '00' + ':' + str("{:02d}".format(i))
        print(mac_address_full)


if __name__ == '__main__':
    # Обработка <Ctrl>+<C>
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
