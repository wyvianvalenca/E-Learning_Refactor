from abc import ABCMeta
from typing import Any, Callable
from typing_extensions import override


class SingletonABCMeta(ABCMeta):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            instance = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance

        print(cls._instances[cls])
        return cls._instances[cls]


class SingletonMeta(type):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        print(cls._instances[cls])
        return cls._instances[cls]
