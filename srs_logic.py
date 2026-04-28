from datetime import date, timedelta as td

import utils

def input_mark():
    while True:
        value = input('Введите оценку от 2 до 5: ')
        if value.isdigit():
            value = int(value)
            if value in range(2, 6):
                return value
        print("Ошибка. Нужно число от 2 до 5.")

def size_ratio(mark, interval, ratio):
    if mark == 2:
        return 1, 2.5
    elif mark == 3:
        ratio -= 0.2
    elif mark == 4:
        pass
    else:
        ratio += 0.2

    interval = max(1, int(interval * ratio))
    return interval, ratio


def repeat_card(cards):
    '''Функция для повтора карточек'''
    today = date.today()
    if not cards:
        print('Карточки не добавлены')
        return
    for i in cards:
        d = date.fromisoformat(i['next_date'])
        if d <= today: # Если дата меньше сегодня, то вывод карточки
            
            print("\nВопрос:")
            print(i['question'])

            input('\nНажмите Enter, чтобы показать ответ...')

            print("\nОтвет:")
            print(i['answer'])

            mark = input_mark()

            interval, ratio = size_ratio(mark, i['interval'], i['ratio'])
            i['interval'] = max(1, interval)
            i['ratio'] = max(1.3, ratio)
            i['next_date'] = str(today + td(days=i['interval']))
    
    


def add_card(cards):
    today = date.today()
    '''Создает файл с карточками или обавляет новые'''
    def new_card():
        question = input('Введите вопрос: \n')
        answer = input('Введите ответ: \n')
        d = {
            "question": question,
            "answer": answer,
            "interval": 1,
            "next_date": str(today + td(days=1)),
            "ratio": 2.5
            }
        cards.append(d)
    
    while True:
        new_card()
        change = input('''
                       Введите 
                       1 Добавить карточку
                       2 Выйти
                       ''')
        if change == '2':
            break





def look(cards):
    '''Позволяет просмотреть все карточки'''
    if not cards:
        print('Карточки не добавлены')
        return
    for i in cards:
        print("\nВопрос:")
        print(i['question'])

        input('\nНажмите Enter, чтобы показать ответ...')

        print("\nОтвет:")
        print(i['answer'])

        delete = input('\nУдалить эту карточку? Введите "да" для удаления, или любое другое слово для продолжения: ')
        if delete.lower() == 'да':
            cards.remove(i)