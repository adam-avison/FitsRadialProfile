#CODE CREATED BY A.AVISON 20-APR-2018#

import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from astropy.io import fits

#--- FITSNAME ---#
fitsName="fix_N7027.JVLA+eMer.eq.image.fits"

#---get fits image data---#
hdulist = fits.open(fitsName)

imData=hdulist[0].data
imData[np.isnan(imData)] = -0.0005 #== set NaNs to something which is a real number
roughSigma=np.median(imData[np.where(imData>0.0)])#=== takes the median non-zero values as a pseudoRMS
levs=np.arange(5.0,55.0,10.0)*roughSigma

#=== DEFINE CeNTRAL POSTION
y_peak=1043  #in pixels
x_peak=990   #in pixels
cutLen=500.0 #in pixels
#-- Plot...
fig, axes = plt.subplots(ncols=2, figsize=[12,6])
axes[0].imshow(imData,cmap='bone',origin='lower')#'gist_ncar'
axes[0].contour(imData,colors='w',linewidths=0.5,levels=levs)

#-- Extract data values along the line...
# Make a line with "num" points...
numCuts=6
angPerCuts=180.0/float(numCuts)

for ang in range(numCuts):
    x1=x_peak-float(np.floor(cutLen*np.cos(np.radians(float(ang)*angPerCuts))))
    y1=y_peak-float(np.floor(cutLen*np.sin(np.radians(float(ang)*angPerCuts))))

    x0=x_peak+float(np.floor(cutLen*np.cos(np.radians(float(ang)*angPerCuts))))
    y0=y_peak+float(np.floor(cutLen*np.sin(np.radians(float(ang)*angPerCuts))))

    num = int(cutLen)
    x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
    # Extract the values along the line, using cubic interpolation
    zi = 0
    zi = scipy.ndimage.map_coordinates(imData, np.vstack((x,y)))

    axes[0].plot(y,x, '-',linewidth=1.0,alpha=0.8,label=str(float(ang)*angPerCuts)+"degrees")
    axes[0].plot(y1,x1, 'g.',linewidth=1.0,alpha=0.05)
    axes[1].plot(zi,'-',alpha=0.8,linewidth=1.0,label=str(float(ang)*angPerCuts)+"degrees")

axes[1].set_xlim([0,cutLen])

#=== OVERLAY 1/r^x models ===#
axes[1].legend()
plt.show()
hdulist.close()
