import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

# 기하평균
def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))

# 현재 가치로 환산
def to_present_value(cash_flow, i_f):
    total_present_value = 0
    for value in cash_flow:
        total_present_value += value / i_f
    
    return total_present_value

# 연간 비용 환산
def to_annual_value(present_value, study_period, i_f):
    """
    AW = present_value(A/P, i_f, study_period)
    
    A/P = (i_f * (1+i_f) ** study_period) / ((1+1_f)**study_period - 1)
    """
    annual_value = present_value * i_f * (1+i_f) ** study_period / ((1+i_f)**study_period - 1)
    
    return annual_value

def krw_formatter(x, pos):
    return f'{x*1e-6:1.1f} M 원'

# 그래프 작성
def plot_cash_flow(ax, title, data, x_range=None, xlabel='Year', ylabel='Cashflow'):
    """
    plot subplot
    """
    if x_range is None:
        x_range = range(len(data))
    ax.bar(
        x_range,
        data)
    ax.grid(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_range)
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(krw_formatter))
    for i,j in zip(x_range,data):
        if j > 0:
            ax.annotate('{:.2f}'.format(j*1e-6), xy=(i-0.5, j))
        elif j < 0:
            ax.annotate('{:.2f}'.format(j*1e-6), xy=(i-0.5, j*1.001))
    

# 그래프 출력
def show_cash_flow(title, data, study_period, size=(20, 5)):
    fig, ax = plt.subplots()
    fig.set_size_inches(*size)
    plot_cash_flow(
        ax=ax,
        title=title,
        data=data)
    
    
#--------------부품비 세부 그래프-----------------#
def item_cash_flow(car_interval, item_interval, item_price, study_period, f):    
    cash_flow = np.zeros(study_period+1)
    if car_interval < item_interval:
        return cash_flow
    
    for year in range(study_period+1):
        vehicle_age = year % car_interval
        if vehicle_age > 0:
            item_price *= (1+f) # 인플레이션
            if vehicle_age % item_interval == 0:
                cash_flow[year] = item_price
    return cash_flow

def plot_item_cash_flow(car_interval, item_df, study_period, f, nrows=None, ncols=2):
    n_items = len(item_df) # 17
    nrows = math.ceil(n_items/ncols) # 8
    fig, ax = plt.subplots(nrows, ncols)
    fig.set_size_inches(30, 100)
    fig.subplots_adjust(wspace=.25, hspace=.25)
    
    # 각 axis에 index 부여 후 하나씩 subplot 작성
    ax_indices = []
    for i in range(nrows):
        for j in range(ncols):
            ax_indices.append( (i, j) )
    
    total_cash_flow = np.zeros(study_period+1)
    
    for idx, (item_name, row) in enumerate(item_df.iterrows()):
        cash_flow = item_cash_flow(
            car_interval=car_interval,
            item_interval=row['교체 주기 (년)'],
            item_price=row['수리비'],
            study_period=study_period,
            f=f)
        total_cash_flow += cash_flow
        
        # plot subplot for each item
        plot_cash_flow(
            ax = ax[ax_indices[idx]],
            title=item_name,
            data=cash_flow)
        
    # items total
    plot_cash_flow(
        ax = ax[ax_indices[-1]],
        title='부품 총합 cashflow',
        data=total_cash_flow)
#--------------부품비 세부 그래프-----------------#