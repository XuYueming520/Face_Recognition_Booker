import data
import face
import excel
import voice
import time as TIME

#命令行更加适合工作人员帮助读者操作，本GUI仅仅依靠读者自己完成的操作

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

import data

_script = sys.argv[0]
_location = os.path.dirname(_script)

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = 'gray40' # X11 color: #666666
_ana1color = '#c3c3c3' # Closest X11 color: 'gray76'
_ana2color = 'beige' # X11 color: #f5f5dc
_tabfg1 = 'black'
_tabfg2 = 'black'
_tabbg1 = 'grey75'
_tabbg2 = 'grey89'
_bgmode = 'light'

def should_speak(info_barriers):
    """判断用户是否需要语音指导"""
    if data.INFO_BARRIERS_SEEING[0] in info_barriers:
        return data.SAY
    return data.WINDOW

def Exit():
    ''''''
    excel.exit()
    face.exit()
    voice.exit()
    root.destroy()
    data.EXIT(0)

def show_favorite(user=None):
    ''''''
    l = []
    if type(user) != excel.Reader:
        user = log_in(False)
        if user == False:
            if len(l) < data.FAVORITE_NUM and 12 <= user <= 18:  # 中学生
                for book in excel.books:
                    if '中学生' in book.book_type:
                        l.append(book.book_name)
                    if len(l) == data.FAVORITE_NUM:
                        break
            data.output(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}',data.WINDOW)
            return

    info_barriers = user.info_barriers

    f = []
    idd = []
    for info in excel.read(excel.E_borrowing_record, excel.row_borrowing_record, excel.col_borrowing_record):
        if int(info[3]) == int(user.id):
            f += excel.Book().get_book(info[5]).book_type
            idd.append(int(info[5]))

    cnt = 0
    for book in excel.books:
        if int(book.book_id) in idd:  # 曾经借过此书
            continue
        if int(book.return_num) == 0:  # 图书馆没书了
            continue
        for x in book.book_type:
            if x in f:
                l.append(book.book_name)
                cnt += 1
                if cnt == data.FAVORITE_NUM:
                    data.output(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}', should_speak(info_barriers))
                    return
                break

    if len(l) != 0:
        if len(l) < data.FAVORITE_NUM and 12 <= user.age <= 18:  # 中学生
            for book in excel.books:
                if '中学生' in book.book_type:
                    l.append(book.book_name)
                if len(l) == data.FAVORITE_NUM:
                    break
        data.output(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}', should_speak(info_barriers))

def log_in(fav=True):
    '''登录 fav 是否是从推荐书籍进来的'''
    info_barriers = []
    userf, cap_screen = face.get_face()
    res = face.recognize_face(userf)

    if res == False:  # 没有注册
        if data.FIRST_RUN:  # 第一次运行
            data.output('检测到本系统为第一次运行,请先注册管理员账户!', should_speak(info_barriers))
            name = data.input('您的名字是什么>>>', should_speak(info_barriers))
            if name is None:
                return
            sex = data.input('您的性别是>>>', should_speak(info_barriers))
            if sex is None:
                return
            age = data.input('您的年龄是>>>', should_speak(info_barriers))
            if age is None:
                return
            ID = data.input('您的身份证号是>>>', should_speak(info_barriers))
            if ID is None:
                return
            # ,ID,name,sex,age,info_barriers
            user = excel.Reader().crate_user(ID, name, sex, age, info_barriers)
            user.admin = True
            user.save()
            face.add_user(userf, user.id)
            if user.flag:
                data.output('注册成功!欢迎使用读书自推送系统!', should_speak(info_barriers))
                if fav:
                    show_favorite(user)
            else:
                data.output('出了点小问题呢，清稍后再试!')
                Exit()
                return False
            return user
        have_info_barriers = data.input('请问您是否需要帮助(是/否)>>>', data.SAY)
        if have_info_barriers == '是':
            data.output('请在家属陪同下完成注册:)', data.SAY)
            for num, describe in data.INFO_BARRIERS:
                if data.input(f'请问您有{describe}障碍吗(是/否)>>>') == '是':
                    info_barriers.append(num)
        sign = data.input('您还没有注册呢,是否现在注册(是/否)>>>', should_speak(info_barriers))
        if sign == '是':
            name = data.input('您的名字是什么>>>', should_speak(info_barriers))
            if name is None:
                return
            sex = data.input('您的性别是>>>', should_speak(info_barriers))
            if sex is None:
                return
            age = data.input('您的年龄是>>>', should_speak(info_barriers))
            if age is None:
                return
            ID = data.input('您的身份证号是>>>', should_speak(info_barriers))
            if ID is None:
                return
            # ,ID,name,sex,age,info_barriers
            user = excel.Reader().crate_user(ID, name, sex, age, info_barriers)
            face.add_user(userf, user.id)
            if user.flag:
                data.output('注册成功!欢迎使用读书自推送系统!', should_speak(info_barriers))
                if fav:
                    show_favorite(user)
            else:
                data.output('出了点小问题呢，清稍后再试!', should_speak(info_barriers))
                Exit()
                return False
        else:
            age = data.input('您的年龄是>>>', should_speak(info_barriers))
            if age is None:
                return
            if fav:
                show_favorite(int(age))
            return False
    else:  # 登录
        user_id = int(res)
        #             user_id = 1668686155
        user = excel.Reader().get_user(user_id)
        if user.flag:
            info_barriers = user.info_barriers
            data.output(f'欢迎{user.name}{"(管理员)" if user.admin else ""}使用本系统!', should_speak(info_barriers))
            if fav:
                show_favorite(user)
        else:
            data.output('出了点小问题呢，清稍后再试!', should_speak(info_barriers))
            Exit()
            return False
    return user

