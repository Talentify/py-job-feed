from abc import abstractmethod, ABC


class ESHitFormatterABC(ABC):

    @staticmethod
    @abstractmethod
    def format(es_hit: dict) -> dict:
        pass

    @staticmethod
    def source() -> str:
        pass
