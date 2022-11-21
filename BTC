import ccxt
import json
import pandas as pd
import time
from datetime import datetime
import datetime, pytz
import sys, os
import math
from decimal import Decimal

# connection
def read_config():
    with open('config.json') as json_file:
        return json.load(json_file)

config = read_config()
api_key = config["API_KEY"]
api_secret = config["API_SECRET"]

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True}
)

#Variables
coin_pair = 'BTC/BUSD'

#function กำหนด zone
def action_point():
  floor = Decimal('0') #โซนล่างสุดของ ที่ต้องใช้ Decimal เพราะ product บางตัวมันเป็นทศนิยม
  ceiling = Decimal('20000') #โซนบนสุดของ
  pip = Decimal('100') #ระยะ
  price_action = [] #สร้าง array ไว้เก็บค่าขอบเขตของ zone
  price_action.append(float(floor)) #ตรงนี้เขียนค่าแรกของ floor ก่อน
  while floor <= ceiling: #ให้ floor + pip ไปเรื่อยๆ จนถึง ceiling
    floor = floor + pip
    if floor <= ceiling:
      price_action.append(float(floor))
  return price_action

#function ตรวจสอบ และสร้าง database
def check_DZD_db():
    tz = pytz.timezone('Asia/Bangkok')
    now1 = datetime.datetime.now(tz)
    month_name = 'x Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[now1.month]
    ret = now1.strftime('BTC_Dense_Zone_Data_%Y_')
    file_name = "{}{}".format(ret, month_name)
    try:
        try_open = pd.read_csv(file_name)
        return file_name
    except:
        zone_list = action_point()
        columns=['Zone']

        for i in range(31):
            columns.append('Day_{}'.format(i+1))

        database = pd.DataFrame(columns=columns)

        for i in range(len(zone_list)):
            database.loc[i, 'Zone'] = zone_list[i]

        database.to_csv(file_name, index=False)
        print('Database Created')

        return file_name

#function เก็บค่าความถี่ในการ rb
def DZD_rec(price,file_name):
    read_DZD = pd.read_csv(file_name)
    zone = read_DZD.Zone
    find_list = 0
    row_list = 0

    for i in range(len(zone)):
        if zone[i] <= price <= zone[i + 1]:
            find_list = zone[i]
            row_list = i

    tz = pytz.timezone('Asia/Bangkok')
    day_check = datetime.datetime.now(tz)
    cur_day = day_check.day
    day_col = 'Day_{}'.format(cur_day)

    if math.isnan(read_DZD.loc[row_list, day_col]):
        read_DZD.loc[row_list, day_col] = 1

    else:
        read_DZD.loc[row_list, day_col] += 1

    read_DZD.to_csv(file_name, index=False)

#function เขียน price ที่ rb ล่าสุด
def write_ap(price):
    data = pd.read_csv('Acted_Price')
    pulldata = data.PriceAct
    data.loc[0, 'PriceAct'] = price
    data.to_csv('Acted_Price', index=False)

#function ตรวจสอบราคาจาก exchange
def raw_price():  # เช็คราคาตลาด
    r1 = json.dumps(exchange.fetch_ticker(coin_pair))  # dump ราคาเป็น json
    dataPriceBTC = json.loads(r1)  # ดึงข้อมูลราคา
    coin_price = dataPriceBTC['last']  # ดึงราคาล่าสุด
    return round(coin_price, 1)

#function ตรวจสอบวันเวลา
def date():
    tz = pytz.timezone('Asia/Bangkok')
    now1 = datetime.datetime.now(tz)
    month_name = 'x Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    return "%d %s %d %s" % (now1.day, month_name, thai_year, time_str)

#function กำหนด % ต่ำสุดในการ rb
def minimum_pip(price):
    data = pd.read_csv('Acted_Price')
    pulldata = data.PriceAct
    acted_price = data.loc[0, 'PriceAct']
    if acted_price == 0:
        data.loc[0, 'PriceAct'] = price
        acted_price = price
        data.to_csv('Acted_Price', index=False)
    percentage = round(price / acted_price * 100, 2)
    per_benchmark = 100.2  #ราคาต้องมากกว่าค่า %คอม
    per_nd = 99.8 #ราคาต้องน้อยกว่าค่า %คอม
    if percentage >= per_benchmark or percentage <= per_nd:
        return 1
    else:
        return 0

check_DZD_db() #เช็ค data ก่อนเริ่ม loop
while True:
    try:
    
        time.sleep(120) #trigger 2mins timebase rebalance ตรงนี้ใครใช้ technical แบบไหนก็จัดการได้ตามสะดวกนะครับ
        price = raw_price()


        if price >= 1 and price < 20000: #ตรวจสอบวราคาว่าอยู่ใน zone ที่เราเทรดไหม
            change = minimum_pip(price)

            if change == 1:
                file_name = check_DZD_db()
                DZD_rec(price,file_name)
                write_ap(price)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

