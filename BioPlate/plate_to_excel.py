import xlsxwriter
import numpy as np

from BioPlate.utilitis import dimension, dict_unique
from io import BytesIO, StringIO


class plateToExcel:
    def __init__(self, file_name, sheets=['plate_representation', 'plate_data'], test=False):
        """

        :param file_name:
        :param sheets:
        """
        self.fileName = file_name
        self.sheets = sheets
        self.last_row = 0
        self.test = test
        self.output = BytesIO() if test else None
        try:
            self.workbook = self.open_excel_file
            self.plate_rep, self.plate_data = self.select_worksheet
        except Error as e:
            print(e)

    @property
    def open_excel_file(self):
        """

        :return:
        """
        if self.test:
        	return xlsxwriter.Workbook(self.output, {'in_memory' : True})
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

    def past_values(self, plate_iterate):
        """
        past well and values in usefull way
        params:plate_iterate : list : [['A1', 'val1'], ['A2', 'val2']]
        wb : an xlswriter.worbook
        :param plate_iterate:
        :return:
        """
        worksheet = self.plate_data
        plate = np.array(plate_iterate)
        shape = plate.shape 
        self.past_values_header(shape[-1], worksheet)
        dim = dimension(plate)
        if dim:
            self.plate_xD_excel(plate, ws=worksheet, row_multi=1)
        else:
            self.plate_2D_excel(plate, ws=worksheet, row_multi=1)

    def past_values_header(self, num_columns, worksheet, hd_column_names=None):
        """

        :param num_columns:
        :param worksheet:
        :param hd_column_names:
        :return:
        """
        if not hd_column_names:
            hd_column_names = ['well', 'value']
            if num_columns > 2:
                [hd_column_names.append("value" + str(hd)) for hd in range(1, num_columns - 1)]
        elif hd_column_names:
            if len(hd_column_names) != num_columns:
                raise ValueError(
                    f"columns name lenght ({len(hd_column_names)}) different of number of columns ({num_columns})")
        worksheet.write_row(0, 0, hd_column_names)
        # return hd_column_names

    def plate_representation(self, plate, header=True, dict_infos=None, acumulate=False):
        """

        :param plate:
        :param header:
        :param dict_infos:
        :param acumulate:
        :return:
        """
        worksheet = self.plate_rep
        hd = self.workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        val = self.workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        row = 0
        dim = dimension(plate)
        if header:
            if dim:
                self.plate_xD_excel(plate, hd_format=hd)
            else:
                self.plate_2D_excel(plate, hd_format=hd)
        else:
            if dim:
                self.plate_xD_excel(plate, format=val)
            else:
                self.plate_2D_excel(plate[1:, 1:], format=val)
        if dict_infos:
            self.plate_information(dict_infos, acumulate=acumulate)

    def plate_information(self, dict_info, ws=None, acumulate=False):
        """

        :param dict_infos:
        :param ws:
        :param acumulate:
        :return:
        """
        worksheet = self.plate_rep
        multi_row = self.last_row
        if acumulate:
        	dict_infos = dict_unique(dict_info)
        else:
        	dict_infos = dict_info
        for key in dict_infos:
            if isinstance(dict_infos[key], dict):
                nested = True
                break
            else:
                nested = False
                break
        if not nested:
            heads = ['infos', 'count']
            worksheet.write_row(multi_row, 1, heads)
            multi_row += 1
            self.past_infos(dict_infos, worksheet, multi_row)
        else:
            heads = ['plate', 'infos', 'count']
            worksheet.write_row(multi_row, 1, heads)
            multi_row += 1
            for plate_num, plate_infos in dict_infos.items():
                val = self.past_infos(plate_infos, worksheet, multi_row, num_plate=plate_num)
                multi_row = val

    def past_infos(self, dicts, worksheet, initial_row, num_plate=None):
        """

        :param dicts:
        :param worksheet:
        :param initial_row:
        :param num_plate:
        :return:
        """
        x = 0
        for key in dicts.keys():
            if num_plate is not None:
                x = 1
                worksheet.write(initial_row, x, num_plate)
            worksheet.write(initial_row, 1 + x, key)
            worksheet.write(initial_row, 2 + x, dicts[key])
            initial_row += 1
        return initial_row

    def plate_2D_excel(self, plate, format=None, hd_format=None, ws=None, row_multi=0):
        """

        :param plate:
        :param format:
        :param hd_format:
        :param ws:
        :param row_multi:
        :return:
        """
        worksheet = self.plate_rep if not ws else ws
        for row, value in enumerate(plate):
            worksheet.write_row(row + row_multi, 0, value, format)
        if hd_format:
            self.header_format(hd_format, 0)
        self.last_row = row + row_multi + 2
        return row + row_multi

    def plate_xD_excel(self, plates, format=None, hd_format=None, ws=None, row_multi=0):
        """

        :param plates:
        :param format:
        :param hd_format:
        :param ws:
        :param row_multi:
        :return:
        """
        worksheet = self.plate_rep if not ws else ws
        newline = 1 if not ws else 0
        for plate in plates:
            if hd_format:
                self.header_format(hd_format, row_multi)
            else:
                if not hd_format and not ws:
                    plate = plate[1:, 1:]
            for row, value in enumerate(plate):
                row = row + row_multi
                worksheet.write_row(row, 0, value, format)
            row_multi += len(plate) + newline
        self.last_row = row_multi
        return row_multi

    def header_format(self, format, row):
        """

        :param format:
        :param row:
        :return:
        """
        self.plate_rep.set_row(row, None, format)
        self.plate_rep.set_column(0, 0, None, format)
