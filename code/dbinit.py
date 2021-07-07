import os
try:
    os.unlink('diner.db')
except:
    print('首次建檔')

import sqlite3
conn = sqlite3.connect('diner.db')
cur = conn.cursor()

#評論
cur.execute('''CREATE TABLE REVIEWS
(ACCOUNT text, STARS interger, REVIEW text)''')

cur.execute("INSERT INTO REVIEWS VALUES('jamie',5,'讚!')")
cur.execute("INSERT INTO REVIEWS VALUES('bob',4,'服務好!')")


#個資
cur.execute('''CREATE TABLE CLIENTINFO
(ID interger,ACCOUNT text, PASSWORD text, NAME text, GENDER text, BIRTH text, PHONE text)''')

cur.execute("INSERT INTO CLIENTINFO VALUES(1,'jamie','caijamie','Jamie','女','2004-11-01','0912345678')")
cur.execute("INSERT INTO CLIENTINFO VALUES(2,'bob','123','bob','男','2004-11-01','1234567890')")


#訂位設定
cur.execute('''CREATE TABLE BKTABLE
(ID interger, SIZE interger, TNUM text)''')

cur.execute("INSERT INTO BKTABLE VALUES(1,4,'A1')")
cur.execute("INSERT INTO BKTABLE VALUES(2,4,'A2')")
cur.execute("INSERT INTO BKTABLE VALUES(3,2,'B1')")
cur.execute("INSERT INTO BKTABLE VALUES(4,2,'B2')")

cur.execute('''CREATE TABLE BKTIME
(ID interger, LD text, TIME text)''')

i_d = 0
open_hour = 11
for i in range(2):
    n = 'lunch' if i == 0 else 'dinner'
    for j in range(5):
        i_d += 1
        cur.execute("INSERT INTO BKTIME VALUES(?,?,?)",
        (i_d,n,str(open_hour).zfill(2)+':'+'0'.zfill(2)))
        open_hour += 1

#訂位
cur.execute('''CREATE TABLE BOOK
 (ACCOUNT text, PHONE text, DATE text , TIME text ,TABLE_NUM text)''')
book_insert = "INSERT INTO BOOK VALUES (?,?,?,?,?)"
import time
t_date = int(time.time())
s_date = time.localtime(t_date)
str_date = time.strftime("%Y-%m-%d",s_date)
cur.execute(book_insert,('jamie','0912345678',str_date,'11:00','A1'))
cur.execute(book_insert,('bob','1234567890',str_date,'11:00','B1'))

#菜單
cur.execute('''CREATE TABLE MENU
(ITEMS text,DISH text, PRIZE interger)''')
cur.execute('''INSERT INTO MENU VALUES('沙拉','海鮮水果沙拉',180)''')
cur.execute('''INSERT INTO MENU VALUES('湯品','玉米濃湯',80)''')
cur.execute('''INSERT INTO MENU VALUES('主餐','菲力牛排',380)''')
cur.execute('''INSERT INTO MENU VALUES('甜品','黑糖麻糬布蕾',60)''')
cur.execute('''INSERT INTO MENU VALUES('飲料','水果茶',120)''')

conn.commit()
conn.close()