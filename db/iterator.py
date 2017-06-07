from abc import ABCMeta, abstractmethod


class Iterator(metaclass=ABCMeta):
    """
    Абстрактный итератор
    """

    _error = None   # класс ошибки, которая прокидывается в случае выхода за границы коллекции

    def __init__(self, collection, cursor) -> None:
        """
        Constructor.

        :param collection: коллекция, по которой производится проход итератором
        :param cursor: изначальное положение курсора в коллекции (ключ)
        """
        self._collection = collection
        self._cursor = cursor

    @abstractmethod
    def current(self) -> object:
        """
        Вернуть текущий элемент, на который указывает итератор
        """
        pass

    @abstractmethod
    def next(self) -> object:
        """
        Сдвинуть курсор на следующий элемент коллекции и вернуть его
        """
        pass

    @abstractmethod
    def has_next(self) -> bool:
        """
        Проверить, существует ли следующий элемент коллекции
        """
        pass

    @abstractmethod
    def remove(self) -> None:
        """
        Удалить текущий элемент коллекции, на который указывает курсор
        """
        pass

    def _raise_key_exception(self) -> None:
        """
        Прокинуть ошибку, связанную с невалидным индексом, содержащимся в курсоре
        """
        raise self._error('Collection of class {} does not have key "{}"'.format(
            self.__class__.__name__, self._cursor))


class ListIterator(Iterator):
    """
    �тератор, проходящий по обычному списку
    """

    _error = IndexError

    def __init__(self, collection: list) -> None:
        super().__init__(collection, 0)

    def current(self) -> object:
        if self._cursor < len(self._collection):
            return self._collection[self._cursor]
        self._raise_key_exception()

    def next(self) -> object:
        if len(self._collection) >= self._cursor + 1:
            self._cursor += 1
            return self._collection[self._cursor]
        self._raise_key_exception()

    def has_next(self) -> bool:
        return len(self._collection) >= self._cursor + 1

    def remove(self) -> None:
        if 0 <= self._cursor < len(self._collection):
            self._collection.remove(self._collection[self._cursor])
        else:
            self._raise_key_exception()
