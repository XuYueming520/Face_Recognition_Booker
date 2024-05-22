print('正在启动程序，请耐心等待……')  # 提示信息

import data  # data要最先导入
import face
import excel
import voice
import time

def quit_program():
    """退出程序"""
    excel.exit()
    face.exit()
    voice.exit()

def should_speak(info_barriers):
    """判断用户是否需要语音指导"""
    if data.INFO_BARRIERS_SEEING[0] in info_barriers:
        return data.SAY
    return data.PRINT

info_barriers = []  # 用户的障碍

def exit(user):
    ''''''
    data.output("正在退出程序中,欢迎下次使用本程序……",should_speak(info_barriers))
    quit_program()
    data.EXIT()

def get_my_borrowing_record(user):
    '''获取用户借阅记录'''
    cnt = 0
    for (borrow_time,return_time,borrow_name,borrow_id,book_name,book_id) in excel.read(excel.E_borrowing_record,excel.row_borrowing_record,excel.col_borrowing_record):
        if int(borrow_id) == int(user.id):
            cnt += 1
            data.output(f'编号为{cnt}的借阅记录:借出时间:{borrow_time},归还时间:{"未归还" if return_time == None else return_time},书名:{book_name}',should_speak(info_barriers))
            
    if cnt > 0:
        data.output(f'您共有{cnt}条借阅记录',should_speak(info_barriers))
    else:  # 没有借阅记录或者用户没有借阅记录
        data.output('您好像还没有借过书吧……',should_speak(info_barriers))
        return False

def get_books(user):
    ''''''
#     print(excel.books)
    
    if len(excel.books) == 0:
        data.output('图书馆内暂时还没有书呢，请联系管理员添加书籍!',should_speak(info_barriers))
        return
    for book in excel.books:
        data.output(f"书名:{book.book_name} 类型:{','.join(book.book_type)} ISBN:{int(book.book_isbn)} 添加时间:{book.add_time} ID:{int(book.book_id)} 借阅次数:{int(book.borrow_cnt)} 馆内现有:{int(book.return_num)} 正在借阅:{int(book.borrow_num)} 图书馆拥有的总数:{int(book.have_num)}",should_speak(info_barriers))

def search_books(user):
    ''''''
    key_words = data.input('请输入您想查询的关键字>>>', should_speak(info_barriers))
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
        data.output('没有找到相应书籍!', should_speak(info_barriers))

def get_info_book(user):
    ''''''
    if len(excel.books) == 0:
        data.output('图书馆内暂时还没有书呢，请联系管理员添加书籍!',should_speak(info_barriers))
        return
    book_name = data.input('请输入您想查询的书名或id>>>',should_speak(info_barriers))
    if not book_name.isnumeric():  # 书名
        flag = False
        for book in excel.books:
            if book.book_name == book_name or book.book_name == f'《{book_name}》':
                flag = True
                book_name = book.book_id
                break
        if not flag:
            data.output("请换本书再试!",should_speak(info_barriers))
            return
    for book in excel.books:
        if int(book.book_id) == int(book_name):
            data.output(f"书名:{book.book_name} 类型:{','.join(book.book_type)} ISBN:{int(book.book_isbn)} 添加时间:{book.add_time} ID:{int(book.book_id)} 借阅次数:{int(book.borrow_cnt)} 馆内现有:{int(book.return_num)} 正在借阅:{int(book.borrow_num)} 图书馆拥有的总数:{int(book.have_num)}",should_speak(info_barriers))
            break

def show_favorite(user):
    ''''''
    l = []
    if type(user) != excel.Reader:
        if len(l) < data.FAVORITE_NUM and 12 <= user <= 18:  # 中学生
            for book in excel.books:
                if '中学生' in book.book_type:
                    l.append(book.book_name)
                if len(l) == data.FAVORITE_NUM:
                    break
        data.output(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}',should_speak(info_barriers))
        return
    f = []
    idd = []
    for info in excel.read(excel.E_borrowing_record,excel.row_borrowing_record,excel.col_borrowing_record):
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
                    data.output(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}',should_speak(info_barriers))
                    return
                break
    
    if len(l) != 0:
        if len(l) < data.FAVORITE_NUM and 12 <= user.age <= 18:  # 中学生
            for book in excel.books:
                if '中学生' in book.book_type:
                    l.append(book.book_name)
                if len(l) == data.FAVORITE_NUM:
                    break
        data.output(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}',should_speak(info_barriers))

