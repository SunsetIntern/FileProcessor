import pandas as pd
import numpy as np
import os
import openpyxl
from typing import List, Optional, Union, Tuple

# Write Code Below
# Index Order: follow raw data order

def create_file(filepath:str, sheetNames:List[str], dataFrames:List[pd.DataFrame]) -> None:
	""" < Precondition >
	The order of the sheetname in {sheetNames} and it's corresponding dataframe in {dataFrames} should be the same.
	i.e. sheetNames[i] will be written with dataFrames[i].
	"""
	writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
	assert len(sheetNames) == len(dataFrames)
	for i in range(len(sheetNames)):
		dataFrames[i].to_excel(writer, index=False, sheet_name=sheetNames[i])
	writer.close()


def write_column(df:pd.DataFrame, columnName:str, content:Union[List, np.ndarray]) -> pd.DataFrame:
	""" 가장 오른쪽 위치에 {columnName}이라는 이름을 가진 column을 추가함. Then returns the updated dataframe.
	"""
	assert len(content) == len(df)             # check if length of content == num of rows
	df[columnName] = content
	return df


def write_row(df:pd.DataFrame, rowName:str, content:Union[List, np.ndarray]) -> pd.DataFrame:
	""" 가장 아래줄에 {rowName}이라는 이름을 가진 row를 추가함. Then returns the updated dataframe.
	"""
	assert len(content) == len(df.columns)     # check if length of content == num of columns
	df.loc[rowName] = content
	return df


def load_data(filepath:str, sheetName:str) -> pd.DataFrame:
	df = pd.read_excel(filepath, sheetName)
	return df


def extract_column(df:pd.DataFrame, columnName:str, isPan:bool, limit=30) -> Tuple[str, np.ndarray]:
	""" Extracts column {columnName} from dataframe {df}.
	If isPan = true, truncate the column at the {limit}'s element. Since this limit value can be changed, refer this value from json file.
	"""
	extracted_series = df[columnName]
	num_elements = len(extracted_series)
	if isPan:
		num_elements = limit
	content = np.array([extracted_series[i] for i in range(num_elements)])
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

def compute_sum_for_property(df:pd.DataFrame, property:str):
	# outputs tuple (property, property_name, )
	# output = {'NL' : {pcn: 3, pfn: 3}, 'AN' : {pcn: 3, pfn: 3}}
	return


