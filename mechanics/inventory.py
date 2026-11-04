from dataclasses import dataclass, field
from core.exceptions import InventoryFullError

@dataclass
class Storage[T]():
    """Хранилище предметов типа T с ограниченной вместимостью (инвентарь, сундук и т.п.)"""

    __max_size : int
    _list_items : list[T] = field(default_factory=list)

    def add_item(self, item : T):
        """Кладёт item в хранилище; если места нет — выбрасывает InventoryFullError"""
        if len(self._list_items) + 1 <= self.__max_size:
            self._list_items.append(item)
        else:
            raise InventoryFullError
        
    def show_max_size(self):
        """Выводит максимальную вместимость хранилища"""
        print(self.__max_size)

    def show_inventory(self):
        """Выводит все предметы хранилища, по одному на строку"""
        print('-------')
        print(*self._list_items, sep='\n')
        print('-------')