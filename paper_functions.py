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
from FileProcessor import *

class integrated_paper_file_generator:
    settings = None       # json file settings, json ptr
    generated_dflist = []
    generated_namelist = []
    class_dict = None

    def __init__(self, settings, class_dict):
        self.settings = settings
        self.class_dict = class_dict
    
    def find_mid_class(self, filepath:str, position:int) -> str:
        """filepath의 file이 어떤 중분류의 file인지 중분류를 return"""
        regex = re.compile(r'A\d+B\d+')
        matchobj = regex.findall(filepath)
        return matchobj[position] # 파일 경로 상에 중분류와 형식이 들어맞는 string이 있을 수 있으므로 가장 마지막으로 탐지된 형태, 즉 파일명에서 추출

    def mid_class_grouping(self, filepaths:list):
        mid_class_to_filepath = {}
        for filepath in filepaths:
            mid_class = self.find_mid_class(filepath, -1)
            if mid_class not in mid_class_to_filepath:
                mid_class_to_filepath[mid_class] = [filepath]
            else:
                mid_class_to_filepath[mid_class].append(filepath)
        return mid_class_to_filepath

    def append_to_lists(self, result:pd.DataFrame, sheet_name:str):
        self.generated_dflist.append(result)
        self.generated_namelist.append(sheet_name)
        return
    
    def generate_excel_file_name(self, loaded_abspaths:list):
        large_class = to_upper_code_class(self.generated_namelist[0], "B")
        prefix = None
        if '누적' in loaded_abspaths[0].split('_')[-1]:
          prefix = 'TB'
        else:
          prefix = 'TA'
        return prefix + "_" + large_class + ".xlsx"

    def generate_excel_file(self):
        path_list = self.settings["loaded_file_abspaths"]
        abspaths = self.mid_class_grouping(path_list)
        self.generate_sheet_1(abspaths)
        self.generate_sheet_2(abspaths)
        self.generate_sheet_3("COUNTRY")
        self.generate_sheet_4("NAME")
        self.generate_sheet_5(abspaths)
        self.generate_sheet_6()
        self.generate_sheet_19()
        self.generate_sheet_20()
        self.generate_sheet_21()
        self.generate_sheet_22()
        self.generate_sheet_23()
        self.generate_sheet_24()
        self.generate_sheet_25()
        self.generate_sheet_26()
        self.generate_sheet_27()
        self.generated_dflist, self.generated_namelist = self.rearrange_sheets(self.generated_dflist, self.generated_namelist)
        saving_filepath = self.settings["result_saving_abspath"] + self.generate_excel_file_name(path_list)
        if not os.path.isdir(self.settings["result_saving_abspath"]):
            os.mkdir(self.settings["result_saving_abspath"])
        create_file(saving_filepath, self.generated_namelist, self.generated_dflist)
        return

    #abspaths = mid_class_grouping(self.settings[loaded_file_abspaths])
    def generate_sheet_1(self, abspaths:dict):
        # for each mid_class in abspaths
        for mid_class in abspaths:
            dflist_country = []
            for f in abspaths[mid_class]:
                data = load_data(f, '국가 자료', self.settings['year_from'], self.settings['year_until'])
                data.rename(columns = {'CODENAME':'CODE_NAME'}, inplace = True)
                data_indexed = generate_index_column(data)
                dflist_country.append(data_indexed)
            df_country = concat_dataframes(dflist_country)
            filename = mid_class + " 국가"
            self.append_to_lists(df_country, filename)
        return

    def generate_sheet_2(self, abspaths:dict):
        for mid_class in abspaths:
            dflist_institution = []
            for f in abspaths[mid_class]:
                data = load_data(f, '기관 자료', self.settings['year_from'], self.settings['year_until'])
                data.rename(columns = {'CODENAME':'CODE_NAME'}, inplace = True)
                data_indexed = generate_index_column(data)
                dflist_institution.append(data_indexed)
            df_institution = concat_dataframes(dflist_institution)
            result = drop_row_by(df_institution, 'TPN', self.settings["TPN_PAN_limit"])
            filename = mid_class + " 업체"
            self.append_to_lists(result, filename)
        return

    def generate_sheet_3(self, property:str):
        for name in self.generated_namelist:
            if name.split(" ")[-1] == '국가':
                df_country = self.generated_dflist[self.generated_namelist.index(name)]
                df_country_no_ind = delete_indices(df_country)
                df_country_sum = compute_sum_for_property(df_country_no_ind, property)
                df_country_mid = generate_sheet_merged_by_class(df_country_sum, 'mid')
                df_country_mid_codename_replaced = generate_sheet_codename_replaced(df_country_mid, self.class_dict)
                result = generate_index_column(df_country_mid_codename_replaced)
                filename = name.replace("국가", "국가 년도별")
                self.append_to_lists(result, filename)
        return

    def generate_sheet_4(self, property:str):
        for name in self.generated_namelist:
            if name.split(" ")[-1] == '업체':
                df_institution = self.generated_dflist[self.generated_namelist.index(name)]
                df_institution_no_ind = delete_indices(df_institution)
                df_institution_sum = compute_sum_for_property(df_institution_no_ind, property)
                df_institution_mid = generate_sheet_merged_by_class(df_institution_sum, 'mid')
                df_institution_mid_codename_replaced = generate_sheet_codename_replaced(df_institution_mid, self.class_dict)
                result = generate_index_column(df_institution_mid_codename_replaced)
                filename = name.replace("업체", "업체 년도별")
                self.append_to_lists(result, filename)
        return
    
    def generate_sheet_5(self, abspaths:dict):
        for mid_class in abspaths:
            dflist_yearly = []
            for f in abspaths[mid_class]:
                data = load_data(f, '년도별 자료', self.settings['year_from'], self.settings['year_until'])
                data.rename(columns = {'CODENAME':'CODE_NAME'}, inplace = True)
                dflist_yearly.append(data)
            df_yearly = concat_dataframes(dflist_yearly)
            result = generate_index_column(df_yearly)
            filename = mid_class + " 소분류 년도별 통합"
            self.append_to_lists(result, filename)
        return

    def generate_sheet_6(self):
        for name in self.generated_namelist:
            if "소분류 년도별 통합" in name:
                df_yearly_mid = generate_sheet_merged_by_class(self.generated_dflist[self.generated_namelist.index(name)], 'mid')
                df_yearly_mid_codename_replaced = generate_sheet_codename_replaced(df_yearly_mid, self.class_dict)
                df_yearly_sum = compute_sum_for_property(df_yearly_mid_codename_replaced, "CODE")
                df_yearly_sum_no_ind = delete_indices(df_yearly_sum)
                filename = name.split(" ")[0] + " 중분류 년도별 통합"
                self.append_to_lists(df_yearly_sum_no_ind, filename)
        return

    def generate_sheet_19(self):
        df_yearly_list = []
        for name in self.generated_namelist:
            if "소분류 년도별 통합" in name:
                temp = self.generated_dflist[self.generated_namelist.index(name)]
                df_yearly = delete_indices(temp)
                df_yearly_list.append(df_yearly)
        df_yearly_concat = concat_dataframes(df_yearly_list)
        df = generate_index_column(df_yearly_concat)
        filename = "소분류 년도별"
        self.append_to_lists(df, filename)
        return
    
    def generate_sheet_20(self):
        df_yearly_list = []
        for name in self.generated_namelist:
            if "중분류 년도별 통합" in name:
                temp = self.generated_dflist[self.generated_namelist.index(name)]
                df_yearly = delete_indices(temp)
                df_yearly_list.append(df_yearly)
        df_yearly_concat = concat_dataframes(df_yearly_list)
        df = generate_index_column(df_yearly_concat)
        filename = "중분류 년도별"
        self.append_to_lists(df, filename)
        return
    
    def generate_sheet_21(self):
        temp = self.generated_dflist[self.generated_namelist.index("중분류 년도별")]
        df_yearly_large = generate_sheet_merged_by_class(temp, 'large')
        df_yearly_large_codename_replaced = generate_sheet_codename_replaced(df_yearly_large, self.class_dict) # TODO
        df_yearly_large_sum = compute_sum_for_property(df_yearly_large_codename_replaced, "CODE")
        df_yearly_no_ind = delete_indices(df_yearly_large_sum)
        filename = "대분류 년도별"
        self.append_to_lists(df_yearly_no_ind, filename)
        return
    
    def generate_sheet_22(self):
        df_institution_list = []
        for name in self.generated_namelist:
            if name.split(" ")[-1] == '업체':
                temp = self.generated_dflist[self.generated_namelist.index(name)]
                df_institution_list.append(temp)
        df_institution_concat = concat_dataframes(df_institution_list)
        filename = "소분류 업체 전체 통합"
        self.append_to_lists(df_institution_concat, filename)
        return
    
    def generate_sheet_23(self):
        df_institution_list = []
        for name in self.generated_namelist:
            if "업체 년도별" in name and "통합" not in name:
                temp = self.generated_dflist[self.generated_namelist.index(name)]
                df_institution_list.append(temp)
        df_institution_concat = concat_dataframes(df_institution_list)
        filename = "중분류 업체 전체 통합"
        self.append_to_lists(df_institution_concat, filename)
        return
    
    def generate_sheet_24(self):
        temp = self.generated_dflist[self.generated_namelist.index("중분류 업체 전체 통합")]
        df_total_large = generate_sheet_merged_by_class(temp, 'large')
        df_large_codename_replaced = generate_sheet_codename_replaced(df_total_large, self.class_dict) # TODO
        df_large_sum = compute_sum_for_property(df_large_codename_replaced, "NAME")
        # df_large_codename = generate_sheet_codename_replaced(df_large, class_dict) # TODO
        # df_large_sum = compute_sum_for_property(df_large_codename, 'COUNTRY')
        df_large_no_ind = delete_indices(df_large_sum)
        result = generate_index_column(df_large_no_ind)
        filename = "대분류 업체"
        self.append_to_lists(result, filename)
        return
    
    def generate_sheet_25(self):
        df_country_list = []
        for name in self.generated_namelist:
            if name.split(" ")[-1] == '국가':
                temp = self.generated_dflist[self.generated_namelist.index(name)]
                df_country_list.append(temp)
        df_country_concat = concat_dataframes(df_country_list)
        filename = "소분류 국가 전체 통합"
        self.append_to_lists(df_country_concat, filename)
        return
    
    def generate_sheet_26(self):
        df_country_list = []
        for name in self.generated_namelist:
            if "국가 년도별" in name and "통합" not in name:
                temp = self.generated_dflist[self.generated_namelist.index(name)]
                df_country_list.append(temp)
        df_country_concat = concat_dataframes(df_country_list)
        filename = "중분류 국가 전체 통합"
        self.append_to_lists(df_country_concat, filename)
        return
    
    def generate_sheet_27(self):
        temp = self.generated_dflist[self.generated_namelist.index("중분류 국가 전체 통합")]
        df_large = generate_sheet_merged_by_class(temp, 'large')
        df_large_codename_replaced = generate_sheet_codename_replaced(df_large, self.class_dict) # TODO
        df_large_sum = compute_sum_for_property(df_large_codename_replaced, 'COUNTRY')
        df_large_no_ind = delete_indices(df_large_sum)
        result = generate_index_column(df_large_no_ind)
        filename = "대분류 국가"
        self.append_to_lists(result, filename)
        return

    def rearrange_sheets(self, df_list:list, sheet_names:list):
        result_name = []
        result_df = []
        ingredient_name = copy.deepcopy(self.generated_namelist)
        ingredient_df = copy.deepcopy(self.generated_dflist)

        suffixes = ['국가', '업체', '국가 년도별', '업체 년도별', '소분류 년도별 통합', '중분류 년도별 통합']
        missing_names = ['소분류 년도별', '중분류 년도별', '대분류 년도별',
                         '소분류 업체 전체 통합', '중분류 업체 전체 통합', '대분류 업체',
                         '소분류 국가 전체 통합', '중분류 국가 전체 통합', '대분류 국가']

        keys = list(self.mid_class_grouping(self.settings['loaded_file_abspaths']).keys())
        # create result_name
        for d in keys:
            for s in suffixes:
                name = d + " " + s
                result_name.append(name)
        result_name.extend(missing_names)

        for n in result_name:
            index = ingredient_name.index(n)
            result_df.append(ingredient_df[index])
            del ingredient_name[index]
            del ingredient_df[index]
        return result_df, result_name