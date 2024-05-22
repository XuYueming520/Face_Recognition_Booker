#####################
from xlwings import App #使用xlwings操作Excel
from os.path import isfile

import time
import data

app = App(visible=False,add_book=False) #visible参数控制创建文件时可见的属性
app.display_alerts = False
app.screen_updating = False
#初始化对象

def save(workbook, path=data.data_path):
    """保存工作簿"""
    workbook.save(path)

if data.FIRST_RUN:
    print(f'检测到指定数据文件({data.data_path})不存在，正在创建……')
    book = app.books.add() #创建新的Excel工作簿操作对象
    
    for i in range(data.work_book_cnt-1,-1,-1):  # 逆序
        book.sheets.add(data.work_book[i])
    # 添加工作表
    del book.sheets['Sheet1'] #此操作删除默认的工作表，不能放在新建自定义工作表之前，会报错

    for i in range(data.work_book_cnt):
        book.sheets[i].range('A1').value = data.work_book_head[i]
    #三个工作簿的表头

    save(book,data.data_path)
    print('创建完毕!')
else:  # 存在数据文件
    print('正在读取数据……')
    book = app.books.open(data.data_path)
    print('读取完毕!')

def exit():
    """退出"""
    save(book)  # 保存
    book.close()  # 关闭
    app.quit()  # 退出

def int_to_str(row,col):
    """行数、列数转换为Excel中的位置"""
    return chr(col+64)+str(row)

def control_cell(table,row,col,command,*info):
    """操作"""
    c = table.range(int_to_str(row,col))
    if command == data.READ:
        return c.value
    elif command == data.WRITE:
        c.value = info
    elif command == data.DELETE:
        c.clear()
        c.delete()
    save(book)

def read(table,row,col):
    '''读取数据'''
    res = []
    for y in range(2,row+1):
        temp = []
        for x in range(1,col+1):
            temp.append(control_cell(table,y,x,data.READ))
        res.append(temp)
    return res

def write(table,row,info):
    """写入数据"""
    for x in range(1,len(info)+1):
        control_cell(table,row,x,data.WRITE,info[x-1])
    save(book)

E_readers = book.sheets[0]
E_books = book.sheets[1]
E_borrowing_record = book.sheets[2]

row_readers = E_readers.used_range.last_cell.row
row_books = E_books.used_range.last_cell.row
row_borrowing_record = E_borrowing_record.used_range.last_cell.row

col_readers = E_readers.used_range.last_cell.column
col_books = E_books.used_range.last_cell.column
col_borrowing_record = E_borrowing_record.used_range.last_cell.column

class Book:
    """书"""
    def __init__(self):
        """初始化"""
        self.flag = False  # 表示这本书是否正常注册
        self.book_name = None

    def __str__(self):
        ''''''
        return f'<Book {self.book_name}>'

    #"书名", "类型", "ISBN", "添加时间", "ID", "借阅次数", "馆内现有", "正在借阅", "图书馆拥有的总数"
    def set_book(self,name,type,ISBN,add_time,ID,borrow_cnt,num,borrowing,have):
        ''''''
        self.add_time = add_time
        self.book_name = name
        self.book_type = type.split(',')
        self.book_isbn = ISBN
        self.book_id = ID
        self.borrow_cnt = borrow_cnt
        self.return_num = num
        self.borrow_num = borrowing
        self.have_num = have
        self.flag = True
        return self
    
    def crate_book(self,book_name,book_type,book_isbn,book_num):
        """创建书本"""
        global row_books,books
        self.add_time = time.ctime(time.time())  # 添加书本的时间
        self.book_id = int(time.time())  # 书的唯一标识符
        self.borrow_cnt = 0  # 被借阅了的次数
        self.borrow_num = 0  # 正在借走的书的个数
        self.book_name = book_name  # 书名
        self.book_type = book_type.split(',')  # 书的类型
        self.book_isbn = book_isbn  # 书的ISBN
        self.return_num = self.have_num = book_num  # 现在图书馆内有的个数,图书馆拥有的书的总数
        row_books += 1
        self.save(True)
        books.append(self)
        self.flag = True
        return self
    
    def get_book(self,book_id):
        """获取书"""
        #["书名", "类型", "ISBN", "添加时间", "ID", "借阅次数", "馆内现有", "正在借阅", "图书馆拥有的总数"]
        for book in books:
            if book.book_id == book_id:
                self.add_time = book.add_time  # 添加书本的时间
                self.book_id = book.book_id  # 书的唯一标识符
                self.borrow_cnt = book.borrow_cnt  # 被借阅了的次数
                self.borrow_num = book.borrow_num  # 正在借走的书的个数
                self.book_name = book.book_name  # 书名
                self.book_type = book.book_type  # 书的类型
                self.book_isbn = book.book_isbn  # 书的ISBN
                self.return_num = book.return_num  # 现在图书馆内有的个数
                self.have_num = book.have_num  # 图书馆拥有的书的总数
                self.flag = True  # 成功
                break
        return self
    
    def save(self,new=False):
        ''''''
        global row_books
        if new:
            write(E_books, row_books, (
                self.book_name, ','.join(self.book_type), str(self.book_isbn), str(self.add_time), str(self.book_id),
                str(self.borrow_cnt), str(self.return_num), str(self.borrow_num), str(self.have_num)))
            return
        for i in range(2,row_books+2):
            if books[i-2].book_id == self.book_id:
                write(E_books,i,(self.book_name, ','.join(self.book_type), str(self.book_isbn), str(self.add_time), str(self.book_id), str(self.borrow_cnt), str(self.return_num), str(self.borrow_num), str(self.have_num)))
                break

