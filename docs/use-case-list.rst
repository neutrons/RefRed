List of use-cases
-----------------

Reflectometry measures the probability R(q) of neutrons to reflect
off the surface of a film as a function of q, the wavevector transfer
perpendicular to the surface of the film.

Q is defined as `q = 4 pi / wl sin(theta)`, where `wl` is the wavelength
of the neutron and `theta` is the reflection angle.

For a complete measurement, several runs have to be made and combined.
Each measurement is made with a choice of `wl` and `theta` such that we
obtain a continuous R(q) curve over a wide range.

RefRed is that application used on 4B to load those runs and select
the reduction parameters that will be used to generate the R(q) curve.

The following are typical use cases:
  - `Load previous reduction from template <load-template.rst>`_
  - `Reduce and export data <reduce-data.rst>`_
  - `Compute scaling factors <compute-scaling-factors.rst>`_
