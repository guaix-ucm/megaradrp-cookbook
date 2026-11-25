.. _Quality_Control:

Quality control, flags and masks
================================

Since version 0.23, the calibration recipes of MEGARA DRP check the quality
of their products, mark the fibers with problems and keep masks of the pixels
that are not corrected as the rest. This section describes these checks, the
flags and the masks, and where to find them. The recipes that use each of
them are described in :ref:`Data_reduction_process`.

Quality of the products
-----------------------

Each calibration recipe gives its result a global quality (QC):

``GOOD``
   All the fibers are valid.

``PARTIAL``
   Some fibers are not valid, at most 5 % of them.

``BAD``
   More than 5 % of the fibers are not valid.

The fibers that are not expected to have light are not counted: the fiber 623
in the LCB and the fiber 635 in the MOS.

The QC is stored in the file ``result.json`` of the results directory, and in
the product itself (the field ``quality_control`` of the JSON products). The
``processing.log`` file lists the fibers that are not valid and the fibers
with each flag. For example, for the wavelength calibration of the cookbook:

.. code-block:: console

   (megara) $ grep "QC\|flag" obsid3_WaveCalib_HR-R_results/processing.log

.. code-block:: console
   :class: my-special-block no-copybutton

   ... megaradrp.recipes.calibration.arc - INFO - start arc recipe QC
   ... megaradrp.recipes.calibration.arc - INFO - solutions with flag 'edge_deviation': 3 [287, 341, 609]
   ... megaradrp.recipes.calibration.arc - INFO - solutions with flag 'interpolated': 34 [188, 213, 221, ...]
   ... megaradrp.recipes.calibration.arc - INFO - Result QC is QC.GOOD
   ... megaradrp.recipes.calibration.arc - INFO - end arc recipe QC

All the solutions are valid, so the QC is ``GOOD``: the flags
``edge_deviation`` and ``interpolated`` are informational. In the cookbook
data, all the calibrations are ``GOOD``.

When numina searches for a calibration in the registry of the reductions,
the products with QC ``BAD`` are not used. A product copied by hand to the
calibration tree is used whatever its QC. Check the QC of each calibration
before reducing the science observations: a ``BAD`` calibration usually means
that the inputs, or the parameters, have to be reviewed.

Trace map
---------

The recipe **MegaraTraceMap** gives each trace these flags:

``weak``
   The peak of the fiber in the reference column is much weaker than those
   of its neighbours. It is informational: the trace is valid.

``truncated``
   The trace does not reach the borders of the useful region of the detector.

``not_completed``
   The trace is truncated, and it could not be completed with the shape of
   the traces of the neighbouring fibers (see the parameter
   ``complete_traces`` in :ref:`Tracing_Fibers`). The trace is not valid.

``crossing``
   The trace comes closer than half the usual distance to the trace of the
   next fiber. Both traces are not valid.

A trace with coefficients that are not finite is not valid either. The fibers
that are not found in the reference column are listed in ``error_fitting``.
The invalid traces are not extracted by the later recipes.

Model map
---------

The recipe **MegaraModelMap** checks the geometry of the profiles fitted to
the fibers. A fiber is flagged when:

``crossing``
   Its centre comes closer to the centre of the next fiber than half the
   usual distance between fibers.

``not_parallel``
   Its centre is not parallel to the centres of its neighbours in the same
   pseudo-slit box (at the border of a box, the only neighbour in the box is
   used).

``width_not_smooth``
   Its width (the sigma of the profile) does not vary smoothly as those of
   its neighbours. The width grows smoothly towards the borders of the
   detector, both along the rows and along the columns.

``amplitude_not_smooth``
   Its amplitude does not vary smoothly along the detector.

The amplitude is not compared between fibers: a fiber can be fainter than its
neighbours. The flagged fibers are not used as neighbours in the checks of
the others. The QC of the model map is ``PARTIAL`` if some fibers are flagged
and ``BAD`` if more than 5 % of them are.

Wavelength calibration
----------------------

The recipe **MegaraArcCalibration** gives each wavelength solution these
flags:

``high_residual``
   The residual of the fit is larger than 0.5 pixels. The solution is not
   valid.

``deviant``
   In the interior of the detector, the wavelengths of the solution differ
   by more than 4 pixels from the median of those of the 5 fibers at each
   side. The solution is not valid.

``edge_deviation``
   The solution differs by more only at the borders of the detector, where
   it extrapolates beyond the lines. It is informational.

``not_refined``
   The solution is that of the first pass, it was not refined with all the
   lines.

``interpolated``
   The coefficients of the first pass of this fiber did not follow the
   smooth variation of the coefficients with the fiber number, and the
   refinement started from the coefficients interpolated from the other
   fibers. It is informational. These fibers are marked with red circles in
   the plots of ``wavecal_iter1.pdf`` and ``wavecal_iter2.pdf``.

The fibers where no line is identified are listed in ``error_fitting``, and
the fibers without trace in ``missing_fibers``. The fibers with an invalid
solution, or without solution, are marked as invalid in the header of the
extension ``FIBERS`` of the RSS (keyword ``FIBnnn_V``) and they are not
resampled in wavelength: their spectra are 0.

Fiber flat
----------

The recipe **MegaraFiberFlatImage** gives each fiber these flags, written in
the keywords ``FIBnnnQF`` of the extension ``FIBERS`` of
``master_fiberflat.fits``:

``faint``
   The fiber is fainter than the limit used to compute the average spectrum
   of the fibers. It is informational.

``deviant``
   The shape of the flat of the fiber differs from the median of its
   neighbours in the pseudo-slit by more than 30 %, in more than 2 % of its
   pixels. It is informational: in the commissioning data, these are steep
   features of the spectrum with small differences in the wavelength
   calibration, and traces off-centre where the signal is weak, and both
   are also in the science spectra.

