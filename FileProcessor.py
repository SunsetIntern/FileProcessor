# Write Code Below
# Index Order: follow raw data order

loaded_dataframe = None

def write_sheet(tobewritten_dataframe):


def write_column(sheet_number, data):
	# append column in sheet sheet_number


def write_row(sheet_number, data):
	# append row in sheet {sheet_number}


def load_data(filepath, sheet_name):
	# open file at {filepath} with sheet {sheet_name}
	# return dataframe


def extract_column(opened_file, isPan):
	# Extracts column from the opened_file
	# if isPan = true, truncate to 30
	# output = (column_name, numpy array)

# --------------- above jinhyung below sojeong ------------------------

def generate_mid_class_per_year_merged_sheet():
	# return dataframe
 	
def generate_index_column(column):
	"""
	inputs numpy array (ex) TCN array)
	returns index array (ex) TCI array)
	"""

def compute_sum_for_property(property:str):
	# outputs tuple (property, property_name, )
	# output = ('COUNTRY', 'NL', {pcn: 3, pfn: 3})