from customgas.customgas import Gas, InputPairs, Percent
import pytest

RESULTS = {
    "density": [0.9259453731211956, 11.386107769211687],
    "viscosity": [1.0820971815994757e-05, 1.5794220284322513e-05],
    "thermal_conductivity": [0.07256846499551482, 0.10770845874268203],
    "thermal_capacity": [1606.7442824776251, 1831.508582224386],
    "molmass": [0.0206430264, 0.0206430264],
    "compressibility": [0.9971697406910944, 0.9917419885733435],
    "specific_gas_constant": [402.7751211905634, 402.7751211905634]
}

GAS = Gas.new(gas_mix={"CarbonDioxide": 0.33, "Hydrogen": 0.33, "Methane": 0.34}, percent=Percent.VOLUME)


@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["density"][0]), (273.15 + 150, 19e5, RESULTS["density"][1])])
def test_density(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.density() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["viscosity"][0]), (423.15, 19e5, RESULTS["viscosity"][1])])
def test_viscosity(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.viscosity() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["thermal_conductivity"][0]), (423.15, 19e5, RESULTS["thermal_conductivity"][1])])
def test_thermal_conductivity(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.thermal_conductivity() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["thermal_capacity"][0]), (423.15, 19e5, RESULTS["thermal_capacity"][1])])
def test_thermal_capacity(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.thermal_capacity() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["molmass"][0]), (423.15, 19e5, RESULTS["molmass"][1])])
def test_molmass(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.molmass() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["compressibility"][0]), (423.15, 19e5, RESULTS["compressibility"][1])])
def test_compressibility(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.compressibility() == expected

@pytest.mark.parametrize("temperature, pressure, expected", [(273.15, 1.01325e5, RESULTS["specific_gas_constant"][0]), (423.15, 19e5, RESULTS["specific_gas_constant"][1])])
def test_specific_gas_constant(temperature, pressure, expected):
    GAS.update_state(pressure, temperature)
    assert GAS.specific_gas_constant() == expected




