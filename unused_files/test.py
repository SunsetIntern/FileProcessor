import re
from typing import Tuple, List, Dict

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


text_f = open("CODE별 CODE_NAME.txt", "r", encoding='UTF-8')
dict_info = convert_text_to_dictionary(text_f)
print(dict_info)