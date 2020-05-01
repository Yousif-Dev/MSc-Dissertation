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
            # Now we need to multiply Efficiency by it.
            self.solar_cell.at[dateandtimeValue, "GHI"] = GHIValue * \
                                                          self.inverter.at[
                                                              result_index, "Efficiency"] / 100
            #Clipping the data
            if self.solar_cell.at[dateandtimeValue, "GHI"] > self.max_power:
                self.solar_cell.at[dateandtimeValue, "GHI"] = self.max_power
    def total_energy(self):
        return (self.solar_cell["GHI"].sum())

if __name__ == "__main__":
    list = [100,10000]
    for i in list:
        solar_cell_IGBT = SolarCell(
        r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\ss_testbed_irrad_2012.csv",
        r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\IGBT.csv", i)

        EnergyBefore = solar_cell_IGBT.total_energy()
        solar_cell_IGBT.invert(option="normalise")
        EnergyAfter = solar_cell_IGBT.total_energy()
        print(i, "IGBT" , EnergyBefore,EnergyAfter, EnergyAfter/EnergyBefore)
        solar_cell_SIC = SolarCell(
            r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\ss_testbed_irrad_2012.csv",
            r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\SIC.csv", i)

        EnergyBefore = solar_cell_SIC.total_energy()
        solar_cell_SIC.invert(option="normalise")
        EnergyAfter = solar_cell_SIC.total_energy()
        print(i, "SIC", EnergyBefore, EnergyAfter, EnergyAfter/EnergyBefore)

