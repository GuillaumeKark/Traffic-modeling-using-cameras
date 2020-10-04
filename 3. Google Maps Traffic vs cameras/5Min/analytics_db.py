# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 13:27:17 2020
@author: Guillaume Karklins
Comment: This file merges input and output gates data and export graph and stats.
"""
import pandas as pd

#define your local path
PATH = ""

maps = pd.read_csv(PATH+"test_output.csv")
inp = pd.read_excel(PATH+"input_gate.xlsx")
out = pd.read_excel(PATH+"output_gate.xlsx")


out_time = out[["Crossing events for gate with ID 3. Columns: Track ID"," Time [s]"]]
out_time = out_time.rename(columns={"Crossing events for gate with ID 3. Columns: Track ID": "id", " Time [s]": "o_time"})

inp_time = inp[["Crossing events for gate with ID 1. Columns: Track ID"," Time [s]"]]
inp_time = inp_time.rename(columns={"Crossing events for gate with ID 1. Columns: Track ID": "id", " Time [s]": "i_time"})

#KEEP IN MIND
#Some vehicles are coming from the perpendicular street and some are leaving on the perpendicular street
#Therefore we need to inner join the tables to keep only the vehicles at the input and output
#This also removes undetected vehicles at the outut
merged = pd.merge(inp_time,out_time, on=["id", "id"])
merged["diff"] = merged["o_time"]-merged["i_time"]

#First Json query was at 10 seconds and last was at 310 seconds
maps["sync_vid"] = 10.0 + maps.index * 30


pre_plot1 = maps[["sync_vid","duration_in_traffic"]]
pre_plot1 = pre_plot1.rename(columns={"sync_vid": "time", "duration_in_traffic": "duration"})
pre_plot1["api"] = 1

pre_plot2 = merged[["i_time","diff"]]
pre_plot2 = pre_plot2.rename(columns={"i_time": "time", "diff": "duration"})
pre_plot2["api"] = 0

plot_table = pd.concat([pre_plot1, pre_plot2])

#chart
import matplotlib.pyplot as plt
plot_table.plot(kind="scatter", x="time", y="duration", c="api", cmap=plt.get_cmap("jet"), colorbar=False, alpha=1)
plt.legend()
plt.show()


#stats
stats_duration = pre_plot2["duration"].describe()
stats_duration.to_excel(PATH + "stats.xlsx", index=True)

