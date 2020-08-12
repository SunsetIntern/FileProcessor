import pandas as pd
import numpy as np
import json
import os
import re
import copy
import openpyxl as xl
import xlsxwriter
from paper_functions import integrated_paper_file_generator
from Patent_Functions import integrated_patent_file_generator
from typing import List, Dict, Optional, Union, Tuple
from pandas.api.types import is_numeric_dtype
from FileProcessor import *

def convert_text_to_dictionary(text_file):
    code_to_codeName_dictionary = {}
    while True:
        line = text_file.readline()

        if not line:
            break

        if line[-1] == '\n':
            line = line[:-1]

        split_line = line.split(" ")
        
        code = split_line[0]

        if len(split_line) == 2:            # CODE_NAME에 공백이 없는 경우
            code_name = split_line[1]
        else:                                 # CODE_NAME에 공백이 포함된 경우
            code_name = ""
            for i in range(1, len(split_line)):
                code_name += split_line[i]

        code_to_codeName_dictionary[code] = code_name

    text_file.close()
    return code_to_codeName_dictionary
    

def generate_stat_file(settings):
    text_file = open("CODE별 CODE_NAME.txt", "r", encoding='UTF-8')
    dict_info = convert_text_to_dictionary(text_file)

    if settings["result_type"] == "PAPER":
        paper = integrated_paper_file_generator(settings, dict_info)
        paper.generate_excel_file()
    else:
        patent = integrated_patent_file_generator(settings, dict_info)
        patent.generate_excel_file()