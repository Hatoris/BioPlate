import xlsxwriter

from BioPlate.utilitis import dimension

class plateToExcel:
	
	def __init__(self, file_name, sheets=['plate_representation', 'plate_data']):
		"""
		file_name : path to excel file,
		sheets : list of sheets name
		"""
		self.fileName = file_name
		self.sheets = sheets
		try:
			self.workbook = self.open_excel_file
			self.plate_rep, self.plate_data = self.select_worksheet
		except Error as e:
			print(e)
	
	@property
	def open_excel_file(self):
		return  xlsxwriter.Workbook(self.fileName)
	
	@property
	def select_worksheet(self):
		worksheets = list()
		for sheet in self.sheets:
			ws = self.workbook.add_worksheet(sheet)
			worksheets.append(ws)
		return worksheets
		
	def close(self):
		self.workbook.close()
	
	def past_values(self, plate_iterate):
		"""
		past well and values in usefull way
		params:
			plate_iterate : list : [['A1', 'val1'], ['A2', 'val2']]
			wb : an xlswriter.worbook
		"""
		worksheet = self.plate_data
		row = 1
		col = 0
		worksheet.write(0, 0,   "well")
		worksheet.write(0, 1,    "value")
		for well, value in plate_iterate:
			worksheet.write(row, col,  well)
			worksheet.write(row, col + 1, value)
			row += 1

		
	def plate_representation(self, plate, header=True):
		worksheet = self.plate_rep
		hd = self.workbook.add_format({'bold': True, 'align' : 'center', 'valign' : 'vcenter'})
		val = self.workbook.add_format({'align' : 'center', 'valign' : 'vcenter'})
		row = 0
		dim = dimension(plate)
		if header:		
			if dim:
				self.plate_xD_excel(plate, hd_format=hd)
			else:
				self.plate_2D_excel(plate, hd_format =hd)
		else:
			if dim:
				self.plate_xD_excel(plate, format=val)
			else:
				self.plate_2D_excel(plate[1:,1:], format=val)
	
	def plate_2D_excel(self, plate, format=None, hd_format=None):
		"""
		
		"""
		worksheet = self.plate_rep
		for row, value in enumerate(plate):
			worksheet.write_row(row, 0, value, format)
		if hd_format:
			self.header_format(hd_format, 0)
			
			
	def plate_xD_excel(self, plates, format=None, hd_format=None):
		"""
		
		"""
		worksheet = self.plate_rep
		row_multi = 0
		for plate in plates:
			if hd_format:
				self.header_format(hd_format, row_multi)
			else:
				plate = plate[1:,1:]
			for row, value in enumerate(plate):
				row = row + row_multi
				worksheet.write_row(row, 0, value, format)
			row_multi += len(plate) + 1
	
	def header_format(self, format, row):
		"""
		
		"""
		self.plate_rep.set_row(row, None, format)
		self.plate_rep.set_column(0, 0, None, format)
