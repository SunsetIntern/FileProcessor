import pandas as pd
import numpy as np
import json
import os
import re
import copy
import openpyxl as xl
import xlsxwriter
from typing import List, Dict, Optional, Union, Tuple
from pandas.api.types import is_numeric_dtype

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

	# coloring the tabs
	notebook = xl.load_workbook(filepath)
	small_yearly = notebook['소분류 년도별']
	small_yearly.sheet_properties.tabColor = '000000'
	mid_yearly = notebook['중분류 년도별']
	mid_yearly.sheet_properties.tabColor = '000000'
	large_yearly = notebook['대분류 년도별']
	large_yearly.sheet_properties.tabColor = '000000'
	institution_small = notebook['소분류 업체 전체 통합']
	institution_small.sheet_properties.tabColor = '00B0F0'
	institution_mid = notebook['중분류 업체 전체 통합']
	institution_mid.sheet_properties.tabColor = '00B0F0'
	notebook.save(filepath)

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


def load_data(filepath:str, sheetName:str, year_from:int, year_until:int) -> pd.DataFrame:
	df = pd.read_excel(filepath, sheetName)
	col_list = df.columns.tolist()
	for c in col_list:
		if '_' in c:
			year = "20" + str(c.split('_')[1])
			if int(year) >= year_from and int(year) <= year_until:
				continue
			else:
				df = df.drop(c, axis = 1)
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

def to_upper_code_class(code:str, sep:str):
	# get substr (upper class code of the given code) by the input sep
	location = code.find(sep)
	return code[:location]

def generate_sheet_merged_by_class(df_ori:pd.DataFrame, class_size:str):
	df = copy.deepcopy(df_ori)
	sep = None
	if class_size == 'mid':
		sep = "C"
	elif class_size == 'large':
		sep = "B"
	else:
		return
	df['CODE'] = df['CODE'].apply(lambda x: to_upper_code_class(x, sep))
	return df

def generate_sheet_codename_replaced(df_ori:pd.DataFrame, class_dictionary:dict):
	df = copy.deepcopy(df_ori)
	for i in range(len(df)):
		inputcode = df.iloc[i]['CODE']
		df.iloc[i, df.columns.get_loc("CODE_NAME")] = class_dictionary[inputcode]
	return df

def generate_index_column(df_ori:pd.DataFrame):
	"""
	input pd.DataFrame (ex) TCN_00 | TPN_00 | ...)
	return pd.DataFrame with index columns (ex) TCN_00 | TCI_00 | TPN_00 | TPI_00 ...
	"""
	df = copy.deepcopy(df_ori)
	col_list = df.columns.tolist()
	new_col_list = []         # column list of the return dataframe(to rearrange the columns)

	for c in col_list:
		if not '_' in c or c == "CODE_NAME":      # CODE, CODENAME, COUNTRY, NAME, etc...
			new_col_list.append(c)
			continue
		col_type = c.split('_')[0]
		col_year = c.split('_')[1]
		new_col = col_type[:2] + "I_" + col_year
		max_value = df[c].max()
		df[new_col] = df[c] / max_value
		new_col_list.extend([c, new_col])
	df_rearranged = df[new_col_list]
	return df_rearranged

def delete_indices(df_ori:pd.DataFrame):
	df = copy.deepcopy(df_ori)
	col_list = df.columns.tolist()
	for c in col_list:
		if c.split('_')[0][-1] == "I":
			col_list.remove(c)
	return df[col_list]

def compute_sum_for_property(df_ori:pd.DataFrame, property:str):
	""" TODO if name is empty, the value should be NaN instead of 0 """
	df = copy.deepcopy(df_ori)
	df_sum = df.groupby(by=property, axis=0, as_index = False).sum()
	original_col = df.columns.tolist()
	missing_col = []
	for c in original_col:
		if is_numeric_dtype(df[c]):
			continue
		elif c == property:
			continue
		else:
			missing_col.append(c)
	for c in missing_col:
		missing_val = df[c].unique()
		if len(missing_val) != 1:
			missing_pairs = {}
			for i in range(len(df)):
				key = df.iloc[i, df.columns.get_loc(property)]
				if key not in missing_pairs:
					missing_pairs[key] = df.iloc[i, df.columns.get_loc(c)]
			df_sum.insert(0, c, "")
			for i in range(len(df_sum)):
				df_sum.iloc[i, df_sum.columns.get_loc(c)] = missing_pairs[df_sum.iloc[i, df_sum.columns.get_loc(property)]]
		else:
			df_sum.insert(0, c, missing_val[0])
	df_rearranged = df_sum[original_col]
	for c in ['CODE', 'CODE_NAME', 'COUNTRY', 'NAME']:
		if df_rearranged.iloc[0, df_rearranged.columns.get_loc(c)] == 0:
			df_rearranged = df_rearranged.astype({c: 'str'})
			df_rearranged[c].replace(['0', '0.0'], '', inplace=True)
	return df_rearranged

def concat_dataframes(dflist:list):
	return pd.concat(dflist)

def drop_row_by(df_ori:pd.DataFrame, column_name:str, threshold:int):
	df = copy.deepcopy(df_ori)
	col_list = df.columns.tolist()
	df.insert(0, 'summation', 0)
	for c in col_list:
		if c.split('_')[0] == column_name:
			df['summation'] = df['summation'] + df[c]
	df = df.drop(df[df.summation < threshold].index)
	return df[col_list]