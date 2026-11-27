MEGARA data reduction cookbook
==============================

This webpage is an updated version of the original cookbook (dated 07/07/2020).
The PDF version of this webpage and the previous versions of the cookbook,
including the original one, are available at `Zenodo
<https://doi.org/10.5281/zenodo.1974953>`_. The original document was prepared
by África Castillo Morales, Sergio Pascual Ramírez and Armando Gil de Paz. As the
aforementioned document has become slightly outdated over time, we have decided
to move the documentation to this website that allows for easier updates.
Nicolás Cardiel López, Mario Chamorro Cazorla and María Chillarón Víctor have
also joined this task.

**Important:** We strongly recommend using the most up-to-date information
available on this `webpage
<https://guaix-ucm.github.io/megaradrp-cookbook/>`_.

.. warning::

   Since February 2026, a new, more simplified data reduction procedure has
   been implemented. Please, see the section `Data reduction <datared.html>`_
   for details.

.. note::

   MEGARA DRP 0.30 adds quality control of the calibrations, masks of the
   zero order of the VPH and of the telluric absorption of the calibration
   lamps, and the automatic
   measurement of ``extraction_offset``. See :ref:`Changes` and
   :ref:`Quality_Control`.

.. toctree::
   :maxdepth: 2

   intro
   megaradrp
   install
   datadesc
   datared
   quality
   healtraces
   brightlines
   crmasks
   megaratools
   issues
   changes
   acronyms

How to cite
-----------

If you use this cookbook, please cite it as:

   Castillo-Morales, Á., Pascual, S., Gil de Paz, A., Cardiel, N.,
   Chamorro-Cazorla, M., *MEGARA Data Reduction Cookbook*, Zenodo,
   https://doi.org/10.5281/zenodo.1974953

This DOI always resolves to the latest version of the cookbook. Each
version has its own DOI, listed in the Zenodo record.

License
-------

The text and the figures of this cookbook are licensed under the `Creative
Commons Attribution 4.0 International License (CC BY 4.0)
<https://creativecommons.org/licenses/by/4.0/>`_. The source code in the
`repository of the cookbook <https://github.com/guaix-ucm/megaradrp-cookbook>`_
(configuration of the documentation, scripts and workflows) is licensed under
the GNU General Public License v3 (GPLv3).
