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

        Returns
        -------

        """
        return type(self).__name__         
                
    def _args_analyse(self, *args):
        """

        Parameters
        ----------
        args

        Returns
        -------

        """
        #add_value, add_row_value, add_column_value
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
           

    #def add_value(self, *args):
        """
        add a value to one given well position (eg : 'A1', 'test 1')
        
        :param str well: 'A1' => On row A in column 1 add a value
        :param str value: 'test 1' => value to add on selected well
        :return: np.array([[0, 1, 2, 3],
                           [A, 'test 1', 0, 0],
                           [B, 0, 0, 0]])
        """

    #def add_value_row(self, *args):
        """
        add value to a given row on a list of column (eg : 'A[2,3]', 'test 2')
        
        :param wells: 'A[2,3]' => On row A add value from column 2 to 3 included
        :param value: 'test 2' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 2', 'test 2'],
                           [B, 0, 0, 0]])
        """

    #def add_value_column(self, *args):
        """
        addvalue to a given column on a list of row (eg : '2[A-B]', 'test 3')
        
        :param wells: '2[A-B]' => On column 2 add value from row A to B included
        :param value: 'test 3' => Value to add on selected wells
        :return: np.array([[0, 1, 2, 3],
                           [A, 0, 'test 3', 0],
                           [B, 0, 'test 3', 0]])
        """

    def add_values(self, *args):
        """

        Parameters
        ----------
        args

        Returns
        -------

        """
        """
        parse dictionaries of multiple value to add with keys are wells and values are value
        
        (eg : {'A1' : 'test 4', 'B3' : 'test 5'})
        :param values: {'A1' : 'test 4', 'B3' : 'test 5'}
        :eturn: plate
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

        Parameters
        ----------
        args

        Returns
        -------

        """
        well, value, *trash = self._args_analyse(*args)
        if isinstance(well, dict):
            self.add_values(*args)
            return self
        self._eval_well_value(well, value)
        return self

    def _eval_well(self, well, value=None):
        """

        Parameters
        ----------
        well
        value

        Returns
        -------

        """
        """
        well = ("All", "R", 2) => self[:,well[2]]
        well = ("All", "C", 2) => self[well[2]]
        well = ("R", 2, 6, 4) => self[well[1]:well[2], well[3]]
        well = ("C", 2, 6, 8) => self[well[1],well[2]: well[3]]
        well = [("C", 2, 8, 13), ("C", 3, 8, 13), ("C", 4, 8, 13)] => self[well[0][1]:well[-1][1] + 1, well[0][2] :well[0][3]]
        well =  [("R", 5, 8, 6), ("R", 5, 8, 7), ("C", 5, 8, 8)] => self[well[0][1]:well[0][2],well[0][3]:well[-1][3] +1]
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

        Parameters
        ----------
        well
        value

        Returns
        -------

        """
        well = BioPlateMatrix(well)
        if isinstance(well, list):
            if len(well) == len(value):
                for w, v in zip(well, value):             
                    self._eval_well(w,v)
            elif len(well) != len(value):
                raise ValueError(f"missmatch between wells ({len(well)}) and values ({len(value)})")
        else:           
            self._eval_well(well, value)

    def get(self, *well):
        """

        Parameters
        ----------
        well

        Returns
        -------

        """
        if len(well) > 1:
            test = lambda x : list(x) if not isinstance(x, str) else x
            return list(map(test, list(map(self._eval_well, map(BioPlateMatrix, well)))))
        else:
            return self._eval_well(BioPlateMatrix(well[0]))

    def save(self, plate_name, **kwargs):
        """

        Parameters
        ----------
        plate_name
        kwargs

        Returns
        -------

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

    def table(self, headers="firstrow", *args, **kwargs):
        """

        Parameters
        ----------
        headers
        args
        kwargs

        Returns
        -------

        """
        """
        return a tabulate object of plate.array
        
        :param plate: numpy.array of a plate object
        :param kwargs: keys arguments use by tabulate function
        :return:
        """
        if not args:
            return tabulate(self, headers=headers, **kwargs)
        
    def iterate(self, order="C", accumulate=True):
        """

        Parameters
        ----------
        order
        accumulate

        Returns
        -------

        """
        yield from BioPlateIterate(self, order=order, accumulate=accumulate)
    
    def count(self, reverse=False):
        """

        Parameters
        ----------
        reverse

        Returns
        -------

        """
        return BioPlateCount(self, reverse=reverse)

    def to_excel(self, file_name,  sheets=['plate_representation', 'plate_data', 'plate_count'], header = True, accumulate = True, order="C",  empty="empty"):
        """

        Parameters
        ----------
        file_name
        sheets
        header
        accumulate
        order
        empty

        Returns
        -------

        """
        from BioPlate.writer.to_excel import BioPlateToExcel
        xls_file = BioPlateToExcel(file_name, sheets=sheets, header=header, accumulate=accumulate, order=order, empty=empty)
        xls_file.representation(self)
        xls_file.data(self)
        xls_file.count(self)
        xls_file.close()