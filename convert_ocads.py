import gsw
# import xarray as xr
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import glob
# import matplotlib.dates as mdates
# import common_functions as cfun
import os as os
import subprocess
import shutil
import os.path, time
import datetime as datetime
from datetime import date
import decimal
from statistics import mode


def decimal_places(number):
    return np.absolute(decimal.Decimal(str(number)).as_tuple().exponent)


def mode_decimals(var):
    array_places = np.zeros(shape=len(var.iloc[:, 0]))
    for i in range(len(var.iloc[:, 0])):
        if pd.isna(var.iloc[i, 0]):
            continue
        else:
            places = decimal_places(var.iloc[i, 0])
            array_places[i] = places
    print(int(mode(array_places)))
    return int(mode(array_places))


os.chdir('/home/hourstonh/Documents/OCADS/todo')

ocads_data = pd.read_csv('./amended_2015-09Carbon.csv', header=[0, 1],
                         skiprows=0, na_values=-999)
print(ocads_data.iloc[0, :])
print(ocads_data.OXYGEN)


# 1 ml/l = 103/22.391 = 44.661 μmol/l
print(ocads_data.CTDSAL)
print(ocads_data.CTDPRS)
sa = gsw.SA_from_SP(ocads_data.CTDSAL, ocads_data.CTDPRS, ocads_data.LONGITUDE, ocads_data.LATITUDE)
pt = gsw.pt_from_t(sa, ocads_data.CTDTMP, ocads_data.CTDPRS, 0)
ct = gsw.CT_from_pt(sa, pt)
print(sa)
print(ct)
print(ocads_data.CTDPRS)
density = gsw.rho(sa, ct, ocads_data.CTDPRS)
print(density)


# 44.661 to convert to umol/l then convert to umol/kg
if ocads_data.CTDOXY.columns[0].upper() == '(ML/L)':
    ocads_data['CTDOXY_2'] = ocads_data.CTDOXY * 44.661 / density * 1000.
    ctdoxy_digits = mode_decimals(ocads_data['CTDOXY'])
    ocads_data['CTDOXY_2'] = ocads_data['CTDOXY_2'].round(decimals=ctdoxy_digits)
if ocads_data.OXYGEN.columns[0].upper() == '(ML/L)':
    ocads_data['OXYGEN_2'] = ocads_data.OXYGEN * 44.661 / density * 1000.
    oxygen_digits = mode_decimals(ocads_data['OXYGEN'])
    ocads_data['OXYGEN_2'] = ocads_data['OXYGEN_2'].round(decimals=oxygen_digits)


ocads_data['NO2+NO3_2'] = ocads_data['NO2+NO3'] / density * 1000.
ocads_data['SILCAT_2'] = ocads_data['SILCAT'] / density * 1000.
ocads_data['PHSPHT_2'] = ocads_data['PHSPHT'] / density * 1000.

no2_no3_digits = mode_decimals(ocads_data['NO2+NO3'])
silcat_digits = mode_decimals(ocads_data['SILCAT'])
phspht_digits = mode_decimals(ocads_data['PHSPHT'])

ocads_data['NO2+NO3_2'] = ocads_data['NO2+NO3_2'].round(decimals=no2_no3_digits)
ocads_data['SILCAT_2'] = ocads_data['SILCAT_2'].round(decimals=silcat_digits)
ocads_data['PHSPHT_2'] = ocads_data['PHSPHT_2'].round(decimals=phspht_digits)

ocads_data.to_csv('./amended_2015-09Carbon_data.csv', na_rep=-999)