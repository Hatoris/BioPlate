from io import BytesIO

import xlsxwriter

from BioPlate import BioPlate
from BioPlate.inserts import Inserts
from BioPlate.stack import Stack
from BioPlate.plate import Plate

class BioPlateToExcel:

    """
    past to excel in different way bioplate object
    plateToExcel.representation: 
        past a representation of a BioPlate object in excel file
    plateToExcel.data:
        past an iteration of BioPlate object in excel
    plateToExcel.count:
        past a count of each value in BioPlate object to excel           
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
        """

        :param file_name: name of excel file
        :param sheets: list of sheetname
        :param header: if header should be put
        :param accumulate: if plate data should be accumulat for same well or listed
        :param order: if iteration should be done by column or row
        :param empty:
        :param test:
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
        """

        :return:
        """
        if self.test:
            return xlsxwriter.Workbook(self.output, {"in_memory": True})
        return xlsxwriter.Workbook(self.fileName)

    @property
    def select_worksheet(self):
        """

        :return:
        """
        worksheets = list()
        for sheet in self.sheets:
            ws = self.workbook.add_worksheet(sheet)
            worksheets.append(ws)
        return worksheets

    def close(self):
        self.workbook.close()

    def get_test(self):
        try:
            return self.output.getvalue()
        except AttributeError:
            return None

    def __header_format_representation(self, format):
        """

        :param format:
        :param row:
        :return:
        """
        self.plate_rep.set_row(self.last_row_representation, None, format)
        self.plate_rep.set_column(0, 0, None, format)

    def representation(self, BPlate):
        """
        get representation of BioPlate in excel file
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
        """
        protected func, write in specified workbook
        """
        self.__header_format_representation(self.hd_format_representation)
        plate = self.plate_split(plate)
        for row, value in enumerate(plate, self.last_row_representation):
            self.plate_rep.write_row(row, 0, value)
        self.last_row_representation += len(plate) + 1

    def _representation_inserts(self, BPlate):
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
            if not isinstance(values, dict):
                keys = keys if keys != "" else self.empty
                V = [keys, values]
                row += 1
                yield row, V
            else:
                for key, value in values.items():
                    if not isinstance(value, dict):
                        key = key if key != "" else self.empty
                        V = [keys, key, value]
                        row += 1
                        yield row, V
                    else:
                        for k, v in value.items():
                            k = k if k != "" else self.empty
                            V = [keys, key, k, v]
                            row += 1
                            yield row, V

    def _header_count(self, len_header, Inserts=False):
        if len_header == 2:
            hd = ["infos", "count"]
        elif len_header == 3:
            if not Inserts:
                hd = ["plate", "infos", "count"]
            else:
                hd = ["position", "infos", "count"]
        elif len_header == 4:
            hd = ["plate", "position", "infos", "count"]
        self.plate_count.write_row(0, 0, hd)
