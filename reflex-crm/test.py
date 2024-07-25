
from datetime import datetime, timedelta, timezone

# 获取当前日期和时间
now = datetime.now()

# 计算15天后的日期
future_date = now + timedelta(days=15)

# 提取15天后的时间部分
future_time = future_date.time()
print(datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))
# print(future_time.strftime(("%Y%m%d%H%M%S")))

# print(now.strftime("%Y%m%d%H%M%S") > future_time.strftime(("%Y%m%d%H%M%S")))