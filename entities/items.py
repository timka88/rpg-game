# TODO : переопределить str
from __future__ import annotations
from abc import ABC, abstractmethod
from core.exceptions import NegativeValueError, NegativeWearLevelError, TargetError
from entities.characters import Character


class Item(ABC): 
    '''базовый класс для всех предметов'''
    def __new__(cls, *args, **kwargs):
        if cls is Item:
            raise TypeError("Нельзя создавать экземпляры базового класса Item")   
        return super().__new__(cls)

class BreakableItem(Item, ABC):
    '''базовый класс для предметов, которые могут изнашиваться'''

    def __init__(self, wear_lvl: float, wear_lvl_max: float):
        self._wear_lvl = wear_lvl
        self.__wear_lvl_max = wear_lvl_max
        self.__is_broken = False

    def __new__(cls, *args, **kwargs):
        if cls is BreakableItem:
            raise TypeError("Нельзя создавать экземпляры абстрактного класса BreakableItem")   
        return super().__new__(cls)


    @property
    def is_broken(self) -> bool:
        return self.__is_broken
 
    @property
    def wear_lvl(self) -> float:
        return self._wear_lvl
 
    @property
    def wear_lvl_max(self) -> float:
        return self.__wear_lvl_max
 
    def lose_wear_lvl(self, amount: float):
        if self.is_broken:
            raise TargetError
        if amount < 0:
            raise NegativeValueError
        
        new_wear_lvl = self._wear_lvl - amount
        if new_wear_lvl < 0:
            raise NegativeWearLevelError
 
        self._wear_lvl = new_wear_lvl
        if new_wear_lvl == 0:
            self.__is_broken = True


class UnbreakableItem(Item, ABC):
    '''абстркатный класс для предметов, которые не имеют износа'''
    def __new__(cls, *args, **kwargs):
        if cls is UnbreakableItem:
            raise TypeError("Нельзя создавать экземпляры абстрактного класса UnbreakableItem")   
        return super().__new__(cls)

class Weapon(BreakableItem, ABC):
    '''абстрактный класс для всех типов оружия'''
    
    def __init__(self, amount_of_damage: float, wear_lvl: float, wear_lvl_max: float):
        super().__init__(wear_lvl, wear_lvl_max)
        self.amount_of_damage = amount_of_damage

    def __new__(cls, *args, **kwargs):
        if cls is Weapon:
            raise TypeError("Нельзя создавать экземпляры абстрактного класса Weapon")   
        return super().__new__(cls)
    
    @abstractmethod
    def attack(self, target: Character):
        '''атакует цель, наносит ей урон и возвращает его'''
        pass

class Sword(Weapon):
    '''меч: средний урон, средняя прочность'''

    def __init__(self, amount_of_damage: float = 15, wear_lvl: float = 100, wear_lvl_max: float = 100):
        super().__init__(amount_of_damage, wear_lvl, wear_lvl_max)

    def attack(self, target: Character):
        '''бьёт цель мечом, тратит 5 ед. прочности, наносит и возвращает урон'''
        self.lose_wear_lvl(min(5, self.wear_lvl))
        print('Взмах мечом!')
        target.take_damage(self.amount_of_damage)

class Spear(Weapon):
    '''копьё: высокий урон, но быстро изнашивается'''

    def __init__(self, amount_of_damage: float = 20, wear_lvl: float = 70, wear_lvl_max: float = 70):
        super().__init__(amount_of_damage, wear_lvl, wear_lvl_max)

    def attack(self, target: Character):
        '''колет цель копьём, тратит 7 ед. прочности, наносит'''
        self.lose_wear_lvl(min(7, self.wear_lvl))
        print('Выпад копьём!')
        target.take_damage(self.amount_of_damage)

class Bow(Weapon):
    '''лук: дальний бой, тратит стрелы'''

    def __init__(self, amount_of_damage: float = 12, wear_lvl: float = 80, wear_lvl_max: float = 80, arrows: int = 20):
        super().__init__(amount_of_damage, wear_lvl, wear_lvl_max)
        self.arrows = arrows

    def attack(self, target: Character):
        '''стреляет в цель из лука: тратит одну стрелу и 3 ед. прочности, наносит урон'''
        if self.arrows <= 0:
            raise TargetError
        self.arrows -= 1
        self.lose_wear_lvl(min(3, self.wear_lvl))
        print('Выстрел из лука!')
        target.take_damage(self.amount_of_damage)

class Armour(BreakableItem, ABC):

    def __init__(self, wear_lvl, wear_lvl_max):
        super().__init__(wear_lvl, wear_lvl_max)
    
    def get_amount_of_protect(self):
        if self.wear_lvl >= 0:
            return self.wear_lvl
        else:
            raise NegativeValueError
    
    def lose_wear_lvl(self, amount):
        cur_lvl = self.wear_lvl
        try:
            super().lose_wear_lvl(self, amount)
        except NegativeWearLevelError:
            return abs(cur_lvl - amount)
        

    


class Amulet(UnbreakableItem):
    '''амулет: даёт постоянный бонус к максимальному здоровью'''

    def __init__(self, hp_bonus: float = 20):
        self.hp_bonus = hp_bonus