"""Draw flights from Tallinn Airport in 2020 and 2023."""

import pandas

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
from typing import Literal

FONT_SIZE = 6
LINE_WIDTH = 1
LINE_ALPHA = 0.6
DPI = None  # reduce this if it takes too long for the program to finish, must be less than 2 ** 16 / 10
TEXT_OFFSET = 0, -7  # relative to its marker
OUTPUT_FILENAME = "mapped_flightsbad.png"

flights20 = pandas.read_csv("otselennud20.csv", sep=",")
flights23 = pandas.read_csv("otselennud23.csv", sep=",")
airports = pandas.read_csv("airports.dat", sep=",").drop("City", axis="columns")

flights20 = flights20.merge(right=airports, on="IATA")
flights23 = flights23.merge(right=airports, on="IATA")

with open("flights20.csv", "w", encoding="utf-8") as f:
    f.write("".join(flights20.to_csv(index=False).split("\n")))

with open("flights23.csv", "w", encoding="utf-8") as f:
    f.write("".join(flights23.to_csv(index=False).split("\n")))

fig: Figure = plt.figure(figsize=(10, 7), dpi=DPI)

# create a Basemap object with Europe's coordinates
m = Basemap(llcrnrlon=-25, llcrnrlat=24,
            urcrnrlon=45, urcrnrlat=72, resolution="l")

# draw coastlines, political boundaries and oceans
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawlsmask(ocean_color="lightblue")

tallinn_lat, tallinn_lon = 59.41329956049999, 24.8327999115
xy_start = m(tallinn_lon, tallinn_lat)

ax: Axes = plt.gca()


def draw_flights(*,
                 line_style: Literal["-", "--", "-.", ":"],
                 line_color: str,
                 marker_color: str,
                 marker_size: int):
    if destination.get("City") == "Tallinn":
        return

    dest_lat = destination.get("Latitude")
    dest_lon = destination.get("Longitude")

    # draw curved line from Tallinn to the destination
    m.drawgreatcircle(tallinn_lon, tallinn_lat, dest_lon, dest_lat, ls=line_style, linewidth=LINE_WIDTH,
                      color=line_color, alpha=LINE_ALPHA)

    # draw marker and add a label to the destination coordinates
    xy_end = m(dest_lon, dest_lat)
    m.plot(*xy_end, marker="o", color=marker_color, markersize=marker_size)
    ax.annotate(destination.get("City"), xy=xy_end, xytext=TEXT_OFFSET, textcoords="offset points",
                fontsize=FONT_SIZE, color="black")


destinations = []

# map flights in 2020
for i, destination in flights20.iterrows():
    destinations.append(destination.get("City"))
    draw_flights(line_style="-", line_color="red", marker_color="blue", marker_size=4)

# map flights in 2023
for i, destination in flights23.iterrows():
    if destination.get("City") in destinations:
        m_size = 2
    else:
        m_size = 4
    draw_flights(line_style="--", line_color="green", marker_color="red", marker_size=m_size)

# draw Tallinn's marker and add its label
ax.annotate("Tallinn", xy=xy_start, xytext=TEXT_OFFSET, textcoords="offset points", fontsize=FONT_SIZE, color="black")
m.plot(*xy_start, marker="o", markersize=4, color="magenta")

plt.title("Flights from Tallinn Airport in years 2020 and 2023 by Andreas Marten Viks")

legend_handles = []
legend_labels = []

# create a red line with a blue marker for flights in 2020
line_20, = ax.plot([], [], linestyle="-", linewidth=LINE_WIDTH, color="red")
marker_20, = ax.plot([], [], marker="o", linestyle="None", markersize=3, color="blue")
legend_handles.append((line_20, marker_20))
legend_labels.append("Flights in 2020")

# create a green dashed line with red markers for flights in 2023
line_23, = ax.plot([], [], linestyle="--", linewidth=LINE_WIDTH, color="green")
marker_23, = ax.plot([], [], marker="o", linestyle="None", markersize=3, color="red")
legend_handles.append((line_23, marker_23))
legend_labels.append("Flights in 2023")

# add the legend to the plot
ax.legend(legend_handles, legend_labels, loc="upper right", fontsize=8)

# save the map to a file
fig.savefig(OUTPUT_FILENAME)
