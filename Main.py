from datetime import datetime
import pytz
import numpy as np
import pandas as pd
import pvlib
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters


class SolarCell(object):

    def __init__(self, solar_cell_location, inverter_location, maximum_power):
        self.solar_cell = pd.read_csv(solar_cell_location, index_col=0, parse_dates=True)
        self.inverter = pd.read_csv(inverter_location)
        self.max_power = maximum_power
        self.inverter["Percent"] = self.inverter["Percent"] * self.max_power / 100

    def print_cell(self):
        print(self.solar_cell)

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


solar_cell = SolarCell(r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\ss_testbed_irrad_2012.csv",
                       r"C:\Users\Coco\Desktop\Personal Folder\Study\-MSc\Dissertation\Data\Inverter.csv", 10000)
solar_cell.print_cell()
solar_cell.invert()
solar_cell.print_cell()
