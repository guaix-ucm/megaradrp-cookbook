.. _Fixing_CR_median:

*********************************
CR not removed by median stacking
*********************************

By default, the various recipes in MEGARA DRP use a median combination of three
or more images to produce an average exposure and eliminate cosmic rays.
However, when exposure times are long, it’s not uncommon for the same pixel to
be hit by a cosmic ray in consecutive exposures.

The most straightforward solution is to visually inspect the resulting image
(e.g., the ``final_rss.fits`` file) and manually interpolate the affected pixels
using data from neighboring pixels. However, it can be more efficient to use an
automated procedure that detects and corrects pixels impacted by cosmic rays
across multiple exposures, eliminating the need for manual intervention.

Such an automatic method is available in the numina subpackage
`crmasks <https://guaix-ucm.github.io/numina-tools/crmasks/crmasks.html>`_, and
it can be easily activated by modifying the default image combination method
used by MEGARA DRP.

This method should only be applied when three or more equivalent exposures are
available. It works by identifying pixels where the signal has been affected by
cosmic rays in more than half of the available exposures, such that the median
combination still retains an erroneous signal.

.. note::

   This method is likely to be useful primarily when reducing science images
   with long exposure times. In general, it is not recommended for the
   reduction of calibration images.

Overall procedure
=================

The main workflow for applying the method is as follows:

1. **Prepare the observation result file**: Create the YAML file that lists the
   individual exposures and specifies additional requirements for the reduction
   recipe associated with the reduction recipe **MegaraCrDetection**.
2. **Run the MEGARA DRP to generate the CR masks**: The execution of the MEGARA
   DRP with this YAML file is interactive (see below), and the result is a FITS
   file named ``crmasks.fits``, which contains several masks that can later be
   used to remove the cosmic rays using different strategies. This
   file must be copied to the `data/` subdirectory.
3. **Run the MEGARA DRP to generate the reduced scientific result**: Once the
   file ``crmasks.fits`` is placed in the `data/` subdirectory, the MEGARA DRP
   can be run again to generate the reduced scientific result, using for that
   purpose the corresponding YAML file. During this step, the user must one of
   the available strategies for combining exposures and removing cosmic rays.
   Instead of using the default ``median`` combination, specify one of the
   following methods in the requirements section:
   ``mediancr``, ``meancrt`` or ``meancr``.

.. note::

   The three available combination methods, ``mediancr``, ``meancrt`` and 
   ``meancr``, produce different results:

   - ``mediancr``: performs a median combination, replacing pixels 
     suspected of being affected by cosmic rays in more than one exposure by
     the minimum value at each pixel across the available exposures.
   - ``meancrt``: generates the mean combination using of a single mask that
     stores all the cosmic rays detected in all the individual exposures,
     replacing each masked pixels by the value obtained when using the
     ``mediancr`` method.
   - ``meancr``: also performs a mean combination, but uses the individual
     cosmic ray masks specifically computed for each available exposure.

   Since the mean has a lower standard deviation than the median, the 
   ``meancrt`` and ``meancr`` methods are generally preferable. Among these
   two, tests suggest that ``meancr`` tends to yield better
   results. However, it is recommended to try all three methods and compare the
   outputs to determine which works best for your specific dataset.

Preparing the observation result file
=====================================

Let's assume that we have three initially equivalent exposures. The process
begins with the creation of a YAML file, e.g.  ``8_generate_crmasks.yaml``,
which lists the individual exposures to be used in the cosmic ray detection
step.

.. literalinclude:: files/8_generate_crmasks_1.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2,4,8

Note that in this file is important to specify:

- ``mode: MegaraCrDetection``, so the MEGARA DRP will know that the
  ``8_generate_crmasks.yaml`` file is intended for generating the CR masks. 

- ``frames:`` one should provide here the list of the individual equivalent
  exposures. 

- ``requirements:`` this section contains a large set of parameters whose
  values define the strategy used for the cosmic-ray detection. This section is
  identical to the ``requirements`` section of the configuration YAML file
  employed by ``numina-crmasks``, which is described in detail in this `link
  <https://guaix-ucm.github.io/numina-tools/crmasks/crmasks.html>`_.


Computing the CR masks
======================

Coincident cosmic rays in the median combination
------------------------------------------------

The recipe is run by doing:

.. code-block:: console

   (megara) $ numina run 8_generate_crmasks.yaml -r control.yaml

From this point, follow the description given in this
`example
<https://guaix-ucm.github.io/numina-tools/crmasks/crmasks.html#example>`_.
**Important**: in that example the generation of
the CR masks is carried out by executing the command-line script
``numina-crmasks``, which makes use of a slightly different input YAML file.


Output file ``crmasks.fits``
----------------------------

The output file ``crmasks.fits`` is generated in the *results/* subdirectory, 
and contains several extensions:

.. code-block:: console

   (megara) $ cd obsid8_LcbImage_LR-R_crmasks_results

.. code-block:: console

   (megara) $ fitsinfo crmasks.fits

.. code-block:: console
   :class: my-special-block no-copybutton

   Filename: crmasks.fits
   No.    Name      Ver    Type      Cards   Dimensions   Format
     0  PRIMARY       1 PrimaryHDU     121   ()      
     1  MEDIANCR      1 ImageHDU         8   (4096, 4112)   uint8   
     2  MEANCRT       1 ImageHDU         8   (4096, 4112)   uint8   
     3  CRMASK1       1 ImageHDU         8   (4096, 4112)   uint8   
     4  CRMASK2       1 ImageHDU         8   (4096, 4112)   uint8   
     5  CRMASK3       1 ImageHDU         8   (4096, 4112)   uint8   
     6  LAMEDIAN      1 ImageHDU         8   (4096, 4112)   float32 

The primary HDU does not contain image data but includes keywords that document the parameters used to generate the masks.

The next extensions store the actual masks computed by the program:

- ``MEDIANCR``: Mask for pixels suspected of being affected by
  two cosmic rays in the median combination.
- ``MEANCRT``: Mask for pixels suspected of being affected by
  a cosmic ray in the mean combination.
- ``CRMASK1``, ``CRMASK2``, ``CRMASK3``: Masks for pixels suspected
  of being affected by a cosmic ray in each of the individual exposures.

In all these masks, pixels suspected of being affected by a cosmic ray
are set to 1, while the rest of the pixels are set to 0.

Finally, the extension ``LAMEDIAN`` contains the corrected image generated by
the L.A. Cosmic algorithm (van Dokkum 2001).

Do not forget to copy the file ``crmasks.fits`` to the `data/` subdirectory
before running the MEGARA DRP to generate the reduced scientific result.

.. code-block:: console

   (megara) $ cp crmasks.fits ../data/

Applying the masks
==================

Once the ``crmasks.fits`` file has been generated, it can be used to remove the
suspected cosmic rays from the combined image.  Several options are available
for this step, depending on the value of ``method`` specified in the
requirements section of the YAML file used to produce the reduced scientific
result. Rather than assuming the combination method is ``median`` (the default
in MEGARA DRP), the user should explicitly specify one of the following
methods: ``mediancr``, ``meancr`` or ``meancrt``. 

Method ``mediancr``
-------------------

For example, when using the **MegaraLcbImage** recipe, the corresponding
YAML file, ``8_LcbImage.yaml`` should define the ``method`` and
``crmasks`` parameters in the requirements section, as follows:

.. literalinclude:: files/8_LcbImage_mediancr.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2, 9-12

Note that the ``crmasks`` parameter must be explicitly specified, and it should
point to the ``crmasks.fits`` file generated in the previous step. This
requirement also gives users the flexibility to rename the file and test
different versions of it (each potentially created with varying detection
thresholds) to evaluate the impact of using different masks.

.. code-block:: console

   (megara) $ numina run 8_LcbImage.yaml -r control.yaml

When using ``method: mediancr``, the MEGARA DRP reads the mask stored in the
``MEDIANCR`` extension of the ``crmasks.fits`` file. The masked pixels (those
suspected of being affected by a cosmic ray in more than one exposure) are
replaced with the corresponding ``min2d`` value at each pixel. As a result, the
final image is identical to ``median2d``, except for the corrected pixels.

Note that under the label ```method_kwargs:`` there are several parameters that
control how the information from the ``crmasks.fits`` file is used:

- ``apply_flux_factor:`` When set to ``True``, the factors listed in the
  ``FLUXF1``, ``FLUXF2``, etc. keywords of the primary HDU in the
  ``crmasks.fits`` file are used to modify the signal of each individual
  exposure before combining them and removing cosmic rays. If this parameter is
  set to ``False``, an effective factor of ``1.0`` is applied (i.e., no change
  is introduced), regardless of the values in the FITS header of the
  ``crmasks.fits`` file.

- ``use_lamedian:``: When set to ``True``, the masked pixels are replaced with
  the corrected value obtained using the L.A. Cosmic algorithm, rather than
  using the minimum value in each pixel.

Method ``meancrt``
------------------

.. literalinclude:: files/8_LcbImage_meancrt.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2, 9-12

When using ``method: meancrt``, the MEGARA DRP reads the mask stored in 
the ``MEANCRT`` extension of the file ``crmasks.fits``. The masked pixels,
which are suspected of being affected by a cosmic ray, are replaced by 
the corresponding values when using ``method: mediancr``. 

As a result, the final image is identical to ``mean2d``, except for the
corrected pixels, where the data is sourced from the image produced by the
``mediancr`` method.

The parameters under the ``method_kwargs:`` label play the same role as
described above for the ``mediancr`` combination method.

Method ``meancr``
-----------------

.. literalinclude:: files/8_LcbImage_meancr.yaml
   :language: yaml
   :linenos:
   :lineno-start: 1
   :emphasize-lines: 2, 9-12

When using ``method: meancr``, the MEGARA DRP reads the masks stored in the
``CRMASK1``, ``CRMASK2`` and ``CRMASK3`` extensions of the file
``crmasks.fits``. The program uses NumPy masked arrays to construct a 3D stack
of the individual exposures, where each image is represented as a masked array
based on its corresponding mask. This allows the program to compute the mean
along the axis corresponding to the image number, excluding the masked pixels.

In cases where a pixel is masked in all individual exposures, the corresponding
pixel in the combined image is set to the ``min2d`` value at that location.

The parameters under the ``method_kwargs:`` label play the same role as
described above for the ``mediancr`` combination method.

