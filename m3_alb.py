import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from math import log10, floor
import sympy as sym

# Exponential regression function assuming c=0
def exp(x, a, b, p=np.e):
    # a * e ** (b * x), assuming c = 0
    return a * p ** (b * x)

# Exponential regression given actual X and Y; returns (a, b) as a tuple
def exp_reg(X, Y, p0):
    # p0 is the initial guess
    popt, pcov = curve_fit(exp, X, Y, p0=p0)
    return popt

# Round x to 5 sig figs
def round5(x):
    return round(x, 4-floor(log10(abs(x))))

# Albuquerque housing units from the original attached data
X1 = np.array([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022], dtype=float)
Y1 = np.array([234.891, 237.735, 239.718, 240.277, 240.961, 241.326, 242.070, 243.402, 244.382, 245.476, 247.926, 252.924, 255.178], dtype=float)

# Find fit of the regression and calculate y_pred for the x values that will be graphed
a, b = exp_reg(X1, Y1, p0=(.002, .006))  # These constants are optional; we picked them so that the regression would calculate faster
X = np.arange(2005, 2080, .01)
Y = exp(X, a, b)

# Create latex equation to be displayed
xs = sym.Symbol('x')
es = sym.Symbol('e')
tex = sym.latex(exp(xs, round5(a), round5(b), p=es)).replace('$', '')

# Print predictions for 10, 20, and 50 years in the future
for x in [2024+10, 2024+20, 2024+50]:
    print(x, round(1000*exp(x, a, b)))

# Plot historical data and line of best fit
plt.figure(figsize=(6, 4))
plt.plot(X, Y, '-r', label='Historical data')
plt.plot(X1, Y1, 'xk', label=f'Fit: ${tex}$')
plt.xlabel('Year')
plt.ylabel('Thousands of housing units')
plt.title(f'Albuquerque housing unit predictions R-sq=0.909')  # R-squared calculated using Desmos
plt.legend()
plt.show()