def borrow_book():
    ''''''
    user = log_in()
    if user == False:
        data.output('请先登录!',data.WINDOW)
        return
    info_barriers = user.info_barriers
    #show_favorite(user)
    book_name = data.input('请输入您想借的书名或id>>>', should_speak(info_barriers))
    if book_name is None:
        return
    if not book_name.isnumeric():  # 书名
        flag = False
        for book in excel.books:
            if book.book_name == book_name or book.book_name == f'《{book_name}》':
                flag = True
                book_name = book.book_id
                break
        if not flag:
            data.output("请换本书再试!", should_speak(info_barriers))
            return
    # 转换成ID统一操作
    i = 1
    flag = False  # 是否借到书
    for book in excel.books:
        if int(book.book_id) == int(book_name):
            if int(book.return_num) > 0:
                flag = True
                book.borrow_cnt += 1
                book.return_num -= 1
                book.borrow_num += 1
                book.save()
                # ["借出时间", "归还时间", "借书人姓名", "借书人id", "借出书名", "书籍id"]
                excel.row_borrowing_record += 1
                excel.write(excel.E_borrowing_record, excel.row_borrowing_record, (str(TIME.ctime(TIME.time())), None, user.name, user.id, book.book_name, book.book_id))  # 借阅记录
                #                 excel.control_cell(excel.E_books, i, 5, data.WRITE, str(int(excel.control_cell(excel.E_books, i, 5, data.READ))+1))  # 借阅次数
                #                 excel.control_cell(excel.E_books, i, 6, data.WRITE, str(int(excel.control_cell(excel.E_books, i, 6, data.READ))-1))  # 馆内现有
                #                 excel.control_cell(excel.E_books, i, 7, data.WRITE, str(int(excel.control_cell(excel.E_books, i, 7, data.READ))+1))  # 正在借阅
                data.output('借书成功!', should_speak(info_barriers))
                break
            else:
                data.output(f'暂时没有{book_name}', should_speak(info_barriers))
        i += 1
    if not flag:
        data.output("请换本书再试!", should_speak(info_barriers))

def return_book():
    ''''''
    user = log_in()
    if user == False:
        data.output('请先登录!',data.WINDOW)
        return
    info_barriers = user.info_barriers
    book_name = data.input('请输入您想归还的书名或ID>>>', should_speak(info_barriers))
    if book_name is None:
        return
    if not book_name.isnumeric():  # 书名
        flag = False
        for book in excel.books:
            if book.book_name == book_name or book.book_name == f'《{book_name}》':
                flag = True
                book_name = book.book_id
                break
        if not flag:
            data.output("请换本书再试!", should_speak(info_barriers))
            return
    # 转换成ID统一操作
    # (borrow_time,return_time,borrow_name,borrow_id,book_name,book_id)
    i = 2
    flag = False
    for info in excel.read(excel.E_borrowing_record, excel.row_borrowing_record, excel.col_borrowing_record):
        if int(info[3]) == int(user.id) and str(info[1]) == 'None' and int(book_name) == int(info[5]):
            flag = True
            for book in excel.books:
                if int(book.book_id) == int(book_name):
                    book.return_num += 1
                    book.borrow_num -= 1
                    book.save()
                    break
            # 书籍
            excel.control_cell(excel.E_borrowing_record, i, 2, data.WRITE, TIME.ctime(TIME.time()))  # 归还时间
            # 借阅记录
            data.output('还书成功!', should_speak(info_barriers))
            break
        i += 1
    if flag:
        show_favorite(user)
    else:
        data.output("请换本书再试!", should_speak(info_barriers))

