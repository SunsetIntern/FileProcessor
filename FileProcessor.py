import pandas as pd
import numpy as np
import os
import openpyxl
from typing import List, Optional, Union

# Write Code Below
# Index Order: follow raw data order

loaded_dataframe = None

def create_file(filepath:str, initial_sheet_name:str, initial_data:pd.DataFrame):
	writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
	initial_data.to_excel(writer, index=False, sheet_name=initial_sheet_name)
	writer.close()

def write_sheet_to_existing_file(filepath:str, sheetName:str, data:pd.DataFrame):
	workbook = openpyxl.load_workbook(filepath)
	if sheetName in workbook.sheetnames:   
		# if sheetName already exists, overwrite the sheet


	else:
		# if sheetName does not exists, create a new sheet
		writer = pd.ExcelWriter(filepath, engine = 'openpyxl')
		writer.book = workbook
		data.to_excel(writer, index=False, sheet_name = sheetName)
		writer.save()
		writer.close()


def write_column(filepath:str, sheetName:str, columnName:str, content:Union[List, np.ndarray]):
	df = load_data(filepath, sheetName)
	assert len(content) == len(df)   # check if length of content == num of rows
	df[columnName] = content
	write_sheet_to_existing_file(filepath, sheetName, df)


def write_row(filepath:str, sheetName:str, rowName:str, content:Union[List, np.ndarray]):
	df = load_data(filepath, sheetName)        # append row in sheet {sheet_number}
	assert len(content) == len(df.columns)     # check if length of content == num of columns
	df[rowName] = content
	write_sheet_to_existing_file(filepath, sheetName, df)


def load_data(filepath:str, sheetName:str):
	df = pd.read_excel(filepath, sheetName)
	return df


def extract_column(df:pd.DataFrame, columnName:str, isPan:bool, limit=30):
	# Extracts column {columnName} from the opened_file's dataframe {df}
	# if isPan = true, truncate to limit(30)
	# output = (column_name, numpy array)
	extracted_series = df[columnName]
	num_elements = len(extracted_series)
	if isPan:
		num_elements = limit
	content = np.array([extracted_series[i] for i in range(num_elements)])
	# TODO : columnName이 output이 아닌 input에 들어가야 하지 않나?
	return (columnName, content)

# --------------- above jinhyung below sojeong ------------------------

def generate_mid_class_per_year_merged_sheet():
	# return dataframe
	return

def generate_index_column(column):
	"""
	inputs numpy array (ex) TCN array)
	returns index array (ex) TCI array)
	"""
	return

def compute_sum_for_property(property:str):
	# outputs tuple (property, property_name, )
	# output = ('COUNTRY', 'NL', {pcn: 3, pfn: 3})
	return


# write_sheet(True, 'test2.xlsx', 'sheet2', pd.DataFrame({"ABCD": [1, 2, 3, 4, 5]}))
write_sheet_to_existing_file('test2.xlsx', 'sheet7', pd.DataFrame({"ABCD": [1, 2, 3, 4]}))
# write_column('test2.xlsx', 'sheet3', 'second_column', [1, 2, 3, 4, 5])

