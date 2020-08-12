import pandas as pd
import numpy as np
import json
import os
import re
import copy
import openpyxl as xl
import xlsxwriter
from Paper_Functions import integrated_paper_file_generator
from typing import List, Dict, Optional, Union, Tuple
from pandas.api.types import is_numeric_dtype
from FileProcessor import *

def generate_stat_file(settings):
    # load the class dictionary
    dict_info = None
    # 아래 class_dict file의 경로 넣기! TODO 이거 json에서 txt로 바꿔야하네 ㅎㅁㅎ
    with open("C:\\Users\\GLaDOS\\Documents\\SJ\\20_Summer_Break\\SunsetIntern\\FileProcessor\\class_dict.json", "r", encoding='UTF-8') as dictfile:
        dict_info = json.load(dictfile)

    if settings["result_type"] == "PAPER":
        paper = integrated_paper_file_generator(settings, dict_info)
        paper.generate_excel_file()