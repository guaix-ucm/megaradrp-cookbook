.. _Fixing_CR_median:

*********************************
CR not removed by median stacking
*********************************

.. warning::

  This functionality is still in the development phase and is not yet fully 
  consolidated. Some future modifications may be introduced as more testing 
  is conducted with new images.

The different recipes in MEGARA DRP use by default a median combination of
three or more images to obtain an average exposure and thus eliminate cosmic
rays. However, when exposure times are long, it is not uncommon for the same
pixel to be affected by a cosmic ray in consecutive exposures. 

The most obvious initial solution is to closely examine the resulting image
(e.g., the ``final_rss.fits`` file) and interpolate the defective pixels using
information from neighboring pixels. However, it may be useful to employ a
procedure that automatically detects and corrects pixels affected by cosmic
rays in consecutive images, so that manual interpolation is not necessary. An
automatic procedure of this kind has been introduced in the **numina** package,
which can be easily invoked by modifying the default image combination method
used by MEGARA DRP.

.. note::

   It is important to note that the ad hoc method described here is susceptible
   to detecting false positives and should be tested and compared with the
   default method (simple median combination).

   **The method has been tested on a limited subset of images and is not
   guaranteed to work optimally in general cases. Users should be aware of this
   limitation and use the method at their own discretion.**

   By properly adjusting the detection parameters, **typically by trial and
   error**, it is possible to minimize the number of false detections. On the
   other hand, the signal in pixels affected by a false multiple cosmic ray
   detection is replaced either by the minimum value at each pixel (across the
   available exposures) or by the median (depending on the chosen combination
   method), so the impact on the combined image is not expected to
   be severe. The benefit of automatically removing pixels affected by more
   than one cosmic ray in the different exposures can outweigh this effect.

   The described method is likely only useful when reducing science images with
   long exposure times. In general, it is not recommended for the reduction of
   calibration images.

Overall description
===================

The method can only be employed when there are three or more **equivalent**
exposures available, and is based on detecting pixels that exhibit an 
unexpected location in a diagnostic diagram built using the median and the 
minimum signal of each pixel across the different exposures.

For the method to work correctly, it is necessary to ensure that the different
exposures are really equivalent, meaning that they should exhibit the same
signal level at each pixel except the expected random noise. Small changes in
the signal level between the different exposures can be tolerated, but large
differences can lead to a large number of false positives.

The method is intended to be used with the MEGARA DRP, although it can also
be applied directly from the command line using the **numina** script
``numina-crmasks``, which is also described later in this document.

The main workflow to apply the method is as follows:

1. **Prepare the observation result file**: The YAML file that contains the
   list of individual exposures and additional requirements for a specific
   reduction recipe associated to the observing mode
   ``mode: MegarCrDetection``.
2. **Run the MEGARA DRP to generate the CR masks**: The execution of the MEGARA
   DRP with this YAML file is interactive (see below), and the result if a FITS
   file, called ``crmasks.fits`` that contains several masks that can be
   employed later to remove the cosmic rays using different strategies. This
   file must be copied to the `data/` subdirectory.
3. **Run the MEGARA DRP to generate the reduced scientific result**: Once the
   file ``crmasks.fits`` is in the `data/` subdirectory, the MEGARA DRP can
   be run again to generate the reduced scientific result, using for that
   purpose the corresponding YAML file. In this step, the user should choose
   between the different available strategies to combine and remove the cosmic
   rays. In particular, instead of assuming that the combination method is
   ``median``, the user should specify one of the following methods in the
   requirements section: ``mediancr``, ``meancrt`` or ``meancr``.

.. note::

   The three available combination methods, ``mediancr``, ``meancrt`` and 
   ``meancr``, produce different results:

   - ``mediancr``: provides the median combination, replacing pixels 
     suspected of having been affected by a cosmic ray in more than one
     exposure by the minimum value at each pixel across the available exposures.
   - ``meancrt``: generates the mean combination, making use of a single mask 
     that stores the cosmic rays detected in all the individual exposures,
     replacing the masked pixels by the value obtained when using
     the ``mediancr`` method.
   - ``meancr``: provides the mean combination, making use of an individual 
     mask specifically computed for each available exposure.

   Since the mean has a lower standard deviation than the median, the 
   ``meancrt`` and ``meancr`` methods are initially preferable. Among these
   two, the tests conducted suggest that the ``meancr`` method tends to yield better
   results. In any case, it is recommended to use all three combination
   methods and compare the resulting outputs.