class Reader:
    """读者"""
    #id ID sex name age info_ admin
    def __init__(self):
        """初始化"""
        self.flag = False  # 表示用户是否为注册成功的正常用户
        self.id = None

    def __str__(self):
        ''''''
        return f'<User {self.id}>'
    
    # "姓名", "性别", "年龄", "ID", "信息障碍", "注册时间", "是否为管理员", "身份证"
    def set_user(self,name,sex,age,id,info_barriers,add_time,admin,ID):
        ''''''
        self.name = name
        self.sex = sex
        self.age = age
        self.id = id
        self.info_barriers = info_barriers
        self.add_time = add_time
        self.admin = admin
        self.ID = ID
        self.flag = True
        return self
    
    def crate_user(self,ID,name,sex,age,info_barriers):
        """创建用户"""
        global row_readers,readers
        self.add_time = time.ctime(time.time())  # 读者注册的时间
        self.id = int(time.time())  # 每个用户的唯一标识符
        self.admin = False  # 是否为管理员
        self.ID = ID  # 身份证
        self.name = name  # 姓名
        self.sex = sex  # 性别
        self.age = age  # 年龄
        self.info_barriers = info_barriers  # 信息障碍
        row_readers += 1
        self.save(True)
        readers.append(self)
        self.flag = True  # 注册成功
        return self
    
    def get_user(self,user_id):
        """获取用户"""
        # "姓名", "性别", "年龄", "ID", "信息障碍", "注册时间", "是否为管理员", "身份证"]
        for reader in readers:
            if reader.id == user_id:  # 匹配到用户
                self.add_time = reader.add_time  # 读者注册的时间
                self.id = reader.id  # 每个用户的唯一标识符
                self.admin = reader.admin  # 是否为管理员
                self.ID = reader.ID  # 身份证
                self.name = reader.name  # 姓名
                self.sex = reader.sex  # 性别
                self.age = reader.age  # 年龄
                self.info_barriers = reader.info_barriers  # 信息障碍
                self.flag = True  # 登录成功
                break
        return self
    
    def apply_to_be_admin(self):
        """申请成为管理员"""
        self.admin = True
        self.save()
    
    def remove_admin(self):
        ''''''
        self.admin = False
        self.save()
    
    def save(self,new=False):
        ''''''
        global row_readers
        if new:
            write(E_readers, row_readers, (
                self.name, self.sex, str(self.age), str(self.id), ','.join(self.info_barriers)+',', str(self.add_time),
                str(self.admin), "'" + str(self.ID)))
            return
        for i in range(2,row_readers+2):
            if readers[i-2].id == self.id:
                write(E_readers,i,(self.name, self.sex, str(self.age), str(self.id), ','.join(self.info_barriers)+',', str(self.add_time), str(self.admin), "'"+str(self.ID)))
                break

'''
读者：读者id，身份证，权限，性别，姓名，年龄，是否信息障碍……
书本：书本id(2211121557)，书名，ISBN，类型（科幻、文学……，视障/听障 需要的书），状态，（评分），借阅次数
图书管理员：读者id，身份证
'''


readers = []
if row_readers != 1:
    # "姓名", "性别", "年龄", "ID", "信息障碍", "注册时间", "是否为管理员", "身份证"
    for info in read(E_readers,row_readers,col_readers):
        readers.append(Reader().set_user(info[0],info[1],int(info[2]),int(info[3]),([] if info[4] is None else info[4].split(',')[:-1]),info[5],bool(info[6]),int(info[7])))

books = []
# print(read(E_books,row_books,col_books))
if row_books != 1:
    # "书名", "类型", "ISBN", "添加时间", "ID", "借阅次数", "馆内现有", "正在借阅", "图书馆拥有的总数"
    for info in read(E_books,row_books,col_books):
        books.append(Book().set_book(info[0],info[1],int(info[2]),info[3],int(info[4]),int(info[5]),int(info[6]),int(info[7]),int(info[8])))