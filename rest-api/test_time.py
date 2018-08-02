import time
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone('Asia/Ho_Chi_Minh')
vn = datetime.now(tz)
delta = timedelta(minutes=60)
vn = vn - delta
vn = vn.strftime('%y-%m-%d %H:%M:%S')
print(vn)
# date = "17-07-31 12:14:16" #Change to whatever date you want
date = time.strptime(vn, "%y-%m-%d %H:%M:%S")
print(date)
epoch = datetime.fromtimestamp(time.mktime(date)).strftime('%s')
print(epoch)
