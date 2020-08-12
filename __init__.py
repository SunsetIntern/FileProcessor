# import libraries and functions
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
from Final import generate_stat_file

if __name__ == "__main__":
    # load the file settings
    file_info = None
    # 아래 settings 파일 경로 넣기!
    with open("C:\\Users\\GLaDOS\\Documents\\SJ\\20_Summer_Break\\SunsetIntern\\FileProcessor\\result_settings.json", "r", encoding='UTF-8') as readfile :
        settings = json.load(readfile)
    generate_stat_file(settings)