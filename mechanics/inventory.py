from dataclasses import dataclass, field
from core.exceptions import InventoryFullError

@dataclass
class Storage[T]():
    """Хранилище предметов типа T с ограниченной вместимостью (инвентарь, сундук и т.п.)"""

    _max_size : int = 32
    _list_items : list[T] = field(default_factory=list)

    def add_item(self, item : T):
        """Кладёт item в хранилище; если места нет — выбрасывает InventoryFullError"""
        if len(self._list_items) + 1 <= self._max_size:
            self._list_items.append(item)
        else:
            raise InventoryFullError

    def has_item(self, item: T):
        """Возвращает True, если item лежит в хранилище, иначе False"""
        return True if item in self._list_items else False

    def show_max_size(self):
        """Выводит максимальную вместимость хранилища"""
        print(self._max_size)

    def show_inventory(self): #TODO перереализовать после items
        """Выводит все предметы хранилища, по одному на строку"""
        print('-------')
        print(*self._list_items, sep='\n')
        print('-------')
    
    def delete_items(self, num : int):
        '''Удаляет item из инвенторя, если он есть'''
        del_item = self._list_items.pop(num)
        print(f"Был удален {del_item} из инвенторя")

@dataclass
class Bag[T](Storage[T]):
    """Сумка: маленькое хранилище на 8 предметов"""

    _max_size : int = field(default=8, init=False)
