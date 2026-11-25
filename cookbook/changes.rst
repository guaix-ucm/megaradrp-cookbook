.. _Changes:

Changes since MEGARA DRP 0.22
=============================

This section summarizes the changes in MEGARA DRP 0.23 that affect the data
reduction described in this cookbook: new parameters of the recipes, changes
of behaviour, and new products. The details are in :ref:`Data_reduction_process`
and in :ref:`Quality_Control`.

Requirements
------------

- MEGARA DRP 0.23 requires Python 3.11 or later and numina 0.42 or later.
- The calibration tree created by ``megaradrp-inittree`` includes the
  dataset of calibrations distributed by the DRP (megaradrp-calibrations,
  2026.11.17): the bad pixel masks, the extinction curve and the
  catalogues of the arc lines.

Quality control and masks
-------------------------

- The trace map, model map, wavelength calibration and fiber flat recipes
  compute the quality of their products (``GOOD``, ``PARTIAL`` or ``BAD``)
  and add quality flags to the fibers. The products with QC ``BAD`` are not
  used from the registry of the reductions. See :ref:`Quality_Control`.
- The images of the calibration lamps have telluric absorption (bands of
  O\ :sub:`2` and H\ :sub:`2`\ O of the air that the light crosses before
  the fibers, up to 3.5 % deep) and the Na D lines of the lamp. The fiber
  flat recipe masks them: it interpolates the flat across them and marks
  them in ``FLATMASK``. See :ref:`Lamp_Tellurics`.
- The master fiber flat has a new extension, ``FLATMASK``, with the pixels
  of the zero order of the VPH and of the absorption windows. It is copied to
  every RSS corrected with the fiber flat. See :ref:`Masks`.
- The fibers with an invalid wavelength solution are not resampled.
- ``megaradrp-cube`` converts ``WLMAP`` and ``FLATMASK`` to the geometry of
  the cube.

New parameters and defaults
---------------------------

=============================  ==============================  ==================  ==========================================
Recipe                         Parameter                       Default             Description
=============================  ==============================  ==================  ==========================================
MegaraTraceMap                 ``auto_reference_column``       ``True``            Search for the peaks in the column where
                                                                                   the weakest pseudo-slit box has the most
                                                                                   contrast, instead of ``reference_column``
MegaraTraceMap                 ``complete_traces``             ``True``            Correct and complete the traces with the
                                                                                   shape of the traces of the neighbouring
                                                                                   fibers
MegaraModelMap                 ``fit_background``              ``True``            Fit a constant background in each local
                                                                                   fit of the profiles
MegaraModelMap                 ``width_limits``                ``[0.8, 3.5]``      Limits of the width (sigma) of the
                                                                                   profiles, in pixels
MegaraModelMap                 ``smooth_widths``               ``2``               Half size, in fibers, of the running
                                                                                   median of the widths before the last fit
MegaraFiberFlatImage           ``smoothing_knot_step``         ``150.0``           Distance in Å between the knots of the
                                                                                   spline that smooths the average spectrum
MegaraFiberFlatImage           ``skip_absorption_windows``     ``True``            Interpolate the flat across the
                                                                                   absorptions of the calibration light
MegaraFiberFlatImage           ``remove_zero_order``           ``True``            Find the zero order of the VPH and
                                                                                   interpolate each fiber across it
MegaraLcbStdStar,              ``skip_sensitivity_windows``    ``True``            Skip the telluric bands and the strong
MegaraMosStdStar                                                                   stellar lines when smoothing the
                                                                                   sensitivity
MegaraLcbStdStar,              ``extra_skip_windows``          ``[]``              Other windows ``[[wl1, wl2], ...]`` (Å,
MegaraMosStdStar                                                                   air) to skip
MegaraLcbStdStar,              ``smoothing_adaptive``          ``False``           Move the knots of the smoothing of the
MegaraMosStdStar                                                                   sensitivity to their best positions
MegaraLcbStdStar,              ``smoothing_knots``             ``5`` (was ``3``)   Number of knots (or list of knots) of the
MegaraMosStdStar                                                                   smoothing of the sensitivity
MegaraTwilightFlatImage        ``normalize_region``            ``[]`` (was         Columns used to normalize the fibers;
                                                               ``[1900, 2100]``)   ``[]`` to choose them automatically
=============================  ==============================  ==================  ==========================================

Changes of behaviour
--------------------

- ``extraction_offset`` accepts the value ``auto`` in the twilight flat,
  acquisition, standard star and science recipes: the offset of the traces
  is measured in each image. The new tool ``megaradrp-trace_offset``
  measures it in any image. See :ref:`Extraction_Offset`.
- **MegaraTraceMap** completes the traces that do not reach the borders of
  the detector with the shape of their neighbours, and flags the traces that
  cross.
- **MegaraModelMap** fits a background, limits and smooths the widths of the
  profiles, and checks the geometry of the result.
- **MegaraArcCalibration** flags the solutions with large residuals or
  deviant from their neighbours, lists as missing the fibers without trace,
  and marks the fibers whose refinement started from interpolated
  coefficients.
- **MegaraFiberFlatImage**:

  - smooths the average spectrum with knots every 150 Å, follows the fall of
    the spectrum at the borders and extrapolates the smoothing linearly
    there;
  - interpolates each fiber across the telluric absorption of the
    calibration light, across the Na D lines of the lamp and across the zero
    order of the VPH;
  - returns the RSS calibrated in wavelength in ``reduced_rss``;
  - flags the fibers and computes the QC of the fiber flat.

- **MegaraTwilightFlatImage**:

  - the default of ``normalize_region`` is now ``[]``: the region starts at
    the columns 1900-2100 and moves away from the zero order of the VPH
    and from the pixels without coverage;
  - the pixels of ``FLATMASK`` are left out of the normalization;
  - the scaling of the images by their median before combining them was
    inverted, and it is fixed;
  - the wavelength calibration is not modified.

- **MegaraLcbStdStar** and **MegaraMosStdStar** smooth the sensitivity only
  in the region of valid flux, skipping the telluric bands and the strong
  lines of the star. By default the spline has 5 fixed knots, equidistant
  in the region of valid flux (before, 3 knots were moved to their best
  positions, and the result was not reproducible). The limits of the
  sensitivity (``PIXLIMF1``, ``PIXLIMF2``...) are 1-based.
- ``megaradrp-cube`` has a quadratic interpolation (``-m quadratic``), its
  sky WCS has a 1-based reference pixel, and its rescaling kernel is
  symmetric.
