# НЕ ЗАБЫТЬ : можно реализовать механику шанса попадания, которая зависит от ловкости цели и точности атакующего
from __future__ import annotations
from abc import (ABC, abstractmethod)
from core.exceptions import (LoseException, TargetError, NegativeValueError, OverflowLimitError, ChoiceError)
from mechanics.inventory import Storage
from entities.items import Armour

DAMAGE = 0

class Character(ABC):
    """Базовый класс любого персонажа: хранит здоровье и ману"""

    def __init__(self, hp: float, hp_max: float, mana: float):
        """Создаёт персонажа с текущим и максимальным здоровьем и запасом маны"""

        if hp <= 0 or hp_max <= 0 or mana < 0:
            raise NegativeValueError
        if hp > hp_max:
            raise OverflowLimitError

        self._hp = hp
        self._hp_max = hp_max
        self._mana = mana

    def take_damage(self, amount_of_damage: float):
        """Уменьшает здоровье на amount_of_damage"""
        if amount_of_damage < 0:
            raise NegativeValueError
        self._hp -= amount_of_damage

    def heal(self, amount: float):
        """Восстанавливает здоровье на amount, но не выше hp_max"""
        if amount < 0:
            raise NegativeValueError
        self._hp = min(self._hp + amount, self._hp_max)

    @abstractmethod
    def attack(self, target: Character):
        """Атакует цель target"""
        pass

    @abstractmethod
    def make_sound(self):
        """Выводит характерный звук персонажа"""
        pass


class Hero(Character, ABC):
    """Персонаж игрока. Его смерть означает поражение"""

    def __init__(self, hp: float, hp_max: float, mana: float):
        """Создаёт героя с пустым инвентарём и без выбранной брони"""
        super().__init__(hp, hp_max, mana)
        self.inventory = Storage()
        self.armour = None

    def choose_armour(self, armour: Armour):
        '''Выбирает броню из инвентаря'''
        if not isinstance(armour, Armour) or not self.inventory.has_item(armour):
            raise ChoiceError
        self.armour = armour

    def _active_armour(self):
        """Выбранная броня, если она в инвентаре и цела, иначе лучшая"""
        if self.inventory.has_item(self.armour) and not self.armour.is_broken:
            return self.armour
        return None

    def take_damage(self, amount_of_damage: float):
        """Получает урон (в том числе и через броню), если здоровье кончилось, выбрасывает LoseException"""
        if amount_of_damage < 0:
            raise NegativeValueError

        armour = self._active_armour()
        if armour is not None:
            amount_of_damage = armour.defend(amount_of_damage)

        super().take_damage(amount_of_damage)
        if self._hp <= 0:
            raise LoseException


class Monster(Character, ABC):
    """Враг. После смерти становится неактивным и не может быть целью"""

    def __init__(self, hp, hp_max, mana):
        """Создаёт монстра в активном (живом) состоянии"""
        super().__init__(hp, hp_max, mana)
        self._is_active = True


    def take_damage(self, amount_of_damage):
        """Получает урон и деактивируется при hp <= 0; по мёртвому — TargetError"""
        if self._is_active:
           super().take_damage(amount_of_damage)
           if self._hp <= 0:
               self._is_active = False
        else:
            raise TargetError

    def heal(self, amount: float):
        """Лечится на amount (не выше hp_max), только если жив"""
        if self._is_active:
            super().heal(amount)


class Knight(Hero):
    """Рыцарь — базовый герой ближнего боя"""

    def attack(self, target: Character):
        """Наносит цели обычный урон"""
        target.take_damage(DAMAGE)
        print(f'Рыцарь нанес {DAMAGE} урона!')

    def make_sound(self):
        """Боевой клич рыцаря"""
        print('AAAAAAAAAA')


class FlyingKnight(Hero):
    """Летающий рыцарь — герой с дополнительной атакой с воздуха"""

    def attack(self, target: Character):
        """Наносит цели обычный урон"""
        target.take_damage(DAMAGE)
        print(f'Рыцарь влетел на {DAMAGE} урона!')

    def make_sound(self):
        """Звук полёта"""
        print('вшшшшш')

    def attack_by_flight(self, target: Character):
        """Особая атака с воздуха: наносит цели полуторный урон (DAMAGE * 1.5)"""
        target.take_damage(DAMAGE*1.5)
        print(f'Рыцарь нанес эпическую атаку на {DAMAGE} урона')

class Archer(Hero):
    '''Лучник. Предпочитает дальний бой'''

    def attack(self, target: Character):
        """Стреляет в цель и наносит урон"""
        target.take_damage(2 * DAMAGE)
        print(f'Стрела лучника пронзила {target}')

    def make_sound(self):
        """Лучник молчит, чтобы не выдать себя"""
        print('... ~ лучник предпочитает не выдавать себя ~')
        


class Goblin(Monster):
    """Гоблин — слабый монстр, может лечиться, пока жив"""

    def attack(self, target: Character):
        """Атакует цель; мёртвый гоблин атаковать не может (TargetError)"""
        if self._is_active:
            target.take_damage(DAMAGE)
            print(f'Гоблин нанес {DAMAGE} урона!')
        else:
            raise TargetError

    def make_sound(self):
        """Рычание гоблина"""
        print('ГРРРРР')


class Skeleton(Monster):
    """Скелет — нежить, лечение на него не действует"""

    def heal(self, amount: float):
        """Ничего не делает: скелет не лечится"""
        if amount < 0:
            raise NegativeValueError
        print("скелет не получил никакой пользы с этого (((")

    def attack(self, target: Character):
        """Атакует цель; мёртвый скелет атаковать не может (TargetError)"""
        if self._is_active:
            target.take_damage(DAMAGE)
            print(f'Скелет нанес {DAMAGE} урона!')
        else:
            raise TargetError

    def make_sound(self):
        """Стук костей"""
        print('стучит костями')


class Dragon(Monster):
    """Дракон — сильный летающий монстр"""

    def attack(self, target):
        """Атакует цель; мёртвый дракон атаковать не может (TargetError)"""
        if self._is_active:
            target.take_damage(DAMAGE)
            print(f'Дракон нанес {DAMAGE} урона!')
        else:
            raise TargetError

    def make_sound(self):
        """Рык дракона"""
        print('~летающе рычит~')

