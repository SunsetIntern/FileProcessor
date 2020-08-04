import pandas as pd
import numpy as np
import os

# Write Code Below
# Index Order: follow raw data order

loaded_dataframe = None

def write_sheet(tobewritten_dataframe):
	"""
	아래 블로그: pandas 엑셀 시트별로 저장하는 방법
	https://m.blog.naver.com/PostView.nhn?blogId=kiddwannabe&logNo=221597578686&proxyReferer=https:%2F%2Fwww.google.com%2F
	"""

def write_column(sheet_number, data):
	# append column in sheet sheet_number
	return

def write_row(sheet_number, data):
	# append row in sheet {sheet_number}
	return

def load_data(filepath, sheet_name):
	"""
	소정이가 잠시 쓰려고 만든 코드
	"""
	df = pd.read_excel(filepath, sheet_name)
	return df
	# open file at {filepath} with sheet {sheet_name}
	# return dataframe


def extract_column(opened_file, isPan):
	# Extracts column from the opened_file
	# if isPan = true, truncate to 30
	# output = (column_name, numpy array)
	return

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