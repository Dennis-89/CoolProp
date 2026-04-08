CustomGas documentation
========================

A thinny wrapper for the `CoolProp` low-level interface.

Example:

.. code-block:: python

    def main():
        gas_temperature = 300
        gas_pressure = 10e5
        gas_mix = {'CarbonDioxide': 0.33, 'Hydrogen': 0.33, 'Methane': 0.34}
        gas = Gas.new(gas_mix=gas_mix, percent=Percent.MASS)
        gas.update_state(gas_pressure, gas_temperature)
        gas.add_water_to_gas_mix(1)
        gas.density()


    if __name__ == "__main__":
        main()



.. autoclass:: customgas::Gas
    :members:
    :exclude-members: new

    .. automethod:: __init__

    .. automethod:: new


.. autoclass:: customgas::Percent
    :members:

.. autoclass:: customgas::InputPairs
    :members: