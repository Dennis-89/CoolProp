from customgas.customgas import Gas, InputPairs, Percent
import pytest

RESULTS = {
    "density": [0.921031, 11.1485],
    "viscosity": [1.10646e-05, 1.5963e-05],
    "thermal_conductivity": [0.0701073, 0.103979],
    "thermal_capacity": [1609.48, 1859.97],
    "molmass": [0.0206428, 0.0206428],
    "compressibility": [0.997571, 0.997571],
}

GAS = Gas.new(gas_mix={"CarbonDioxide": 0.33, "Hydrogen": 0.33, "Methane": 0.34}, percent=Percent.VOLUME)





@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 101325, RESULTS["density"][0]), (273.15 + 150, 19e5, RESULTS["density"][1])])
def test_density(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.density() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 101325, RESULTS["viscosity"][0]), (423.15, 19e5, RESULTS["viscosity"][1])])
def test_viscosity(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.viscosity() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 101325, RESULTS["thermal_conductivity"][0]), (423.15, 19e5, RESULTS["thermal_conductivity"][1])])
def test_thermal_conductivity(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.thermal_conductivity() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 101325, RESULTS["thermal_capacity"][0]), (423.15, 19e5, RESULTS["thermal_capacity"][1])])
def test_thermal_capacity(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.thermal_capacity() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 101325, RESULTS["molmass"][0]), (423.15, 19e5, RESULTS["molmass"][1])])
def test_molmass(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.molmass() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 101325, RESULTS["compressibility"][0]), (423.15, 19e5, RESULTS["compressibility"][1])])
def test_compressibility(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.compressibility() == expected



