from typing import (
    Dict,
    List,
    Tuple,
    Optional,
    Union,
    Any,
    overload,
    Sequence,
    Generator,
    Callable,
    MutableMapping,
)

import numpy as np

from BioPlate.iterate import BioPlateIterate


class BioPlateCount:
    """A row is symbolise by it's letter, a column by a number"""

    @overload  # BioPlate
    def __new__(
        cls, plate: np.ndarray, reverse: bool = False
    ) -> MutableMapping[str, int]:  # pragma: no cover
        pass

    @overload  # Inserts
    def __new__(
        cls, plate: np.ndarray, reverse: bool = False
    ) -> MutableMapping[str, Dict[str, int]]:  # pragma: no cover
        pass

    @overload  # Stack of BioPlate
    def __new__(
        cls, plate: np.ndarray, reverse: bool = False
    ) -> MutableMapping[int, Dict[str, int]]:  # pragma: no cover
        pass

    @overload  # Stack of Inserts
    def __new__(
        cls, plate: np.ndarray, reverse: bool = False
    ) -> MutableMapping[int, MutableMapping[str, Dict[str, int]]]:  # pragma: no cover
        pass

    def __new__(cls, plate, reverse=False):
        cls.plate = plate
        cls.reverse = reverse
        cls.plate_iterated = BioPlateIterate(plate, OnlyValue=True)
        return cls.count()

    @classmethod
    def __count(cls, plate: np.ndarray) -> Dict[str, int]:
        """

        :param plate:
        :return:
        """
        unique, count = np.unique(plate, return_counts=True)
        count_in_dict = dict(zip(unique, count))
        count_ordered = dict(
            sorted(count_in_dict.items(), key=lambda x: x[1], reverse=cls.reverse)
        )
        return count_ordered

    @overload  # BioPlate
    def count(cls) -> Dict[str, int]:  # pragma: no cover
        pass

    @overload  # Inserts
    def count(cls) -> MutableMapping[str, Dict[str, int]]:  # pragma: no cover
        pass

    @overload
    def count(cls) -> MutableMapping[int, Dict[str, int]]:  # pragma: no cover
        pass

    @overload
    def count(
        cls
    ) -> MutableMapping[int, MutableMapping[str, Dict[str, int]]]:  # pragma: no cover
        pass

    @classmethod
    def count(cls):
        if cls.plate.name == "Plate":
            return cls.count_BioPlatePlate()
        elif cls.plate.name == "Inserts":
            return cls.count_BioPlateInserts()
        else:
            return cls.count_BioPlateStack()

    @classmethod
    def count_BioPlateInserts(cls) -> MutableMapping[str, Dict[str, int]]:
        result = {}
        result["top"] = cls.__count(next(cls.plate_iterated))
        result["bot"] = cls.__count(next(cls.plate_iterated))
        return result

    @classmethod
    def count_BioPlatePlate(cls) -> Dict[str, int]:
        return cls.__count(next(cls.plate_iterated))

    @overload
    def count_BioPlateStack(
        cls
    ) -> MutableMapping[int, Dict[str, int]]:  # pragma: no cover
        pass

    @overload
    def count_BioPlateStack(
        cls
    ) -> MutableMapping[int, MutableMapping[str, Dict[str, int]]]:  # pragma: no cover
        pass

    @classmethod
    def count_BioPlateStack(cls):
        result = {}
        index = 0
        for plate in BioPlateIterate(cls.plate, OnlyValue=True):
            if plate.name == "Plate":
                result[index] = cls.count_BioPlatePlate()
                pass
            elif plate.name == "Inserts":
                try:
                    result[index] = cls.count_BioPlateInserts()
                except StopIteration:
                    break
            index += 1
        return result
