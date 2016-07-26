#
# Written by Rahul Palamuttam <rahulpalamut@gmail.com>
# last revision: 2016-7-26
#

import numpy as np
import matplotlib as mlb
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_pdf import PdfPages

"""
    Numer.ai is a stock market prediction competition... yada yada yada.
    You can find more details here : http://numer.ai/
    HistogramPlots.py takes the csv data in numerai_training_data.csv and plots
    histograms of the 21 features in a PDF.

    Each PDF page consists of 3 rows of plots. Each row corresponds to a feature.
    Each of the three plots in a row consists of:
    1. cumulative histogram for the feature
    2. histogram of feature points labeled true
    3. labeled of feature points labeled false

    The script initially sets the tick label sizes to 5 for readability purposes.
"""

mlb.rcParams['xtick.labelsize'] = 5
mlb.rcParams['ytick.labelsize'] = 5

def plot_histogram(feature, bins, plot, feature_title, color):
    """
        Plots a histogram.
    """
    mu, sigma = round(np.mean(feature), 4), round(np.std(feature), 4)
    n, bins, patches = plot.hist(feature, bins, normed=False, facecolor=color)
    y = mlab.normpdf(bins, mu, sigma)
    l = plot.plot(bins, y, 'r--', linewidth=1)
    plot.set_title(feature_title + ' : avg = ' + str(mu) + ' std = ' + str(sigma), fontsize=8)
    plot.grid(True)

def save_pdf_page(training_df, pdf, starting_feature, plots_per_page):
    """
        Saves plots to one page of pdf.
    """
    f, axarr = plt.subplots(plots_per_page, 3)
    for i in range(starting_feature, starting_feature + plots_per_page):
        feature1 = training_df[:, i]
        feature1_true = training_df[training_df[:, 21] == 1, i]
        feature1_false = training_df[training_df[:, 21] == 0, i]
        plot_histogram(feature1, 100, axarr[i - starting_feature, 0], "Ftr " + str(i), "blue")
        plot_histogram(feature1_true, 100, axarr[i - starting_feature, 1], "Ftr " + str(i) + " True", "green")
        plot_histogram(feature1_false, 100, axarr[i - starting_feature, 2], "Ftr " + str(i) + " False", "red")
    pdf.savefig(f)
    plt.close()

def run():
    pdf = PdfPages('multipage_pdf.pdf')
    pages = 7
    training_df = np.loadtxt("numerai_training_data.csv", skiprows=1, usecols=np.arange(0,22), delimiter=",")
    for i in range(0, pages):
        save_pdf_page(training_df, pdf, i * 3, 3)
    pdf.close()
    print "done"

run()