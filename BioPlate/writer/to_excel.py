from io import BytesIO

import xlsxwriter

from BioPlate import BioPlate
from BioPlate.object.inserts import Inserts
from BioPlate.object.stack import Stack
from BioPlate.object.plate import Plate

class BioPlateToExcel:
    """Past BioPlate object to excel file.     
    """

    def __init__(
        self,
        file_name,
        sheets=["plate_representation", "plate_data", "plate_count"],
        header=True,
        accumulate=True,
        order="C",
        empty="empty",
        test=False,
    ):
        """This class is instentiate with parameters for excel file. BioPlate object are only pass to method.
        
        Parameters
        ----------------
        file_name: str
            name of excel file
        sheets: List[str]
            list of sheetname (default is ["plate_representation", "plate_data", "plate_count"])
        header: bool
            if header should be put
        accumulate: bool
            if plate data should be accumulate for same well or listed
        order: str, {"R", "C"}
            if iteration should be done by column or row
        empty: str
            Name of well without value 
        test : bool
            For testing purpose, return in memory object
        """
        self.fileName = file_name
        self.sheets = sheets
        self.last_row_representation = 0
        self.test = test
        self.output = BytesIO() if test else None
        self.header = header
        self.accumulate = accumulate
        self.order = order
        self.empty = empty
        try:
            self.workbook = self.open_excel_file
            self.plate_rep, self.plate_data, self.plate_count = self.select_worksheet
            self.hd_format_representation = self.workbook.add_format(
                {"bold": True, "align": "center", "valign": "vcenter"}
            )
            self.hd_format_inserts = self.workbook.add_format(
                {
                    "bold": True,
                    "font_color": "red",
                    "align": "center",
                    "valign": "vcenter",
                }
            )
        except Exception as e:
            raise e

    @property
    def open_excel_file(self):
        """Create a ``xlsxwriter Workbook`` to work with. If test is ``True`` when class is instenciate this function will return a in `memory Workbook`_.
        
        .. _memory Workbook: https://xlsxwriter.readthedocs.io/workbook.html
        .. _`xlsxwriter.Workbook`: https://xlsxwriter.readthedocs.io/workbook.html
        
        Returns
        -----------
        Workbook : `xlsxwriter.Workbook`_                
            An object to write excel file
            
         
        """
        if self.test:
            return xlsxwriter.Workbook(self.output, {"in_memory": True})
        return xlsxwriter.Workbook(self.fileName)

    @property
    def select_worksheet(self):
        """Create worksheets object for each sheets given.
        
        Returns
        -----------
        worksheets : List[xlsxwriter.worksheets]
            Return a list of `worksheets`_        
            
            .. _worksheets: https://xlsxwriter.readthedocs.io/worksheet.html#worksheet
        
        
        """
        worksheets = list()
        for sheet in self.sheets:
            ws = self.workbook.add_worksheet(sheet)
            worksheets.append(ws)
        return worksheets

    def close(self):
        """Close workbook properly        
        """
        self.workbook.close()

    def get_test(self):
        """Return list of value stocked in memory of workbook.
        
        Returns
        ---------
        values : Dict[str, List[List]]
            returns values passed to workbook as dict with sheetnames as key and value as list of values.       
        
        """
        try:
            return self.output.getvalue()
        except AttributeError:
            return None

    def __header_format_representation(self, format):
        """Function to pass header format representation to workbook object
        
        Parameters
        ---------------
        format : Dict
            Dict of format to apply to plate header following xlswriter rules
            
        """
        self.plate_rep.set_row(self.last_row_representation, None, format)
        self.plate_rep.set_column(0, 0, None, format)

    def representation(self, BPlate):
        """This function put reprenstation of BPlate depending on is type (Plate, Inserts, Stack)
        
        Parameters
        --------------
        BPlate : BioPlate
            BioPlate object to represent in spreqdsheets
            
        """
        if isinstance(BPlate, Plate):
            self._representation(BPlate)
        elif isinstance(BPlate, Stack):
            for plate in BPlate:
                if isinstance(plate, Plate):
                    self._representation(plate)
                elif isinstance(plate, Inserts):
                    self._representation_inserts(plate)
        elif isinstance(BPlate, Inserts):
            self._representation_inserts(BPlate)

    def _representation(self, plate):
        """Pass Plate representation to spreadsheet
        
        Parameters
        --------------
        plate : Plate
            Plate object to represent
            
        """
        self.__header_format_representation( self.hd_format_representation)
        plate = self.plate_split(plate)
        for row, value in enumerate(plate, self.last_row_representation):
            self.plate_rep.write_row(row, 0, value)
        self.last_row_representation += len(plate) + 1

    def _representation_inserts(self, BPlate):
        """Pass Inserts representation to spreadsheet
        
        Parameters
        --------------
        BPlate : Inserts
            Inserts object to represent
            
        """
        position = ["TOP", "BOT"]
        for pos, plate_part in zip(position, BPlate):
            rm = self.last_row_representation
            self._representation(plate_part)
            if self.header:
                self.plate_rep.write(rm, 0, pos, self.hd_format_inserts)

    def plate_split(self, plate):
        """
        Remove row and column
        """
        if self.header:
            return plate
        else:
            return plate[1:, 1:]

    def data(self, BPlate, accumulate=None, order=None, header=None):
        """
        add to worksheet plate data, well and their value in column, ordered by column or row. If accumulated, well will be writen once.
        header should be a list of column name
        """
        order = self.order if order is None else order
        accumulate = self.accumulate if accumulate is None else accumulate
        if isinstance(BPlate, Inserts) or isinstance(
            BPlate[0], Inserts
        ):
            self._data(
                BPlate, accumulate=accumulate, order=order, inserts=True, header=header
            )
        else:
            self._data(BPlate, accumulate=accumulate, order=order, header=header)

    def _data(self, BPlate, accumulate=True, order="C", header=None, inserts=False):
        for row, value in enumerate(
            BPlate.iterate(accumulate=accumulate, order=order), 1
        ):
            self.plate_data.write_row(row, 0, value)
        len_column = len(value) - 1
        if not inserts:
            hd = self.__header_data_BP(len_column, accumulate=accumulate)
        else:
            hd = self.__header_data_Inserts(len_column, accumulate=accumulate)
        head = hd if header is None else header
        self.plate_data.write_row(0, 0, head)

    def __header_data_BP(self, len_column, accumulate=True):
        hd = ["well"]
        Add = lambda n: "value" + str(n) if accumulate else "value"
        header = list(map(Add, range(len_column)))
        hd = hd + header
        return hd

    def __header_data_Inserts(self, len_column, accumulate=True):
        len_column = len_column // 2
        hd = ["well"]
        if accumulate:
            header = []
            for n in range(len_column):
                header += ["top" + str(n), "bot" + str(n)]
        else:
            header = ["top", "bot"]
        hd = hd + header
        return hd

    def count(self, BPlate):
        self._count(BPlate)

    def _count(self, BPlate):
        for row, V in self.__count(BPlate):
            self.plate_count.write_row(row, 0, V)
        self._header_count(len(V), Inserts=isinstance(BPlate, Inserts))

    def __count(self, BPlate):
        row = 0
        for keys, values in BPlate.count().items():
            if isinstance(values, dict):
                for key, value in values.items():
                    if isinstance(value, dict):
                        for k, v in value.items():
                            row += 1
                            yield row, self._count_empty([keys, key, k, v])                            
                    else:
                        row += 1
                        yield row, self._count_empty([keys, key, value])
            else:
                row += 1
                yield row, self._count_empty([keys, values])
                
    def _count_empty(self, key_list):
        """
        Evaluate if key_list is compose of empty string, if True return the empty value set when class is instantiate, otherwise return the key
        """
        return [key if key != "" else self.empty for key in key_list]

    def _header_count(self, len_header, Inserts=False):
        """
        Add to sheet appropriate columns names, depending on number of row in each row
        """
        hd = ["infos", "count"]
        if len_header == 3:
            if not Inserts:
                hd.insert(0, "plate")
            else:
                hd.insert(0, "position")
        elif len_header == 4:
            hd.insert(0, "plate")
            hd.insert(1, "position")           
        self.plate_count.write_row(0, 0, hd)
