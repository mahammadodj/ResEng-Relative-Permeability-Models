import numpy as np


def burdine_brooks_corey(Sw, Swr=0.1, Snwr=0.2, krwo=0.3, krnwo=0.8, lambda_=2):
    """Burdine integrated Brooks-Corey: returns krw, krnw."""
    Swd = np.clip((Sw - Swr) / (1 - Swr - Snwr), 0, 1)   # normalized water saturation

    krw = krwo * Swd**(2 / lambda_ + 3)
    krnw = krnwo * (1 - Swd)**2 * (1 - Swd**(2 / lambda_ + 1))
    return krw, krnw


if __name__ == "__main__":
    Sw = np.linspace(0.1, 0.8, 8)
    print(burdine_brooks_corey(Sw))
