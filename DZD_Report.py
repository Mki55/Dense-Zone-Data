from datetime import datetime
import datetime, pytz
import pandas as pd


def FZD_report_db():
  try:
    try_open = pd.read_csv('FZD_Report')

  except:
    columns=['Today_Zone','Today',  'Yesterday_Zone', 'Yesterday', 'Last_3d_Zone','Last_3d',  'Last_7d_Zone', 'Last_7d', 'Last_Month_Zone','Last_Month']
    database = pd.DataFrame(columns=columns)
    database.to_csv('FZD_Report', index=False)


def report_FZD():
  tz = pytz.timezone('Asia/Bangkok')
  now1 = datetime.datetime.now(tz)
  last_month_name = 'x Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[now1.month-1]
  ret = now1.strftime('BTC_Dense_Zone_Data_%Y_')
  last_file_name = "{}{}".format(ret, last_month_name)
  month_name = 'x Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[now1.month]
  file_name = "{}{}".format(ret, month_name)

  open_FZD_db = pd.read_csv('FZD_Report')
  db_source = pd.read_csv(file_name)

  data_column_yesterday = getattr(db_source,'Day_{}'.format(now1.day-1))
  ranked_yesterdey = data_column_yesterday.sort_values(ascending=False) [:5]
  yesterdey_zone = db_source.Zone[ranked_yesterdey.index] [:5]

  data_column = getattr(db_source,'Day_{}'.format(now1.day))
  ranked_day = data_column.sort_values(ascending=False) [:5]
  day_zone = db_source.Zone[ranked_day.index] [:5]


  box_3 = []
  for i in range(3):
    try:
      if now1.day-i == 0:
        continue
      best_val_3 = getattr(db_source,'Day_{}'.format(now1.day-i))
      best_val_3[np.isnan(best_val_3)] = 0

      if type(box_3) is list:
        box_3 = best_val_3
      else:
        box_3 = box_3 + best_val_3
    except:
      continue
  ranked_3d = box_3.sort_values(ascending=False) [:5]
  day3_zone = db_source.Zone[ranked_3d.index] [:5]


  box_7 = []
  for i in range(7):
    try:
      if now1.day-i == 0:
        continue
      best_val_7 = getattr(db_source,'Day_{}'.format(now1.day-i))
      best_val_7[np.isnan(best_val_7)] = 0

      if type(box_7) is list:
        box_7 = best_val_7
      else:
        box_7 = box_7 + best_val_7
    except:
      continue
  ranked_7d = box_7.sort_values(ascending=False) [:5]
  day7_zone = db_source.Zone[ranked_7d.index] [:5]

  try:
    file_last_M = pd.read_csv(last_file_name)
    box_month = []
    for i in range(31):
      try:
        if now1.day-i == 0:
          continue
        best_val_month = getattr(db_source,'Day_{}'.format(1+i))
        best_val_month[np.isnan(best_val_month)] = 0

        if type(box_month) is list:
          box_month = best_val_month
        else:
          box_month = box_month + best_val_month
      except:
        continue
    
    ranked_month = box_month.sort_values(ascending=False) [:5]
    month_zone = db_source.Zone[ranked_month.index] [:5]

    open_FZD_db.loc[i, 'Last_Month'] = list(ranked_month)[i]
    open_FZD_db.loc[i, 'Last_Month_Zone'] = list(month_zone)[i]
    open_FZD_db.to_csv('FZD_Report', index=False)

  except:
    print('No monthly information')

  for i in range(5):
    open_FZD_db.loc[i, 'Today'] = list(ranked_day)[i]
    open_FZD_db.loc[i, 'Today_Zone'] = list(day_zone)[i]

    open_FZD_db.loc[i, 'Yesterday'] = list(ranked_yesterdey)[i]
    open_FZD_db.loc[i, 'Yesterday_Zone'] = list(yesterdey_zone)[i]

    open_FZD_db.loc[i, 'Last_3d'] = list(ranked_3d)[i]
    open_FZD_db.loc[i, 'Last_3d_Zone'] = list(day3_zone)[i]

    open_FZD_db.loc[i, 'Last_7d'] = list(ranked_7d)[i]
    open_FZD_db.loc[i, 'Last_7d_Zone'] = list(day7_zone)[i]
    
    open_FZD_db.to_csv('FZD_Report', index=False)

  


FZD_report_db()
report_FZD()
reoortpan = pd.read_csv('FZD_Report')
pd.DataFrame(reoortpan)
