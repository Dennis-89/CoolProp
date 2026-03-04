#!/usr/bin/env python
from math import prod

from attrs import define, field
from CoolProp.CoolProp import PropsSI
from customgas.customgas import Gas as NewGas, InputPairs, Percent
from timeit import timeit

# FIXME Temperature could be the return value and the given values could be
#   enthalpy or something else. See line 67 and 105

@define
class AbstractGas:
    def density(self, temperature, pressure):
        return self._property_si(temperature, pressure, "D")

    def viscosity(self, temperature, pressure):
        return self._property_si(temperature, pressure, "V")

    def thermal_conductivity(self, temperature, pressure):
        return self._property_si(temperature, pressure, "L")

    def thermal_capacity(self, temperature, pressure):
        return self._property_si(temperature, pressure, "CP0MASS")

    def molmass(self, temperature, pressure):
        return self._property_si(temperature, pressure, "molemass")

    def mass_enthalpy(self, temperature, pressure):
        return self._property_si(temperature, pressure, "H")

    def molar_enthalpy(self, temperature, pressure):
        return self._property_si(temperature, pressure, "Hmolar")

    def compressibility(self, temperature, pressure):
        return self._property_si(temperature, pressure, "Z") / 100

    def isentropic_coefficient(self, temperature, pressure):
        return self._property_si(
            temperature, pressure, "isentropic_expansion_coefficient"
        )

    def temperature_from_enthalpy(self, enthalpy, pressure):
        return self._property_si(
            enthalpy, pressure, "T"
        )

    def specific_gas_constant(self, temperature, pressure):
        return self._property_si(
            temperature, pressure, "gas_constant"
        ) / self._property_si(temperature, pressure, "molemass")


@define(hash=True)
class Gas(AbstractGas):
    name = field(factory=str)

    def _property_si(self, temperature, pressure, property_type):
        #
        # CoolProp can't handle these properties of CarbonMonoxide
        #
        gas_name = (
            "Nitrogen"
            if self.name == "CarbonMonoxide"
               and (property_type == "V" or property_type == "L")
            else self.name
        )
        try:
            if property_type == "T":
                enthalpy = temperature
                return PropsSI(property_type, "H", enthalpy, "P", pressure, gas_name)
            return PropsSI(property_type, "T", temperature, "P", pressure, gas_name)
        except ValueError:
            raise


@define
class GasMixture(AbstractGas):
    """
    Create a Gas-Mixture out of `Gas`-class or even out of `GasMixture`-class.
    :param component_to_percent: Is a dictionary like `{Gas("CO2"): 100}`
    Note the total percent have to be 100.
    """

    component_to_percent = field(factory=dict)

    def _property_si(self, temperature, pressure, property_type):
        #
        # thermal_capacity need to request with mass-percent
        #
        if property_type == "CP0MASS":
            component_to_percent = dict(
                zip(
                    self.component_to_percent.keys(),
                    switch_percent(
                        *zip(
                            *[
                                (component._property_si(300, 1e5, "molemass"), percent)
                                for component, percent in self.component_to_percent.items()
                            ]
                        )
                    ),
                )
            )
        else:
            component_to_percent = self.component_to_percent
        if property_type == "T":
            enthalpy = temperature
            return sum(
                percent / 100 * component._property_si(enthalpy, pressure, property_type)
                for component, percent in component_to_percent.items()
            )
        return sum(
            percent / 100 * component._property_si(temperature, pressure, property_type)
            for component, percent in component_to_percent.items()
        )


def switch_percent(bases, percents):
    """
    Calculate mass-percent to volume-percent or mass-percent to volume-percent

    :param list bases: gas-constants for calculate to volume-percent, mol-masses for calculate to mass-percent
    :param list percents: Percent of each gas-component
    :return list: Each calculated percent
    """
    total = sum(map(prod, zip(bases, percents)))
    return [base * percent / total * 100 for base, percent in zip(bases, percents)]


def old():
    norm_temp = 273.15
    norm_druck = 1.01325e5
    gas_mix = {Gas("CarbonDioxide"): 33, Gas("Hydrogen"): 33, Gas("Methane"): 34}
    GasMixture(gas_mix).density(norm_temp, norm_druck)
    GasMixture(gas_mix).viscosity(norm_temp, norm_druck)
    GasMixture(gas_mix).thermal_conductivity(norm_temp, norm_druck)
    GasMixture(gas_mix).thermal_capacity(norm_temp, norm_druck)
    GasMixture(gas_mix).molmass(norm_temp, norm_druck)

    GasMixture(gas_mix).compressibility(norm_temp, norm_druck)
    GasMixture(gas_mix).specific_gas_constant(norm_temp, norm_druck)

    temp_test_1 = 273.15 + 150
    druck_test_1 = 19e5

    gas_mix = {Gas("CarbonDioxide"): 33, Gas("Hydrogen"): 33, Gas("Methane"): 34}
    GasMixture(gas_mix).density(temp_test_1, druck_test_1)
    GasMixture(gas_mix).viscosity(temp_test_1, druck_test_1)

    GasMixture(gas_mix).thermal_conductivity(temp_test_1, druck_test_1)

    GasMixture(gas_mix).thermal_capacity(temp_test_1, druck_test_1)
    GasMixture(gas_mix).molmass(temp_test_1, druck_test_1)

    GasMixture(gas_mix).compressibility(temp_test_1, druck_test_1)
    GasMixture(gas_mix).specific_gas_constant(temp_test_1, druck_test_1)

    temp_test_1 = 273.15 + 150
    druck_test_1 = 19e5

    gas_mix = {Gas("CarbonMonoxide"): 33, Gas("Hydrogen"): 33, Gas("Methane"): 34}
    GasMixture(gas_mix).density(temp_test_1, druck_test_1)
    GasMixture(gas_mix).viscosity(temp_test_1, druck_test_1)
    GasMixture(gas_mix).thermal_conductivity(temp_test_1, druck_test_1)
    GasMixture(gas_mix).thermal_capacity(temp_test_1, druck_test_1)
    GasMixture(gas_mix).molmass(temp_test_1, druck_test_1)
    GasMixture(gas_mix).compressibility(temp_test_1, druck_test_1)
    GasMixture(gas_mix).specific_gas_constant(temp_test_1, druck_test_1)

def new():
    norm_temp = 273.15  # °K
    norm_druck = 1.01325e5  # bar abs
    gas_mix = {"CarbonDioxide": 0.33, "Hydrogen": 0.33, "Methane": 0.34}
    gas = NewGas.setup(gas_mix=gas_mix, percent=Percent.MASS)
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
    old = timeit(old, number=100)
    print(f"Durchlauf der alten API: {old:.3f} Sekunden")
    new = timeit(new, number=100)
    print(f"Durchlauf der neuen API: {new:.3f} Sekunden")
    print(f"Die neue API ist {(old / new):.3f} mal schneller")




