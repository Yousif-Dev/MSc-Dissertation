from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import pvlib
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from RenewableNinjaAPI import get_ninja_data

class SolarCell(object):

    def __init__(self, solar_cell_data, inverter_location, maximum_power, loc=[52.4068, 1.5197], tilt=0,
                 azimuth=180, pv_array_size = 1):
        self.solar_cell = solar_cell_data
        self.solar_cell["GHI"] = self.solar_cell["GHI"]*pv_array_size
        self.inverter = pd.read_csv(inverter_location)
        self.max_power = maximum_power
        self.loc = loc
        self.tilt = tilt
        self.azimuth = azimuth
        self.panel = 0

    def return_cell(self):
        return self.solar_cell

    def invert(self, option="None"):
        if option == "percent":
            self.inverter["Percent"] = self.inverter["Percent"] * self.max_power / 100
        elif option == "normalise":
            self.inverter["Percent"] = (self.inverter["Percent"] / self.inverter["Percent"].max()) * self.max_power
        for i in range(len(self.solar_cell)):
            GHIValue = self.solar_cell["GHI"].iloc[i]
            dateandtimeValue = self.solar_cell.index[i]
            # Gets index of Row
            result_index = self.inverter['Percent'].sub(GHIValue).abs().idxmin()
            # Now we need to multiply Efficiency by it.
            self.solar_cell.at[dateandtimeValue, "GHI"] = GHIValue * \
                                                          self.inverter.at[
                                                              result_index, "Efficiency"] / 100
            # Clipping the data
            if self.solar_cell.at[dateandtimeValue, "GHI"] > self.max_power:
                self.solar_cell.at[dateandtimeValue, "GHI"] = self.max_power

    def total_energy(self):
        return self.solar_cell["GHI"].sum()


if __name__ == "__main__":
    #The main event am I right
    SCData = get_ninja_data()
    solar_cell = SolarCell(
        SCData,
        r"D:\Personal Folder\Study\-MSc\Dissertation\Data\Industrial Inverters\PVI-10.0-I-OUTD.csv", 10)
    print(solar_cell.total_energy())
    solar_cell.invert(option = "percent")
    print(solar_cell.total_energy())