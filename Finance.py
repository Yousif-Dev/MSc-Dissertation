import pandas as pd
from datetime import datetime
from RenewableNinjaAPI import get_ninja_data
SD = "2016-01-01"
ED = "2017-01-01"
solar_panda = get_ninja_data(startdate=SD, enddate=ED)
money = pd.read_csv("epex_UK_half_hourly_day_ahead_prices.csv" , parse_dates=["timestamp"])
#print(money.loc[money['timestamp'] == date, ['price']])
totalcash = pd.DataFrame()
x = 0
print(solar_panda.index[0])