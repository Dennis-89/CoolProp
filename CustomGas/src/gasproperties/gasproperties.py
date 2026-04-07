#!/usr/bin/env python
from math import exp, isclose, prod

from attrs import define, field
from CoolProp.CoolProp import PropsSI

# https://de.wikipedia.org/wiki/Wasserdampf
WATER_CONSTANT = 461.4
AIR_CONSTANT = 287.1


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
        return self._property_si(enthalpy, pressure, "T")

    def pressure_from_density(self, density, temperature):
        return self._property_si(temperature, density, "P")

    def specific_gas_constant(self, temperature, pressure):
        return self._property_si(
            temperature, pressure, "gas_constant"
        ) / self._property_si(temperature, pressure, "molemass")


@define(hash=True)
class Gas(AbstractGas):
    """
    Create a :class:`Gas`-object to get properties depending on given parameters.

    :param str name: The gas-name like `Gas("CO2")`. For detail information about gases go
        through the `CoolProp-Documentation <https://coolprop.org/general_information.html>`_.

    Possible properties are:

    - density in kg/m³
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - viscosity in Pa s
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - thermal_conductivity in W/m/K
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - thermal_capacity in J/kg/K
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - molmass in kg/mol
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - mass_enthalpy in J/kg
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - molar_enthalpy in J/mol
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - compressibility as a factor between 0 and 1
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - isentropic_coefficient as a factor
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    - temperature_from_enthalpy in Kelvin
        Call with gas-enthalpy (J/mol) and gas-pressure (Pascal)

    - pressure_from_density in Pascal
        Call with gas-temperature (Kelvin) and gas-density (kg/m³)

    - specific_gas_constant in J/(kg * K)
        Call with gas-temperature (Kelvin) and gas-pressure (Pascal)

    Example:

    gas = Gas("CO2")

    density = gas.density(300, 10e5)
    """

    name = field(factory=str)

    def _property_si(self, temperature, pressure, property_type):
        #
        # CoolProp can't handle these properties of CarbonMonoxide
        #
        gas_name = (
            "Nitrogen"
            if self.name == "CarbonMonoxide" and property_type in ["V", "L"]
            else self.name
        )
        try:
            if property_type == "T":
                enthalpy = temperature
                return PropsSI(property_type, "H", enthalpy, "P", pressure, gas_name)
            elif property_type == "P":
                density = pressure
                return PropsSI(property_type, "T", temperature, "D", density, gas_name)
            return PropsSI(property_type, "T", temperature, "P", pressure, gas_name)
        except ValueError:
            raise


def _is_valid(gas_mix, *_):
    _is_full(gas_mix.component_to_percent)


def _is_full(component_to_percent):
    total = sum(component_to_percent.values())
    if not isclose(1, total, abs_tol=0.0001):
        error = f"Sum of gas is {total} an not 1"
        raise ValueError(error)


@define
class GasMixture(AbstractGas):
    """
    Create a Gas-Mixture out of :class:`Gas()` or even out of :class:`GasMixture()`.

    :param dict component_to_percent: Is a dictionary like `{Gas("CO2"): 1}`. Note the total percent have to be 1.

    For list of allowed properties and usage, see :class:`Gas()` documentation.
    """

    component_to_percent = field(factory=dict, validator=_is_valid)
    _start_components = field(factory=dict, init=False)

    def __attrs_post_init__(self):
        self._start_components = self.component_to_percent

    def _property_si(self, temperature, pressure, property_type):
        #
        # thermal_capacity need to request with mass-percent
        #
        if property_type == "CP0MASS":
            components = self.component_to_percent.keys()
            mass_percents = _switch_percent(
                [
                    component._property_si(300, 1e5, "molemass")
                    for component in components
                ],
                self.component_to_percent.values(),
            )
            component_to_percent = dict(zip(components, mass_percents))
        else:
            component_to_percent = self.component_to_percent
        if property_type == "T":
            enthalpy = temperature
            return sum(
                percent * component._property_si(enthalpy, pressure, property_type)
                for component, percent in component_to_percent.items()
            )
        return sum(
            percent * component._property_si(temperature, pressure, property_type)
            for component, percent in component_to_percent.items()
        )

    def add_water_to_gas_mix(self, humidity, temperature, pressure):
        """
        Recalculation of the gas mix to account for the water content in the gas.
        This is an approximation, as the absorption of water in dry air serves as the basis for the calculation.

        :param int | float humidity: In fraction
        :param int | float temperature: The gas temperature in Kelvin
        :param int | float pressure: The gas pressure in Pascal
        :return None:
        """
        water_mass = get_water_content(
            humidity, pressure, _get_vapour_pressure(temperature)
        )
        components_to_percent = self._start_components.items()
        gas_mass = sum(
            percent * gas.density(temperature, pressure)
            for gas, percent in components_to_percent
        )
        water_percent = 1 / (water_mass + gas_mass) * water_mass
        gas_percent = 1 - water_percent
        self.component_to_percent = {
                name: gas_percent * percent
                for name, percent in components_to_percent
            } | {Gas("H2O"): water_percent}



def _switch_percent(bases, percents):
    """
    Calculate mass-percent to volume-percent or volume-percent to mass-percent

    :param list bases: gas-constants for calculate to volume-percent, mol-masses for calculate to mass-percent
    :param list percents: Percent of each gas-component
    :return list: Each calculated percent
    """
    total = sum(map(prod, zip(bases, percents)))
    return [base * percent / total * 100 for base, percent in zip(bases, percents)]


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
    gas_temperature = 300
    gas_pressure = 10e5
    gas_to_percent = {
        Gas("CarbonDioxide"): 0.33,
        Gas("Hydrogen"): 0.33,
        Gas("Methane"): 0.34,
    }
    gas_mix = GasMixture(gas_to_percent)
    print(gas_mix.thermal_capacity(300, 1e5))
    print(f"Start ohne Wasser:\n{gas_mix}")
    for humidity in range(0, 110, 10):
        gas_mix.add_water_to_gas_mix(
            humidity * 1e-2, gas_temperature, gas_pressure
        )
        print(f"Gasmix bie einer Feuchte von {humidity}%:\n{gas_mix}")


if __name__ == "__main__":
    main()
