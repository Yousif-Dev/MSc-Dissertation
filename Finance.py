import pandas as pd


def financial_calculator(solar_data):
    """Returns a financial figure in £ of how much money you would generate by selling electricity from solar
    cell, takes solar cell data and dates"""
    money = pd.read_csv("epex_UK_half_hourly_day_ahead_prices.csv" , parse_dates=["timestamp"])
    money_resampled = money.resample("H", on = "timestamp").mean()
    final_cash = 0
    for i in range(len(solar_data)):
        GHIValue = solar_data["GHI"].iloc[i]
        dateandtimeValue = solar_data.index[i]
        money_generated = GHIValue * money_resampled.loc[money_resampled.index == dateandtimeValue]["price"].values[0]
        final_cash += money_generated
    # /1000 because ninja gives figure in Watts
    return (final_cash/1000)
