from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import numpy as np
%matplotlib auto
# Import data
odata = np.loadtxt('O-polar_ZnO/PL_430.txt', skiprows=1).T
zndata = np.loadtxt('Zn-polar_ZnO/PL_430.txt', skiprows=1).T
# Import calibration spectrum
calib = np.loadtxt('Zn-polar_ZnO/calib.txt', skiprows=1).T
# find peaks in calibration spectrum
peaks, params = find_peaks(calib[1], prominence=1000)
# create figure
fig = plt.figure()
ax = fig.add_subplot(111)

# Verify that the correct peaks were found
# ax.plot(*calib)
# ax.plot(peaks,calib[1][peaks],'x')

# Assign peaks in calibration to proper wavelengths
P = [435.83, 404.66, 365.02]


def linear(x, m, b):
    return m * x + b


# Linear fit of pixel values and wavelengths
fit, cov = curve_fit(linear, peaks, P)
# Conversion function from pixel space to eV space


def p2eV(pixel):
    return 1240 / (pixel * fit[0] + fit[1])


# save some finger strength
eV = p2eV(odata[0])
# plot data
plt.plot(eV, odata[1], label='O-Polar')
plt.plot(eV, zndata[1], label='Zn-Polar')
# set plot parameters
ax.set(xlabel='Photon Energy (eV)', ylabel='Counts (a.u.)')
# Find peaks in spectrum
znpeaks, znparams = find_peaks(zndata[1], prominence=100)
# Get rid of unwanted peaks
znpeaks = znpeaks[2:]
# Plot peak values on same plot as spectra
[plt.plot(p2eV(i), zndata[1][i], 'x',
          label=f'{p2eV(i):.3f}eV') for i in znpeaks]
plt.legend()
plt.show()
