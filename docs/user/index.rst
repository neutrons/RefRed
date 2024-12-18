User Guide
----------

Reflectometry measures the probability :math:`R(q)` of neutrons to reflect
off the surface of a film as a function of :math:`q`, the wavevector transfer
perpendicular to the surface of the film.

:math:`q` is defined as :math:`q = 4 \pi / wl \sin(\theta)`, where :math:`wl` is the wavelength
of the neutron and :math:`\theta` is the reflection angle.

For a complete measurement, several runs have to be made and combined.
Each measurement is made with a choice of :math:`wl` and :math:`\theta` such that we
obtain a continuous :math:`R(q)` curve over a wide range.

RefRed is that application used on 4B to load those runs and select
the reduction parameters that will be used to generate the :math:`R(q)` curve.

The following are typical use cases:

.. toctree::
   :maxdepth: 1

   load-template
   compute-scaling-factors
   reduce-data
