#################
from os import getcwd
from os.path import isfile
from pyttsx3 import init
import tkinter.messagebox
import tkinter.simpledialog
import pyaudio

INPUT = input  # 后面会重载input函数,在此先做备份
EXIT = exit  # 同理

FAVORITE_NUM = 10  # 推荐的书的本数

data_path = fr"{getcwd()}\data.xlsx"  # Excel存放路径
work_book = ["用户","书","借阅记录"]  # 工作表
work_book_cnt = len(work_book)  # 工作表个数
work_book_head = [["姓名", "性别", "年龄", "ID", "信息障碍", "注册时间", "是否为管理员", "身份证"],
                  ["书名", "类型", "ISBN", "添加时间", "ID", "借阅次数", "馆内现有", "正在借阅", "图书馆拥有的总数"],
                  ["借出时间", "归还时间", "借书人姓名", "借书人id", "借出书名", "书籍id"]]

FIRST_RUN = not isfile(data_path)

READ = 0
WRITE = 1
DELETE = 2

SAMPLERATE = 16000  # 样本
CHANNELS = 1  # 通道
BITDEPTH = pyaudio.paInt16  # 位深
BUFSIZE = 1052  # 一次处理的样本

sayer = init()
def say(s):
    """朗读文本"""
    sayer.say(s)
    sayer.runAndWait()

VOICE_APP_ID = "-------------------------------------------------------------------------------------"
VOICE_API_Key = "-------------------------------------------------------------------------------------"
VOICE_Secret_Key = "-------------------------------------------------------------------------------------"

APP_ID = "-------------------------------------------------------------------------------------"
API_Key = "-------------------------------------------------------------------------------------"
Secret_Key = "-------------------------------------------------------------------------------------"
Group_name = "-------------------------------------------------------------------------------------"

import voice
NUMBERS = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
SYMBOLS = [',','，','.','。']
REPLACES = [('南','男'),
            ('徐月明','徐跃鸣'),
            ('徐岳明','徐跃鸣'),
            ('学名','徐跃鸣'),
            ('逗号',','),
            ('空格',' ')]
def make(s):
    """将语音识别过后的句子进行加工"""
    for x in SYMBOLS:
        s = s.replace(x,'')  # 删去标点符号
    for x in range(len(NUMBERS)):
        s = s.replace(NUMBERS[x],str(x))  # 把中文数字转换成阿拉伯数字
    for a,to in REPLACES:
        if s == a:
            return to
    return s

def listen(s):
    """语音识别"""
    say(s+'，请在接下来5秒内正确回答')  # 输出提示语
    voice.record()
    res = voice.recognize_voice()
    if res == False:
        return False
    return make(res)

PRINT = 0
SAY = 1
WINDOW = 2
def output(info,how=PRINT):
    """输出"""
    if how == PRINT:
        print(info)
    elif how == SAY:
        print(info)
        say(info)
    elif how == WINDOW:
        print(info)
        tkinter.messagebox.showinfo('无障碍图书管理系统',f"无障碍图书管理系统提醒您:{info}")

def input(tip,how=PRINT):
    """输入"""
    if how == PRINT:
        return INPUT(tip)
    elif how == SAY:
        print(tip,end='')
        ans = listen(tip)
        print(ans)
        return ans
    elif how == WINDOW:
        print(tip,end='')
        ans = tkinter.simpledialog.askstring(title='无障碍图书管理系统',prompt=f'无障碍图书管理系统需要{tip}',initialvalue=tip)
        print(ans)
        return ans

# 信息障碍的代号和解释
INFO_BARRIERS_SEEING = ['0','阅读']
INFO_BARRIERS_LISTENING = ['1','听力']
INFO_BARRIERS_SPEAKING = ['2','说话']
INFO_BARRIERS = [INFO_BARRIERS_SEEING,
                 INFO_BARRIERS_LISTENING,
                 INFO_BARRIERS_SPEAKING]