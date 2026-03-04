from customgas.customgas import Gas, InputPairs, Percent

RESULTS = [
    (0.921031, 1.10646e-05, 0.0701073, 1609.48, 0.0206428, 0.997571),
    (11.1485, 1.5963e-05, 0.103979, 1859.97, 0.0206428, 0.997571),
]



def conditions():
    gas_mix = {"CarbonDioxide": 0.33, "Hydrogen": 0.33, "Methane": 0.34}
    gas = Gas.setup(gas_mix=gas_mix, percent=Percent.MASS)
    for temperature, pressure in [
        (273.15, 101325),
        (273.15 + 150, 19e5),
        (273.15 + 150, 19e5),
    ]:
        gas.update_state(pressure, temperature)
        yield gas


def test_gas():
    for gas, results in zip(conditions(), RESULTS):
        assert gas.density() == results[0]
        assert gas.viscosity() == results[1]
        assert gas.thermal_conductivity() == results[2]
        assert gas.thermal_capacity() == results[3]
        assert gas.molmass() == results[4]
        assert gas.compressibility() == results[5]
    gas = Gas.setup(name="Air")
    gas.input_pair = InputPairs.ENTHALPY_PRESSURE
    gas.update_state(300, 1e5)
    assert gas.temperature == 300