def borrow(user):
    ''''''
    show_favorite(user)
    book_name = data.input('请输入您想借的书名或id>>>',should_speak(info_barriers))
    if not book_name.isnumeric():  # 书名
        flag = False
        for book in excel.books:
            if book.book_name == book_name or book.book_name == f'《{book_name}》':
                flag = True
                book_name = book.book_id
                break
        if not flag:
            data.output("请换本书再试!",should_speak(info_barriers))
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
                #["借出时间", "归还时间", "借书人姓名", "借书人id", "借出书名", "书籍id"]
                excel.row_borrowing_record += 1
                excel.write(excel.E_borrowing_record,excel.row_borrowing_record,(time.ctime(time.time()), None, user.name, user.id, book.book_name, book.book_id))  # 借阅记录
#                 excel.control_cell(excel.E_books, i, 5, data.WRITE, str(int(excel.control_cell(excel.E_books, i, 5, data.READ))+1))  # 借阅次数
#                 excel.control_cell(excel.E_books, i, 6, data.WRITE, str(int(excel.control_cell(excel.E_books, i, 6, data.READ))-1))  # 馆内现有
#                 excel.control_cell(excel.E_books, i, 7, data.WRITE, str(int(excel.control_cell(excel.E_books, i, 7, data.READ))+1))  # 正在借阅
                data.output('借书成功!',should_speak(info_barriers))
                break
            else:
                data.output(f'暂时没有{book_name}',should_speak(info_barriers))
        i += 1
    if not flag:
        data.output("请换本书再试!",should_speak(info_barriers))

def give_back(user):
    ''''''
    book_name = data.input('请输入您想归还的书名或ID>>>',should_speak(info_barriers))
    if not book_name.isnumeric():  # 书名
        flag = False
        for book in excel.books:
            if book.book_name == book_name or book.book_name == f'《{book_name}》':
                flag = True
                book_name = book.book_id
                break
        if not flag:
            data.output("请换本书再试!",should_speak(info_barriers))
            return
    # 转换成ID统一操作
    # (borrow_time,return_time,borrow_name,borrow_id,book_name,book_id)
    i = 2
    flag = False
    for info in excel.read(excel.E_borrowing_record,excel.row_borrowing_record,excel.col_borrowing_record):
        if int(info[3]) == int(user.id) and str(info[1]) == 'None' and int(book_name) == int(info[5]):
            flag = True
            for book in excel.books:
                if int(book.book_id) == int(book_name):
                    book.return_num += 1
                    book.borrow_num -= 1
                    book.save()
                    break
            # 书籍
            excel.control_cell(excel.E_borrowing_record, i, 2, data.WRITE, time.ctime(time.time()))  # 归还时间
            # 借阅记录
            data.output('还书成功!',should_speak(info_barriers))
            break
        i += 1
    if flag:
        show_favorite(user)
    else:
        data.output("请换本书再试!",should_speak(info_barriers))

def apply_to_be_Admin(user):
    ''''''
    if user.admin:
        data.output(f'{user.name},您已成为本图书馆的管理员,无需再次进行此操作',should_speak(info_barriers))
        return
    user.apply_to_be_admin()
    data.output(f'{user.name},您已成为本图书馆的管理员!',should_speak(info_barriers))

