from tabulate import tabulate
from BioPlate.database.plate_historic_db import PlateHist
from BioPlate.Matrix import BioPlateMatrix
from BioPlate.Iterate import BioPlateIterate
from BioPlate.Count import BioPlateCount


class BioPlateManipulation:
    """This parent class grouped all method that can be applied to BioPlate instance"""
             
    @property
    def name(self):
        """
        Get object name (BioPlate, BioPlateInserts, BioPlateArray)
        
        Returns
        -------
        name : str
            name of instance 
        
        Exemples:
        ---------        
        >>> plate = BioPlate(12, 8)
        >>> plate.name
        BioPlate

        """
        return type(self).__name__         
                
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
                
        Exemples
        ----------
        
        >>> BioPlateManipulation._args_analyse({"A1" : "test"})
        ({"A1" : "test"}, None)
        >>> BioPlateManipulation._args_analyse("A[1-2]",  ["test", "test1"])
        ("A[1-2]",  ["test", "test1"])

        """
        dict_in = any(isinstance(arg, dict) for arg in args)
        list_in = any(isinstance(arg, list) for arg in args)
        if len(args) == 2 and not dict_in :
            well, value, *trash = args
        if len(args) == 1 and dict_in:
            well, *trash = args
            value = None
        if len(args) == 2 and list_in:
            well, value, *trash = args
        return well, value                                        

    def _add_values(self, *args):
        """
        Add values is use to seperate well, value of dict and assign it to each well.
        
        Parameters
        ----------
        
        well : dict
                  dictionary of well, value to assign     

        Returns
        -------
            
        BioPlate : BioPlate
                        return instance of plate
         
         Raises
         ---------
         
         AttributeError
             If args is not a dict
         
            
        """
        well_dict, *trash = self._args_analyse(*args)
        try:
            Eval = lambda W_V : self._eval_well_value(W_V[0], W_V[1])
            list(map(Eval, well_dict.items()))
            return self
        except AttributeError:
            return f"{type(well_dict)} is a wrong format, dictionary should be used"

    """
        parse an add_value_row or column in a compact manner and pass it to evaluate(eg : 'A-C[1-5]', ['val1' , 'val2', 'val3'])
        
        :param multi_wells: 'A-C[1-5]' => On row A, B and C add value from column 1 to 5 included
        :param values: ['val1' , 'val2', 'val3'] => On row A add value 'val1', on row B add value 'val2' from column 1 to 5
        :return: plate
       
    """
    def set(self, *args):
        """
        Main entry point to assign value on plate

        Parameters
        ----------
          well : dict or str
                   - if dict, well must contain well identifier as key and value to assign as value.eg : {"A2" : "value", "A[3-6]" : 42}
                   - if string, well is only a well identifier eg : "G5"
         value : list or str or int or float
                      - if list, value should be presented with multiple well identifer
                      "B-D[2-5]", ["value1", "value2", "value3"]

        Returns
        -------
         BioPlate : BioPlate
                        return instance of plate
         
         Exemples
         -----------
         
         see :ref:`fn_set`
        
        """
        well, value, *trash = self._args_analyse(*args)
        if isinstance(well, dict):
            return self._add_values(*args)
        self._eval_well_value(well, value)
        return self

    def _eval_well(self, well, value=None):
        """
        This function assign a value, if `value` is not None, else this funvtion return selected well.
        
        Parameters
        ----------
        well : tuple or list
                well position rendered by BioPlateMatrix
        value : str or int or float or None
                value to assign to a given well
        
        Returns
        -------
        
        None : None
            If value is given, function assign to well value and return None
        selected_well : str or int or float or np.array
            If value is None, return the selected well
        
        """
        """
        well = ("All", "R", 2) => self[:,well[2]]
        well = ("All", "C", 2) => self[well[2]]
        well = ("R", 2, 6, 4) => self[well[1]:well[2], well[3]]
        well = ("C", 2, 6, 8) => self[well[1],well[2]: well[3]]
        well = [("C", 2, 8, 13), ("C", 3, 8, 13), ("C", 4, 8, 13)] => self[well[0][1]:well[-1][1] + 1, well[0][2] :well[0][3]]
        well =  [("R", 5, 8, 6), ("R", 5, 8, 7), ("R", 5, 8, 8)] => self[well[0][1]:well[0][2],well[0][3]:well[-1][3] +1]
        """
        if well[0] == "R":
            if value is not None: 
                self[well[1]:well[2], well[3]] = value
            else:
                return self[well[1]:well[2], well[3]]
        elif well[0] == "C":
            if value is not None:
                self[well[1], well[2]:well[3]] = value
            else:
                return self[well[1], well[2]:well[3]]
        elif well[0] == "All":
             if well[1] == "R":
                 if value is not None:
                     if isinstance(value, list):
                         self[1:,1:][well[2]][0:len(value)] = value
                     else:
                         self[1:,1:][well[2]] = value
                 else:
                     return self[1:,1:][well[2]]
             elif well[1] == "C":
                 if value is not None:
                     if isinstance(value, list):
                         self[1:,1:][:,well[2]][0:len(value)] = value
                     else:
                         self[1:,1:][:,well[2]] = value
                 else:
                     return self[1:,1:][:,well[2]]
        else:
            if value is not None:
                self[well[0], well[1]] = value
            else:
                if isinstance(well, tuple):
                    return self[well[0], well[1]]
                elif well[0][0] == "R":
                    return self[well[0][1]:well[0][2],well[0][3]:well[-1][3] +1]
                elif well[0][0] == "C":
                    return self[well[0][1]:well[-1][1] + 1,well[0][2]:well[0][3]]

    def _eval_well_value(self, well, value):
        """
        Pre process well and value for _eval_well. Transform well str and dict to tuple or list of integer posution for numpy indexing.
        
        Parameters
        ----------
       well : dict or str
            - if dict, well must contain well identifier as key and value to assign as value. eg : {"A2" : "value", "A[3-6]" : 42}
           - if string, well is only a well identifier eg : "G5"
        value : str or int or float or None
                value to assign to a given well

        Returns
        -------
        None : None
            Only pre process well value
            
         Raises
         ---------
         ValueError
             If number of column or row is not equal to value when value are in list
        """
        well = BioPlateMatrix(well)
        if isinstance(well, list):
            if isinstance(value, list):
                if len(well) == len(value):
                    for w, v in zip(well, value):             
                        self._eval_well(w,v)
                elif len(well) != len(value):
                    raise ValueError(f"missmatch between wells ({len(well)}) and values ({len(value)})")
            else:
                for w in well:
                    self._eval_well(w, value)
        else:           
            self._eval_well(well, value)

    def get(self, *well):
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
            test = lambda x : list(x) if not isinstance(x, str) else x
            return list(map(test, list(map(self._eval_well, map(BioPlateMatrix, well)))))
        else:
            return self._eval_well(BioPlateMatrix(well[0]))

    def save(self, plate_name, **kwargs):
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
        if not dbName :
            phi = PlateHist()
        else:
            phi = PlateHist(db_name=dbName)
        well = next(BioPlateIterate(self, OnlyValue=True)).shape
        numWell = well[0] * well[1]
        response = phi.add_hplate(numWell, plate_name, self)
        if isinstance(response, str):
            return response
        elif isinstance(response, int):
            dict_update = {"plate_name": plate_name,
                           "plate_array": self}
            return phi.update_hplate(dict_update, response, key="id")

    def table(self, headers="firstrow", **kwargs):
        """
        Transform BioPlate object to table
        
        Parameters
        ----------
        headers : str (by default "firstrow")
        kwargs : dict
            To know kwargs see `Tabulate`_
            
        _`Tabulate`: https://pypi.org/project/tabulate/#description

        Returns
        -------
            table : str
                outputs a nicely formatted plain-text table

        """
        return tabulate(self, headers=headers, **kwargs)
        
    def iterate(self, order="C", accumulate=True):
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
    
    def count(self, reverse=False):
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

    def to_excel(self, file_name,  sheets=['plate_representation', 'plate_data', 'plate_count'], header = True, accumulate = True, order="C",  empty="empty"):
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
        xls_file = BioPlateToExcel(file_name, sheets=sheets, header=header, accumulate=accumulate, order=order, empty=empty)
        xls_file.representation(self)
        xls_file.data(self)
        xls_file.count(self)
        xls_file.close()