Preparing the observation result file
=====================================

Let's assume that we have three initially equivalent exposures. The initial
YAML file is ``8_generate_crmasks.yaml``, which contains the list of
individual exposures.

.. literalinclude:: files/8_generate_crmasks_1.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2

This initial file is quite simple: one only has to take care of specifying
``mode: MegarCrDetection``, so the MEGARA DRP will know that the
``8_generate_crmasks.yaml`` file is intended to generate the CR masks. The
other important point is to ensure that the list of individual exposures
contains three or more equivalent exposures.

Computing the CR masks
======================

Initial execution
-----------------

The recipe is run by doing:

.. code-block:: console

   (megara) $ numina run 8_generate_crmasks.yaml -r control.yaml

After some time (typically around one minute, that is needed to perform
the required numerical simulations), the program generates the
following plot, showing the diagnostic diagram to detect double cosmic rays
in the median combination. This plot is saved in the *work* subdirectory
with the name ``diagnostic_histogram2d.png``. The figure is also displayed, so
the user can interactively examine it and stop the program execution if
necessary.

.. image:: _static/crmasks/diagnostic_histogram2d_1.png
   :width: 100%
   :alt: diagnostic diagram to detect double cosmic rays in median combination

The three (or more) available individual exposures are arranged into a 3D
stack, from which it is easy to generate 2D images (with the same dimensions as
the individual exposures) that contain the minimum value ``min2d``, maximum
value ``max2d``, and median value ``median2d`` at each pixel along the sequence
of available exposures. On the vertical axis of the previous figure, the
difference between the ``median2d`` and ``min2d`` of each pixel is shown, while
the horizontal axis displays ``min2d - bias``.  

Note that the diagnostic diagram, which is actually a 2D histogram in the 
previous plot, is shown twice: the left image is the result
of running a predefined number of simulations (10 in this example; this number
can be modified), using the `median2d` data to generate synthetic exposures, 
using for that purpose the gain, readout noise and bias values. Note that in
the case of MEGARA, the individual exposures are preprocessed prior to the
generation of the diagnostic diagram, including overscan subtraction, trimming, 
and gain correction (data is transformed from ADU to electrons). For that 
reason, the code assume that gain=1.0, the readout noise = 3.4 electrons
(see the keywords RDNOISE1 and RDNOISE2 in the FITS headers), and bias = 0
electrons.

The right image is directly the same diagnostic diagram, but using the actual
data from the individual exposures.

Returning to the left image, at each bin in the horizontal axis, the histogram
data is converted to a cumulative distribution function (CDF), and the red 
crosses indicate the ``median2d - min2d`` values at which the probability of 
finding a single pixel above them is low enough so one only expects one pixel 
to be above those values. The blue solid line is a spline fit to the red
crosses. The orange, green and red lines are an extension of the blue line
to be placed above the red crosses (this is performed by adding a different
weight to the vertical distance between the fitted points, depending on their
location above/below the previous fit). The resulting final fit can be employed
to define a detection boundary, so pixels that lie above this line are
suspected of having been affected by a cosmic ray in more than one exposure.

The detection boundary is plotted again in the right image. In this
case we can see that there are a very large number of pixels above the
detection boundary, which is not a good sign. This means that the different
exposures are not equivalent, and the method will likely produce a large
number of false positives. In this case, it is recommended to stop the
execution, modify the YAML file to include the option to rescale the images,
and run the program again.

Checking the flux level of the individual exposures
---------------------------------------------------

We accomplish this by adding the requirement 
``flux_factor: auto``. By default, this parameter is set to ``none``, which
means that all the exposures are assumed to be equivalent (internally the
code transforms this parameter to ``1.0`` for each exposure).

.. literalinclude:: files/8_generate_crmasks_2.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 8-9

.. code-block:: console

   (megara) $ numina run 8_generate_crmasks.yaml -r control.yaml

