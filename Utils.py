import os, json
import tkinter
from tkinter import filedialog
import re
from typing import List, Dict, Tuple
from Final import *
from Constants import *

def load_json(fname):
    with open(fname, encoding="utf-8-sig") as f:
        json_obj = json.load(f)

    return json_obj


def write_json(data, fname):
    def _conv(o):
        if isinstance(o, (np.int64, np.int32)):
            return int(o)
        raise TypeError

    with open(fname, "w", encoding="utf-8") as f:
        json_str = json.dumps(data, ensure_ascii=False, default=_conv)
        f.write(json_str)

    return f


def load_file(fileSettings, listbox):
    filenames = list(filedialog.askopenfilenames(initialdir="/", title="Select file"))
    for filename in filenames:
        if filename not in fileSettings.loaded_file_abspaths:
            listbox.insert(fileSettings.loaded_file_nums, filename)
            fileSettings.loaded_file_nums += 1
            fileSettings.loaded_file_abspaths.append(filename)


def choose_savepath(fileSettings, label):
    dir = os.path.abspath(filedialog.askdirectory())
    fileSettings.result_saving_abspath = dir
    label.config(text=f'      {dir}      ')


def clearLoadedFiles(fileSettings, listbox):
    listbox.delete(0, fileSettings.loaded_file_nums - 1)
    fileSettings.loaded_file_nums = 0
    fileSettings.loaded_file_abspaths = []
    

def generateStatFile(fileSettings, year_from_combobox, year_until_combobox, limit_combobox, progressbar):
    if fileSettings.loaded_file_nums == 0:  return
    progressbar.start(50)
    year_from = year_from_combobox.get()
    year_until = year_until_combobox.get()
    limit = limit_combobox.get()

    fileSettings.year_from = year_from
    fileSettings.year_until = year_until
    fileSettings.TPN_PAN_limit = limit
    
    jsonFilepath = f'{fileSettings.result_saving_abspath}\\{fileSettings.result_type}_result_settings.json'
    write_json(fileSettings.makeJsonObject(), jsonFilepath)
    settings = load_json(jsonFilepath)
    generate_stat_file(settings)
    progressbar.stop()


def setup_savepath_screen(frame, patentFileSettings, paperFileSettings):
    tkinter.Label(frame, text="파일저장 경로설정", font=BIG_FONT).place(x=15, y=20)
    tkinter.Label(frame, text=f'▶ 특허 통계파일 저장경로 ', font=MID_BIG_FONT).place(x=30, y=113)
    tkinter.Label(frame, text=f'▶ 논문 통계파일 저장경로 ', font=MID_BIG_FONT).place(x=30, y=283)
    
    patent_display_savepath = tkinter.Label(frame, text=f'      {DEFAULT_SAVE_PATH}      ', height=2, font=MID_FONT, borderwidth=2, relief="solid")
    patent_display_savepath.place(x=55, y=170)

    paper_display_savepath = tkinter.Label(frame, text=f'      {DEFAULT_SAVE_PATH}      ', height=2, font=MID_FONT, borderwidth=2, relief="solid")
    paper_display_savepath.place(x=55, y=340)


    tkinter.Button(frame, text="저장 경로 변경", font=SMALL_FONT, width=14, height=2, 
        command= lambda: choose_savepath(patentFileSettings, patent_display_savepath), repeatdelay=1000, repeatinterval=100).place(x=355, y=105)

    tkinter.Button(frame, text="저장 경로 변경", font=SMALL_FONT, width=14, height=2, 
        command= lambda: choose_savepath(paperFileSettings, paper_display_savepath), repeatdelay=1000, repeatinterval=100).place(x=355, y=275)

def setup_main_screen(frame, content_type, fileSettings):
    tkinter.Label(frame, text="파일 불러오기", font=BIG_FONT).place(x=5, y=5)
    tkinter.Label(frame, text="통계 파일 생성", font=BIG_FONT).place(x=5, y=300)
    tkinter.Label(frame, text="파일", font=MID_FONT).place(x=15, y=375)

    if content_type == "PATENT":
        limit_text = "PAN 임계값"
        limit_range = [i for i in range(1, PAN_LIMIT_RANGE + 1)]
    else:
        limit_text = "TPN 임계값"
        limit_range = [i for i in range(1, TPN_LIMIT_RANGE + 1)]

    tkinter.Label(frame, text=limit_text, font=MID_FONT).place(x=550, y=450)
    tkinter.Label(frame, text="년도범위지정", font=MID_FONT).place(x=15, y=450)
    tkinter.Label(frame, text="~", font=MID_BIG_FONT).place(x=316, y=450)

    scrollbar = tkinter.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    listbox = tkinter.Listbox(frame, yscrollcommand = scrollbar.set, width=125, height=14)
    listbox.place(x=0, y=50)
    scrollbar["command"] = listbox.yview

    tkinter.Button(frame, text="초기화", font=MID_FONT, width=10, height=1, 
            command=lambda: clearLoadedFiles(fileSettings, listbox), repeatdelay=1000, repeatinterval=100).place(x=630, y=5)

    tkinter.Button(frame, text="불러오기", font=MID_FONT, width=10, height=1, 
            command=lambda: load_file(fileSettings, listbox), repeatdelay=1000, repeatinterval=100).place(x=760, y=5)

    progressbar = tkinter.ttk.Progressbar(frame, maximum=100, mode="determinate", length=600, orient="horizontal")
    progressbar.place(x=90, y=380)

    limit_combobox = tkinter.ttk.Combobox(frame, font=MID_FONT, width = 10, height=15, values=limit_range)
    limit_combobox.place(x=700, y=450)
    limit_combobox.current(DEFAULT_LIMIT - 1)
    
    year_from_combobox = tkinter.ttk.Combobox(frame, font=MID_FONT, width = 10, height=15, values=YEAR_RANGE)
    year_from_combobox.place(x=165, y=450)
    year_from_combobox.current(DEFAULT_YEAR_FROM - YEAR_FROM_MIN)

    year_until_combobox = tkinter.ttk.Combobox(frame, font=MID_FONT, width = 10, height=15, values=YEAR_RANGE)
    year_until_combobox.place(x=355, y=450)
    year_until_combobox.current(DEFAULT_YEAR_UNTIL - YEAR_FROM_MIN)

    tkinter.Button(frame, text="생성", font=MID_FONT, width=10, height=1, 
            command= lambda: generateStatFile(fileSettings, year_from_combobox, year_until_combobox, limit_combobox, progressbar), repeatdelay=1000, repeatinterval=100).place(x=730, y=370)
  


class FileSettings:

    def __init__(self, resultType):
        self.result_type = resultType
        self.result_saving_abspath = DEFAULT_SAVE_PATH
        self.loaded_file_nums = 0
        self.loaded_file_abspaths = []
        self.year_from = DEFAULT_YEAR_FROM
        self.year_until = DEFAULT_YEAR_UNTIL
        self.TPN_PAN_limit = DEFAULT_LIMIT

    def makeJsonObject(self):
        data = {
            "result_type": self.result_type,
            "result_saving_abspath": self.result_saving_abspath,
            "loaded_file_nums": self.loaded_file_nums,
            "loaded_file_abspaths": self.loaded_file_abspaths,
            "year_from": self.year_from,
            "year_until": self.year_until,
            "TPN_PAN_limit": self.TPN_PAN_limit
        }
        return data