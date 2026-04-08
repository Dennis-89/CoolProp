#!/usr/bin/env python

from enum import Enum
from functools import cache
from math import isclose, exp

from CoolProp import CoolProp

# https://de.wikipedia.org/wiki/Wasserdampf
WATER_CONSTANT = 461.4
AIR_CONSTANT = 287.1

class InputPairs(Enum):
    """
    An Enum-class to use one of the input-pairs.

    'Pressure and Temperature' or 'Temperature and density'
    """
    PRESSURE_TEMPERATURE = CoolProp.PT_INPUTS
    TEMPERATURE_DENSITY = CoolProp.DmassT_INPUTS


class Percent(Enum):
    """
    An Enum class to use the percent in mass- or volume-percent.
    """
    MASS = 0
    VOLUME = 1


class Gas(CoolProp.AbstractState):
    """
    Wrapper for the `CoolProp <https://coolprop.org/>`_-Lowlevel-API to get a more readable
    and cleaner source code. The free backend 'HEOS' is used.
    Use `new()` function to create a `Gas` instance.
    """

    BACKEND = "HEOS"

    def __init__(self, backend, name):
        """
        See :func:`Gas.new` for creating a `Gas` instance.
        """
        CoolProp.AbstractState.__init__(self)
        self.specify_phase(CoolProp.iphase_gas)
        self._input_pair = CoolProp.PT_INPUTS

    @classmethod
    def new(cls, **kwargs):
        """
        Function to create a new `Gas` instance. The `name` argument specifies the gas name. To create a gas mixture,
        use the `gas_mix` and `percent` keyword arguments. Example:
        Gas.new(gas_mix={'CarbonDioxide': 0.5, 'Hydrogen': 0.5}, percent=Percent.MASS).
        `percent` is a constant of the :class:`Percent()` and indicates whether it is a mass-percent or
        a volume-percent values.

        :param kwargs: name: str | gas_mix: dict  percent: int
        :return: :class:`Gas()`
        """

        name = kwargs.get("name", None)
        if name is not None:
            return cls(Gas.BACKEND, name)
        try:
            gas_mix = kwargs["gas_mix"]
            volume_percent = kwargs["percent"]
        except KeyError as e:
            error = f"Setup-Signature should be like `Gas.setup(name='CO2')` or `Gas.setup(gas_mix={{'CO2: 0.5', 'H2': 0.5}}, percent=Percent.MASS)` and not <{kwargs!r}>"
            raise KeyError(error) from e
        if not isclose(sum(gas_mix.values()), 1.0, abs_tol=1e-5):
            raise ValueError("Sum of gas_mix is not 1")
        gas_names = set(gas_mix.keys())
        gas = cls(Gas.BACKEND, "&".join(gas_names))
        (
            gas.set_mole_fractions(list(gas_mix.values()))
            if volume_percent
            else gas.set_mass_fractions(list(gas_mix.values()))
        )
        return gas

    @property
    def input_pair(self):
        """
        Get or set the input-pair. You have to use one of the InputPairs-constant
        or import something like that, from `CoolProp <https://coolprop.org/>`_.

        :param InputPairs value: InputPairs-like object. See :class:`InputPairs`
        """
        return self._input_pair

    @input_pair.setter
    def input_pair(self, value):
        self._input_pair = value.value

    def update_state(self, *args):
        """
        Set a new gas-state in order to the `input_pair`. Be carful to
        use the values in the right order. See
        `CoolProp-Documentation <https://coolprop.org/_static/doxygen/html/namespace_cool_prop.html#a58e7d98861406dedb48e07f551a61efb>`_

        :param list args:  [int | float]
        """
        if len(args) != 2:
            raise ValueError(
                "You have to provide two inputs for the given `InputPairs`!"
            )
        self.update(self.input_pair, *args)

    def density(self):
        """
        :return float: density in kg/m³
        """
        return self.rhomass()

    def thermal_conductivity(self):
        """
        :return float: thermal conductivity in W/m/K
        """
        return self.conductivity()

    def thermal_capacity(self):
        """
        :return float: thermal capacity (mass constant, pressure specific) in J/kg/K
        """
        return self.cp0mass()

    def thermal_capacity_volume(self):
        """
        :return float: thermal capacity (mass constant, volume specific) in J/kg/K
        """
        return self.cvmass()

    @cache
    def molmass(self):
        """
        :return float: molar-mass in kg/mol
        """
        return self.molar_mass()

    def mass_enthalpy(self):
        """
        :return float: mass-enthalpy in J/kg
        """
        return self.hmass()

    def molar_enthalpy(self):
        """
        :return float: molar-enthalpy in J/mol
        """
        return self.hmolar()

    def compressibility(self):
        """
        :return float: compressibility-factor
        """
        return self.compressibility_factor()

    def isentropic_coefficient(self):
        """
        :return float: isentropic-expansion-coefficient
        """
        return self.keyed_output(CoolProp.iisentropic_expansion_coefficient)

    def specific_gas_constant(self):
        """
        :return float: specific gas-constant in J/(kg * K)
        """
        return self.gas_constant() / self.molmass()

    def temperature(self):
        """
        :return float: temperature in K
        """
        return self.T()

    def pressure(self):
        """
        :return float: pressure in Pa
        """
        return self.p()

    def add_water_to_gas_mix(self, humidity):
        """
        Recalculation of the gas mix to account for the water content in the gas.
        This is an approximation, as the absorption of water in dry air serves as the basis for the calculation.

        :param int | float humidity: In fraction
        :return: :class:`Gas` with :class:`Percent`.VOLUME and the calculates parts of water.
        """
        water_mass = get_water_content(
            humidity, self.pressure(), _get_vapour_pressure(self.temperature())
        )
        water_percent = 1 / (water_mass + self.density()) * water_mass
        gas_percent = 1 - water_percent
        gas_mix = {name: gas_percent * percent for name, percent in zip(self.fluid_names() + ["H2O"], self.get_mole_fractions() + [water_percent])}
        return self.new(gas_mix=gas_mix, percent=Percent.VOLUME)