def search_book():
    ''''''
    user = log_in()
    if user == False:
        data.output('请先登录!',data.WINDOW)
        return
    info_barriers = user.info_barriers
    key_words = data.input('请输入您想查询的关键字>>>', data.WINDOW)
    if key_words is None:
        return
    flag = False
    if key_words.isnumeric():
        for book in excel.books:
            if int(book.book_id) == int(key_words):
                flag = True
                data.output(
                    f"书名:{book.book_name} 类型:{','.join(book.book_type)} ISBN:{int(book.book_isbn)} 添加时间:{book.add_time} ID:{int(book.book_id)} 借阅次数:{int(book.borrow_cnt)} 馆内现有:{int(book.return_num)} 正在借阅:{int(book.borrow_num)} 图书馆拥有的总数:{int(book.have_num)}",
                    should_speak(info_barriers))
                return
    if not flag:  # 关键字
        for y in key_words.split(' '):
            for book in excel.books:
                if y in book.book_type or y in book.book_name:
                    flag = True
                    data.output(
                        f"书名:{book.book_name} 类型:{','.join(book.book_type)} ISBN:{int(book.book_isbn)} 添加时间:{book.add_time} ID:{int(book.book_id)} 借阅次数:{int(book.borrow_cnt)} 馆内现有:{int(book.return_num)} 正在借阅:{int(book.borrow_num)} 图书馆拥有的总数:{int(book.have_num)}",
                        should_speak(info_barriers))
    if not flag:
        data.output('没有找到相应书籍!',should_speak(info_barriers))

