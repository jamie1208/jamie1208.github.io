from adb import DB
class Guest():
    def __init__(self):
        self.menu_title = '客人'
        self.account = '' 
        self.menu = {
            'a':'登入 . 註冊',
            'b':'評價',
            'c':'訂位',#查詢訂位
            'd':'瀏覽菜單',
            'q':'離開', 
        }
        self.menu_func = {
            'a': lambda db,ft: self.login(db,ft),
            'b': lambda db,ft: self.reviews(db,ft),
            'c': lambda db,ft: self.booking(db,ft),
            'd': lambda db,ft: self.see_menu(db,ft),
        }
        self.divider = '='*20
        self.lst = ['沙拉','湯品','主餐','甜品','飲料']

    def show_menu(self):
        """ 主選單
        """
        print(self.divider)
        print(self.menu_title)
        print(self.divider)
        if self.account == '':
            print(self.menu_title,'尚未註冊')
        else:
            print(self.menu_title,self.account)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def login(self, db,func_title):
        """ 登入.註冊
        1. 登入帳號 (判斷是否已有帳號)
        2. 註冊 : ID、帳號、姓名、性別、生日、電話
        """
        while True:
            while True:
                client_account = input('請輸入帳號 :')
                client_pass = input('請輸入密碼: ')
                if client_account != '' and client_pass != '':
                    break
                else:
                    print('---輸入錯誤---')
            if db.check_if_existed(client_account) :
                if db.check_passwords(client_account,client_pass):
                    self.account = client_account
                    db.print_client_info(client_account,'ACCOUNT')
                    break
            else:
                db.client_existed(client_account,client_pass)
                print('---註冊成功---')
                self.account = client_account
                break

    def reviews(self, db,func_title):
        """ 評價
        1. 顯示所有評論、平均評分
        2. 問是否要評價
        3. 評分? 評價?
        """
        avgstar = db.avg_star()
        print('\n平均星等: {}星'.format(avgstar))
        db.show_reviews()
        q = input('是否要撰寫評論?(y/n)').lower()
        if q == 'y':
            db.reviews(self.account)
            db.show_reviews()
            print('---評分完成，歡迎再次光臨!---')
        elif q != 'n':
            print('輸入錯誤，請重新輸入 !')

    def booking(self, db,func_title):
        """ 訂位 #目前有?筆訂位 #新增、查詢、修改
        1. 詢問訂位日期
        2. 人數
        3. 是否靠窗
        3. 顯示空位 (a區 位置靠窗)
        """
        while True:
            print('\n'+self.divider)
            print('日期')
            print(self.divider)
            b_date = db.booking_date()
            up_p = db.uplimit_p()
            print('--- 上限人數 :{}人 ---'.format(up_p))
            b_people = int(input('人數 (ex:5): '))
            if b_people>up_p:
                print('超過上限人數，訂位失敗 !')
                break
            print('\n'+self.divider)
            print('時段')
            print(self.divider)
            b_time = db.booking_time()
            print('** 確認時段',b_time,'**')
            print()
            is_window = input('是否要靠窗 (y/n): ')
            confirm,reselect = db.book(b_date,b_time,b_people,is_window,self.account)
            if confirm == 'y':
                print('訂位成功 !')
                break
            elif confirm == 'n':
                reselect = input('是否重新訂位(y/n)?').lower()
            if reselect == 'n':
                print('訂位失敗 !')
                break
    
    def see_menu(self, db,func_title):
        """ 瀏覽菜單
        """
        db.select_menu(self.lst)

with DB() as db:
    aguest = Guest()
    while True:
        func_id, func_name = aguest.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            if aguest.account == '':
                func_id = 'a'
                print('請先登入、註冊')
            aguest.menu_func[func_id](db,func_name)
        print()