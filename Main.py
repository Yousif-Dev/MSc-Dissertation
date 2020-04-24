from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import pvlib
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters


class SolarCell(object):

    def __init__(self, solar_cell_location, inverter_location, maximum_power, loc = [52.4068,1.5197]):
        self.solar_cell = pd.read_csv(solar_cell_location, index_col=0, parse_dates=True)
        self.inverter = pd.read_csv(inverter_location)
        self.max_power = maximum_power
        self.inverter["Percent"] = self.inverter["Percent"] * self.max_power / 100
        self.inverter.rename(columns={"Percent": "Power"})
        self.erbs = 0
        self.loc = loc
    def return_cell(self):
        return self.solar_cell

    def invert(self):
        for i in range(len(self.solar_cell)):
            GHIValue = self.solar_cell["GHI"].iloc[i]
            dateandtimeValue = self.solar_cell.index[i]
            # Gets index of Row
            result_index = self.inverter['Percent'].sub(GHIValue).abs().idxmin()
            # Now we need to multiply Efficiency by it.
            self.solar_cell.at[dateandtimeValue, "GHI"] = self.solar_cell.at[dateandtimeValue, "GHI"] * \
                                                          self.inverter.at[
                                                              result_index, "Efficiency"] / 100
    def efficiency(self):
        hourly_resampled = self.solar_cell.resample("H").mean()
        date = pd.date_range(start = hourly_resampled.index[0], end = hourly_resampled.index[-1], freq = "H")
        print(date)
        solar_pos = pvlib.solarposition.get_solarposition(date,self.loc[0],self.loc[1])
        self.erbs = pvlib.irradiance.erbs(hourly_resampled["GHI"], solar_pos["apparent_zenith"], date)
        return(self.erbs)

if __name__ == "__main__":

    solar_cell = SolarCell(
        r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\ss_testbed_irrad_2012.csv",
        r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\Inverter.csv", 10000)
    print(solar_cell.efficiency())