import csv
import numpy as np
from matplotlib import pyplot as plt
import plotly.plotly as py

fname = "data11.csv"
file = open(fname, "rb")

try:
    reader = csv.reader(file)
    fit_mean = []
    fit_best = []
    iterations = []
    for row in reader:
        if row[1] == "mean":
            fit_mean.append(row[3])
            iterations.append(row[0])
        elif row[1] == "best":
            fit_best.append(row[3])

    plt.plot(iterations, fit_mean, '--', linewidth=2)
    plt.plot(iterations, fit_best, '--', linewidth=2)
    plt.ylabel('some numbers')

    plt.show()

finally:
    file.close()
