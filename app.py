from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capacity):
        self._items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, title, quantity):
        pass

    @abstractmethod
    def remove(self, title, quantity):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, quantity):
        if title in self._items:
            self._items[title] += quantity
        else:
            self._items[title] = quantity
        self._capacity -= quantity

    def remove(self, title, quantity):
        result = self._items[title] - quantity
        if result > 0:
            self._items[title] = result
        else:
            del self._items[title]
        self._capacity += quantity

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


class Shop(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 20

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())

    def add(self, title, quantity):
        if title in self._items:
            self._items[title] += quantity
        else:
            self._items[title] = quantity
        self._capacity -= quantity

    def remove(self, title, quantity):
        result = self._items[title] - quantity
        if result > 0:
            self._items[title] = result
        else:
            del self._items[title]
        self._capacity += quantity


class Request:
    def __init__(self, string):
        self.string = self.split_string(string)
        self.from_ = self.string[4]
        self.to = self.string[6]
        self.amount = int(self.string[1])
        self.product = self.string[2]

    @staticmethod
    def split_string(string):
        return string.split(' ')

    def __repr__(self):
        return f'Доставить {self.amount} {self.product} из {self.from_} в {self.to}'


def main():
    while (True):
        user_input = input('Введите запрос: ')

        if user_input == 'stop':
            break

        request = Request(user_input)

        if request.from_ == request.to:
            print('Пункт назначения == Пункт отправки')
            continue

        if request.from_ == 'склад':
            if request.product in store.items:
                print(f'Нужный товар есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте {request.from_} нет такого товара')
                continue

            if store.items[request.product] >= request.amount:
                print(f'Нужное количество есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте {request.from_} не хватает {request.amount - store.items[request.product]}')
                continue

            if shop.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(f'В пункте {request.to} не хватает {request.amount - shop.get_free_space} места')
                continue

            store.remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} из пункта {request.from_}')
            print(f'Курьер везет {request.amount} {request.product} из пункта {request.from_} в пункт {request.to}')
            shop.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в пункт {request.to}')

        else:
            if request.product in shop.items:
                print(f'Нужный товар есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте {request.from_} нет такого товара')
                continue

            if shop.items[request.product] >= request.amount:
                print(f'Нужное количество есть в пункте \"{request.from_}\"')
            else:
                print(f'В пункте {request.from_} не хватает {request.amount - shop.items[request.product]}')
                continue

            if store.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(f'В пункте {request.to} не хватает {request.amount - store.get_free_space} места')
                continue

            shop.remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} из пункта {request.from_}')
            print(f'Курьер везет {request.amount} {request.product} из пункта {request.from_} в пункт {request.to}')
            store.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в пункт {request.to}')

        print('-' * 30)
        print('На складе:')
        for title, quantity in store.items.items():
            print(f'{title}: {quantity}')
        print(f'Свободного места {store.get_free_space}')

        print('-' * 30)
        print('В магазине:')
        for title, quantity in shop.items.items():
            print(f'{title}: {quantity}')
        print(f'Свободного места {shop.get_free_space}')


if __name__ == "__main__":
    store = Store()
    shop = Shop()

    store_items = {
        'чипсы': 10,
        'сок': 20,
        'кофе': 7,
        'печеньки': 38
    }

    store.items = store_items
    main()
