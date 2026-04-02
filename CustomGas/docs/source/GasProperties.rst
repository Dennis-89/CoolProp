GasProperties documentation
===========================

A thinny wrapper for the `CoolProp` Highlevel interface.

Example

.. code-block:: python

    from gasproperties import GasMixture, Gas

    def main():
        gas_temperature = 300
        gas_pressure = 10e5
        gas_to_percent = {
            Gas("CarbonDioxide"): 0.33,
            Gas("Hydrogen"): 0.33,
            Gas("Methane"): 0.34,
        }
        gas_mix = GasMixture(gas_to_percent)
        print(f"Start ohne Wasser:\n{gas_mix}")
        for humidity in range(0, 110, 10):
            gas_mix = gas_mix.get_mix_with_water(
                gas_to_percent, humidity * 1e-2, gas_temperature, gas_pressure
            )
            print(f"Gasmix bie einer Feuchte von {humidity}%:\n{gas_mix}")


    if __name__ == "__main__":
        main()



.. autoclass:: gasproperties::Gas
    :members:

.. autoclass:: gasproperties::GasMixture
    :members:

.. automethod:: gasproperties::get_water_content


