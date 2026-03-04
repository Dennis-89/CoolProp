#!/usr/bin/env python

from enum import Enum
from functools import cache
from math import isclose
from timeit import timeit

from CoolProp import CoolProp


class InputPairs(Enum):
    PRESSURE_TEMPERATURE = CoolProp.PT_INPUTS
    TEMPERATURE_DENSITY = CoolProp.DmassT_INPUTS


class Percent(Enum):
    MASS = 0
    VOLUME = 1


class Gas(CoolProp.AbstractState):
    """
    Wrapper for the `CoolProp`-Lowlevel-API to get a more readable
    and cleaner source code.
    """

    BACKEND = "HEOS"

    def __init__(self, backend, name):
        CoolProp.AbstractState.__init__(self)
        self.specify_phase(CoolProp.iphase_gas)
        self._input_pair = CoolProp.PT_INPUTS

    @classmethod
    def new(cls, **kwargs):
        name = kwargs.get("name", None)
        if name is not None:
            return cls(Gas.BACKEND, name)
        try:
            gas_mix = kwargs["gas_mix"]
            volume_percent = kwargs["percent"]
        except KeyError:
            error = f"Setup-Signature should be `Gas.setup(name='CO2')` or `Gas.setup(gas_mix={{'CO2: 50', 'H2': 50}}, percent=Percent.MASS)` and not <{kwargs!r}>"
            raise KeyError(error)
        if not isclose(sum(gas_mix.values()), 1.0, abs_tol=1e-5):
            raise ValueError(f"Sum of gas_mix is not 1")
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
        return self._input_pair

    @input_pair.setter
    def input_pair(self, value):
        self._input_pair = value.value

    def update_state(self, *args):
        if len(args) != 2:
            raise ValueError(
                "You have to provide two inputs for the given `InputPairs`!"
            )
        self.update(self.input_pair, *args)

    def density(self):
        return self.rhomass()

    def thermal_conductivity(self):
        return self.conductivity()

    def thermal_capacity(self):
        return self.cp0mass()

    def thermal_capacity_volume(self):
        return self.cvmass()

    @cache
    def molmass(self):
        return self.molar_mass()

    def mass_enthalpy(self):
        return self.hmass()

    def molar_enthalpy(self):
        return self.hmass()

    def compressibility(self):
        return self.compressibility_factor()

    def isentropic_coefficient(self):
        return self.keyed_output(CoolProp.iisentropic_expansion_coefficient)

    def specific_gas_constant(self):
        return self.gas_constant() / self.molmass()

    def temperature(self):
        return self.T()

    def pressure(self):
        return self.p()


def main():
    norm_temp = 273.15  # °K
    norm_druck = 1.01325e5  # bar abs
    gas_mix = {"CarbonDioxide": 0.33, "Hydrogen": 0.33, "Methane": 0.34}
    gas = Gas.new(gas_mix=gas_mix, percent=Percent.MASS)
    gas.update_state(norm_druck, norm_temp)
    gas.density()
    gas.viscosity()
    gas.thermal_conductivity()
    gas.thermal_capacity()
    gas.molmass()
    gas.compressibility()
    gas.specific_gas_constant()

    temp_test_1 = 273.15 + 150
    druck_test_1 = 19e5
    gas.update_state(druck_test_1, temp_test_1)

    gas.density()
    gas.viscosity()
    gas.thermal_conductivity()
    gas.thermal_capacity()
    gas.molmass()
    gas.compressibility()
    gas.specific_gas_constant()

    temp_test_1 = 273.15 + 150
    druck_test_1 = 19e5

    gas.update_state(druck_test_1, temp_test_1)

    gas.density()
    gas.viscosity()
    gas.thermal_conductivity()
    gas.thermal_capacity()
    gas.molmass()

    gas.compressibility()
    gas.specific_gas_constant()


if __name__ == "__main__":
    result = timeit(main, number=100)
    print(result)