In this case, the program generates new 2D histograms, computing the number
of pixels for different reasonable combinations of the ratio between each
individual exposure and the median of the three exposures. In principle, this
ratio should be close to 1.0, but the program examines a range between 0.5 and
1.5.

.. image:: _static/crmasks/flux_factor1.png
   :width: 100%
   :alt: computation of the flux factor for the first exposure

.. image:: _static/crmasks/flux_factor2.png
   :width: 100%
   :alt: computation of the flux factor for the second exposure

.. image:: _static/crmasks/flux_factor3.png
   :width: 100%
   :alt: computation of the flux factor for the third exposure

The 2D histograms is shown twice: the left image is the actual histogram, 
whereas the right image is the first histogram after applying a cleaning
procedure to remove isolated pixels. The program then computes a spline fit at
each side of the vertical bin that contains the 1.0 value (blue and red
solid lines), and finds the mode
at both sides (above and below the 1.0 value). This helps to determine an
approximate scaling factor that takes into account the flux corresponding to
the pixels with the higher signal.

In this example, it seems clear that the first exposure exhibits a lower flux
(by a factor of around 0.78), the second exposure is very close to the unity
(factor 1.01), and the third exposure is slightly higher (factor 1.11). These
factors are then employed when generating the simulated diagnostic diagram,
which in this case is more similar to the one generated using the actual data
from the individual exposures.

.. image:: _static/crmasks/diagnostic_histogram2d_2.png
   :width: 100%
   :alt: diagnostic diagram to detect double cosmic rays in median combination

When necessary, the flux factors can be specified directly specified as a 
requirement in the YAML file, as follows: ``flux_factor: [0.78, 1.01, 1.11]``
(with one value of each individual exposure).

Note that the detection boundary in the last diagnostic diagram is extended
below zero and above the maximum value of the ``min2d - bias`` axis.

Detecting suspected double cosmic rays in the median combination
----------------------------------------------------------------

Once we are satisfied with the comparison of the diagnostic diagrams
corresponding to the simulated and actual data, the program proceeds with the
computed detection boundary.

