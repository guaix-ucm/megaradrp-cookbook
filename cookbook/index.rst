MEGARA data reduction cookbook
==============================

This webpage is an updated version of the original cookbook (dated 07/07/2020),
available in PDF format at this `zenodo link
<https://zenodo.org/records/3932063>`_. That document was prepared by África
Castillo Morales, Sergio Pascual Ramírez and Armando Gil de Paz. As the
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
