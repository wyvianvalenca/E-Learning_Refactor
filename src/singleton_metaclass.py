from abc import ABCMeta
from typing import Any
from typing_extensions import override


class SingletonABCMeta(ABCMeta):
    """ SINGLETON PATTERN - Metaclasse para classes abstratas que garante uma única instância """

    _instances: dict[type, Any] = {}

    @override
    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            instance = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance

        print(cls._instances[cls])
        return cls._instances[cls]


class SingletonMeta(type):
    """ SINGLETON PATTERN - Metaclasse para classes que garante uma única instância """

    _instances: dict[type, Any] = {}

    @override
    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        print(cls._instances[cls])
        return cls._instances[cls]
