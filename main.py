import argparse

from typing import Optional

from positions import list_of_strings_positions
from strings import list_of_strings, stop_words


class TextFormatter:
    def __init__(self, strings: list, positions: list, stop_words: Optional[list] = None):
        self.strings = strings
        self.positions = positions
        self.stop_words = stop_words if stop_words else []

    def get_as_list(self, username: str) -> list:
        """
        Метод возвращает правильно сформированный список слов итогового текста.
        Среди возвращаемых элементов не должно содержаться слов из списка стоп-слов.
        Элементы списка, содержащие шаблон {username}, должны быть заменены на значение переменной username.
        :param username: Имя пользователя
        :return: Список слов в правильном порядке
        """
        dict_text = {}
        for i, position_word in enumerate(self.positions):
            if type(position_word) is list:
                for position in position_word:
                    dict_text[position] = self.strings[i]
            else:
                dict_text[position_word] = self.strings[i]
        list_text = []
        for key, word in sorted(dict_text.items()):
            if word == '{username}':
                word = username
            if word not in self.stop_words:
                list_text += [word]
        return list_text

    def get_as_text(self, username: str) -> str:
        """
        Метод возвращает текст, сформированный из списка слов и позиций.
        В возвращаемом тексте не должно быть стоп-слов.
        Шаблон {username} должен быть заменён на значение переменной username.
        Каждое новое предложение должно начинаться с большой буквы.
        Между знаком препинания и впереди стоящим словом не должно быть пробелов.
        :param username: Имя пользователя
        :return: Текст, отформатированный согласно условиям задачи
        """
        text = ''
        for word in self.get_as_list(username):
            if not text:
                text += word.title()
            elif text[-1] in ['.', '!', '?', ':'] and word not in ['.', '!', '?', ':']:
                text += ' ' + word.title()
            elif word in ['.', '!', '?', ':', ',']:
                text += word
            else:
                text += ' ' + word
        return text


formatter = TextFormatter(list_of_strings, list_of_strings_positions, stop_words)

arguments_parser = argparse.ArgumentParser(prog="python main.py", description="Консольный рассказчик.")
arguments_parser.add_argument('-u',
                              '--username',
                              action='store',
                              help='Имя пользователя в истории')

arguments = arguments_parser.parse_args()

if arguments.username:
    print(formatter.get_as_text(arguments.username))