def setting(user):
    ''''''
    global info_barriers
    user.ID = data.input(f'您的身份证从{user.ID}更改为>>>',should_speak(info_barriers))
    user.name = data.input(f'您的姓名从{user.name}更改为>>>',should_speak(info_barriers))
    user.sex = data.input(f'您的性别从{user.sex}更改为>>>',should_speak(info_barriers))
    user.age = data.input(f'您的年龄从{user.age}更改为>>>',should_speak(info_barriers))
    user.info_barriers = []
    info_barriers = []
    have_info_barriers = data.input('请问您是否需要帮助(是/否)>>>',should_speak(info_barriers))
    if have_info_barriers == '是':
        for num,describe in data.INFO_BARRIERS:
            if data.input(f'请问您有{describe}障碍吗(是/否)>>>',should_speak(info_barriers)) == '是':
                user.info_barriers.append(num)
                info_barriers.append(num)
    user.save()
#     self.ID = ID  # 身份证
#     self.name = name  # 姓名
#     self.sex = sex  # 性别
#     self.age = age  # 年龄
#     self.info_barriers = info_barriers  # 信息障碍

def add_book(user):
    ''''''
    name = data.input("请输入本书的名字>>>",should_speak(info_barriers))
    type = data.input(f"请输入{name}的类型>>>",should_speak(info_barriers))
    while 1:
        isbn = data.input(f"请输入{name}的ISBN>>>",should_speak(info_barriers))
        if not isbn.isnumeric():
            data.output(f'ISBN需要为整数而不是{isbn}',should_speak(info_barriers))
        else:
            isbn = int(isbn)
            break
    while 1:
        num = data.input(f"请输入{name}的数量>>>",should_speak(info_barriers))
        if not num.isnumeric():
            data.output(f'数量需要为整数而不是{num}',should_speak(info_barriers))
        else:
            num = int(num)
            break
    #book_name,book_type,book_isbn,book_num
    excel.Book().crate_book(name,type,isbn,num)
    data.output(f"{name}添加成功!",should_speak(info_barriers))

def remove_admin(user):
    ''''''
    apply = data.input('警告:此操作将要撤销您的管理员身份,请慎重考虑(是/否)>>>',should_speak(info_barriers))
    if apply == '是':
        user.remove_admin()
        data.output(f'{user.name},已撤销您本图书馆的管理员的身份!',should_speak(info_barriers))
    else:
        data.output('操作已取消!',should_speak(info_barriers))

COMMANDS = [('0','退出程序',exit),
            ('1','查询本账号借阅记录',get_my_borrowing_record),
            ('2','查看图书馆现有书籍',get_books),
            ('3','查询书本',search_books),
            ('4','查询图书信息',get_info_book),
            ('5','借书',borrow),
            ('6','还书',give_back),
            ('7','申请成为管理员',apply_to_be_Admin),
            ('8','更改账户设置',setting)]

COMMANDS_OF_ADMIN = [('0','退出程序',exit),
                     ('1','添加书籍',add_book),
                     ('2','取消管理员',remove_admin)]

def main():
#     """主程序"""
#     try:
        global info_barriers
        userf,cap_screen = face.get_face()
        res = face.recognize_face(userf)

        if res == False:  # 没有注册
            if data.FIRST_RUN:  # 第一次运行
                data.output('检测到本系统为第一次运行,请先注册管理员账户!',should_speak(info_barriers))
                name = data.input('您的名字是什么>>>', should_speak(info_barriers))
                sex = data.input('您的性别是>>>', should_speak(info_barriers))
                age = data.input('您的年龄是>>>', should_speak(info_barriers))
                ID = data.input('您的身份证号是>>>', should_speak(info_barriers))
                # ,ID,name,sex,age,info_barriers
                user = excel.Reader().crate_user(ID, name, sex, age, info_barriers)
                user.admin = True
                user.save()
                face.add_user(userf, user.id)
                if user.flag:
                    data.output('注册成功!欢迎使用读书自推送系统!', should_speak(info_barriers))
                    show_favorite(user)
                else:
                    data.output('出了点小问题呢，清稍后再试!')
                    quit_program()
                    return
            else:
                have_info_barriers = data.input('请问您是否需要帮助(是/否)>>>',should_speak(info_barriers))
                if have_info_barriers == '是':
                    data.output('请在家属陪同下完成注册:)',data.SAY)
                    for num,describe in data.INFO_BARRIERS:
                        if data.input(f'请问您有{describe}障碍吗(是/否)>>>') == '是':
                            info_barriers.append(num)
                sign = data.input('您还没有注册呢,是否现在注册(是/否)>>>',should_speak(info_barriers))
                if sign == '是':
                    name = data.input('您的名字是什么>>>',should_speak(info_barriers))
                    sex = data.input('您的性别是>>>',should_speak(info_barriers))
                    age = data.input('您的年龄是>>>',should_speak(info_barriers))
                    ID = data.input('您的身份证号是>>>',should_speak(info_barriers))
                    #,ID,name,sex,age,info_barriers
                    user = excel.Reader().crate_user(ID,name,sex,age,info_barriers)
                    face.add_user(userf,user.id)
                    if user.flag:
                        data.output('注册成功!欢迎使用读书自推送系统!',should_speak(info_barriers))
                        show_favorite(user)
                    else:
                        data.output('出了点小问题呢，清稍后再试!',should_speak(info_barriers))
                        quit_program()
                        return
                else:
                    age = data.input('您的年龄是>>>',should_speak(info_barriers))
                    show_favorite(int(age))
                    return
        else:  # 登录
            user_id = int(res)