def _get_vapour_pressure(temperature):
    """
    :param int | float temperature: In Kelvin
    :return float: In Pascal
    """
    temperature -= 273.15
    # Numbers, expect 273.15, are thermodynamic constants without specific names.
    # Ask your Thermodynamic-College for more information.
    return 0.006112 * exp(17.269 * temperature / (temperature + 237.3)) * 1e5

def get_water_content(humidity, gas_pressure, vapour_pressure):
    """
    Get the water content in air depends on the given humidity, pressure, and temperature.

    `AIR_CONSTANT` and `WATER_CONSTANT` in J/(kg*K)

    :param int | float humidity: In fraction number (0...1)
    :param int | float gas_pressure: In Pascal
    :param int | float vapour_pressure: In Pascal
    :return float: In kg/kg
    """
    partial_pressure = humidity * vapour_pressure
    return (AIR_CONSTANT / WATER_CONSTANT) * (
            partial_pressure / (gas_pressure - partial_pressure)
    )


def main():
    # norm_temp = 300
    # norm_druck = 5e5
    # gas_mix = {'CarbonDioxide': 0.3296538521744456, 'Hydrogen': 0.3296538521744456, 'Methane': 0.3396433628463985, 'H2O': 0.0010489328047103897}
    # gas = Gas.new(gas_mix=gas_mix, percent=Percent.VOLUME)
    # gas.update_state(norm_druck, norm_temp)
    # print(gas.density())
    norm_temp = 300
    norm_druck = 5e5
    gas_mix = {'CarbonDioxide': 0.33, 'Hydrogen': 0.33, 'Methane': 0.34}
    gas = Gas.new(gas_mix=gas_mix, percent=Percent.MASS)
    gas.update_state(norm_druck, norm_temp)
    gas.add_water_to_gas_mix(1)
    d = gas.density()
    v = gas.viscosity()
    t = gas.thermal_conductivity()
    tc = gas.thermal_capacity()
    m = gas.molmass()
    gas = Gas.new(gas_mix=gas_mix, percent=Percent.VOLUME)
    gas.update_state(norm_druck, norm_temp)
    gas.add_water_to_gas_mix(1)
    assert d == gas.density()
    assert v == gas.viscosity()
    assert t == gas.thermal_conductivity()
    assert tc == gas.thermal_capacity()
    assert m == gas.molmass()
    # gas.compressibility()
    # gas.specific_gas_constant()
    #
    # temp_test_1 = 273.15 + 150
    # druck_test_1 = 19e5
    # gas.update_state(druck_test_1, temp_test_1)
    #
    # gas.density()
    # gas.viscosity()
    # gas.thermal_conductivity()
    # gas.thermal_capacity()
    # gas.molmass()
    #
    # gas.compressibility()
    # gas.specific_gas_constant()


if __name__ == "__main__":
    main()
