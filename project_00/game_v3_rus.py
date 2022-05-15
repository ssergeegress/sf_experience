"""Алгоритм угадывания случайного числа.
Модификация задачи ""Проект 0: Угадай число"
курса "Специализация Data Science" Онлайн-школы "SкillFactory" — https://skillfactory.ru.
Репозиторий — https://github.com/ssergeegress.
"""

from sys import argv, exit
from itertools import permutations
import numpy as np


def awesome_help_epilogue():

    print(f'\n-- Запуск программы с параметром [-v] ([--verbose])'
          f'\n   позволит получить подробный вывод по каждому из проходов.\n'
          f'\n-- Запуск программы с параметром [-с] ([--choice])'
          f'\n   позволит задать границы диапазона и количество проходов'
          f'\n   с подстановкой последних введённых значений, либо'
          f'\n   значений по умолчанию при пропуске ввода.\n'
          f'\n-- Запуск программы с параметром [-s] ([--seed])'
          f'\n   позволит "заморозить" последовательности генерируемых'
          f'\n   значений для обеспечения воспроизводимости кода.\n'
          f'\n-- Данный алгоритм построен так, что по умолчанию в ходе'
          f'\n   перебора чисел каждый раз выбирается среднее в пределах'
          f'\n   скорректированных границ ("центр" текущего диапазона).'
          f'\n   Запуск программы с параметром [-r] ([--random])'
          f'\n   изменит поведение алгоритма таким образом,'
          f'\n   что в пределах текущего диапазона число будет'
          f'\n   каждый раз генерироваться случайным образом.\n'
          f'\n-- Параметры можно комбинировать, при этом допустим'
          f'\n   любой порядок их расположения, а также слитное'
          f'\n   написание для аббревиатур — [-cv] или [-vc].\n'
          f'\n-- Запуск программы с неизвестными произвольными параметрами'
          f'\n   выведет результат отработки значений по умолчанию.\n'
          f'\n-- Запуск программы без параметров выведет результат'
          f'\n   отработки значений по умолчанию и этот текст.\n\n')


def full_argv_list(*args: str) -> list:
    """Функция генерирует отформатированный список параметров
    и их комбинаций для перехвата из командной строки (Bash)
    с целью задействования соответствующих опций.

    Args: Литеры параметров

    Returns: 
        list: Отформатированный список комбинаций
    """
    full_combo_list = []
    argv_list = ['choice', 'random', 'seed', 'verbose']
    argv_list_abbreviated = ['c', 'r', 's', 'v']
    iter_len = len(argv_list) + 1
    for i in range(1, iter_len):
        for combo in permutations(argv_list, i):
            if any(arg in combo for arg in args):
                full_combo_list.append('--' + ' --'.join(combo))
        for combo in permutations(argv_list_abbreviated, i):
            if any(arg in combo for arg in args):
                full_combo_list.append('-' + ''.join(combo))

    return full_combo_list


def random_predict(number: int, iteration_number: int, random_attempts: bool,
                   *args: int) -> int:
    """Функция основного цикла.
    Именно здесь происходит "угадывание" числа на каждом
    из проходов и вывод промежуточных результатов.

    Args:
        number (int): Загаданное число
        iteration_number (int): Счётчик проходов
        random_attempts (bool): Флаг смены механизма перебора
        *args: (int): Границы диапазона

    Returns:
        int: Отгаданное число
    """
    predict_number = int(np.mean([*args]))
    predict_numbers = []
    predict_low = args[0]
    predict_high = args[1]
    count = 0

    while True:
        predict_numbers.append(predict_number)
        count += 1
        if predict_number < number:
            predict_low = predict_number + 1  # нижняя граница
        elif predict_number > number:
            predict_high = predict_number - 1  # верхняя граница
        else:
            break  # число совпадает с загаданным
        if random_attempts == True:
            if number == args[0]:
                predict_low -= 1  # экранирование ошибки low >= high
            predict_number = np.random.randint(predict_low, predict_high + 1)
        else:
            predict_number = int(np.mean([predict_low, predict_high]))

    # блок параметра подробого вывода:
    if any(arg in argv for arg in full_argv_list('v', 'verbose')):
        print(f'\n> Проход {iteration_number}. Порядок перебора:'
              f'\n  {predict_numbers}\n'
              f'  Число — {number}, попыток — {count};')

    return count