The diagnostic diagram is shown again, but in this case not as a 2D histogram,
but as a scatter plot, where the red crosses indicate the pixels that are
suspected of having been affected by a cosmic ray in more than one exposure,
with the total number of affected pixels displayed in the legend. This plot
is saved in the *work/* subdirectory with the name ``diagnostic_mediancr.png``.

.. image:: _static/crmasks/diagnostic_mediancr.png
   :width: 100%
   :alt: diagnostic diagram for mediancr

In this particular example, 256 pixels have been flagged as suspected of
having been affected by a cosmic ray in more than one exposure. These pixels
are then surrounded by a 1-pixel-wide border, so nearby pixels that are
only slightly affected by the same cosmic ray can be included. This dilation
factor can be modified by setting the requirement ``dilation`` in the YAML 
file. In this case, the initial 256 pixels are expanded to 1592 pixels after
applying the dilation factor of 1. After this process, these pixels are then 
grouped when they form a connected cluster (each group being an individual CR 
hit affecting contiguous pixels). These CR detections are then sorted using the 
distance above the detection boundary, so they can be displayed in order,
starting with the pixels most likely to have been affected by two cosmic rays.

For each case, a figure like the one shown below is generated in a file
called ``mediancr_identified_cr.pdf`` in the *work* subdirectory. Note that
this figure is not shown interactively, so the user should open it after
the program finishes its execution. By default, only the first 10 suspected
double cosmic rays are displayed, but this can be modified by setting the
requirement ``maxplots`` in the YAML file (a negative number indicates that all the suspected
CR hits should be displayed). In this example, a total of 138 suspected CR
hits have been identified, as indicated in the plot title.

.. image:: _static/crmasks/mediancr_identified_cr.png
   :width: 100%
   :alt: example of pixels affected by two cosmic rays in a group of 3 exposures

The first row shows the three individual exposures available in this example.
In the second row, the left image presents the simple median combination, the
center image shows the pixels detected as affected by two cosmic rays
(surrounded by a 1-pixel-wide border), and the right image displays the median
combination with the affected pixels replaced by the minimum value from the
individual exposures.

Detecting cosmic rays in the mean combination
---------------------------------------------

After the detection of suspected double cosmic rays in the median
combination, the program proceeds to detect suspected cosmic rays in the
mean combination. Note that this ``mean2d`` image contains the CR of all the
individual exposures.

The resulting diagnostic diagram is shown below, where the red crosses indicate the pixels that are suspected of having been affected by a cosmic 
ray in the combined exposure. This plot is saved in the *work/* subdirectory 
with the name ``diagnostic_meancr.png``.

.. image:: _static/crmasks/diagnostic_meancr.png
   :width: 100%
   :alt: diagnostic diagram for mean

The number of pixels suspected of having been affected by a cosmic ray in the
mean combination is, not surprisingly, much larger than what was found in the
median combination. In this case, 82171 pixels have been flagged as suspected of
having been affected by a cosmic ray. This number increases to 296655 when
applying the dilation factor of 1.

Detecting cosmic rays in the individual exposures
-------------------------------------------------

The program also generates diagnostic diagrams for each individual exposure.
These plots are saved in the *work/* subdirectory with the names
``diagnostic_crmask1.png``, ``diagnostic_crmask2.png``, and
``diagnostic_crmask3.png`` (one for each individual exposure). 

.. image:: _static/crmasks/diagnostic_crmask1.png
   :width: 30%
   :alt: diagnostic diagram for first individual exposure

.. image:: _static/crmasks/diagnostic_crmask2.png
   :width: 30%
   :alt: diagnostic diagram for second individual exposure

.. image:: _static/crmasks/diagnostic_crmask3.png
   :width: 30%
   :alt: diagnostic diagram for third individual exposure

In this case, the data plotted in the vertical axis is the initial 
``median2d - min2d`` but scaled by the corresponding flux factor for each 
individual exposure.

When computing the mask for each individual exposure, the code imposes that
the masked pixels in each individual mask must be also masked in the mask
associated to the mean combination previously described.


Output file ``crmasks.fits``
----------------------------

The output file ``crmasks.fits`` is generated in the *results/* subdirectory, 
and contains several extensions:

.. code-block:: console

   (megara) $ cd obsid8_LcbImage_LR-R_crmasks_results
   (megara) $ fitsinfo crmasks.fits
   Filename: crmasks.fits
   No.    Name      Ver    Type      Cards   Dimensions   Format
     0  PRIMARY       1 PrimaryHDU     121   ()      
     1  MEDIANCR      1 ImageHDU         8   (4096, 4112)   uint8   
     2  MEANCRT       1 ImageHDU         8   (4096, 4112)   uint8   
     3  CRMASK1       1 ImageHDU         8   (4096, 4112)   uint8   
     4  CRMASK2       1 ImageHDU         8   (4096, 4112)   uint8   
     5  CRMASK3       1 ImageHDU         8   (4096, 4112)   uint8   

Note the primary HDU only contains keywords with information concerning
the parameters used to generate the masks. The extensions contain the
different masks computed by the program:

- ``MEDIANCR``: the mask for the pixels suspected of having been affected by
  two cosmic rays in the median combination.
- ``MEANCRT``: the mask for the pixels suspected of having been affected by
  a cosmic ray in the mean combination.
- ``CRMASK1``, ``CRMASK2``, ``CRMASK3``: the masks for the pixels suspected
  of having been affected by a cosmic ray in the individual exposures.

In all cases, the pixels suspected of having been affected by a cosmic ray
are set to 1, while the rest of the pixels are set to 0.

Do not forget to copy the file ``crmasks.fits`` to the `data/` subdirectory
before running the MEGARA DRP to generate the reduced scientific result.

.. code-block:: console

   (megara) $ cp crmasks.fits ../data/

Additional program parameters
-----------------------------

The reduction recipe that generates the CR masks assumes several default values
for the relevant parameters. These parameters can be modified by setting their
values in requirements section of the YAML file.

- ``gain``: detector gain (electron/ADU). This parameter is kept in order to
  reuse the code for other instruments. As previously mentioned, since the
  MEGARA exposures are preprocessed prior the CR masks generation (and the
  data converted from ADU to electrons), gain is assumed to be 1.0.
- ``rnoise``: readout noise (ADU). In the case of MEGARA, here the code assumes
  a value of 3.4 electrons, which is the readout noise of the MEGARA detector
  (see the keywords RDNOISE1 and RDNOISE2 in the FITS headers). 
- ``bias`` (default value 0.0): bias value (ADU). This also must be set to zero
  for MEGARA because the bias level is also part of the preprocessing
  performed by the MEGARA DRP.
- ``flux_factor`` (default ``none``): this parameter can be set to a list of
  values, one for each individual exposure, or to ``auto``. If set to ``auto``,
  the program will compute the flux factor for each individual exposure by
  examining the ratio between each individual exposure and the median. 
  If set to ``none``, all the exposures are assumed to be equivalent (i.e., the flux
  factor is set to 1.0 for each exposure). A single float number (e.g. 1.0) can
  also be specified, which means that all the exposures are assumed to have the
  same flux factor.
- ``knots_splfit`` (default 3): total number of knots employed in the spline
  fit employed to define the detection boundary.
- ``nsimulations`` (default 10): number of simulations to perform for each
  set of individual exposures in order to generate the simulated diagnostic
  diagram.
- ``niter_boundary_extension`` (default 3): number of iterations to
  extend the detection boundary above the red crosses in the diagnostic
  diagram.
- ``weight_boundary_extension`` (default 10): weight to apply to the
  vertical distance between the fitted points in the diagnostic diagram when
  extending the detection boundary above the red crosses. The points above the
  previous fit are multiplied by this value raised to the power of the
  iteration number. This forces the fit to accommodate near the upper
  boundary defined by the red crosses in the simulated diagnostic diagram.
- ``threshold`` (default 0.0): minimum threshold for ``median2d - min2d`` in
  the diagnostic diagrams. This is an additional constraint in addition to the
  detection boundary, so pixels that are below this threshold are not
  considered as suspected.
- ``minimum_max2d_rnoise`` (default 5.0): minimum value of ``max2d`` in
  readout noise units to consider a pixel as a double cosmic ray. This avoids
  false positives when a pixel exhibits a large negative value in one of the
  individual exposures.
- ``interactive`` (default True): if True, the code generates interactive
  matplotlib plots, allowing the user to use the
  zoom and pan buttons. If False, the code runs without displaying the plots,
  but they are still saved in the *work/* subdirectory.
- ``dilation`` (default 1): the pixels composing each cosmic ray can be
  surrounded by a dilation factor, which expands the mask around the detected
  cosmic ray pixels. A value of zero means that no dilation is applied.
  Typically a value of 1 is useful, since it allow to replace the tails of
  cosmic rays (whose pixels exhibit a lower signal).
- ``seed`` (default None): the random seed used to generate the simulated
  diagnostic diagram. If None, the seed is randomly generated.
- ``plots`` (default True): if True, a PDF file called
  ``mediancr_identified_cr.pdf`` is generated with some or all the individual 
  double cosmic rays identified.
- ``semiwindow`` (default 15): the semiwindow size (pixels) to plot the double
  cosmic rays. Only used if ``plots`` is True.
- ``color_scale`` (default minmax): the color scale employed in the
  ``mediancr_identified_cr.pdf`` images. Only used if ``plots`` is True. The
  valid options are minmax and zscale.
- ``maxplots`` (default 10): the maximum number of suspicious double cosmic
  rays to display. Note that setting a limit is useful when experimenting with
  the program parameters, as it prevents generating an excessively large number
  of plots due to false positive detections. A negative value indicates that 
  all the suspected double CR are displayed (note that enabling this may 
  introduce a noticeable penalty in execution time). This option is only used 
  if ``plots`` is True.
- ``save_preprocessed`` (default False): if True, the program saves the
  preprocessed individual exposures in the *work/* subdirectory. This is useful
  for debugging purposes, but it is not necessary for the normal operation of
  the program.

Applying the masks
==================

Once the file ``crmasks.fits`` has been generated, it can be used to
remove the suspected double cosmic rays from the combined image. In this sense,
several options are available, depending on the value of ``method`` in the
requirements section of the YAML file used to generate the reduced scientific
result. In this sense, instead of assuming that the combination method is
``median`` (default value in MEGARA DRP), the user should specify one of the 
following methods: ``mediancr``, ``meancr`` or ``meancrt``. 

Method ``mediancr``
-------------------

For example, when using the recipe **MegaraLcbImage**, the corresponding
YAML file, ``8_LcbImage.yaml`` should define the ``method`` and the 
``crmasks`` parameters in the requirements section, as follows:

.. literalinclude:: files/8_LcbImage_mediancr.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2, 9-10

Note that it is necessary to explicitly specify the ``crmasks`` parameter,
which should point to the file ``crmasks.fits`` generated in the previous step.
On the other hand, this allows the user to rename this file, placing different
versions of it generated with different detection boundaries and testing the
effect of using different masks.

.. code-block:: console

   (megara) $ numina run 8_LcbImage.yaml -r control.yaml

When using ``method: mediancr``, the MEGARA DRP will read the mask stored in 
the extension ``MEDIANCR`` of the file ``crmasks.fits``. The masked pixels,
which are suspected of having been affected by a cosmic ray in more that one
exposure, are replaced by the corresponding ``min2d`` value at each pixel
This means that the resulting image is identical to ``median2d``, except 
for those corrected pixels.

Method ``meancrt``
------------------

.. literalinclude:: files/8_LcbImage_meancrt.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2, 9-10

When using ``method: meancrt``, the MEGARA DRP will read the mask stored in 
the extension ``MEANCRT`` of the file ``crmasks.fits``. The masked pixels,
which are suspected of having been affected by a cosmic ray are replaced by 
the corresponding value when using ``method: mediancr``. 

This means that the resulting image is identical to ``mean2d``, except 
for those corrected pixels, where the information is taken from the 
image obtained by applying the ``mediancr`` method.


Method ``meancr``
-----------------

.. literalinclude:: files/8_LcbImage_meancr.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2, 9-10

When using ``method: meancr``, the MEGARA DRP will read the masks stored in 
the extensions ``CRMASK1``, ``CRMASK2`` and ``CRMASK3`` of the file 
``crmasks.fits``. The program makes use of the functionality provided by 
the numpy masked arrays to build a 3D stack of the individual exposures,
where the masked pixels associated to each individual image are employed to
define the corresponding masked array. This allows to compute the mean along
the axis corresponding to the image number, so the resulting image is
the mean of the individual exposures, excluding the masked pixels.

In this case, it is possible to have pixels which are masked in all the
individual exposures. In this case, the resulting pixel in the combined image
will be set to the ``min2d`` value at that pixel.

Using the command line script
=============================

It is also possible to compute the CR masks and to apply them directly in
an arbitray set of images using the command line script
``numina-crmasks``.

For example, one can execute the **MegaraCrDetection** recipe using the
requirement ``save_preprocessed: True`` in the YAML file, so the
preprocessed individual exposures are saved in the *work/* subdirectory 
with the names ``preprocessed_1.fits``, ``preprocessed_2.fits``, and
``preprocessed_3.fits``.

.. code-block:: console

   (megara) $ cd obsid8_LcbImage_LR-R_crmasks_work
   (megara) $ ls preprocessed_*.fits > list.txt
   (megara) $ cat list.txt
   preprocessed_1.fits
   preprocessed_2.fits
   preprocessed_3.fits

The script ``numina-crmasks`` must be executed twice: first to compute the
CR masks, and then to apply them to the individual exposures.

Step 1: masks generation
------------------------

.. code-block:: console

   (megara) $ $ numina-crmasks compute \
   --inputlist list.txt \
   --gain 1.0 \
   --rnoise 3.4 \
   --flux_factor '[0.78, 1.01, 1.11]' \
   --interactive \
   --output_masks crmasks.fits

Note that in this case it is important to specify the gain and readout noise.
The flux factor is also specified: in this case we are providing the individual
values for each individual exposure. Note that the numbers are given as a
quoted string. The output file is called ``crmasks.fits``, but any other
name can be used.

The full list of available parameters can be obtained by executing:

.. code-block:: console

   (megara) $ numina-crmasks compute --help
   usage: numina-crmasks compute [-h] --inputlist INPUTLIST [--gain GAIN]
                                 [--rnoise RNOISE] [--bias BIAS]
                                 [--flux_factor FLUX_FACTOR]
                                 [--knots_splfit KNOTS_SPLFIT]
                                 [--nsimulations NSIMULATIONS]
                                 [--niter_boundary_extension NITER_BOUNDARY_EXTENSION]
                                 [--weight_boundary_extension WEIGHT_BOUNDARY_EXTENSION]
                                 [--threshold THRESHOLD]
                                 [--minimum_max2d_rnoise MINIMUM_MAX2D_RNOISE]
                                 [--interactive] [--dilation DILATION]
                                 [--output_masks OUTPUT_MASKS] [--plots]
                                 [--semiwindow SEMIWINDOW]
                                 [--color_scale {minmax,zscale}]
                                 [--maxplots MAXPLOTS] [--extname EXTNAME]

   options:
     -h, --help            show this help message and exit
     --inputlist INPUTLIST
                           Input text file with list of 2D arrays.
     --gain GAIN           Detector gain (ADU)
     --rnoise RNOISE       Readout noise (ADU)
     --bias BIAS           Detector bias (ADU, default: 0.0)
     --flux_factor FLUX_FACTOR
                           Flux factor to be applied to each image
     --knots_splfit KNOTS_SPLFIT
                           Total number of knots for the spline fit to the
                           detection boundary (default: 3)
     --nsimulations NSIMULATIONS
                           Number of simulations to compute the detection
                           boundary (default: 10)
     --niter_boundary_extension NITER_BOUNDARY_EXTENSION
                           Number of iterations for the extension of the
                          detection boundary (default: 3)
     --weight_boundary_extension WEIGHT_BOUNDARY_EXTENSION
                           Weight for the detection boundary extension (default:
                           10)
     --threshold THRESHOLD
                           Minimum threshold for median2d - min2d to flag a pixel
                           (default: None)
     --minimum_max2d_rnoise MINIMUM_MAX2D_RNOISE
                           Minimum value for max2d in rnoise units to flag a
                           pixel (default: 5.0)
     --interactive         Interactive mode for diagnostic plot (program will
                           stop after the plot)
     --dilation DILATION   Dilation factor for cosmic ray mask
     --output_masks OUTPUT_MASKS
                           Output FITS file for the cosmic ray masks
     --plots               Generate plots with detected double cosmic rays
     --semiwindow SEMIWINDOW
                           Semiwindow size for plotting double cosmic rays
     --color_scale {minmax,zscale}
                           Color scale for the plots (default: 'minmax')
     --maxplots MAXPLOTS   Maximum number of double cosmic rays to plot (-1 for
                           all)
     --extname EXTNAME     Extension name in the input arrays (default:
                           'PRIMARY')

Step 2: masks application
-------------------------

The second step is to apply the generated masks, making use of the desired
combination method: ``mediancr``, ``meancrt`` or ``meancr``. For example, to
apply the masks using the ``mediancr`` method, one can execute:

.. code-block:: console

   (megara) $ numina-crmasks apply \
   --inputlist list.txt \
   --input_mask crmasks.fits \
   --output_combined result.fits \
   --combination mediancr

In this example, the combined image is saved in the file ``result.fits``.

Full details of the available parameters can be obtained by executing:

.. code-block:: console

   (megara) $ numina-crmasks apply --help
   usage: numina-crmasks apply [-h] --inputlist INPUTLIST
                               --input_mask INPUT_MASK
                               --output_combined OUTPUT_COMBINED
                               [--combination {mediancr,meancrt,meancr}]
                               [--extname EXTNAME]

   options:
     -h, --help            show this help message and exit
     --inputlist INPUTLIST
                           Input text file with list of 2D arrays.
     --input_mask INPUT_MASK
                           Input FITS file with the cosmic ray masks
     --output_combined OUTPUT_COMBINED
                           Output FITS file with the combined image
     --combination {mediancr,meancr,meancrt}
                           Combination method to apply the masks (default:
                           mediancr)
     --extname EXTNAME     Extension name in the input arrays (default:
                           'PRIMARY')
