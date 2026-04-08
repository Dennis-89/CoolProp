Todo 08th April 2026:

- Check the enthalp-value to be sure it is the correct one.

# Gases-Doc

For HighLevel-API (I called it Gasproperties):
```bash
pip install gasproperties --extra-index-url https://dennis-89.github.io
```
For LowLevel-API (I called ist CustomGas):
```bash
pip install customgas --extra-index-url https://dennis-89.github.io
```

Then just [Download the docs](https://github.com/Dennis-89/CoolProp/blob/main/CustomGas/docs/build/html/index.html) or read below and have fun!

# GasProperties
See documentation for usage and see below for install.

```python
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
        gas_mix = gas_mix.add_water_to_gas_mix(
            gas_to_percent, humidity * 1e-2, gas_temperature, gas_pressure
        )
        print(f"Gasmix bie einer Feuchte von {humidity}%:\n{gas_mix}")


if __name__ == "__main__":
    main()
```


Example CustomGas Usage
-------------
See also what is happening when know gas state is set.

```python
[dennis@dennis CP]$ python -m venv .venv
[dennis@dennis CP]$ . .venv/bin/activate
(.venv) [dennis@dennis CP]$pip install customgas --extra-index-url https://dennis-89.github.io
(.venv) [dennis@dennis CP]$ python
Python 3.13.11 (main, Dec  5 2025, 00:00:00) [GCC 15.2.1 20251111 (Red Hat 15.2.1-4)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from customgas import Gas, Percent
>>> gas_mix = {"CarbonDioxide": 0.33, "Hydrogen": 0.33, "Methane": 0.34}
>>> gas = Gas.new(gas_mix=gas_mix, percent=Percent.MASS)
>>> gas.density()
-inf
>>> gas.update_state(101325, 273.15)
>>> gas.density()
0.9351349203421592
>>>
```

