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
)
from collections.abc import Iterable

import numpy as np
import numpy.core.defchararray as ncd
from tabulate import tabulate

from BioPlate.count import BioPlateCount
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.iterate import BioPlateIterate
from BioPlate.matrix import BioPlateMatrix


class BioPlateManipulation:
    """This parent class grouped all method that can be applied to BioPlate instance.
    
    """

    def __getitem__(self, index): #pragma: no cover
        return self[index]

    def __setitem__(self, index, value):#pragma: no cover
        self[index] = value

    @property
    def name(self: "BioPlateManipulation") -> str:
        """
        Get object name (BioPlate, Inserts, Array)

        Returns
        -------
        name : str
            name of instance

        Examples
        ---------
        >>> from BioPlate import BioPlate
        >>> plate = BioPlate(12, 8)
        >>> plate.name
        BioPlate

        """
        return type(self).__name__

    @overload
    def _args_analyse(
        self: "BioPlateManipulation", well: Dict[str, Any], value: None
    ) -> Tuple[Dict[str, Any], None]:  # pragma: no cover
        pass

    @overload
    def _args_analyse(
        self: "BioPlateManipulation", well: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], None]:  # pragma: no cover
        pass

    @overload
    def _args_analyse(
        self: "BioPlateManipulation",
        well: str,
        value: List[Any],
    ) -> Tuple[str, Union[str, int, float, List[Any], None]]:  # pragma: no cover
        pass


    @overload
    def _args_analyse(
        self: "BioPlateManipulation",
        well: str,
        value: Union[str, int, float, List[Any], None],
    ) -> Tuple[str, Union[str, int, float, List[Any], None]]:  # pragma: no cover
        pass

    def _args_analyse(self, *args):
        """

        Parameters
        ----------
        well : dict or str
                   stand alone args with value for each well
         value : list or str or int or float
                      list of value or value alone

        Returns
        -------
        well : dict or str
                    well position
         value : list or str or int or float or None
                     value for given well, None if dict was pass as argument
                
        Examples
        ----------
        
        >>> BioPlateManipulation._args_analyse({"A1" : "test"})
        ({"A1" : "test"}, None)
        >>> BioPlateManipulation._args_analyse("A[1-2]",  ["test", "test1"])
        ("A[1-2]",  ["test", "test1"])

        """
        if len(args) == 1:
            well, *trash = args
            value = None
            return well, value
        if len(args) == 2:
            well, value, *trash = args
            return well, value

    @overload
    def set(
        self: "BioPlateManipulation", well: Dict[str, Any], value: None
    ) -> Union["BioPlateManipulation", str]:  # pragma: no cover
        pass

    @overload
    def set(
        self: "BioPlateManipulation", well: Dict[str, Any]
    ) -> Union["BioPlateManipulation", str]:  # pragma: no cover
        pass

    @overload
    def set(
        self: "BioPlateManipulation",
        well: str,
        value: Union[str, int, float, List[Any], None],
    ) -> Union["BioPlateManipulation", str]:  # pragma: no cover
        pass

    def set(self, *args, merge=False):
        """Main entry point to assign value on plate 
           
        Parameters 
        ----------
          well : dict or str
              - if dict, well must contain well identifier as key and value to assign as value.eg : {"A2" : "value", "A[3-6]" : 42} 
              - if string, well is only a well identifier eg : "G5" 

         value : list or str or int or float 
             - if list, value should be presented with multiple well identifer "B-D[2-5]", ["value1", "value2", "value3"]

        merge : bool (by default False) 
            Value on well are not overide but added
        Returns
        -------
         BioPlate : BioPlate
             return instance of plate

         Exemples
         --------    
         see :ref:`Set-values-on-plate`
                 
        """
        well, value = self._args_analyse(*args)
        if not isinstance(well, str) and isinstance(well, Iterable):
            generator = well.items() if isinstance(well, dict) else well
            for key, val in generator:
                if merge:
                    self.set(key, val, merge=True)
                else:
                    self.set(key, val)
            return self
        well = BioPlateMatrix(str(well))
        if isinstance(value, list):
            plate_shape = self[well.row, well.column].shape
            len_plate_shape = len(plate_shape)
            if len_plate_shape > 1:
                if well.pos == "R":
                    resh_val = np.reshape(value, (plate_shape[0], 1))
                else:
                    resh_val = value
                if merge:
                    self[well.row, well.column] = ncd.add(
                        self[well.row, well.column], resh_val
                    )
                    return self
                self[well.row, well.column] = resh_val
                return self
            else:
                if merge:
                    self[well.row, well.column][: len(value)] = ncd.add(
                        self[well.row, well.column][: len(value)], value
                    )
                    return self
                self[well.row, well.column][: len(value)] = value
                return self
        if merge:
            self[well.row, well.column] = ncd.add(self[well.row, well.column], value)
            return self
        self[well.row, well.column] = value
        return self

    def get(
        self: "BioPlateManipulation", *well: str
    ) -> Union[List[str], Optional["BioPlateManipulation"], List[Sequence[Any]]]:
        """
        Use to retrive informations from BioPlate instance 
        
        Parameters
        ----------
        well : str
            well is only a well identifier eg : "G5", "2[B-G]"         
        Returns
        -------
        One_well : str
            get back value in one well eg : "G5"
        multiple_well : np.array
            get back all value eg : "2[B-G]"
        multiple_well_multiple_identifier : list
            return a list of eqch given arguments
                 
        """
        if len(well) > 1:
            querry = list()
            for w in well:
                result = self[w]
                if isinstance(result, str):
                    querry.append(result)
                else:
                    querry.append(result.tolist())
            return querry
        else:
            return self[str(well[0])]

    def save(self: "BioPlateManipulation", plate_name: str, **kwargs) -> Optional[str]:
        """
        Save BioPlate objwct to plate history database 
        
        Parameters
        ----------
        plate_name : str
            name of plate to save it in database eg : "expetiment 1"
        kwargs : dict
            To know kwargs see :func:`~BioPlate.database.plate_historic_db.PlateHist.add_hplate`

        Returns
        -------
        response : str
            database response for adding or updating plate historic database 
        
        
        """
        dbName = kwargs.get("db_hist_name")
        if not dbName:
            phi = PlateHist()
        else:
            phi = PlateHist(db_name=dbName)
        well = next(BioPlateIterate(self, OnlyValue=True)).shape
        numWell = well[0] * well[1]
        response = phi.add_hplate(numWell, plate_name, self)
        if isinstance(response, str):
            return response
        else:
            dict_update = {"plate_name": plate_name, "plate_array": self}
            return phi.update_hplate(dict_update, response, key="id")

    def table(
        self: "BioPlateManipulation", headers: str = "firstrow", **kwargs
    ) -> tabulate:
        """
        Transform BioPlate object to table
        
        Parameters
        ----------
        headers : str (by default "firstrow")
        kwargs : dict
            To know kwargs see `Tabulate <https://pypi.org/project/tabulate/#description>`_

        Returns
        -------
            table : str
                outputs a nicely formatted plain-text table

        """
        return tabulate(self, headers=headers, **kwargs)

    def iterate(
        self: "BioPlateManipulation", order: str = "C", accumulate: bool = True
    ) -> Generator:
        """
        Generaror to Iterate a BioPlate instance by column or row, with ability to group value of same well
        
        Parameters
        ----------
        order : { 'C', 'R'}
            Iterate by column (C) or by row (R)
        accumulate : bool (by default True)
            Group data of same well together

        Yields
        -------
        well : tuple
            each iteration contain well identifier and value(s) eg : ("B2", "value")
        

        """
        yield from BioPlateIterate(self, order=order, accumulate=accumulate)

    def count(self: "BioPlateManipulation", reverse: bool = False):
        """
        Count number of occurance in BioPlate instance
        
        Parameters
        ----------
        reverse : bool (by default false)

        Returns
        -------
        
        result : dict
            return a dict of occurance name : number of occurance
        """
        return BioPlateCount(self, reverse=reverse)

    def to_excel(
        self: "BioPlateManipulation",
        file_name: str,
        sheets: List[str] = ["plate_representation", "plate_data", "plate_count"],
        header: bool = True,
        accumulate: bool = True,
        order: str = "C",
        empty: str = "empty",
    ):
        """
        Send BioPlate instance to spreadsheet
        
        Parameters
        ----------
        file_name : str
            name of new created spreadsheet
        sheets : list[str]
            name of sheets
        header : bool (default is True)
            if header should be present in plate representation
        accumulate : bool (default is True)
            If data in BioPlate object should be accumulate or not see :func:`~BioPlate.Manipulation.BioPlateManipulation.iterate`
        order : {"C", "R"}
            Iterate value by column or row
        empty : str
            value assign to empty well 

        Returns
        -------
        spreadsheet : None
            create a spreasheet at given filename (should contain path also)
        """
        from BioPlate.writer.to_excel import BioPlateToExcel
        xls_file = BioPlateToExcel(
            file_name,
            sheets=sheets,
            header=header,
            accumulate=accumulate,
            order=order,
            empty=empty,
            test=False,
        )
        xls_file.representation(self)
        xls_file.data(self)
        xls_file.count(self)
        xls_file.close()
