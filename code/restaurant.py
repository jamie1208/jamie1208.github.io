from adb import DB
class restaurant():
    def __init__(self):
        self.menu_title = '餐廳'
        self.menu = {
            'a':'查詢資料', #訂位量分析
            'b':'時間設定',
            'c':'桌位設定',
            'd':'菜單設定',
            'q':'離開',
        }
        self.menu_func = {
            'a': lambda db,ft: self.find_imformation(db,ft),
            'b': lambda db,ft: self.time_set(db,ft),
            'c': lambda db,ft: self.table_set(db,ft),
            'd': lambda db,ft: self.menu_set(db,ft),
        }
        self.divider = '='*20

    def show_menu(self):
        """ 主選單
        """
        print(self.divider)
        print(self.menu_title)
        print(self.divider)
        for fid, fname in self.menu.items():
            print('%s:%s' % (fid, fname))
        print(self.divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', '無此功能！'

    def find_imformation(self,db,func_title):
        """ 查詢資料
        客戶資料 (依電話、帳號)
        訂位查詢 (依日期、時段)
        """
        print('\n1.客戶查詢 2.訂位查詢')
        ch = eval(input('>>>'))
        if ch == 1:
            print('\n*** 客戶查詢 ***')
            print('1.依電話查詢 2.依帳號查詢')
            ch1 = eval(input('>>>'))
            p_info = input('請輸入客戶資料 :')
            print()
            p = 'PHONE' if ch1 == 1 else 'ACCOUNT'
            db.print_client_info(p_info,p)
        elif ch == 2:
            print('\n*** 訂位查詢 ***')
            db.show_bookinfo()
            print('\n1.依日期查詢 2.依時段查詢')
            ch1 = eval(input('>>>'))
            p_info = input('請輸入資料 :')
            print()
            p = 'DATE' if ch1 == 1 else 'TIME'
            db.print_book_info(p_info,p)
        else:
            print('無此選項 !')


    def time_set(self,db,func_title):
        """ 時間設定
        """
        db.show_time_list()
        ch_time = input("是否要修改(y/n)?").lower()
        if ch_time == 'y':
            db.set_time()
            db.show_time_list()

    def table_set(self,db,func_title):
        """ 桌位設定
        """
        db.show_bktable()
        ch_table = input("是否要修改(y/n)?").lower()
        if ch_table == 'y':
            print("--- A 區靠窗 B 區不靠窗 ---")
            a_num = eval(input("A區座位數 :"))
            b_num = eval(input("B區座位數 :"))
            db.table_dict(a_num,b_num)
            db.show_bktable()

    def menu_set(self,db,func_title):
        """ 菜單設定
        """
        lst = ['沙拉','湯品','主餐','甜品','飲料']
        lst1 = ['增修','刪除','查詢','列表']
        while True:
            ch1 = eval(input('\n1.增修 2.刪除 3.查詢 4.列表 5.離開\n>>>'))
            if ch1 == 5:
                break
            else:
                print('\n***[{}]***'.format(lst1[ch1-1]))
                if ch1 == 4:
                    db.select_menu(lst)
                elif ch1 == 3:
                    lst_1 = []
                    item = eval(input('1.沙拉 2.湯品 3.主餐 4.甜品 5.飲料\n>>>'))
                    if str(item).isdigit() and 6>item>0:
                        lst_1.append(lst[item-1])
                        db.select_menu(lst_1)
                    else:
                        print('無此選項 !')
                elif ch1 == 2:
                    db.change_menu(ch1)
                elif ch1 == 1:
                    db.change_menu(ch1)
                else:
                    print('無此選項 !')
            

with DB() as db:
    arestaurant = restaurant()
    while True:
        func_id, func_name = arestaurant.show_menu()
        if func_id == 'q':
            break
        elif func_id == '':
            print(func_name)
        else:
            arestaurant.menu_func[func_id](db,func_name)
        print()