``broken``
   The level of the fiber is not positive, or the flat has values that are
   not finite. The fiber is not valid.

.. _Masks:

Masks of the RSS
----------------

The RSS images produced by the recipes have two extensions with one value
per fiber and wavelength, with the same shape as the RSS:

``WLMAP``
   The spectral coverage of each fiber: 1 in the pixels where the fiber has
   data after the wavelength calibration, 0 elsewhere (at the ends of the
   spectral range, and in the fibers without a valid wavelength solution).

``FLATMASK``
   The pixels of each fiber where the fiber flat is interpolated, or does
   not correct the light. It is a bit mask, the meaning of each bit is in
   the header of the extension:

   ============  =======  ==========  ===============================================
   Value         Bit      Keyword     Meaning
   ============  =======  ==========  ===============================================
   1             1        ZEROINT     Zero order of the VPH, interpolated in the
                                      fiber flat
   2             2        ZEROWEAK    Zero order of the VPH, weak, not interpolated
   4             3        ABSINT      Absorption of the calibration light,
                                      interpolated in the fiber flat
   ============  =======  ==========  ===============================================

The fiber flat recipe creates ``FLATMASK`` in ``master_fiberflat.fits``. The
correction of the fiber flat copies it to the RSS that it corrects (or
combines it with the mask that the RSS already has), so it reaches the
twilight flat, the standard star and the science RSS. The fiber flats made
with earlier versions of the DRP have only the zero order, in an extension
named ``ZOMASK``.

The pixels marked in ``FLATMASK`` are not wrong, but they deserve care:

- In the zero order of the VPH (bits 1 and 2), the science spectrum has
  light that is not corrected (see below).
- In the absorption windows (bit 4), the fiber flat is interpolated, so the
  small-scale structure of the flat is not corrected there. These windows
  coincide with telluric bands: the science spectrum has its own telluric
  absorption there, which the fiber flat does not correct.

The zero order of the VPH
-------------------------

The zero order of the VPH is diffuse light that reaches the detector in a
band of fixed columns, both between the fibers and on them. In the fiber
flat it is light added to the spectrum of each fiber, not a change of its
response. If it were left in the fiber flat, dividing by it would
over-correct those pixels of the science spectra, and the zero order of the
science image would still be there.

The fiber flat recipe measures the band in the rows between the traces of
the flat. When it is brighter than 2 % of the level of the fibers, each fiber
is interpolated across it (bit 1 of ``FLATMASK``). When it is between 1 % and
2 %, it is only marked (bit 2). This is controlled by the parameter
``remove_zero_order`` (see the section on the fiber flat in
:ref:`Data_reduction_process`).

In the commissioning data, the zero order was found in these VPHs:

=======  =======================  ======================
VPH      Wavelengths (Å)          Treatment
=======  =======================  ======================
MR-V     5639-5658                interpolated (bit 1)
HR-I     8607-8623                interpolated (bit 1)
HR-R     6607-6618                interpolated (bit 1)
MR-G     5194-5211                interpolated (bit 1)
MR-VR    6170-6191                interpolated (bit 1)
LR-B     4761-4810                marked (bit 2)
MR-B     4793-4811                marked (bit 2)
MR-R     6594-6620                marked (bit 2)
MR-Z     9227-9262                marked (bit 2)
=======  =======================  ======================

The wavelengths are those of all the fibers: the band is at fixed columns, so
its wavelength changes along the pseudo-slit, and each fiber covers only a
part of the range.

The zero order is not removed from the science images. The twilight flat
recipe leaves it out of the region used to normalize the fibers.

.. _Absorption_Windows:

Absorption windows
------------------

Two tables of windows, distributed with the DRP, are skipped when smooth
curves are fitted to the spectra:

``flat_absorption_windows.ecsv``
   The absorptions of the light of the calibration lamps in its path through
   the air (O\ :sub:`2` and H\ :sub:`2`\ O bands) and the Na D lines, for the
   resolution of each family of VPHs (LR, MR and HR). The fiber flat recipe
   interpolates the flat of each fiber across them (parameter
   ``skip_absorption_windows``), and marks them with bit 4 of ``FLATMASK``.

``sensitivity_skip_windows.ecsv``
   The telluric bands deeper than 3 % at the resolution of the LR VPHs,
   computed from a model of the transmission of the atmosphere (ESO
   SkyCalc), and the strong lines of the standard stars (Balmer, Ca II H and
   K, the Ca II triplet and the Paschen lines). The standard star recipes
   skip them when they smooth the sensitivity (parameter
   ``skip_sensitivity_windows``). Other windows can be added with
   ``extra_skip_windows``.

The sensitivity keeps the telluric absorption of the standard star in the
broad H\ :sub:`2`\ O band beyond 9250 Å, at the red end of LR-Z: there, the
fall of the response of the instrument cannot be separated from the
absorption with a single standard star.

Masks in the cubes
------------------

The tool ``megaradrp-cube`` converts the extensions ``WLMAP`` and
``FLATMASK`` of the RSS to the geometry of the cube (wavelength, y, x), with
the WCS of the cube:

- ``WLMAP`` is 1 in the pixels of the cube inside the field of view where
  the fibers without data contribute at most 1 % of the value, and 0
  elsewhere.
- ``FLATMASK`` has in each pixel the bits of the fibers that contribute more
  than 1 % of its value.

Since the zero order of the VPH is at fixed columns of the detector, its
wavelength changes from fiber to fiber. In the cube it is not a plane, but a
band whose wavelength changes across the field of view, with a pattern that
follows the position of the fibers in the pseudo-slit. Use ``FLATMASK`` to
find it before interpreting a spatial structure at those wavelengths.
