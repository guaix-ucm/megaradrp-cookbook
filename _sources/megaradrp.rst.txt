
MEGARA Data Reduction Pipeline
==============================

|image1|

**Figure 3:** *Data processing scheme of the MEGARA DRP.*

The deployment of the MEGARA instrument at GTC was accompanied
by the installation of a fully functioning Data Reduction Pipeline (DRP
hereafter) developed in Python that worked both online at the telescope
and offline. The online version of the DRP allows for on-the-fly data
processing, which includes bias correction, trimming, fiber tracing and
fixed-aperture extraction, fiber-flat and twilight-flat correction and
wavelength calibration. The offline processing (to which this cookbook
is devoted) additionally includes a detailed cross-talk-corrected
extraction and absolute flux calibration whenever possible. The MEGARA
DRP can be obtained through *github* at
https://github.com/guaix-ucm/megaradrp (section 3). Line lists and the
CCD Bad-Pixels Mask (BPM) are available at
https://zenodo.org/record/2270518.

The MEGARA DRP has been designed to cope with all effects associated to
the observation with a fiber-fed spectrograph on which the detection of
the light is done with a Charge-Coupled Device (CCD). These effects
include the removal of the bias level and the dark current associated to
the MEGARA CCD, the tracing and extraction of the flux from each fiber
on the CCD, the variation in the wavelength calibration solution along
the (pseudo-)slit of the spectrograph and the correction from the
variation in sensitivity (from blue-to-red and global) from fiber to
fiber and the determination of the system efficiency. In **Figure 3** we
show the data processing scheme followed by the MEGARA DRP. We note here
that the wavelength calibration is performed quite early on in the
reduction procedure as the correction for blue-to-red variation in
sensitivity has to be done once the wavelength of the light falling in
each pixel and each fiber is known.

The final products of the MEGARA DRP are “reduced” Row-Stacked Spectra
(RSS hereafter) 2D images including for 623 (644) fiber spectra for the
LCB (MOS) mode, all using a common flux calibration and wavelength
solution with constant reciprocal dispersion for all fibers. Based on
the averaged spectrum of all fibers to be used for sky subtraction (by
default all 56 sky fibers in the LCB and all unassigned minibundles in
the case of the MOS) the DRP also generates a sky-subtracted “final” RSS
spectrum. No combo products combining different spectral setups are yet
generated.


.. |image1| image:: _static/image10.png
   :width: 6.63681in
   :height: 3.09306in