#             user_id = 1668686155
            user = excel.Reader().get_user(user_id)
            if user.flag:
                info_barriers = user.info_barriers
                data.output(f'欢迎{user.name}{"(管理员)" if user.admin else ""}使用本系统!',should_speak(info_barriers))
                show_favorite(user)
            else:
                data.output('出了点小问题呢，清稍后再试!',should_speak(info_barriers))
                quit_program()
                return
        
#         c = data.input(f'{data.LOGIN_EXIT}:退出,{data.LOGIN_REGISTER}:注册,{data.LOGIN_SIGN_IN}:登录>>>',data.SAY)
#         if c == data.LOGIN_EXIT:
#             quit_program()
#             return
#         elif c == data.LOGIN_REGISTER:
#             data.output('不方便的人员请在家属陪同下完成注册:)',data.SAY)
#             have_info_barriers = data.input('请问您是否存在信息障碍(是/否)>>>',should_speak(info_barriers))
#             if have_info_barriers == '是':
#                 for num,describe in data.INFO_BARRIERS:
#                     if data.input(f'请问您有{describe}障碍吗(是/否)>>>') == '是':
#                         info_barriers.append(num)
#             name = data.input('您的名字是什么>>>',should_speak(info_barriers))
#             sex = data.input('您的性别是>>>',should_speak(info_barriers))
#             age = data.input('您的年龄是>>>',should_speak(info_barriers))
#             ID = data.input('您的身份证号是>>>',should_speak(info_barriers))
#             #,ID,name,sex,age,info_barriers
#             user = excel.Reader().crate_user(ID,name,sex,age,info_barriers)
#             face.add_user(userf,user.id)
#             if user.flag:
#                 data.output('注册成功!欢迎使用读书自推送系统!',should_speak(info_barriers))
#             else:
#                 data.output('出了点小问题呢，清稍后再试!')
#                 quit_program()
#                 return
#         elif c == data.LOGIN_SIGN_IN:
#             user_id = int(face.recognize_face(userf))
# #             user_id = 1668686155
#             user = excel.Reader().get_user(user_id)
#             if user.flag:
#                 info_barriers = user.info_barriers
#                 data.output(f'欢迎{user.name}{"(管理员)" if user.admin else ""}使用本系统!',should_speak(info_barriers))
#                 show_favorite(user)
#             else:
#                 data.output('您还没有被注册呢亲,请先注册.',should_speak(info_barriers))
#                 quit_program()
#                 return
#         else:
#             data.output('输入有误,请重试')
#             quit_program()
#             return
        
        while 1:
            command = data.input(f'输入操作({";".join([f"{num}:{tip}" for num,tip,f in COMMANDS])}{";管理员:管理员操作" if user.admin else ""})',should_speak(info_barriers))
            if command == '管理员':  # 管理员操作单独处理
                cmd = data.input(f'输入管理员操作({";".join([f"{num}:{tip}" for num,tip,f in COMMANDS_OF_ADMIN])})',should_speak(info_barriers))
                flag = False  # 是否找到合适的命令并执行
                for num,tip,f in COMMANDS_OF_ADMIN:
                    if num == cmd or cmd == tip:
                        flag = True
                        f(user)
                        break
                if not flag:  # 输入有误
                    data.output(f'输入有误:未知的命令:"{cmd}",请重试!',should_speak(info_barriers))
                continue  # 不执行普通用户的命令的判断
            flag = False  # 是否找到合适的命令并执行
            for num,tip,f in COMMANDS:
                if num == command or command == tip:
                    flag = True
                    f(user)
                    break
            if not flag:  # 输入有误
                data.output(f'输入有误:未知的命令:"{command}",请重试!',should_speak(info_barriers))
