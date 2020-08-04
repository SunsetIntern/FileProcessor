# import libraries and functions
import json
from FileProcessor import *

if __name__ == "__main__":
    # load the file settings
    file_info = None
    with open("settings.json", "r", encoding="UTF-8") as settings :
        file_info = json.load(settings)

    # print(file_info)

    file_path = file_info["folder_path"] + "\\" + file_info["file_name"]
    sheet_name = file_info["sheet_name"]

    # test load_data
    df = load_data(file_path, sheet_name)
    print(df)