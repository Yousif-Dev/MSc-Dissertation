from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import pvlib
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters


class SolarCell(object):

    def __init__(self, solar_cell_location, inverter_location, maximum_power, loc=[52.4068, 1.5197], tilt=0,
                 azimuth=180):
        self.solar_cell = pd.read_csv(solar_cell_location, index_col=0, parse_dates=True)
        self.inverter = pd.read_csv(inverter_location)
        self.max_power = maximum_power
        self.loc = loc
        self.tilt = tilt
        self.azimuth = azimuth
        self.panel = 0
    def return_cell(self):
        return self.solar_cell


    def invert(self, option = "None"):
        if option == "percent":
            self.inverter["Percent"] = self.inverter["Percent"] * self.max_power / 100
        elif option == "normalise":
            self.inverter["Percent"] = (self.inverter["Percent"]/self.inverter["Percent"].max())*self.max_power
        for i in range(len(self.solar_cell)):
            GHIValue = self.solar_cell["GHI"].iloc[i]
            dateandtimeValue = self.solar_cell.index[i]
            # Gets index of Row
            result_index = self.inverter['Percent'].sub(GHIValue).abs().idxmin()
            #Clip the power
            if GHIValue > self.max_power:
                GHIValue == self.max_power
            # Now we need to multiply Efficiency by it.
            self.solar_cell.at[dateandtimeValue, "GHI"] = self.solar_cell.at[dateandtimeValue, "GHI"] * \
                                                          self.inverter.at[
                                                              result_index, "Efficiency"] / 100
    def total_energy(self):
        return (self.solar_cell["GHI"].sum())

if __name__ == "__main__":
    solar_cell = SolarCell(
        r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\ss_testbed_irrad_2012.csv",
        r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\IGBT.csv", 1000)
    EnergyBefore = solar_cell.total_energy()
    solar_cell.invert(option="normalise")
    EnergyAfter = solar_cell.total_energy()
    print(EnergyBefore,EnergyAfter)