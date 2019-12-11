



class Set:

    def __init__(self, bioplate, *elements, merge=False):
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
        self.bioplate = bioplate
        self.well, self.value = self._args_analyse(*elements)
        self.merge = merge


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