# #         while 1:
# #             command = input('输入操作(0:退出程序;1:查询本账号借阅记录;2:查看图书馆现有书;3:借书;4:还书)')
# #             
# #             if command == '0':
# #                 break
# #             elif command == '1':
# #                 flag = 0
# #                 if len(excel.borrowing_record) == 0:
# #                     print('您好像还没有借过书吧……')
# #                     continue
# #                 for (id,lend_time,return_time,r_name,book_name) in excel.borrowing_record:
# #                     if r_name == name:
# #                         flag += 1
# #                         print(f'编号为{id}的借阅记录:借出时间:{lend_time},归还时间:{"未归还" if return_time == None else return_time},书名:{book_name}')
# #                 if flag:
# #                     print(f'您共有{flag}条借阅记录')
# #                 else:
# #                     print('您好像还没有借过书吧……')
# #             elif command == '2':
# #                 if len(excel.books) == 0:
# #                     print('没有书')
# #                     continue
# #                 for (book_name,book_type,have_num,add_time) in excel.books:
# #                     print(f'书名:{book_name} 类型:{book_type} 剩余数目:{have_num} 添加时间:{add_time}')
# #             elif command == '3':
# #                 book_list = []
# #                 
# #                 if len(excel.borrowing_record) != 0:
# #                     for (id,lend_time,return_time,r_name,book_name) in excel.borrowing_record:
# #                         if r_name == name:
# #                             book_list.append(book_name)
# #                     love_book_type = []
# #                     for (book_name,book_type,have_num,add_time) in excel.books:
# #                         if book_name in book_list:
# #                             love_book_type += book_type.split(',')
# #                     
# #                     l = []
# #                     for (book_name,book_type,have_num,add_time) in excel.books:
# #                         for x in book_type.split(','):
# #                             if x in love_book_type and book_name not in book_list:
# #                                 l.append(book_name)
# #                     
# #                     if len(l) != 0:
# #                         print(f'系统根据您的喜好,自动为您推荐书籍:{",".join(l)}')
# #                 
# #                 book_name = input('请输入您想借的书名>>>')
# #                 i = 1
# #                 for (r_book_name,book_type,have_num,add_time) in excel.books:
# #                     if r_book_name == book_name:
# #                         if int(have_num) > 0:
# #                             excel.write(excel.E_books,i,3,int(have_num)-1)
# #                             excel.write(excel.E_borrowing_record,excel.row_borrowing_record+1,1,excel.row_borrowing_record)
# #                             excel.write(excel.E_borrowing_record,excel.row_borrowing_record+1,2,ctime())
# #                             excel.write(excel.E_borrowing_record,excel.row_borrowing_record+1,4,name)
# #                             excel.write(excel.E_borrowing_record,excel.row_borrowing_record+1,5,book_name)
# #                             excel.row_borrowing_record += 1
# #                             
# #                             excel.books[i-1][2] -= 1
# #                             excel.borrowing_record.append([excel.row_borrowing_record,ctime(),None,name,book_name])
# #                             
# #                             print('借书成功!')
# #                             break
# #                         else:
# #                             print(f'暂时没有{book_name}')
# #                     i += 1
# #             elif command == '4':
# #                 book_name = input('请输入您想归还的书名>>>')
# #                 for (id,lend_time,return_time,r_name,r_book_name) in excel.borrowing_record:
# #                     if r_name == name and return_time == None and r_book_name == book_name:
# #                         i = 1
# #                         for (a_book_name,_,_,_) in excel.books:
# #                             if a_book_name == book_name:
# #                                 excel.write(excel.E_books,i,3,excel.books[i-1][2]+1)
# #                                 excel.books[i-1][2] += 1
# #                                 break
# #                             i += 1
# #                         i = 1
# #                         for (_,_,_,_,a_book_name) in excel.borrowing_record:
# #                             if a_book_name == book_name:
# #                                 excel.write(excel.E_borrowing_record,i+1,3,ctime())
# #                                 excel.borrowing_record[i-1][2] = ctime()
# #                                 break
# #                             i += 1
# #                         
# #                         print('还书成功')
# #                         break
# #             elif command == 'Admin':
# #                 command = input('管理员操作(0:退出;1:增加书本)')
# #                 
# #                 if command == '0':
# #                     break
# #                 elif command == '1':
# #                     book_name = input('输入书本的名称>>>')
# #                     book_type = input(f'输入{book_name}的类型(使用英文逗号分割",")>>>')
# #                     have_num = input(f'输入拥有{book_name}的剩余数量>>>')
# #                     
# #                     excel.write(excel.E_books,excel.row_books+1,1,book_name)
# #                     excel.write(excel.E_books,excel.row_books+1,2,book_type)
# #                     excel.write(excel.E_books,excel.row_books+1,3,int(have_num))
# #                     excel.write(excel.E_books,excel.row_books+1,4,ctime())
# #                     excel.row_books += 1
# #                     
# #                     excel.books.append([book_name,book_type,int(have_num),ctime()])
# #                     
# #                     print(f'添加书本{book_name}成功!')
# #                 else:
# #                     print(f'输入有误:未知的命令:"{command}"')
# #             else:
# #                 print(f'输入有误:未知的命令:"{command}"')
# #         
        data.output('欢迎下次使用本系统!',should_speak(info_barriers))
        quit_program()
