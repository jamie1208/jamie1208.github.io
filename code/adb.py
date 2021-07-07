import datetime
from sqlite3.dbapi2 import Error
import time
class DB():
    def __init__(self):
        self.conn = None
        self.cur = None
        self.lst = ['沙拉','湯品','主餐','甜品','飲料']

    def __enter__(self):
        self.open()
        return self
    
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        """ 開啟資料庫連線
        """
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('diner.db')
            self.cur = self.conn.cursor()
        return True

    def close(self):
        """ 關閉資料庫連線
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True
    def show_reviews(self):
        """ 顯示評論
        """
        print('\n評論: ')
        self.cur.execute("SELECT ACCOUNT FROM REVIEWS")
        name_len = self.cur.fetchall()[0]
        long_name = '0'
        for i in name_len:
            if len(i)>len(long_name):
                long_name = i
        self.cur.execute("SELECT * FROM REVIEWS")
        all_reviews = self.cur.fetchall()
        for i in all_reviews:
            print('{:{}} {}顆星: {}'.format(i[0],len(long_name),i[1],i[2]))
        print()

    def avg_star(self):
        """ 計算平均評分
        """
        self.cur.execute("SELECT AVG(STARS) FROM REVIEWS")
        avg_star = round(self.cur.fetchone()[0],2)
        return avg_star

    def reviews(self,account):
        """ 撰寫評論
        """
        while True:
            star = int(input('評分 (1-5): '))
            if star not in (1,2,3,4,5):
                print('輸入錯誤，請重新輸入')
            else:
                break
        review = input('撰寫評論: ')
        self.cur.execute("INSERT INTO REVIEWS VALUES (?, ?, ?)",(account, star, review))
        self.conn.commit()

    def check_if_existed(self,client_account):
        """ 檢查是否註冊
        """
        self.cur.execute("SELECT COUNT(*) FROM CLIENTINFO WHERE ACCOUNT=?",(client_account,))
        if self.cur.fetchone()[0] == 1:
            return True
        else:
            return False

    def check_passwords(self,client_account,pass_word):
        """ 檢查密碼
        """
        self.cur.execute("SELECT PASSWORD FROM CLIENTINFO WHERE ACCOUNT=?",(client_account,))
        right_pass = self.cur.fetchone()[0]
        if pass_word == right_pass:
            return True
        else:
            print('---密碼錯誤,請重新輸入---')
            print()
                
    def print_client_info(self,client_info,info):
        """ 查詢客戶資訊
        """
        self.cur.execute("SELECT * FROM CLIENTINFO WHERE {}=?".format(info),(client_info,))
        client = self.cur.fetchall()[0]
        print('編號: {}\n帳號: {}\n密碼: {}\n姓名: {}\n性別:{}\n生日: {}\n電話: {}'.format(*client)) 

    def client_existed(self,client_account,client_password):
        """ 客戶註冊
        """
        can_existed = True
        while can_existed:
            wronginfo = ''
            c_name = input('姓名: ')
            gender = input('性別 (F.女 M.男): ').upper()
            if gender not in ('F','M'):
                can_existed = False
                wronginfo+='性別 '
            birth = input('生日 (1999-11-01): ')
            try:
                d = datetime.datetime.strptime(birth,"%Y-%m-%d")
                fdate = d.date()
            except:
                can_existed = False
                wronginfo += '生日 '
            phone_num = input('電話號碼 (0912345678): ')
            if phone_num.isdigit() == False or len(phone_num) != 10:
                can_existed = False
                wronginfo += '電話號碼'
            if can_existed :
                break
            else:
                can_existed = True
                print('{} 輸入錯誤，請重新輸入'.format(wronginfo))
        client_id = self.max_id('CLIENTINFO')
        self.cur.execute("INSERT INTO CLIENTINFO VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (client_id, client_account, client_password, c_name, gender, fdate, phone_num))
        self.conn.commit()

        
    def max_id(self,table):
        """取得最大ID
        """
        self.cur.execute("SELECT MAX(ID) FROM {}".format(table))
        return self.cur.fetchone()[0]+1

    def localtime(self) :
        """ 取得未來一年時間
        """
        now = datetime.datetime.now()
        now_d = now.strftime('%Y-%m-%d')
        delta = datetime.timedelta(days=365)
        n_days = now+delta
        ny = n_days.strftime('%Y-%m-%d')
        return ny,now_d

    def print_book_info(self,bookinfo,info):
        """ 查詢訂位資料
        """
        self.cur.execute("SELECT * FROM BOOK WHERE {}=?".format(info),(bookinfo,))
        file = self.cur.fetchall()
        print('{:7} {:8}  {:7} {:4} {}'.format('帳號','電話','日期','時間','桌號'))
        for f in file:
            f = list(f)
            print('{:7} {:10}  {:10}  {}   {}'.format(*f))

    def check_date(self,y,m):
        """ 檢查日期錯誤
        """
        big_m = [1,3,5,7,8,10,12]
        small_m = [2,4,6,9,11]
        leap_y = 'n'
        if y%4 == 0 and y%400 != 0:
            leap_y = 'y'
        if m in big_m:
            day = 31
        else:
            if m == 2:
                day = 29 if leap_y == 'y' else 28
            else:
                day = 30
        return day
            

    def booking_date(self):
        """ 訂位日期 (2021-7-9 type = str)
        """
        next_d,now_d= self.localtime()
        while True:
            n = 0
            print('--- 只能預定{}前的位置 ---'.format(next_d))
            y = input('訂位年份 :')
            m = input('訂位月份 :')
            d = input('訂位日期 :')
            book_d = '{}-{}-{}'.format(y,m.zfill(2),d.zfill(2))
            if book_d>next_d or book_d<now_d:
                n = 1
            if int(m)>12 or int(m)<1:
                n = 1
            else:
                day = self.check_date(int(y),int(m))
                if int(d)>day or int(d)<1:
                    n =1
            if n == 1:
                print('您輸入的日期超過預定範圍，請重新輸入 !')
            else :
                print('**確認日期',book_d,'**')
                break
        return book_d

    def booking_time(self):
        """ 訂位時間 (1100 type = str)
        """
        time_tuple = self.show_time_list()
        n = time_tuple[-1][0] #取得time中最大ID
        ch_t = input('用餐時間 (1-{}): '.format(n))
        return time_tuple[int(ch_t)-1][2]

    def uplimit_p(self):
        """ 上限人數
        """
        self.cur.execute("SELECT SUM(SIZE) FROM BKTABLE")
        limit_p = self.cur.fetchone()[0]
        return limit_p

    def book(self,b_date,b_time,b_people,is_window,account):
        """ 訂位
        """
        confirm = ''
        reselect = ''
        self.cur.execute("SELECT * FROM BKTABLE")
        all_table = self.cur.fetchall()
        table_dic = {} #桌號、人數字典
        for i in all_table:
            table_dic[i[2]] = i[1]
        table_list = list(table_dic.keys()) #桌號list
        self.cur.execute("SELECT TIME, TABLE_NUM FROM BOOK WHERE DATE=?",(b_date,))
        dayinfo = self.cur.fetchall() #當日已訂位資料
        ard_t = [] #已訂位桌號
        for i in dayinfo:
            if i[0]== b_time:
                ard_t.append(i[2])
        left_t = list(set(table_list)-set(ard_t)) #剩餘桌號
        left_tnum = 0 #剩餘位置總人數
        for t in left_t:
            left_tnum += table_dic[t]  
        if dayinfo == [] or ard_t == []:
            table = table_list
        elif left_tnum < b_people:
            print('** 本時段訂位已滿 **')
            reselect = input('是否重選時段(y/n)? ').lower()
        else:
            table = left_t
        if reselect == '':
            if is_window == 'n':
                table.sort(reverse=True)
            sum_num = 0
            t_lst = [] #訂位桌號
            for i in table:
                sum_num += table_dic[i]
                t_lst.append(i)
                if sum_num >= b_people :
                    break
            self.cur.execute("SELECT PHONE FROM CLIENTINFO WHERE ACCOUNT =?",(account,))
            phone = self.cur.fetchone()[0].zfill(10)
            book_insert = "INSERT INTO BOOK VALUES (?,?,?,?,?)"
            for i in t_lst:
                self.cur.execute(book_insert,(account,phone,b_date,b_time,i))
            print('\n'+'*'*10)
            str_table = ','.join(t_lst)
            print('帳號: {}\n電話: {}\n日期: {}\n時間: {}\n人數: {}\n桌號: {}'.format(account,phone,b_date,b_time,b_people,str_table))
            print('*'*10)
            confirm = input('是否確認訂位(y/n)? ').lower()
            if confirm =='y':
                self.conn.commit()
        return confirm,reselect
        
    def show_bookinfo(self):
        """ 訂位資料顯示
        """
        self.cur.execute("SELECT * FROM BOOK")
        file = self.cur.fetchall()
        print()
        print('{:7} {:8}  {:7} {:4} {}'.format('帳號','電話','日期','時間','桌號'))
        for f in file:
            f = list(f)
            print('{:7} {:10}  {:10}  {}   {}'.format(*f))
        pass

    def table_dict(self,a_num,b_num): #finish
        """ 桌位設定
            a1-a4 (4 people) b1-b4 (2 people) b5-b8 (4 people)
        """
        self.cur.execute("DELETE FROM BKTABLE")
        self.conn.commit
        table_dict = {}
        for i in range(1,a_num+1):
            n = 'A'+str(i)
            table_dict[n] = 4
        for j in range(1,b_num+1):
            n = 'B'+str(j)
            m = 2 if j<=b_num//2 else 4
            table_dict[n] = m
        self.set_bktable(table_dict)
    
    def set_bktable(self,t_dict):
        """ 桌位儲存到資料庫
        """
        keys = list(t_dict.keys())
        for i,n in enumerate(keys):
            i_d = i+1
            size = t_dict[n]
            tnum = n
            self.cur.execute("INSERT INTO BKTABLE VALUES(?,?,?)",
            (i_d,size,tnum))
        self.conn.commit()

    def show_bktable(self):
        """ 桌位列表顯示
        """
        print()
        print('{:2s}  {:2s}  {:2s}'.format('ID','人數','桌號'))
        self.cur.execute("SELECT * FROM BKTABLE")
        table_list = self.cur.fetchall()
        for i in table_list:
            print('{:>2d}  {:>3d}  {:>4s}'.format(*i))

    def set_time(self): 
        """ 時間設定
        """
        self.cur.execute("DELETE FROM BKTIME")
        self.conn.commit()
        self.time_list = [[],[],[]]
        ls = input('lunch start time (11 00): ').split(' ')
        le = input('lunch end time (14 00): ').split(' ')
        ds = input('dinner start time (17 00): ').split(' ')
        de = input('dinner end time (22 00): ').split(' ')
        lst = [ls,ds,le,de]
        interval = int(input('interval: '))
        i_d = 0
        for i in range(2):
            hour = int(lst[i][0])
            minute = int(lst[i][1])
            n = 'lunch' if i == 0 else 'dinner'
            while True:
                if hour*100+minute>int(lst[i+2][0])*100+int(lst[i+2][1]):
                    break
                i_d += 1
                self.cur.execute("INSERT INTO BKTIME VALUES(?,?,?)",
                (i_d,n,str(hour).zfill(2)+':'+str(minute).zfill(2)))
                minute += interval
                hour = minute//60+hour
                minute %= 60
        self.conn.commit()

    def show_time_list(self): 
        """ 時間列表顯示
        """
        print()
        self.cur.execute("SELECT * FROM  BKTIME")
        time_list = self.cur.fetchall()
        print('{:2s}   {:6s}  {:2s}'.format('ID','午/晚','時段'))
        for i in time_list:
            print('{:>2d}   {:8s} {}'.format(*i))
        return time_list

    def select_menu(self,ch_it):
        """ 查詢指定菜單
        """
        for i in ch_it:
            self.cur.execute("SELECT DISH ,PRIZE FROM MENU WHERE ITEMS =?",(i,))
            select_it = self.cur.fetchall()
            print('\n----- {} -----'.format(i))
            for j in select_it:
                print('${:<4} {:8s}'.format(j[1],j[0]))
    
    def change_menu(self,ch1):
        """ 增修、刪除菜單
        """
        while True:
            lst = []
            item = eval(input('1.沙拉 2.湯品 3.主餐 4.甜品 5.飲料 6.離開\n>>>'))
            if item == 6:
                break
            elif str(item).isdigit() and 7>item>0:
                dish = self.lst[item-1]
            else:
                print('無此選項 !')
            if ch1 == 1:
                name = input('菜名 :')
                p = input('價錢 :')
                menu_insert = "INSERT INTO MENU VALUES (?,?,?)"
                self.cur.execute(menu_insert,(dish,name,int(p)))
            else:
                id = 0
                self.cur.execute("SELECT DISH ,PRIZE FROM MENU WHERE ITEMS =?",(dish,))
                alldish = self.cur.fetchall()
                print('{:2}  {:4}  {}'.format('編號','價錢','菜名'))
                for d in alldish :
                    id += 1
                    print('{:2}   {:4}  {:>6}'.format(id,d[1],d[0]))
                ch = eval(input('>>>'))
                if str(ch).isdigit() and id>=ch>0 :
                    self.cur.execute("DELETE FROM MENU WHERE DISH =?",(alldish[ch-1][0],))
                    print('成功刪除此{} !\n'.format(dish))
                else:
                    print('無此選項 !\n')
        self.conn.commit()



        
if __name__ == '__main__':
    print('This is the DB restaurant.')