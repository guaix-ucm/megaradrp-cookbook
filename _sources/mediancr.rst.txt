.. _Fixing_CR_median:

*********************************
CR not removed by median stacking
*********************************

The different recipes in MEGARA DRP use by default a median combination of
three or more images to obtain an average exposure and thus eliminate cosmic
rays. However, when exposure times are long, it is not uncommon for the same
pixel to be affected by a cosmic ray in consecutive exposures. For this reason,
a procedure has been introduced to address this issue.


The mediancr method
===================

.. warning::

   It is important to note that the ad hoc method described here is susceptible
   to detecting false positives and should be tested and compared with the
   default method (simple median combination).

   **The method has been tested on a limited subset of images and is not
   guaranteed to work optimally in general cases. Users should be aware of this
   limitation and use the method at their own discretion.**

   By properly adjusting the detection parameters, **typically by trial and
   error**, it is possible to minimize the number of false detections. On the
   other hand, the signal in pixels affected by a false multiple cosmic ray
   detection is replaced by the minimum value at each pixel (across the
   available exposures), so the impact on the combined image is not expected to
   be severe. The benefit of automatically removing pixels affected by more
   than one cosmic ray in the different exposures can outweigh this effect.

   The described method is likely only useful when reducing science images with
   long exposure times. In general, it is not recommended for the reduction of
   calibration images.

The method can only be employed when there are three or more exposures
available, and is based on detecting pixels that simultaneously verify two
different criteria. The first one is shown in the following figure, which is
automically generated in the *work* subdirectory with
the name ``mediancr_diagnostic.png``.

.. image:: _static/mediancr/mediancr_diagnostic.png
   :width: 100%
   :alt: diagnostic diagram to detect cosmic rays in median combination

The three (or more) available individual exposures are arranged into a 3D
stack, from which it is easy to generate 2D images (with the same dimensions as
the individual exposures) that contain the minimum value ``min2d``, maximum
value ``max2d``, and median value ``median2d``. On the vertical axis of the
previous figure, the difference between the ``median2d`` and ``min2d`` of each
pixel is shown, while the horizontal axis displays ``min2d - bias``.  The
different lines correspond to the result of performing numerical simulations
using the gain, readout noise, bias, and the minimum and maximum flatfield
values. These simulations are computed for discrete values of ``min2d - bias``
(represented as filled circles overimposed on the lines).  For each of these
values, the percentiles 50 and 98 are computed. Since the simulated values are
unavoidably noisy, the predictions are fitted using splines (dashed lines,
which are difficult to see unless a zoom is performed). The exclusion boundary
(orange line) is computed by extending the difference between the spline fit to
the percentiles 98 and 50 beyond the spline fit to the percentile 98. This
extension is controlled by a parameter named ``times_boundary_extension`` (see
below).  Pixels that lie above the calculated exclusion boundary are marked as
suspected of having been hit by a cosmic ray in more than one exposure (red x's
in the figure; the total number of pixels is displayed in the legend). An
additional requirement (not shown) is imposed: the considered pixel must have a
``max2d`` value above three times the readout noise (this avoids pixels with
negative signal very close to the bias level in the raw images).

**The signal in the suspected pixels is replaced, in the** ``median2d``
**image, by the corresponding** ``min2d`` **value.** This means that the
resulting image is identical to ``median2d``, except for those corrected
pixels.

To apply this combination method, it is necessary to explicitly specify that
``mediancr`` should be used (instead of the default ``median`` method) 
in the requirements list of the observation result file. For example:

.. literalinclude:: files/8_LcbImage_mediancr.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 9-22

It is important to note that, in addition to specifying the method as ``method:
mediancr``, some additional parameters must also be provided under the
``method_kwargs:`` key, in particular:

- ``gain``: the detector gain (electron/ADU). Although the MEGARA detector
  exhibits two different gains (1.60 and 1.73; one value for each detector
  half), here we can use a single value.  This is not critical because the two
  values are not very different and the detection criterium is more sensitive
  to the following parameters.
- ``rnoise``: the readout noise (ADU)
- ``bias`` (default value 0.0): bias value (ADU). **This must be set to zero
  for MEGARA because the code that applies the mediancr method receives
  preprocessed exposures where the bias level has already been subtracted.**
- ``flatmin`` (default 1.0): the minimum simulated normalized flatfield value.
- ``flatmax`` (default 1.0): the maximum simulated normalized flatfield value.
- ``times_boundary_extension`` (default 3.0): number of times that the vertical
  distance between the percentiles 98 and 50 of the simulated data is employed
  to define the exclusion boundary beyond the percentile 98.
- ``interactive`` (default False): if True, the code generates an interactive
  matplotlib plot with the diagnostic diagram (allowing the user to use the
  zoom and pan buttons). It is very convenient to set this parameter to True,
  interactively examine the diagnostic diagram, stop the program execution, and
  try changing the values of ``flatmin``, ``flatmax``, and
  ``times_boundary_extension``. Other parameters such as ``rnoise`` and
  ``gain`` can also be modified, although the user should take into account
  that the objective is to find an automatic way to select uncorrected cosmic
  rays, not to make use of realistic values of gain, readout noise or flatfield
  variation. Note that the values of ``flatmin`` and ``flatmax`` can be used
  to allow the simulations to account, to some extent, for the effect of signal
  variations in different MEGARA exposures. This can happen, for example, in
  sky lines (when exposure times are long), or due to small shifts in the
  telescope pointing.
- ``dilation`` (default 1): the pixels composing each cosmic ray can be
  surrounded by a dilation factor, which expands the mask around the detected
  cosmic ray pixels. A value of zero means that no dilation is applied.
  Typically a value of 1 is useful, since it allow to replace the tails of
  cosmic rays (whose pixels exhibit a lower signal).
- ``plots`` (default False): if True, a PDF file called 
  ``mediancr_identified_cr.pdf`` is
  generated with the individual double cosmic rays identified.
  Note that enabling this option may introduce a noticeable penalty in
  execution time.
- ``semiwindow`` (default 15): the semiwindow size to plot the double cosmic
  rays. Only used if ``plots`` is True.
- ``color_scale`` (default minmax): the color scale employed in the
  ``mediancr_identified_cr.pdf`` images. Only used if ``plots`` is True. The
  valid options are minmax and zscale.
- ``maxplots`` (default 10): the maximum number of suspicious cosmic rays to
  display. Note that setting a limit is useful when experimenting with the
  previous values of ``gain``, ``rnoise``, etc., as it prevents
  generating an excessively large number of plots due to false positive
  detections. A negative value indicates that all the suspected double CR are
  displayed. This option is only used if ``plots`` is True.

Pixels suspected of having been affected by cosmic rays in two of the
available exposures are grouped when they form a connected cluster. These are
then sorted using the detection criteria, so they can be displayed in order,
starting with the pixels most likely to have been affected by two cosmic rays.
For each case, a figure like the one shown below is generated.

.. image:: _static/mediancr/mediancr_identified_cr.png
   :width: 100%
   :alt: example of pixels affected by two cosmic rays in a group of 3 exposures

The first row shows the three individual exposures available in this example.
In the second row, the left image presents the simple median combination, the
center image shows the pixels detected as affected by two cosmic rays
(surrounded by a 1-pixel-wide border), and the right image displays the median
combination with the affected pixels replaced by the minimum value from the
individual exposures.