def score_game(random_predict) -> int:
    """Генератор "загадывания" случайных чисел.
    Здесь также задаются границы диапазона и количество проходов,
    которые передаются на вход функции основного цикла, и вывод
    итогового результата.

    Args:
        random_predict (_type_): Функция основного цикла

    Returns:
        int: Среднее количество попыток
    """
    # блок параметра задания произвольных значений
    # и определения значений по умолчанию:
    if any(arg in argv for arg in full_argv_list('c', 'choice')):
        try:
            with open('tmp.txt', 'r') as tmp_file:
                tmp_predict_list = tmp_file.read().splitlines()
        except FileNotFoundError:
            exit('\n  Недостаточно данных!\n'
                '  Запустите программу без параметров\n'
                '  для создания файла исходных значений.\n')
        awesome_requests = [
            f'\n  Введите первую границу диапазона (целое число, включительно) [{tmp_predict_list[0]}]: ',
            f'  Введите вторую границу диапазона (целое число, включительно) [{tmp_predict_list[1]}]: ',
            f'  Введите количество проходов (целое число, отличное от \'0\') [{tmp_predict_list[2]}]: '
        ]
        awesome_exception_answers = [
            '\n  Обратите внимание на условие ввода!'
            '\n  Выход.\n\n',
            '\n  Попыток перебора нет. At least, You really tried!\n'
            '  To try, or not to try, that was the very question!\n'
        ]
        try:
            predict_low = int(input(awesome_requests[0]) or tmp_predict_list[0])
            predict_high = int(input(awesome_requests[1]) or tmp_predict_list[1])
            if predict_low > predict_high:  # расстановка границ по возрастанию
                predict_low, predict_high = predict_high, predict_low
            predict_size = abs(int(input(awesome_requests[2]) or tmp_predict_list[2]))
            if predict_size == 0:  # экранирование ошибки ввода '0'
                exit(awesome_exception_answers[1])
        except ValueError:
            exit(awesome_exception_answers[0])
    else:
        predict_low = 1
        predict_high = 100
        predict_size = 1000
    with open('tmp.txt', 'w') as tmp_file:
        tmp_file.write(f'{predict_low}\n{predict_high}\n{predict_size}\n')

    # фиксация для воспроизводимости (по параметру):
    if any(arg in argv for arg in full_argv_list('s', 'seed')):
        np.random.seed(1)

    # создание списка случайных чисел:
    random_array = np.random.randint(predict_low,
                                     predict_high + 1,
                                     size=(predict_size))

    # блок параметра смены механизма перебора
    random_attempts = False
    if any(arg in argv for arg in full_argv_list('r', 'random')):
        random_attempts = True
    # # раскомментируйте для более наглядного сравнения механизмов:    
    #     print(f'\n  На каждой из попыток в пределах текущего диапазона'
    #           f'\n  число генерировалось случайным образом.')
    # else:
    #     print(f'\n  На каждой из попыток в пределах текущего диапазона'
    #           f'\n  выбиралось среднее от значений его границ (центр).')

    # генератор проходов цикла:
    count_ls = []
    iteration_number = 1
    for number in random_array:
        count_ls.append(
            random_predict(number, iteration_number, random_attempts,
                           predict_low, predict_high))
        iteration_number += 1
    score = int(np.mean(count_ls))
    score_min = int(np.min(count_ls))
    score_max = int(np.max(count_ls))

    print(
        f'\n  За {predict_size} проходов данный алгоритм угадывал число в диапазоне'
        f'\n  от {predict_low} до {predict_high} включительно в среднем с {score} попыток:'
        f'\n  минимум — с {score_min}, максимум — с {score_max} попыток.\n')

    # блок запуска без параметров (второе условие
    # добавлено только для отработки в Jupyter):
    if len(argv) == 1 or './game_v3_rus.py' in argv:
        awesome_help_epilogue()

    return score


if __name__ == "__main__":
    score_game(random_predict)
