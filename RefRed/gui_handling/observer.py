from dataclasses import dataclass

from qtpy.QtWidgets import QSpinBox


class SpinBoxObserver:
    r"""Stores the last value for each of the registered QSpinBox objects.

    Attributes
    ----------
    NAN : int
        Represents a value that the QSpinBox object cannot take
    QUANTUM : int
        The minimum allowed change in value for any of the registered QSpinBox objects
    """

    NAN: int = -1
    QUANTUM: int = 1

    @dataclass
    class RegistryEntry:
        r"""Helper class to encapsulate entries in the registry of SpinBoxObserver._registry"""

        spin_box: QSpinBox
        last_value: int

    def __init__(self):
        self._registry = {}  # database holding the last value for each of the registered QSpinBox objects

    def entry_key(self, spin_box: QSpinBox) -> int:
        r"""Generates a unique key for the given spin_box object using its memory address"""
        return id(spin_box)

    def get_entry(self, spin_box: QSpinBox) -> RegistryEntry:
        r"""Retrieves the registry entry for the given ``spin_box``.

        If ``spin_box`` is not registered, it is first registered with default ``last_value=SpinBoxObserver.NAN``
        """
        key = self.entry_key(spin_box)
        if key not in self._registry:
            self.register(spin_box)
        return self._registry[key]

    def register(self, spin_box, last_value=NAN):
        r"""Registers a new spin box in the internal registry with an optional initial last_value.

        Parameters
        ----------
        spin_box
            The spin_box object to register.
        last_value: The optional initial last_value for the spin_box. Default is the NAN constant.
        """
        key = self.entry_key(spin_box)
        self._registry[key] = self.RegistryEntry(spin_box=spin_box, last_value=last_value)

    def quantum_change(self, spin_box: QSpinBox) -> bool:
        r"""Determines if the current value of ``spin_box`` changed by exactly the QUANTUM amount from the last value.

        Additionally, it updates the last value stored in the registry with the current value
        Parameters
        ----------
        spin_box
            The spin box object to check for quantum change.

        Returns
        -------
        ``True`` if the current value differs from the last value by exactly the QUANTUM amount, ``False`` otherwise.
        """
        entry = self.get_entry(spin_box)
        last_value, new_value = entry.last_value, spin_box.value()
        entry.last_value = new_value
        return abs(new_value - last_value) == self.QUANTUM
