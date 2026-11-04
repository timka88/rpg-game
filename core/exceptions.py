from abc import (abstractmethod, ABC)

class GameException(Exception, ABC):
    """Базовое исключение для всех игровых ошибок и событий"""
    pass

class ScriptException(Exception, ABC):
    """Базовое исключение для всех ошибок в логике сценария и механик"""
    @abstractmethod
    def show_message(self):
        '''Выводит разработчику сообщение о его ошибке'''
        pass

class OverflowLimitError(ScriptException):
    """Значение параметра (hp, мана, размер и т.п.) превышает допустимый максимум"""

    def show_message(self):
        """Выводит сообщение о превышении максимальной границы"""
        print('Указанный параметр превышает максимальную границу')

class NegativeValueError(ScriptException):
    """Передано отрицательное значение там, где допустимо только >= 0"""

    def show_message(self):
        """Выводит сообщение об отрицательном значении"""
        print('Значение не может быть отрицательным')

class GameOverException(GameException, ABC):
    """Базовое исключение окончания игры (победа, поражение, таймаут)"""

    @abstractmethod
    def show_message(self):
        """Выводит игроку сообщение о причине окончания игры"""
        pass

class LoseException(GameOverException):
    """Игра окончена поражением: герой погиб"""

    def show_message(self):
        """Выводит сообщение о поражении"""
        print("Вы проиграли")

class WinException(GameOverException):
    """Игра окончена победой игрока"""

    def show_message(self):
        """Выводит сообщение о победе"""
        print('Поздравляем! Вы выиграли')

class TimeLimitException(GameOverException):
    """Игра окончена из-за истечения лимита времени"""

    def show_message(self):
        """Выводит сообщение об истечении времени"""
        print('Истекло время выполнения')

class InventoryFullError(GameException):
    """В инвентаре нет места для нового предмета"""
    pass

class NotEnoughManaError(GameException):
    """У персонажа недостаточно маны для действия"""
    pass

class TargetError(GameException):
    """Недопустимая цель или действие (например, цель уже мертва)"""
    pass

class ChoiceError(GameException):
    """Игрок сделал недопустимый выбор"""
    pass
