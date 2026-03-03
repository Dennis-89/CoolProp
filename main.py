from timeit import timeit
from src.customgas import Wrapper


def main():
    Wrapper.Gas("Helium").density(290, 2e5)
    gas_mix = {Wrapper.Gas("Helium"): 50, Wrapper.Gas("Argon"): 50}
    Wrapper.GasMixture(gas_mix).molmass(300, 4e5)


if __name__ == "__main__":
    duration = timeit(main, number=1)
    print(duration)