#     except Exception as e:
#         data.output(f'程序似乎遇到了一些问题……{e}')
#         quit_program()

if __name__ == '__main__':
    main()


'''
1.《论语译注》 杨伯峻
2.《三国演义》 罗贯中
3.《西游记》 吴承恩
4.《水浒传》 施耐庵
5.《红楼梦》 曹雪芹
6.《鲁迅作品选读》
7.《子夜》 茅盾
8.《家》 巴金
9.《骆驼祥子》 老舍
10.《围城》 钱钟书
15.《汤姆叔叔的小屋》
16.《少年维特之烦恼》 (德)歌德
17.《钢铁是怎样炼成的》 (前苏)奥斯特洛夫斯基
19.《唐·吉诃德》 (西班牙)塞万提斯
21.《简爱》 (英)夏绿蒂·勃朗特
22.《巴黎圣母院》 (法)雨果
23.《红与黑》 (法)司汤达
24.《复活》 (俄)托尔斯泰
25.《欧也妮·葛朗台》 (法)巴尔扎克
26.《匹克威克外传》 (英)狄更斯
27.《老人与海》 (美)海明威
28.《雪国》 (日)川端康成
29.《麦田守望者》 (美)塞林格
30.《莫泊桑中短篇小说选》
31.《契诃夫中短篇小说选》
32.《马克吐温中》
33.《欧亨利短篇小说选》
34.《中外微型小说读本》(自编)
35.《唐诗三百首》
36.《中学生宋词选读》(自编)
37.《中学生元曲选读》(自编)
38.《中外抒情诗选》(自编)
40.《毛泽东诗词鉴赏》 吴功正
41.《泰戈尔诗选》
42.《普希金诗选》
43.《草叶集》 (美)惠特曼
44.《窦娥冤》 关汉卿
45.《雷雨》 曹禺
46.《伪君子》 (法)莫里哀
47.《莎士比亚戏剧选》(自编)
48.《繁星·春水》 冰心
49.《文化苦旅》 余秋雨
50.《蒙田散文选》
'''