class window:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x450+660+210")
        top.minsize(600, 450)
        top.maxsize(1920, 1080)
        top.resizable(1,  1)
        top.title("无障碍图书自推送系统")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.iconbitmap(r'.\icon.ico')

        self.top = top

        self.welcome = tk.Label(self.top)
        self.welcome.place(relx=0.0, rely=0.0, relheight=6/45, relwidth=1)
        self.welcome.configure(activebackground="#f9f9f9")
        self.welcome.configure(background="#d9d9d9")
        self.welcome.configure(compound='center')
        self.welcome.configure(disabledforeground="#a3a3a3")
        self.welcome.configure(font="-family {宋体} -size 30")
        self.welcome.configure(foreground="#000000")
        self.welcome.configure(highlightbackground="#d9d9d9")
        self.welcome.configure(highlightcolor="black")
        self.welcome.configure(text='''欢迎使用无障碍图书自推送系统''')

        self.about = tk.Button(self.top, command=lambda:data.output('本系统由徐跃鸣一人创作!',data.WINDOW))
        self.about.place(relx=1-49/600, rely=1-18/450, relheight=18/450, relwidth=49/600)
        self.about.configure(activebackground="beige")
        self.about.configure(activeforeground="black")
        self.about.configure(background="#d9d9d9")
        self.about.configure(compound='left')
        self.about.configure(disabledforeground="#a3a3a3")
        self.about.configure(foreground="#000000")
        self.about.configure(highlightbackground="#d9d9d9")
        self.about.configure(highlightcolor="black")
        self.about.configure(pady="0")
        self.about.configure(text='''关于作者''')

        self.borrow_book = tk.Button(self.top,command=borrow_book)
        self.borrow_book.place(relx=0.1, rely=0.2, relheight=135/450, relwidth=210/600)
        self.borrow_book.configure(activebackground="beige")
        self.borrow_book.configure(activeforeground="black")
        self.borrow_book.configure(background="#d9d9d9")
        self.borrow_book.configure(compound='left')
        self.borrow_book.configure(disabledforeground="#a3a3a3")
        self.borrow_book.configure(font="-family {楷体} -size 24 -weight bold")
        self.borrow_book.configure(foreground="#000000")
        self.borrow_book.configure(highlightbackground="#d9d9d9")
        self.borrow_book.configure(highlightcolor="black")
        self.borrow_book.configure(pady="0")
        self.borrow_book.configure(relief="groove")
        self.borrow_book.configure(text='''借书''')
        self.tooltip_font = "TkDefaultFont"
        self.borrow_book_tooltip = \
        ToolTip(self.borrow_book, self.tooltip_font, '''借阅书籍''')

        self.return_book = tk.Button(self.top,command=return_book)
        self.return_book.place(relx=0.55, rely=0.2, relheight=135/450, relwidth=210/600)
        self.return_book.configure(activebackground="beige")
        self.return_book.configure(activeforeground="black")
        self.return_book.configure(background="#d9d9d9")
        self.return_book.configure(compound='left')
        self.return_book.configure(disabledforeground="#a3a3a3")
        self.return_book.configure(font="-family {楷体} -size 24 -weight bold")
        self.return_book.configure(foreground="#000000")
        self.return_book.configure(highlightbackground="#d9d9d9")
        self.return_book.configure(highlightcolor="black")
        self.return_book.configure(pady="0")
        self.return_book.configure(relief="groove")
        self.return_book.configure(text='''还书''')
        self.tooltip_font = "TkDefaultFont"
        self.return_book_tooltip = \
        ToolTip(self.return_book, self.tooltip_font, '''归还书籍''')

        self.search = tk.Button(self.top,command=search_book)
        self.search.place(relx=0.1, rely=0.578, relheight=135/450, relwidth=210/600)
        self.search.configure(activebackground="beige")
        self.search.configure(activeforeground="black")
        self.search.configure(background="#d9d9d9")
        self.search.configure(compound='left')
        self.search.configure(disabledforeground="#a3a3a3")
        self.search.configure(font="-family {楷体} -size 24 -weight bold")
        self.search.configure(foreground="#000000")
        self.search.configure(highlightbackground="#d9d9d9")
        self.search.configure(highlightcolor="black")
        self.search.configure(pady="0")
        self.search.configure(relief="groove")
        self.search.configure(text='''查询''')
        self.tooltip_font = "TkDefaultFont"
        self.search_tooltip = \
        ToolTip(self.search, self.tooltip_font, '''查询图书馆内的书籍''')

        self.show_favorite = tk.Button(self.top,command=show_favorite)
        self.show_favorite.place(relx=0.55, rely=0.578, relheight=135/450, relwidth=210/600)
        self.show_favorite.configure(activebackground="beige")
        self.show_favorite.configure(activeforeground="black")
        self.show_favorite.configure(background="#d9d9d9")
        self.show_favorite.configure(compound='left')
        self.show_favorite.configure(disabledforeground="#a3a3a3")
        self.show_favorite.configure(font="-family {楷体} -size 24 -weight bold")
        self.show_favorite.configure(foreground="#000000")
        self.show_favorite.configure(highlightbackground="#d9d9d9")
        self.show_favorite.configure(highlightcolor="black")
        self.show_favorite.configure(pady="0")
        self.show_favorite.configure(relief="groove")
        self.show_favorite.configure(text='''推荐''')
        self.tooltip_font = "TkDefaultFont"
        self.show_favorite_tooltip = \
        ToolTip(self.show_favorite, self.tooltip_font, '''根据您的喜好推荐图书馆内的书籍''')

        self.Return = tk.Button(self.top,command=Exit)
        self.Return.place(relx=1-49/600, rely=1-18/450-28/450, relheight=28/450, relwidth=49/600)
        self.Return.configure(activebackground="beige")
        self.Return.configure(activeforeground="black")
        self.Return.configure(background="#d9d9d9")
        self.Return.configure(compound='left')
        self.Return.configure(disabledforeground="#a3a3a3")
        self.Return.configure(foreground="#000000")
        self.Return.configure(highlightbackground="#d9d9d9")
        self.Return.configure(highlightcolor="black")
        self.Return.configure(pady="0")
        self.Return.configure(relief="ridge")
        self.Return.configure(text='''退出程序''')

# Support code for Balloon Help (also called tooltips).
# derived from http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
from time import time, localtime, strftime
class ToolTip(tk.Toplevel):
    """ Provides a ToolTip widget for Tkinter. """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=0.5, follow=True):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')
    def spawn(self, event=None):
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)
    def show(self):
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
    def move(self, event):
        self.lastMotion = time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)
    def hide(self, event=None):
        self.visible = 0
        self.withdraw()
    def update(self, msg):
        self.msgVar.set(msg)
#                   End of Class ToolTip

def main():
    ''''''
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = window(_top1)
    #print('test')

    root.mainloop()

if __name__ == '__main__':
    main()