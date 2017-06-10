import pandas as pd
import numpy as np
import math
from utils import geo_mean

# 이자율/인플레이션 계산 연도
year_index = [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]

# 이자율 (i_f)
i_f_list = [1.0487, 1.0430, 1.0225, 1.0237, 1.0300, 1.0287, 1.0250, 1.0212, 1.0162, 1.0125]
i_f_df = pd.DataFrame(data=i_f_list, index=year_index)
i_f = geo_mean(i_f_df) - 1

# 인플레이션 (f)
f_list = [1.0250, 1.0470, 1.0280, 1.0300, 1.0400, 1.0220, 1.0130, 1.0130, 1.0070, 1.0100]
f_df = pd.DataFrame(data=f_list, index=year_index)
f = geo_mean(f_df) - 1

# 일평균 주행거리 (km)
daily_driving = 37.6

# 연간 주행거리 (km)
annual_driving = 365 * daily_driving # 13,724 km

# 연비 (km/l)
fuel_efficiency = 10.1

# 국내유가 (원/l)
oil_price = 1472.65

# 연간 유류비
annual_oil_cost = annual_driving / fuel_efficiency * oil_price

# 연간 주차비
parking_fee = 656600

# 차량 가격
car_price = 36000000

# 취득세율
acquisition_rate = 0.07

# 자동차세
car_taxes = [780000, 741000, 700200, 663000, 624000, 585000, 546000, 507000, 468000, 429000]

# 자동차보험
car_insurance = [948520, 948520, 681950, 681950, 681950, 681950, 681950, 681950, 365270, 365270]

# 운전자보험
driver_insurance = 215839

# 감가상각률
salvage_rates = [0.84, 0.715, 0.664, 0.594, 0.541, 0.499, 0.423, 0.355, 0.298, 0.271]

# Study Period
study_period = 20


# ----------------------------------부품비----------------------------------#
item_names = ['엔진오일', '미션오일', '에어필터', '디퍼렌셜오일', '연료필터', '타이밍벨트', '냉각수','브레이크패드', '브레이크라이닝',
              '브레이크오일', '파워스티어링오일', '점화플러그', '배터리', '와이퍼', '타이어', '타이어위치교환', '클러치디스크']

# 교체 주기 주행거리 (km)
replacement_distances = [15000, 60000, 30000, 120000, 60000, 100000, 200000, 62890, 120000, 40000, 120000, 160000, 'N/A', 40000, 60000, 10000, 80000]

# 교체 주기 (년)
replacement_interval = []
for replacement_distance in replacement_distances:
    if type(replacement_distance) == int:
        replacement_interval.append(math.ceil(replacement_distance/annual_driving))
    else:
        replacement_interval.append(3)
# 부품 가격
item_prices = [7150, 4200, 14160, 66010, 55380, 110300, 7680, 28390, 16380, 15100, 3470, 8280, 219650, 23870, 112450, 0, 201470]
# 부품 개수
item_numbers = [6, 7.5, 1, 1, 1, 1, 3, 1, 1, 1, 1, 4, 1, 1, 4, 1, 1]
# 공임
replacement_fee = [20700, 34500, 13800, 28175, 34500, 28175, 28175, 34500, 28175, 27600, 13800, 69000, 28175, 6900, 13800, 34500, 34500]

item_columns = ['교체 주기 주행거리 (km)', '교체 주기 (년)', '부품 가격', '개수', '공임']

item_df = pd.DataFrame(
    data=np.array([replacement_distances, replacement_interval, item_prices, item_numbers, replacement_fee]).T,
    index=item_names,
    columns=item_columns)

item_df[['교체 주기 (년)', '부품 가격', '개수', '공임']] = item_df[['교체 주기 (년)', '부품 가격', '개수', '공임']].astype(float)
item_df[['교체 주기 (년)', '부품 가격', '공임']] = item_df[['교체 주기 (년)', '부품 가격', '공임']].astype(int)
item_df['수리비'] = (item_df['부품 가격']*item_df['개수']+item_df['공임']).astype(int)
# ----------------------------------부품비----------------------------------#




